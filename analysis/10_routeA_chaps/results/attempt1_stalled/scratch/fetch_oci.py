"""Fetch one platform of a public ghcr image into an OCI layout dir, resuming blobs with
HTTP Range across connection drops. Usage: fetch_oci.py REPO TAG OUTDIR"""
import hashlib, json, os, sys, time, urllib.request, urllib.error

repo, tag, out = sys.argv[1:4]
REG = "https://ghcr.io"
OCI_IDX = "application/vnd.oci.image.index.v1+json"
OCI_MAN = "application/vnd.oci.image.manifest.v1+json"


def retry(f):
    for i in range(1000):
        try:
            return f()
        except Exception as e:  # noqa: BLE001
            print(f"  retry {i}: {e}", flush=True)
            time.sleep(min(30, 2 + i))
    raise SystemExit("gave up")


def token():
    u = f"{REG}/token?scope=repository:{repo}:pull"
    return json.load(urllib.request.urlopen(u, timeout=60))["token"]


def get(path, accept=None, headers=None):
    h = {"Authorization": f"Bearer {token()}"}
    if accept:
        h["Accept"] = accept
    h.update(headers or {})
    return urllib.request.urlopen(urllib.request.Request(f"{REG}/v2/{repo}/{path}", headers=h), timeout=120)


blobs = os.path.join(out, "blobs", "sha256")
os.makedirs(blobs, exist_ok=True)


def save_bytes(data):
    d = hashlib.sha256(data).hexdigest()
    open(os.path.join(blobs, d), "wb").write(data)
    return d


def blob(digest, size):
    hexd = digest.split(":")[1]
    p = os.path.join(blobs, hexd)
    while True:
        have = os.path.getsize(p) if os.path.exists(p) else 0
        if have == size:
            break
        print(f"blob {hexd[:12]} {have/1e6:.0f}/{size/1e6:.0f} MB", flush=True)
        try:
            r = get(f"blobs/{digest}", headers={"Range": f"bytes={have}-"})
            if have and r.status != 206:
                have = 0
                open(p, "wb").close()
            with open(p, "ab") as f:
                while True:
                    c = r.read(1 << 20)
                    if not c:
                        break
                    f.write(c)
        except Exception as e:  # noqa: BLE001
            print(f"  drop: {e}", flush=True)
            time.sleep(3)
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 22), b""):
            h.update(c)
    if h.hexdigest() != hexd:
        os.remove(p)
        raise SystemExit(f"digest mismatch {digest}")
    print(f"blob {hexd[:12]} ok", flush=True)


idx_raw = retry(lambda: get(f"manifests/{tag}", accept=f"{OCI_IDX},{OCI_MAN}").read())
idx = json.loads(idx_raw)
man_desc = next(m for m in idx["manifests"] if m.get("platform", {}).get("architecture") == "amd64")
man_raw = retry(lambda: get(f"manifests/{man_desc['digest']}", accept=OCI_MAN).read())
assert "sha256:" + save_bytes(man_raw) == man_desc["digest"]
man = json.loads(man_raw)
for d in [man["config"]] + man["layers"]:
    blob(d["digest"], d["size"])
ref = f"ghcr.io/{repo}:{tag}"
json.dump({"schemaVersion": 2, "mediaType": OCI_IDX, "manifests": [
    {**{k: man_desc[k] for k in ("mediaType", "digest", "size", "platform")},
     "annotations": {"io.containerd.image.name": ref, "org.opencontainers.image.ref.name": tag}}]},
    open(os.path.join(out, "index.json"), "w"))
json.dump({"imageLayoutVersion": "1.0.0"}, open(os.path.join(out, "oci-layout"), "w"))
print("layout complete", ref, man_desc["digest"])

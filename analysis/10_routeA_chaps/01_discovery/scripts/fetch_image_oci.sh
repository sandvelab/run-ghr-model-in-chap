#!/usr/bin/env bash
# Fetch one linux/amd64 image from ghcr.io with resumable, digest-checked curl downloads,
# assemble it as an OCI image layout and `docker load` it under its original tag.
#
# Why: on a slow or flaky link ghcr.io cuts long transfers ("unexpected EOF"), and with
# the overlay2 store Docker throws away a partly downloaded layer when a pull fails, so
# `docker pull` (and `chaps run`, which pulls through docker compose) restarts a 1.4 GB
# layer from zero on every attempt. curl -C - resumes instead. The bytes are checked
# against their sha256 digests, so what gets loaded is the published image, unmodified.
#
# Usage: fetch_image_oci.sh <repo> <tag> <work_dir>
#   e.g. fetch_image_oci.sh chap-models/chapkit_ghr_model sha-dfb2e3f /tmp/w
set -euo pipefail
REPO="$1"; TAG="$2"; WORK="$3"
REF="ghcr.io/$REPO:$TAG"
if docker image inspect "$REF" >/dev/null 2>&1; then echo "$REF already present"; exit 0; fi

D="$WORK/oci-$(echo "$REPO" | tr / _)-$TAG"
mkdir -p "$D/blobs/sha256"
sha256() { if command -v shasum >/dev/null; then shasum -a 256 "$1"; else sha256sum "$1"; fi | cut -d' ' -f1; }
token() { curl -fsS "https://ghcr.io/token?scope=repository:$REPO:pull" | sed -E 's/.*"token":"([^"]+)".*/\1/'; }
ACCEPT='application/vnd.oci.image.index.v1+json,application/vnd.docker.distribution.manifest.list.v2+json,application/vnd.oci.image.manifest.v1+json,application/vnd.docker.distribution.manifest.v2+json'

get_manifest() { # $1 = tag or digest, $2 = output file
  curl -fsS -H "Authorization: Bearer $(token)" -H "Accept: $ACCEPT" \
    "https://ghcr.io/v2/$REPO/manifests/$1" -o "$2"
}

# Index -> the linux/amd64 manifest digest (plain-text parsing, no jq/python needed).
get_manifest "$TAG" "$D/top.json"
if grep -q '"manifests"' "$D/top.json"; then
  MDIGEST=$(tr -d '\n ' < "$D/top.json" | grep -oE '\{[^{}]*"digest":"sha256:[0-9a-f]{64}"[^{}]*"platform":\{"architecture":"amd64","os":"linux"' \
            | grep -oE 'sha256:[0-9a-f]{64}' | head -1)
  [ -n "$MDIGEST" ] || { echo "no linux/amd64 manifest in index" >&2; exit 1; }
  get_manifest "$MDIGEST" "$D/blobs/sha256/${MDIGEST#sha256:}"
else
  MDIGEST="sha256:$(sha256 "$D/top.json")"
  cp "$D/top.json" "$D/blobs/sha256/${MDIGEST#sha256:}"
fi
MFILE="$D/blobs/sha256/${MDIGEST#sha256:}"
[ "sha256:$(sha256 "$MFILE")" = "$MDIGEST" ] || { echo "manifest digest mismatch" >&2; exit 1; }
MSIZE=$(wc -c < "$MFILE" | tr -d ' ')
MTYPE=$(tr -d '\n ' < "$MFILE" | grep -oE '"mediaType":"[^"]+"' | head -1 | cut -d'"' -f4)

# Every blob the manifest names (config + layers), each resumed until its digest matches.
for dg in $(tr -d '\n ' < "$MFILE" | grep -oE 'sha256:[0-9a-f]{64}' | sort -u); do
  hex=${dg#sha256:}; out="$D/blobs/sha256/$hex"
  [ -f "$out" ] && [ "$(sha256 "$out")" = "$hex" ] && continue
  for attempt in $(seq 1 200); do
    curl -fL -sS --retry 3 --speed-limit 1000 --speed-time 60 -C - \
      -H "Authorization: Bearer $(token)" -o "$out.part" \
      "https://ghcr.io/v2/$REPO/blobs/$dg" && break
    echo "blob ${hex:0:12}: attempt $attempt cut off at $(wc -c < "$out.part" | tr -d ' ') bytes, resuming" >&2
    sleep 3
  done
  [ "$(sha256 "$out.part")" = "$hex" ] || { echo "blob ${hex:0:12} digest mismatch" >&2; rm -f "$out.part"; exit 1; }
  mv "$out.part" "$out"; echo "blob ${hex:0:12} ok"
done

printf '{"imageLayoutVersion":"1.0.0"}' > "$D/oci-layout"
cat > "$D/index.json" <<EOF
{"schemaVersion":2,"mediaType":"application/vnd.oci.image.index.v1+json","manifests":[{"mediaType":"$MTYPE","digest":"$MDIGEST","size":$MSIZE,"annotations":{"io.containerd.image.name":"$REF","org.opencontainers.image.ref.name":"$TAG"}}]}
EOF
rm -f "$D/top.json"
# Docker's classic (overlay2) loader reads a docker-archive manifest.json, not the OCI
# index.json alone; without it docker load falls back to the legacy format and fails
# ("blobs/json: no such file"). Write one beside the OCI index, as `docker save` does.
M1=$(tr -d '\n ' < "$MFILE")
CFG=$(echo "$M1" | grep -oE '"config":\{[^}]*\}' | grep -oE 'sha256:[0-9a-f]{64}')
LAYERS=$(echo "$M1" | grep -oE '"layers":\[.*\]' | grep -oE 'sha256:[0-9a-f]{64}' \
         | sed -E 's#sha256:(.*)#"blobs/sha256/\1"#' | paste -sd, -)
printf '[{"Config":"blobs/sha256/%s","RepoTags":["%s"],"Layers":[%s]}]\n' "${CFG#sha256:}" "$REF" "$LAYERS" > "$D/manifest.json"
(cd "$D" && tar -cf - oci-layout index.json manifest.json blobs) | docker load
docker image inspect "$REF" >/dev/null && echo "loaded $REF"

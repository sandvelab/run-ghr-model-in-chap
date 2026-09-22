result: results/anchor_manifest.tsv
script: scripts/verify_anchors.py
        sha256:1f0e95e17129d66d9e89f3caac204b8751e0363454bf114bfbf7bea9dbd374a2
invocation: ../../environment/env/bin/python scripts/verify_anchors.py
            (called by run.sh, which sets PYTHON to the pinned environment)
inputs: ../../Archive/data-lao/sha256sums.txt  sha256:1b942cc34c0cff472803a1fb039b3b2d32e4393d06265ae381af8ff5e65f069e
        ../../Archive/data-lao/chap_LAO_admin1_monthly.csv  sha256:19488aa1fc4d961ae1a6aeb75b874789576877664fce47713628f497a06fff56
        ../../Archive/data-lao/chap_LAO_admin1_monthly_schema.json  sha256:ff750db4202c32fc187b26bb3566b4f981b94467664502e76cbd09977dd06210
        ../../Archive/model-route-a/git-metadata.txt  sha256:2ffe8e38f7379317944f907ca96cbe1cdb4aa700897ba824ad240d28aab834e2
        ../../Archive/model-route-b/git-metadata.txt  sha256:e37d744c0b6a3d3a32bcb46e7669567cb277664aaa96c9591496dc8f7fe4a73b
        ../../Archive/platform-chap/install-metadata.txt  sha256:e9de559295ec1652322fe1500a1bd751b0df918a8e0d89b29f19a4dffb0f38b5
        ../../Archive/platform-chap/chap-tool-freeze.txt  sha256:5450e303781d77a8f8faa5a6fbf6fe12c4190311b1e561f9a21b34600f9e04a2
environment: environment/ (project main; stdlib-only Python 3.13.0, environment/lock.txt empty)
seeds: project 20260921; component none -- the script is deterministic and draws no randomness
commit: 8ac3c8f
instructions-commit: d2459b1
node: analysis/01_anchors
produced: 2026-09-21
alternatives-considered: the anchors could have been pinned by tag or by "latest on main"
  rather than by commit; rejected because both model repositories are actively pushed to and
  a later session would then be unable to tell which code produced a result. The archived
  model copies could have kept their .git directories, which would have made the pin
  self-evidencing; rejected because a nested repository inside Archive/ is invisible to this
  repository's own version control, so the archived copy would not in fact be versioned here.
  The commit is instead recorded in git-metadata.txt beside the detached tree. The platform
  is pinned as captured state rather than by digest, because it is an external installation
  this repository does not own; the 174-package freeze is what makes it reconstructible.
agency: agent-autonomous (mechanics); human-pointed (which repositories and which data)
information: agent-retrieved -- commits, licences and package versions read from the
  repositories and from the local install at pin time, not recalled

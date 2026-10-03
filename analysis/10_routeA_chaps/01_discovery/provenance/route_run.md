# Provenance — the route reproduced by its own script in a clean shell (batch 14)

result: results/clean_run/eval.nc
          sha256:1702329f43fc70a6f937ed304b0caea2c737b1d3b425ac8df551a79f6c56637a
        results/clean_run/evaluation_plot.html
          sha256:94bb605aec7fd008eeaa81aa0f0a1159ae6258a4e13cad2dd1c1ca6b9ab1189d
        results/clean_run/metrics.csv
          sha256:17782a84cd5c691d841a10cea1db301c8e7ca5d0c937e128fde0f1758ba17c5a
        results/clean_run/run_route.log
          sha256:70d82bdf14609c409f972287eda19a52912d4c418bd03a3ada69c77b3e858d02
script: scripts/run_route.sh
          sha256:616aca3a30226bf6e0bad34fad9aacff57a8d7a8b4dd310233c3569f73339825
        scripts/fetch_image_oci.sh
          sha256:188c77a2e9eb4a4cac0d4ab869bacfd741bcad6893eb8626c47144737be1bff2
invocation: env -i HOME=<empty scratch dir> PATH=/usr/bin:/bin bash scripts/run_route.sh results/clean_run <scratch>/cleanwork (exit 0, 23 min of execution 14:45–15:08Z), run by the discovering agent. Launched 11:55Z; the host slept until 14:37Z and the script began at ~14:45Z (log rows 43–46)
inputs: the Lao CSV and GeoJSON fetched by the script from https://raw.githubusercontent.com/dhis2/climate-health-data/refs/heads/main/lao/ — a branch, not the pinned commit; the script checks them against the sha256 of Archive/data-lao/ and stops on a mismatch. chaps, uv and chap-core 2.3.1 are installed by the script into the work dir from their public installers and PyPI
environment: its own (above); Docker Desktop as in discovery.md
seeds: none can be set; the script run's metrics differ from the manual run's (CRPS 149.8 against 149.2, MAE 127.7 against 124.1; coverage 10–90 identical at 0.815)
commit: 459c7f9
instructions-commit: ea5aa2f
node: analysis/10_routeA_chaps/01_discovery
produced: 2026-10-03
untested branches: the image fetch. The image was already in Docker, so the prefetch printed "already present" and chaps only checked the tag against the registry; a machine without it adds the download (about 1.5 h on this link with the resumable fetcher; chaps' own pull, SKIP_PREFETCH=1, failed twice here). uv's installer skipped its own checksum check under the bare PATH (no sha256sum on macOS)
agency: agent-autonomous
information: agent-retrieved

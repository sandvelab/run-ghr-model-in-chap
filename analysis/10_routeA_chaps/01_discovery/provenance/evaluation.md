# Provenance — the evaluation, as run by hand down the route (batch 14)

result: results/eval.nc
          sha256:767d399b13c2b16d52f01c595c2003bee5f7f98ab2968894e3244a3be2dc9221
        results/evaluation_plot.html
          sha256:51469679660dcaebcfe32bebf9a717583309182666cb5cc52ad9f22f19b2ad88
        results/metrics.csv
          sha256:4aed3c062f918423084f5612aa0e43c74a6bba9b0d5f6f57f75a6a071f199efc
        results/chap_eval.log
          sha256:c7a2a92b09199fcae6edee951ef8d42ddd9eecf0377ffacc9f26a6b97532d94a
        results/plot_backtest.log
          sha256:06cb18eb4deb0d59494356d7e90d632e1244a8efea79000d0936ed5cb9b1c499
        results/export_metrics.log
          sha256:38fc025fda6709c5761a0d925dee5dd4dd09a2205b7eece9fc2963826b88a9d7
        results/model_service.log
          sha256:f7ead2673a440c2538adcaee89d2545d478e85e5312438e27bd1932c82c1f026
        results/chaps_run_attempt1.log
          sha256:91a46a45f44c918897f83608597b07bc7b53cbae20932a15b6f3540f8e482c75
        results/chaps_run_attempt2.log
          sha256:916725b92f25034fae87ca948e48398fecff87ac01239bd92992c58f4e0c8444
        results/fetch_image_oci.log
          sha256:053391e32fc6d24da5a019f758d941666f8271d025d02701502767b9099f2f4c
script: scripts/fetch_image_oci.sh
          sha256:188c77a2e9eb4a4cac0d4ab869bacfd741bcad6893eb8626c47144737be1bff2
invocation: chaps run https://github.com/chap-models/chapkit_ghr_model --port 5060 --timeout 7000 (failed, rc=18, 93 min: chaps_run_attempt1.log) ; bash scripts/fetch_image_oci.sh chap-models/chapkit_ghr_model sha-dfb2e3f <scratch> (twice: the first fetched every blob and failed at docker load, the second repacked and loaded) ; chaps run <same URL> --port 5060 --timeout 1500 (chaps_run_attempt2.log) ; chap eval --model-name http://localhost:5060 --dataset-csv Archive/data-lao/chap_LAO_admin1_monthly.csv --output-file results/eval.nc --run-config.is-chapkit-model ; chap plot-backtest --input-file eval.nc --output-file evaluation_plot.html ; chap export-metrics --input-files eval.nc --output-file metrics.csv — all run by the discovering agent
inputs: Archive/data-lao/chap_LAO_admin1_monthly.{csv,geojson}, read in place
environment: as discovery.md; the image's id equals its published config digest (results/image_id.txt)
seeds: none can be set; see discovery.md
commit: 459c7f9
instructions-commit: ea5aa2f
node: analysis/10_routeA_chaps/01_discovery
produced: 2026-10-03
alternatives-considered: chaps init + chaps up (a full chap-core deployment) with chaps models test --backtest — rejected by the agent: that backtest scores on model-generated sample data, not the Lao files, and the host had 14.4 GB free against the ~25 GB chaps' docs ask for (log row 13). Re-running chaps run as its error message suggests — rejected by the agent: Docker discards a partly downloaded layer when a pull fails, so the 1.42 GB layer would restart from zero (row 27)
known gaps: fetch_image_oci.log holds the first fetcher run only (it ends rc=1 at the docker load step; it shows the 1.42 GB layer cut off five times and resumed each time — the agent's notes say four). The output of the second, successful run was not kept; the load is evidenced by row 31 and by image_id.txt
agency: agent-autonomous (the discovering agent)
information: agent-retrieved

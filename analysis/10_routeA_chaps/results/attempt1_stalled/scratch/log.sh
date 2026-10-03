#!/bin/bash
P="/Users/geirksa_1_2_3/ai/special-purpose vaults/run-ghr-model-in-chap"
exec "$P/.venv/bin/python" "$P/AI-internal/useful-scripts/log_step.py" "$P/analysis/10_routeA_chaps/01_discovery/results/discovery_log.tsv" --kind "$1" --ref "$2" --outcome "$3" --note "$4"

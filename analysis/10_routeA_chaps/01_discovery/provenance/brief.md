# Provenance — the brief given to the batch 14 discovering agent

result: results/brief_as_given.md
          sha256:314f1cd8406bbbd828e04112108edda29d76bcbf3c36bf9ac11c536778775af1
script: none — derived by the orchestrator from analysis/09_routeA_iteration3/01_discovery/results/brief_as_given.md with sed, substituting the node path and appending one sentence to item 1 naming chaps as the route
invocation: sed -e 's#analysis/09_routeA_iteration3/01_discovery#analysis/10_routeA_chaps/01_discovery#g' -e '<item 1 substitution>' (the full diff against batch 12's brief is the node path in five places plus item 1)
inputs: analysis/09_routeA_iteration3/01_discovery/results/brief_as_given.md
environment: none
seeds: none
commit: 21af6c2 (before this batch's setup commit)
node: analysis/10_routeA_chaps/01_discovery
produced: 2026-10-02
alternatives-considered: rewording item 7, which says "beyond `chap eval`" and so leans toward the chap CLI — rejected to keep the brief verbatim; the lean is named in the plan's §4b. A chaps-only brief forbidding the chap CLI — put to the human and declined
agency: human-set (the route and the framing); agent-autonomous (the wording of the added sentence)

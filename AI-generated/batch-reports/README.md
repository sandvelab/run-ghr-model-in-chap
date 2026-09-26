# batch-reports

One report per executed batch, written when the batch runs, named `YY-MM-DD_bNN_shortName.md`.
Each says what the batch asked, what it found, and which file grounds every number in it. No
re-run produces the same report twice, so nothing here is pruned and nothing here is edited
after the fact — a later correction is a later report, not a rewrite.

The plan's §6 carries the ledger these correspond to, and links back to each report by name.

## Currently here — iteration 2

- `26-09-22_b01_anchors.md` — the platform, model and data anchors, pinned and archived.
- `26-09-22_b03b04_routesDiscovered.md` — how the two discovering agents were kept independent,
  and what each reported.
- `26-09-22_b05_routeReports.md` — each route in full: resources, process, invocation, results.
- `26-09-22_b06_comparativeReport.md` — route A against route B on effort, with the results
  reported per route and not compared.
- `26-09-23_b08b_configurability.md` — whether route A's model can be configured through CHAP
  at all, and the variant sweep run through an interposed proxy.
- `26-09-23_b08c_thirdCase.md` — a third model, to test whether the `MLproject` mechanism
  delivers a configuration where chapkit does not.
- `26-09-23_b10_humanCost.md` — what each route would cost a *human* rather than an agent, for
  two personas, to a default evaluation.

## Currently here — iteration 3 (route A only)

- `26-09-26_b12_routeA.md` — route A on chapkit 2.1.2 with the model at `a9532c7`: resources,
  process, invocation, evaluation, and the human cost for batch 10's two personas.
- `26-09-26_b12_whatChanged.md` — iteration 2's route A against iteration 3's: success, agent
  time and tokens, estimated human time, and what one pair of runs cannot separate.
- `26-09-26_b13_configurability.md` — batch 8b's configuration test repeated on the upgraded
  pair, with nothing interposed: configuration now reaches the model.

Batches 2, 7, 8 and 9 have no report here: 2 and 7 were folded into the reports above, 8
produced the overview instead, and 9 is open.

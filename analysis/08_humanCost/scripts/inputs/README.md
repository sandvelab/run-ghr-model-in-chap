# Inputs to the human-cost model

Two kinds of file, kept apart on purpose.

**Measured** — not here. `results/doc_sizes.tsv` and `results/machine_waits.tsv` are written by
`scripts/lib/measure_inputs.py` from the archived repositories, the installed `chap-core`, the
CLI's own `--help` output and the discovery logs' timestamps. Nothing in this directory can
change them.

**Authored** — everything here. These are this project's assumptions about human pace and
human knowledge, written down so they can be argued with and replaced. Substituting your own
`act_costs.tsv`, `reading_rates.tsv`, `personas.tsv` or `modifiers.tsv` and re-running
`run.sh` re-costs both routes without touching a measured value.

| File | What it fixes |
|---|---|
| `steps.tsv` | The act sequence, one row per step of the normalised discovery window, with the act class, the document read, and the prerequisites the route gates that step on. Rows marked `added` are steps a human takes that no agent log could contain. |
| `prerequisites.tsv` | Every prerequisite the routes gate on, and what it costs to acquire if you do not have it. |
| `personas.tsv` | What each persona holds, holds partially, or lacks. |
| `modifiers.tsv` | What `partial` and `lack` do to a step's time, and what fraction of the acquisition cost is paid. |
| `act_costs.tsv` | Base minutes per act class per persona. `read_doc` is computed instead, from measured length. |
| `reading_rates.tsv` | Words per minute, and the spread between a good run and a bad one. |
| `divergences.tsv` | Where a persona's path stops being the agent's path, as conditional rules rather than as narrative. |
| `documents.tsv` | Which file or command stands behind each `read_doc` step, for the measurement script to count. |

## The rule that decides what gets charged

**A prerequisite is charged only where the route cannot proceed without it.** A step the agent
took on its own initiative, whose outcome changed nothing, does not make its subject a
requirement of the route. Route B's `docker info` is the case that forced this rule to be
written down: the agent ran it, route B needs no container runtime, and charging a persona who
has never used Docker for learning Docker on route B would have inverted one of this study's
actual findings.

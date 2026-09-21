# Discovery log format

The measurement instrument of this project. Read it before writing or reading a
`discovery_log.tsv`; do not improvise a column from memory of what it probably was.

Both routes log into this one shape so that their effort can be compared at all. A log in a
different shape is not a smaller version of the measurement — it is no measurement, because
every statistic in `analysis/04_comparison` is defined over these columns.

## The file

`results/discovery_log.tsv` in the route's node. Tab-separated, one header line, UTF-8,
Unix line endings. **Appended to at the moment of each step**, never written in one go at the
end (plan §3). A row is written when the step happens, not when it is understood.

| Column | Contents |
|---|---|
| `step` | Integer, starting at 1, strictly increasing by 1 |
| `ts_utc` | `YYYY-MM-DDTHH:MM:SSZ`, non-decreasing down the file |
| `kind` | `resource` · `command` · `decision` · `blocker` · `milestone` |
| `ref` | The thing itself: a URL, a file path, the command line as run, or a milestone name |
| `outcome` | `used` · `discarded` · `ok` · `failed` · `open` · `resolved` |
| `note` | One line, no tab characters, no newlines. What it was and what came of it |

### What each `kind` means, and which outcomes it may take

- **`resource`** — a documentation page, README, source file, issue, or example that was
  *read*. `used` if it contributed to the invocation that finally worked; `discarded` if it
  was read and did not. One row per distinct resource, the first time it is opened.
- **`command`** — a command that was *run*. `ok` or `failed`. The `ref` is the command line
  as it was actually run, so that the log doubles as the trace of what was tried.
- **`decision`** — a judgment call made along the way. `used` if taken, `discarded` if
  considered and not taken. The `note` carries the basis.
- **`blocker`** — something outside the route that stopped progress: a daemon not running, a
  registry that needs credentials, a missing prerequisite. `open` when hit, and a second row
  `resolved` when it clears.
- **`milestone`** — a fixed point in the route, always `ok`. The vocabulary is closed,
  because these are what the two routes are aligned on:

  | `ref` | Reached when |
  |---|---|
  | `first_doc_opened` | The first documentation of any kind is opened |
  | `model_obtained` | The model's code is on the machine |
  | `model_runs_standalone` | The model trains or predicts at all, outside CHAP (skip if the route never does this) |
  | `model_registered_with_chap` | CHAP can see the model as a model |
  | `evaluation_started` | The evaluation command is launched |
  | `evaluation_complete` | CHAP has written an evaluation result to a file |
  | `route_abandoned` | The route is given up, with the reason in `note` |

## Worked rows

```
step	ts_utc	kind	ref	outcome	note
1	2026-09-21T09:02:11Z	milestone	first_doc_opened	ok	starting from the repository README
2	2026-09-21T09:02:11Z	resource	https://github.com/example/model#readme	used	names the entry point and the config file
3	2026-09-21T09:07:45Z	command	git clone https://github.com/example/model	ok	
4	2026-09-21T09:07:52Z	milestone	model_obtained	ok	
5	2026-09-21T09:11:03Z	command	chap evaluate --model-name model --dataset lao.csv	failed	unknown option --model-name
6	2026-09-21T09:12:40Z	resource	https://docs.example.org/chap/cli	discarded	documents a different major version
```

## What is computed from it

`analysis/04_comparison/scripts/summarise_discovery.py` validates every log against this
specification and then writes, per route: resources consulted, used and discarded; commands
run and failed; blockers hit and left unresolved; dead ends; elapsed minutes in total and to
`evaluation_complete`; the counts of resources and commands *before* `evaluation_complete`;
and whether the route reached an evaluation at all.

It also writes two integrity statistics — the number of distinct timestamps, and the largest
number of rows sharing one timestamp. A log written in one sitting at the end shows up as a
handful of distinct timestamps carrying many rows each, and the plan's §3 requires that such
a log be reported as not admissible for the effort measures rather than quietly used.

## Beside it

`results/discovery_notes.md` — the narrative the counts cannot carry: what was confusing,
what a page implied that turned out not to hold, why a path was abandoned. Written by the
same agent, and quoted rather than summarised when the reports are built.

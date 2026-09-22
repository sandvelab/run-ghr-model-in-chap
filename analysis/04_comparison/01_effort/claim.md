# Claim

How should effort be read off two discovery logs written by two different agents? The counts are defined over the log's columns, but two agents given the same format can still code the same act differently, so the reading itself is a judgment call with more than one defensible answer.

## Children

kind: alternatives
main-path: b_normalised

## Environment

inherits: the project main environment (`environment/`)

## Answers

_(Each belongs in the claim collection under `Human-AI-collaboration/claims/` with a pointer
to the result grounding it.)_

**The two readings order the routes identically, and the normalisation reverses nothing.**
Route A costs more than route B on every statistic that orders, under both readings. What the
rules change is the size of the gap, and they change it in one direction: towards each other.
Dead ends go from 4:2 to 3:2, resources from 6:4 to 5:4, commands from 17:15 to 11:9.

**`b_normalised` is the main path.** The question this project asks is a comparison, and the
normalisation is what makes two logs written by two different agents comparable at all.
`a_asLogged` stays runnable as the only purely observational reading — it measures what the
agents recorded, including where they recorded the same kind of act differently.

**Face value gets one thing backwards, which is why the fork exists.** As logged, route A has
**zero** failed commands and route B has one. Route A in fact had two commands fail; its agent
marked them `ok` before reading their output and recorded the failures in later rows, then
logged its own decision not to rewrite them. Rule 1 attributes each failure to the command
that failed, wherever the agent put it, and declines to charge the route twice by counting the
correcting row as a blocker as well.

**Rule 2 is the larger effect and the less obvious one.** Both logs continue past the moment
the route first worked, and unequally: 16 further rows for route A, 11 for route B. Counting
those charges a route for verifying a script and reading a plot format, which is not the cost
of finding out how to run the model. Restricting to the discovery window cuts route A from 43
rows to 27 and route B from 33 to 22.

**Everything each rule touched is written down** (`b_normalised/results/what_the_rules_changed.md`),
per route, so the reading can be audited rather than taken on trust. The logs themselves are
never edited: the rules are applied in memory, at the point where they can be disagreed with.

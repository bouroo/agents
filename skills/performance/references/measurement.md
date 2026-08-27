# Measurement Methodology

> Load on demand. The short cycle lives in [performance](../SKILL.md); this file is the detail.

Optimization without measurement is guessing, and guesses about bottlenecks are wrong ~80% of the time. Profile before optimizing; every step below produces an artifact: a captured command, a report file, a benchmark result. The artifact is the evidence; the narrative is not.

## The Cycle

**Define, Benchmark, Diagnose, Improve, Compare**, repeated.

1. **Define your metric**: latency, throughput, memory, or CPU? Without a target, optimizations are random. Pick one primary metric and state the target.
2. **Write an atomic benchmark**: isolate one function per benchmark to avoid result contamination. A benchmark touching everything proves nothing about anything.
3. **Measure baseline**: capture to a file as an executable audit trail (`report-1.txt`). The file, not memory, is the record.
4. **Diagnose**: rule out external bottlenecks first (below), then apply the routing table in the SKILL.
5. **Improve (ACT)**: apply ONE optimization at a time, with an explanatory comment naming why.
6. **Compare**: use a statistical comparator to confirm significance; paste the comparison in the report or commit so reviewers see the exact delta.
7. **Repeat**: increment the report number, catalog findings, and tackle the next bottleneck.

One change at a time is non-negotiable. Bundling changes destroys causality: you cannot tell which change helped, which hurt, and which did nothing.

## Rule Out External Bottlenecks First

Before optimizing code, verify the bottleneck is in your process. If 90% of latency is a slow DB query or upstream API call, local allocation tuning will not move the number.

**Diagnose:**

- An **off-CPU profiler** shows I/O wait time. If off-CPU dominates, the bottleneck is external.
- **Distributed tracing** shows which upstream span is slow.
- A **thread or task dump** shows workers blocked in socket reads or DB drivers.

**When external:** optimize that component: query tuning, caching, connection pools, circuit breakers, batch sizing. Re-profile after each external fix; the internal hot path may have moved or vanished.

## Benchmark Hygiene

- **Isolate one function per benchmark.** One benchmark touching everything produces contaminated, unattributable results.
- **Capture to a file.** Baseline and each iteration land in a numbered report so the audit trail survives session compaction.
- **Control the environment.** Noise from background load, thermal throttling, and power management swamps small gains. Run on a quiet machine; disable CPU frequency scaling if the platform allows; warm up before measuring.
- **Use a statistical comparator.** Single runs lie. Compare distributions, not point estimates; report variance and confidence, not just means.
- **Beware micro-benchmark traps.** Dead-code elimination, constant folding, and escape analysis can make a benchmark "prove" a speedup that the real code never gets. Inspect generated assembly or IR when a result looks too good.
- **Re-baseline after structural change.** If the surrounding code or inputs change, the old baseline no longer compares.

## Cross-references

- [tactics](./tactics.md) the countermeasures each diagnosis routes to.
- [verification](../../verification/SKILL.md) the same executable-evidence standard applied to a performance claim.

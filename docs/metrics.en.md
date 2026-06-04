# Metrics

Full Chinese version: [metrics.md](./metrics.md)

This system focuses on **delivery efficiency + flow health + quality risk + planning reliability + engineering efficiency**, with graceful degradation based on data availability.

## Categories

### Delivery & Flow

- Throughput
- Delivery cycle time (p50/p75/p95)
- Processing cycle time (p50/p75/p95)
- Average WIP and Aging WIP

Primary source: project management (`data_source`)

### Quality

- Defect-related signals (requirements/dev/testing)
- Defect rate, reopen rate
- Escaped defects (count and rate)

Primary sources: bug system (`bug_source`) + project management (`data_source`)

### Planning Reliability

- Commitment achievement
- Scope change
- Iteration throughput/completion/carryover (optional)

Primary source: project management (`data_source`)

### Engineering Efficiency

- PR cycle time, review latency
- Change size distribution

Primary source: Git (`git_source`)

### CI / Quality Gates

- CI frequency, CI success rate
- Code scan pass rate

Primary source: CI (`ci_source`)

## Thresholds

Targets and thresholds come from `metrics.targets` in `work/meta/config.yaml`.

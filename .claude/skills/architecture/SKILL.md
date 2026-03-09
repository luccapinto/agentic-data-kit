---
name: architecture
description: Architectural decision-making framework for Data Engineering and Analytics. Focuses on Medallion Architecture, Data Mesh, Batch vs Streaming, and Dimensional Modeling. 
allowed-tools: Read, Glob, Grep
---

# Architecture Decision Framework (Data Focus)

> "Requirements drive pipelines. Volume informs processing. Modeling organizes truth."

## 🎯 Selective Reading Rule

**Read ONLY files relevant to the request!** Check the content map, find what you need.

| File | Description | When to Read |
|------|-------------|--------------|
| `context-discovery.md` | Questions to ask, project classification | Starting data architecture design |
| `medallion.md` | Bronze, Silver, Gold layers | Designing Data Lakehouse pipelines |
| `batch-vs-streaming.md` | Lambda, Kappa, micro-batching | Deciding latency vs throughput |
| `dimensional-modeling.md` | Star Schema, Facts, Dimensions | Modeling the Gold layer for BI / Analytics |
| `data-mesh.md` | Decentralized data ownership | Designing organizational data structure |

---

## 🔗 Related Skills

| Skill | Use For |
|-------|---------|
| `@[skills/database-design]` | Physical Database schema design |
| `@[skills/databricks-patterns]` | Implementing architecture in Databricks |
| `@[skills/tmdl-modeling]` | Semantic layer deployment |

---

## Core Principles

1. **Idempotency is Mandatory:** Pipelines must be rerunnable without duplicating data.
2. **Immutability in Source:** Never UPDATE or DELETE in Bronze. Append only.
3. **Keep Compute Close to Data:** Avoid moving large datasets across networks unnecessarily.
4. **Late Binding:** Apply heavy business logic and aggregations as late as possible (Silver to Gold).

---

## Validation Checklist

Before finalizing data architecture:

- [ ] Data volume, velocity, and variety clearly understood
- [ ] Requirements for SLA (freshness) defined
- [ ] Storage vs Compute costs evaluated 
- [ ] Appropriate processing layer chosen (Batch vs Streaming)
- [ ] Idempotency strategies defined

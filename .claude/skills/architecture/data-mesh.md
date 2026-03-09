# Data Mesh

Data Mesh is an organizational and architectural paradigm that shifts away from centralized monolithic data lakes/warehouses toward a decentralized, domain-driven design.

## The Four Pillars

### 1. Domain-Oriented Decentralization
- **Concept:** Data ownership is distributed among cross-functional domain teams (e.g., Sales, Marketing, Logistics) rather than a central "Data Team".
- **Why:** Central teams become bottlenecks. Domain teams understand their own data best.

### 2. Data as a Product
- **Concept:** Domain teams treat data not as a byproduct of their applications, but as a formal product they offer to the rest of the organization.
- **Requirements:** The data product must be discoverable, addressable, trustworthy, self-describing, and interoperable.

### 3. Self-Serve Data Infrastructure as a Platform
- **Concept:** A dedicated platform team builds the underlying tooling and infrastructure (computing, storage, orchestration) to enable domain teams to build data products autonomously.
- **Goal:** Hide the underlying complexity. "Make it easy to do the right thing."

### 4. Federated Computational Governance
- **Concept:** A governing body (representing domain owners and platform engineers) establishes and enforces global rules.
- **Examples:** Naming conventions, security, compliance, interoperability standards, and data quality metrics.

## When to Use Data Mesh
- Massive organizational scale where central data engineering is failing to keep up.
- Not a technical solution for technical problems; it's a socio-technical solution for organizational scaling problems. Small teams (under 10 data engineers) should likely stick to a centralized Lakehouse.

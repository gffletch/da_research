# Delegated Authorization for AI Agents — Research Corpus

A living bibliography and knowledge graph tracking IETF, OIDF, academic, and industry work on how authority delegates from humans to AI agents.

**Maintainer:** George Fletcher (george@practicalidentity.com) — IAM / delegated-authorization practitioner  
**Corpus as of Jul 2026:** 191 sources across 6 tabs; 131 Active IETF Drafts

---

## Live views

| Page | Description |
|------|-------------|
| [IETF Cluster Analysis](https://gffletch.github.io/da_research/ietf_cluster_analysis.html) | Interactive map of 9 consolidation clusters across 131 Active IETF Drafts — color-coded by WG status, expandable per-cluster draft lists |
| [Protocol Boundary Map](https://gffletch.github.io/da_research/protocol_boundary_map.html) | One proposal for clean boundaries between DMSC, AgentProtocol, DAWN, WIMSE, OAuth, and WebBotAuth — click-to-expand layers, light/dark theme |
| [Knowledge Graph](https://gffletch.github.io/da_research/agent_authz_graph.html) | D3 force-directed graph of 74 nodes and 116 edges across the corpus (note: graph lags the workbook — see below) |

---

## What this tracks

The corpus covers six overlapping protocol families currently active in the IETF agent authorization space:

- **OAuth** — authorization tokens, delegation chains (RFC 8693, RFC 9396), scope attenuation, the 90+ individual draft extensions
- **WIMSE** — cryptographic workload identity for running agent processes (SPIFFE/SPIRE substrate)
- **WebBotAuth** — authentication of bots and AI agents to public web origin servers (HTTP Message Signatures, Signature Agent Card, Privacy Pass anonymous path)
- **DAWN** — federated, protocol-neutral discovery of agents, workloads, and services before connection
- **AgentProtocol (AGTP / A2A)** — agent-to-agent and agent-to-resource communication protocols; AGTP (port 4480, 18-method vocabulary) and Google Agent2Agent community submissions
- **DMSC** — gateway-centric multi-agent coordination with cross-organizational governance; Chinese telecom / academic consortium; MACP architecture

The bibliography also covers Published RFCs, OpenID Foundation specs (AuthZEN, FAPI, CAEP/SSF), Other Standards & Government (Kantara, W3C, NIST, EU AI Act), Academic Papers, and Industry & Implementations.

The [protocol boundaries analysis](protocol_boundaries_analysis.md) proposes clean ownership boundaries for each layer and documents the four open boundary tensions: discovery (DAWN vs. DMSC gateway vs. AGTP DISCOVER), web-facing identity (WebBotAuth vs. WIMSE mTLS), OAuth scope vs. AGTP authority scope, and DMSC governance vs. OAuth authorization.

---

## Files

### Canonical sources (edit these)

| File | Description |
|------|-------------|
| `build.py` | Bibliography builder — all 191 sources inline as 5-tuples `(title, summary, url, standards_org, comments)`. Run `python build.py` to regenerate the workbook. |
| `agent_authz_graph.json` | RAG-ready knowledge graph: 74 nodes, 116 edges. Self-describing (node_types, edge_types, categories, RAG guidance embedded). Currently lags the workbook (last synced at 92-source mark). |

### Generated outputs (tracked in git for diff visibility)

| File | Description |
|------|-------------|
| `delegated_authorization_research.xlsx` | The bibliography workbook — 6 content tabs plus an Index. Source of truth for counts. |
| `agent_authz_graph.html` | Interactive D3 force-directed visualization of the knowledge graph (~391 KB, D3 inlined for offline use). |
| `ietf_cluster_analysis.html` | Interactive cluster map — 9 consolidation clusters, color-coded WG status, expandable draft lists. |
| `protocol_boundary_map.html` | Interactive infographic — 6-layer protocol stack with click-to-expand detail and open boundary tensions. |
| `ietf_consolidation_analysis.pptx` | 12-slide informational deck covering the 9 clusters (no recommendations; survey/landscape tone). |

### Analysis documents

| File | Description |
|------|-------------|
| `consolidation_analysis.md` | Full 9-cluster analysis: which drafts overlap, what the consolidation pressure looks like per cluster. |
| `protocol_boundaries_analysis.md` | Proposed layer boundaries for the six protocol families; 4 open boundary tensions documented. |

### Build scripts

| File | Description |
|------|-------------|
| `validate.py` | Sanity check — loads the workbook, prints tab counts, confirms Index total, lists unparseable rows, checks URLs. Run after every edit. |
| `build_graph.py` | Knowledge graph builder (stale relative to the workbook; run manually when a graph rebuild is requested). |
| `build_consolidation_deck.py` | PowerPoint deck builder for `ietf_consolidation_analysis.pptx`. |

---

## Workbook tab structure

| Tab | Count | Notes |
|-----|-------|-------|
| Index | cover | Auto-summed |
| Published RFCs | 4 | Foundation primitives (RFC 6749, 7009, 8693, 9396) |
| Active IETF Drafts | 131 | Where the action is — WG + individual drafts across all six protocol families |
| OpenID Foundation | 11 | AuthZEN 1.0, ARAP, FAPI, CAEP/SSF, HEART |
| Other Standards & Govt | 6 | Kantara, W3C VC, NIST AI RMF, EU AI Act |
| Academic Papers | 5 | arXiv + IEEE |
| Industry & Implementations | 34 | Vendor blogs, reference implementations, the McGuinness Mission-Bound series |

---

## Adding a new source

1. Edit `build.py` — locate the right tab section and add the row as a 5-tuple `(title, summary, url, standards_org, comments)`.
2. Run `python build.py` to regenerate the workbook.
3. Run `python validate.py` to confirm counts and URL integrity.
4. Commit — git history is the version trail.
5. Graph rebuild is deliberate and batched, not automatic. Update `build_graph.py` and rerun only when structurally significant changes warrant it.

See `CLAUDE.md` for placement rules, narration style conventions, and the full pending watch list.

---

## Author clusters worth following

- **Karl McGuinness** (Independent, former Okta SVP): 11 individual I-Ds, 1 OIDF profile (ARAP), 4 Mission-Bound blog posts. Most concentrated single-author body of work in the corpus.
- **Kühlewind / Birkholz** (Ericsson / Fraunhofer SIT): `draft-kuehlewind-audit-architecture` is the HUB — composes 10+ other specs into a single auditable architecture.
- **Dick Hardt**: `draft-hardt-oauth-aauth-protocol` is the principled OUTLIER — zero OAuth dependencies; argues PoP-by-default and AS-to-AS federation are architectural changes, not extensions.
- **Chris Hood / Nomotic**: 18-draft AGTP suite; a complete protocol stack replacement for agent communication.

---

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install openpyxl python-pptx
python validate.py
```

Requires Python 3.9+. No external network access needed for build or validate.

---

## License

Research corpus. Content represents publicly available standards documents and analysis. No warranty expressed or implied.

# IETF Agent Authorization Drafts — Consolidation Analysis

**Date:** 2026-07-10  
**Corpus:** 158 sources; 98 Active IETF Drafts  
**Scope:** Active IETF Drafts tab only

## Framing

Three consolidation scenarios exist based on WG adoption status within a cluster:

- **2+ WG-adopted drafts in a cluster** — already settled at the WG level; individual drafts extend/profile each WG item rather than seeking merger
- **1 WG-adopted draft** — individual drafts are candidates for absorption into the WG item (before it reaches RFC) or companion specs alongside it (after)
- **0 WG-adopted drafts** — individual-to-individual consolidation required before any can seek WG adoption

## WG-Adopted Drafts in the Corpus

| Draft | Status |
|---|---|
| `draft-ietf-oauth-identity-chaining` | IESG-approved, RFC Editor queue |
| `draft-ietf-oauth-transaction-tokens` | WG, WGLC at -09; IESG target Dec 2026 |
| `draft-ietf-oauth-identity-assertion-authz-grant` (ID-JAG) | WG, -03 |
| `draft-ietf-oauth-attestation-based-client-auth` | WG, -10 |
| `draft-ietf-oauth-first-party-apps` | WG, -03 |
| `draft-ietf-oauth-spiffe-client-auth` | WG (adopted from schwenkschuster), -01 |
| `draft-ietf-oauth-browser-based-apps` | WG, -26 |
| `draft-ietf-oauth-security-topics-update` | WG, -01 |

WIMSE WG has its own adopted suite (arch, identifier, mutual-tls, http-signature) — treated as a separate WG throughout.

---

## Cluster A — Transaction Token Extensions

**WG anchor:** `draft-ietf-oauth-transaction-tokens` (1 WG draft, WGLC)

| Draft | Relationship to WG item |
|---|---|
| `draft-araut-oauth-transaction-tokens-for-agents` | Profiles TxnTokens with `act`, `agentic_ctx`, `actchain` — directly extends the WG spec; WG will likely absorb these claims into the base draft or make araut a companion profile |
| `draft-fletcher-transaction-token-chaining-profile` | Uses TxnTokens as the subject credential in RFC 8693 to cross domain boundaries — a different problem (cross-domain) the WG draft deliberately defers; natural companion spec once TxnTokens reaches RFC |
| `draft-zhu-oauth-async-delegation` | Delegation Handle for async token refresh without re-prompting user — addresses a gap the WG draft acknowledges but doesn't solve; candidate for absorption in a future revision |

**Action:** araut and zhu are absorption candidates into the WG draft. fletcher is the right shape for a separate companion spec. No individual-to-individual merging needed — three distinct problems.

---

## Cluster B — Cross-Domain Identity / Token Exchange

**WG anchor:** `draft-ietf-oauth-identity-chaining` (past merge point — at RFC Editor; cannot absorb new material)

Since identity-chaining is past the point of absorption, individual drafts in this space become **companion specs to the future RFC**, not merges:

| Draft | Relationship |
|---|---|
| `draft-fletcher-transaction-token-chaining-profile` | Profiles identity-chaining + TxnTokens together — natural companion RFC |
| `draft-mcguinness-token-xchg-target-svc-disco` | Discovery of token-exchange targets — fills a gap assumed by identity-chaining; standalone companion |
| `draft-mcguinness-oauth-id-assertion-framework` | Trust framework for who can issue into a namespace — prerequisite context for identity-chaining's issuer validation |
| `draft-mcguinness-oauth-domain-authorized-issuer` | DNS-based trust method implementing id-assertion-framework |
| `draft-liu-oauth-chain-delegation` | Structured delegation lineage — extends what identity-chaining can express; also overlaps with Cluster D |

**Action:** id-assertion-framework + domain-authorized-issuer should merge (they are architecturally one spec split across two documents). The rest stand alone as companion specs to the identity-chaining RFC.

---

## Cluster C — Client Authentication / Instance Identity

**WG anchor:** `draft-ietf-oauth-attestation-based-client-auth` (1 WG draft, -10)

| Draft | Relationship |
|---|---|
| `draft-mcguinness-oauth-client-instance-assertion` | Instance-level identity within an attestation flow — extends the WG draft's "client instance" concept; strong absorption candidate |
| `draft-mcguinness-oauth-ai-agent-instance` | AI-specific instance profiling on top of client-instance-assertion — one layer higher; profiles the WG draft for agent platforms |

**Action:** client-instance-assertion is a near-certain absorption target into the WG draft. ai-agent-instance profiles both and should wait for that absorption before seeking WG adoption. These two should consolidate first, then seek absorption together.

---

## Cluster D — Actor Chain Representation

**WG anchor:** None

No WG item exists for "how to represent and cryptographically verify delegation chains in RFC 8693."

| Draft | Approach | WG fit |
|---|---|---|
| `draft-mcguinness-oauth-actor-profile` | Profiles `act` claim; structural rules; chain validation; no per-hop crypto | Strong — incremental on RFC 8693 |
| `draft-mcguinness-oauth-actor-receipts` | Per-hop signed receipts; verifiable provenance layer | Extends actor-profile; same author |
| `draft-mcguinness-oauth-actor-proofs` | Hash-chained per-hop proof claim | Extends actor-profile; same author |
| `draft-mw-oauth-actor-chain` | 6 cryptographic chain profiles (Declared/Verified × Full/Subset/Actor-Only); addresses chain-splicing directly | Comprehensive but 97 pages |
| `draft-liu-oauth-chain-delegation` | `delegation_chain` array with per-hop authorization constraints | Parecki co-authorship = WG adoption credibility |

**Action (individual → individual):** The McGuinness triad (actor-profile + receipts + proofs) should consolidate into one draft before seeking WG adoption — they are one coherent design written by one author. mw-actor-chain and liu-chain-delegation need to reconcile: liu's Parecki co-authorship gives it the cleaner WG adoption path; mw's cryptographic rigor is the technical contribution. Most likely outcome: liu becomes the WG item with mw's cryptographic profiles incorporated as the verification mechanism.

---

## Cluster E — Token Attenuation / Sub-delegation

**WG anchor:** None

| Draft | Approach |
|---|---|
| `draft-niyikiza-oauth-attenuating-agent-tokens` | RAR-based monotonic attenuation; offline chain verification; typed constraint vocabulary |
| `draft-mishra-oauth-agent-grants` (DAAP) | New JWT claims (agt, dev, grnt, scp, bdg); depth-limiting; cascade revocation; budget-bounded grants |
| `draft-li-oauth-delegated-authorization` | Hierarchical delegation token type; client mints subordinate narrowly-scoped tokens |
| `draft-ni-oauth-batch-authorization-delegation` | Batch RAR + Token Exchange for multi-agent orchestration efficiency |

**Action (individual → individual):** niyikiza, DAAP, and li-delegated all assert the same invariant (sub-delegate cannot exceed root authority) via incompatible mechanisms. They must consolidate before any can seek WG adoption under the OAuth recharter "Complex Delegation" milestone. niyikiza's RAR-based approach aligns best with existing WG investment in RFC 9396. Cascade revocation (DAAP) and budget-bounding (DAAP) are the most distinctive transferable concepts. Batch-delegation (ni) is a distinct efficiency mechanism that could stand separately or as a section.

---

## Cluster F — Pre-Action Authorization / Permit-Before-Commit

**WG anchor:** None

| Draft | Approach |
|---|---|
| `draft-lee-orprg-permit-receipts` | Abstract framework; requirements and data model for PermitReceipts; verifier-before-execution |
| `draft-nelson-agent-delegation-receipts` | Concrete: user's private key signs Authorization Objects before runtime; append-only log; -10 |
| `draft-williams-intent-token` | Lightweight: signed human-declared authorization envelope; positioned as OAuth complement, not replacement |

**Action (individual → individual):** Lee's abstract framework + Nelson's mechanism is the natural merge — lee provides the requirements framing, nelson provides the normative protocol (most iterated draft in this space at -10). Williams is distinct enough (lighter-weight, explicit OAuth complement positioning) to stand separately. Target: one "OAuth Pre-Execution Authorization" spec from lee + nelson, with Williams as an optional lightweight profile appendix.

---

## Cluster G — HTTP Authorization Challenge Signals

**WG anchor:** None directly. `draft-ietf-oauth-first-party-apps` (WG) defines an Authorization Challenge Endpoint for *user authentication* step-up — related but distinct; not the right absorption target.

| Draft | What's insufficient | Trigger |
|---|---|---|
| `draft-rosomakho-oauth-txn-challenge` | Transaction-specific authorization; RS challenges, human approves at AS | RS-initiated |
| `draft-kahrer-oauth-client-challenge-protocol` | Client-level assertion or VP; AS challenges the client mid-flow | AS-initiated |
| `draft-mcguinness-oauth-insufficient-claims` | Credential claims; RS signals which specific claims are missing | RS-initiated |

**Action (individual → individual):** These three operate at the same "you need more before I can serve you" layer but address distinct insufficiency types. They must coordinate on a shared error-code namespace and challenge-response envelope before seeking WG adoption — three separate specs introducing new OAuth error codes in the same family is exactly what OAuth WG chairs try to prevent. An umbrella "OAuth Authorization Insufficiency Signaling" framework with three named profiles is the likely convergence path to WG adoption.

---

## Cluster H — AIP Name Collision — BLOCKING

**WG anchor:** None

| Draft | Approach |
|---|---|
| `draft-singla-agent-identity-protocol` (AIP) | Six-layer model (identity → reputation); W3C DID; G1/G2/G3 grant tiers; 75+ pages |
| `draft-prakash-aip` (AIP) | IBCTs; JWT/Ed25519 + Biscuit+Datalog; MCP/A2A bindings; technically strong |
| `draft-aip-agent-identity-protocol` (AIP) | Per-tool-call AIP Token; YAML policy; HITL proxy |

**Action:** Name collision is a **blocking issue** — no WG adoption path opens until the IETF secretariat forces re-slugs. Only after re-slugging can the WG assess overlap and consolidation. Prakash's technical approach (Biscuit+Datalog) is the strongest for WG adoption if the DID dependency issue is resolved. Singla and aip-agent-identity-protocol are broadly scoped agent identity frameworks with significant overlap; those two are the more likely consolidation pair.

---

## Cluster I — WIMSE Extensions for AI Agents

**WG anchor:** WIMSE WG has 4 adopted WG drafts (arch, identifier, mutual-tls, http-signature) — but these are *core* WIMSE, not agent-specific. Individual agent-focused submissions are not competing with those WG items; they are extending the WIMSE framework into a new application domain.

| Draft | Role |
|---|---|
| `draft-ni-wimse-ai-agent-identity` | Applicability statement mapping WIMSE to AI agent use cases; -02; most developed |
| `draft-reece-wimse-cross-org-delegation` | Problem statement for cross-org delegation gap |
| `draft-jiang-wimse-heterogeneous-credential` | Multi-format credential verification across WIMSE deployments; -01 |
| `draft-schwenkschuster-wimse-trust-domain-discovery` | Trust bundle discovery endpoint; companions draft-ietf-oauth-spiffe-client-auth |
| `draft-winmagic-wimse-condition-bounded-credentials` | Posture-conditioned (not time-bounded) credential validity |
| `draft-munoz-wimse-authorization-evidence` | Signed authorization-evidence records for WIMSE-authorized actions |

**Action:** ni-wimse-ai-agent-identity as applicability statement is the natural WIMSE WG adoption target — it frames why WIMSE applies to agents. The others are protocol extensions the WIMSE WG would evaluate individually after the applicability statement is adopted. reece's problem statement and jiang's heterogeneous-credential are the two most likely to feed into a WIMSE WG work item as they address gaps in the core WIMSE architecture; schwenkschuster-trust-domain-discovery and munoz-wimse-authorization-evidence can stand separately or as WIMSE WG milestones.

---

## Summary Table

| Cluster | WG anchors | Type | Primary action |
|---|---|---|---|
| A — TxnToken extensions | 1 (txn-tokens, WGLC) | Individual → WG absorption | araut + zhu absorb into WG; fletcher → companion spec |
| B — Cross-domain identity | 1 (identity-chaining, past merge point) | Individual → companion spec | id-assertion-framework + domain-authorized-issuer merge; rest are companion specs |
| C — Client/instance auth | 1 (attestation-based-client-auth) | Individual → WG absorption | client-instance-assertion + ai-agent-instance consolidate, then absorb |
| D — Actor chain | 0 | Individual → individual | McGuinness triad consolidate; mw + liu consolidate |
| E — Token attenuation | 0 | Individual → individual | niyikiza + DAAP + li consolidate; ni-batch may stand separately |
| F — Pre-action permit | 0 | Individual → individual | lee + nelson merge; williams stays as optional profile |
| G — HTTP challenge signals | 0 (adjacent to FiPA, different problem) | Individual → individual | Coordinate error-code namespace; umbrella → WG adoption |
| H — AIP collision | 0 | **BLOCKING** | Re-slug required before any analysis is meaningful |
| I — WIMSE agent extensions | 4 (WIMSE core, different scope) | Individual → WG applicability | ni-wimse as adoption target; others extend individually |

---

## Watch Points

- **OAuth WG recharter "Complex Delegation" milestone** — once active, will force consolidation decisions in Clusters D, E, and G; the WG chairs will either pick winners or mandate consolidation
- **identity-chaining RFC number** — once assigned, companion specs in Cluster B can reference a stable RFC rather than a draft
- **transaction-tokens WGLC** — once complete and advancing to IESG, absorption decisions for Cluster A (araut, zhu) become urgent
- **AIP re-slugging** — Cluster H is inert until resolved; IETF secretariat involvement likely required

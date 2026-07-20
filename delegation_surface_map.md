# Delegation Surface Map: Where "Delegation" Is Being Defined Across the Corpus

**Date:** 2026-07-20
**Corpus:** 191 sources; 131 Active IETF Drafts
**Companion to:** `protocol_boundaries_analysis.md`

## Purpose

The Protocol Boundary Map answers *"which family owns which layer?"* This document answers a different question that cuts across every layer of that map: **how many distinct semantic models of "delegation" are currently being defined, and by whom?**

Delegation is not a layer — it is a cross-cutting concern that appears in OAuth tokens, AGTP protocol headers, DMSC gateway routing decisions, WIMSE workload assertions, WebBotAuth bot identities, W3C verifiable credentials, and (proposed) AUDIT audit records. Each surface encodes a different mental model of what "acting on behalf of" means, what evidence is required, how attenuation works, and what revocation looks like.

Fifteen distinct delegation semantic models are in flight across the corpus as of July 2026. This document enumerates them, distinguishes surfaces that **redefine** delegation from those that **profile or compose** an existing definition, and closes with a targeted analysis of the AUDIT BoF charter — the newest and highest-risk potential seventh definitional surface.

---

## Executive Summary

- **15 delegation semantic models** are currently defined or proposed across the corpus, distributed across 4 categories.
- **6 IETF working groups** (OAuth, WIMSE, WebBotAuth, DAWN, and proposed AUDIT and DMSC BoFs) plus 3 non-IETF venues (OpenID Foundation, W3C, and independent architect blogs) are all producing delegation-adjacent normative or informative text.
- **Within the OAuth WG alone**, at least 5 distinct delegation mechanics are in individual drafts, plus 3 semantic frames, plus the WG's own Complex Delegation recharter milestone. Intra-WG fragmentation is the largest current source of definitional overlap.
- **The AUDIT charter is Observer-posture at the top level** — the text explicitly commits to composing OAuth, WIMSE, RATS, SCITT, W3C Trace Context, and vCon rather than replacing them. This is genuinely reassuring. However, two of the four proposed deliverables have latent drift potential toward defining delegation semantics as a side effect. Specific text to watch is called out in the AUDIT Charter Analysis section below.

---

## The Four Categories

Delegation surfaces fall into four categories with materially different composition risk profiles.

| Category | Description | Models | Composition risk |
|---|---|---|---|
| **1. OAuth-layer mechanics** | How tokens *carry* delegation — the wire format | 5 | High intra-OAuth fragmentation; low cross-family risk |
| **2. OAuth-layer semantics** | What authority is being *conveyed* by those tokens | 3 | Medium — each model implies a different consent story |
| **3. Non-OAuth surfaces** | Delegation declared outside the OAuth token stream | 4 | High cross-family collision risk (this is where the Protocol Boundary Map tensions live) |
| **4. Cross-cutting concerns** | Delegation as observed / evidenced / escalated by adjacent systems | 3 | Depends on posture — Observer safe, Arbiter dangerous |

---

## Category 1: OAuth-Layer Delegation Mechanics

Five distinct wire-format models for representing delegation in OAuth tokens. All extend, replace, or ignore RFC 8693's `act` claim baseline.

### 1A. Informational actor chain (baseline)

- **Key drafts:** RFC 8693, `draft-mcguinness-oauth-actor-profile`
- **Defines:** Nested `act` claim carrying the actor identity; chain of `act.act.act...` for multi-hop. Informational only — chain integrity depends on each hop being trusted.
- **Composition with RFC 8693:** IS the baseline. Actor Profile adds `sub_profile` classification and uniform processing rules across JWT assertion grants, access tokens, and Transaction Tokens.
- **Layer:** OAuth
- **Notes:** McGuinness's profile deliberately leaves provenance out of scope; the informational-chain limitation is documented, not fixed. Composes with model 1B for the verified-chain case.

### 1B. Cryptographically verifiable actor chain

- **Key drafts:** `draft-mw-oauth-actor-chain` (re-slugged from `draft-mw-spice-actor-chain-05`)
- **Defines:** Per-hop signatures and commitment chain so any consumer can verify the chain without trusting intermediate issuers. Six sub-profiles covering declared vs. verified branches and cross-domain re-issuance.
- **Composition with RFC 8693:** Extends. Plain 8693 impersonation-shaped outputs remain valid and are outside this profile family.
- **Layer:** OAuth
- **Notes:** Directly addresses the "chain splicing" weakness in 8693. Complementary to the McGuinness Actor Profile — same problem space, different security posture.

### 1C. Attenuating capability tokens

- **Key drafts:** `draft-niyikiza-oauth-attenuating-agent-tokens`
- **Defines:** Macaroon-style third-party caveats let each delegation hop narrow (never widen) the authority carried by the token. Bearer-verifiable attenuation.
- **Composition with RFC 8693:** Extends the token model with a caveat structure orthogonal to `act`. In principle composes with 1A/1B for identity-plus-attenuation.
- **Layer:** OAuth
- **Notes:** Only draft in the corpus that treats delegation as *authority narrowing*. All other models preserve or transform authority; this one is designed to shrink it.

### 1D. Agent grants with cascade revocation

- **Key drafts:** `draft-mishra-oauth-agent-grants` (DAAP — Delegated Agent Authorization Protocol)
- **Defines:** New JWT claims (`agt`, `dev`, `grnt`, `scp`, `bdg`), depth-limiting on sub-delegation, and cascade revocation of the entire delegation subtree when any ancestor is revoked.
- **Composition with RFC 8693:** Replaces rather than extends — the claim set is intentionally distinct from `act`. Runs alongside 8693 rather than composing with it.
- **Layer:** OAuth
- **Notes:** Structural overlap with `draft-niyikiza-oauth-attenuating-agent-tokens` (both propose budget-bounded grants). OAuth WG will likely expect consolidation with the actor-chain and Mission-Bound work before either can advance.

### 1E. Transaction Token chaining

- **Key drafts:** `draft-ietf-oauth-transaction-tokens` (WG), `draft-araut-oauth-transaction-tokens-for-agents`, `draft-fletcher-transaction-token-chaining-profile`
- **Defines:** Short-lived signed JWTs that propagate through a call chain, carrying request-level authorization context that outlives (or replaces, at trust-domain boundaries) the original access token.
- **Composition with RFC 8693:** Different token type — composes with 8693 rather than replacing it. Chaining profile explicitly handles cross-domain Transaction Token handoff.
- **Layer:** OAuth (intra-service and cross-service request tracing)
- **Notes:** The chaining profile is normatively referenced by the McGuinness Mission-Bound OAuth MVP as the alternative to ID-JAG for Transaction-Token-rooted cross-AS flows.

---

## Category 2: OAuth-Layer Delegation Semantics

Three distinct semantic frames for *what* is being delegated. These are complementary to Category 1 (they can use any of the wire mechanics) but each implies a different consent story and a different authoritative record.

### 2A. On-behalf-of user grant (per-request)

- **Key drafts:** `draft-oauth-ai-agents-on-behalf-of-user`, `draft-li-oauth-delegated-authorization`
- **Defines:** The authorization request explicitly names the agent that will act (`requested_actor` parameter); the AS issues a token with delegation semantics baked in at grant time.
- **Composition with RFC 8693:** Extends the authorization request; the resulting token uses the `act` claim per 1A.
- **Layer:** OAuth
- **Notes:** Explicit, per-request. Closest to "traditional" OAuth flavor. Loses the ability to represent long-running or dynamic delegation.

### 2B. Cross-domain identity chaining

- **Key drafts:** `draft-ietf-oauth-identity-chaining` (WG), `draft-ietf-oauth-identity-assertion-authz-grant` (ID-JAG, Parecki/McGuinness/Campbell, WG-adopted)
- **Defines:** Preserving identity and call chain information across trust domains via a shared IdP. Same-user access to a downstream API through a chain of AS trust relationships.
- **Composition with RFC 8693:** Extends 8693 for the cross-AS case.
- **Layer:** OAuth
- **Notes:** WG-adopted (identity chaining) and near-WG (ID-JAG). The Fletcher Transaction Token Chaining Profile is positioned as the alternative for Transaction-Token-rooted flows where ID-JAG doesn't apply.

### 2C. Mission (durable AS-stored authority record)

- **Key drafts:** `draft-mcguinness-oauth-mission-bound-minimum-profile` (target I-D per McGuinness MVP blog post, not yet on Datatracker), `draft-mcguinness-oauth-mission-bound-runtime-enforcement-profile` (target I-D per IBAC blog post, not yet on Datatracker); Mission-Bound OAuth blog series in Industry tab
- **Defines:** A first-class OAuth object — a durable AS-stored record of what the user approved. Tokens, scopes, PDP decisions, and audit records all reference the Mission. Tokens become downstream projections of a persistent authority object rather than the authority itself.
- **Composition with RFC 8693:** Additive — adds a `mission` claim to tokens; existing 8693 flows continue to work. Runtime Enforcement Profile layers IBAC (Intent-Based Access Control) on top.
- **Layer:** OAuth (but conceptually above the token layer)
- **Notes:** The most architecturally ambitious of the semantic models. Cross-AS handoff uses ID-JAG (2B) for user-rooted flows or the Fletcher Transaction Token Chaining Profile (1E) for Txn-Token-rooted flows. Explicit conformance ladder L0–L5.

---

## Category 3: Non-OAuth Delegation Surfaces

Four surfaces where delegation is declared outside the OAuth token stream. These are the sources of the tensions documented in `protocol_boundaries_analysis.md`.

### 3A. Protocol-header authority declaration (AGTP)

- **Key drafts:** `draft-hood-independent-agtp` (Agent-Authority-Scope header), `draft-hood-agtp-composition`, `draft-bu-agentproto-security-principal-binding`
- **Defines:** Declares agent authority at the protocol layer in a mandatory header, rather than only inside the OAuth token. `hood-agtp-composition` specifies that AGTP headers take normative precedence over adjacent-layer fields.
- **Composition with RFC 8693:** Parallel and preemptive. AGTP-native infrastructure enforces the AGTP header; OAuth-native resource servers enforce token claims. `bu-agentproto-security-principal-binding` (Jul 2026) is the first draft actively working the composition semantics.
- **Layer:** AgentProtocol
- **Notes:** This is Boundary Tension #3 in the Protocol Boundary Map. Genuine cross-layer redefinition — the same delegation concept has two authoritative representations with different verifiers and freshness models.

### 3B. Gateway-mediated task delegation (DMSC)

- **Key drafts:** `draft-li-dmsc-macp`, `draft-li-dmsc-inf-architecture`, `draft-sz-dmsc-iaip`, `draft-yang-dmsc-ioa-task-protocol`, `draft-somoza-dmsc-atn-agent-trust-negotiation`, `draft-dunbar-dmsc-gw-scenarios-gap-analysis`
- **Defines:** Task assignment across administrative domains as a coordination-layer concern, not a token concern. The gateway is the normative delegation point — it decides which agents to route intent to, negotiates capability, and records the coordination contract.
- **Composition with RFC 8693:** Orthogonal at the model level; defers to OAuth for sub-agent token-layer authorization within delegated tasks. There is no DMSC profile of OAuth delegation.
- **Layer:** DMSC (Coordination)
- **Notes:** This is Boundary Tension #4 in the Protocol Boundary Map. The dunbar gap analysis explicitly positions DMSC as filling the cross-org governance gap that OAuth doesn't own — an implicit assertion that OAuth's delegation semantics are insufficient at the coordination layer.

### 3C. Workload identity assertion (WIMSE)

- **Key drafts:** `draft-ietf-wimse-arch`, `draft-ietf-wimse-workload-identity-use-cases`, `draft-ietf-oauth-spiffe-client-auth` (WG), `draft-schwenkschuster-wimse-trust-domain-discovery`, `draft-ni-wimse-ai-agent-identity`
- **Defines:** Cryptographic identity for running agent processes. Workload-to-workload calls with SPIFFE SVIDs are implicit delegation — one workload acts as itself but on behalf of an upstream request that originated with a user.
- **Composition with RFC 8693:** Feeds into OAuth via `spiffe-client-auth` — SVID becomes an OAuth client assertion, which becomes an OAuth token carrying an `act` claim. WIMSE identity → OAuth authorization is the WG-adopted handoff.
- **Layer:** WIMSE
- **Notes:** WIMSE deliberately does not define delegation semantics — the handoff is clean. However, cross-trust-domain workload calls have delegation-like implications that the current WIMSE drafts do not explicitly address.

### 3D. Web-facing agent authentication (WebBotAuth)

- **Key drafts:** `draft-meunier-webbotauth-registry` (Signature Agent Card), `draft-meunier-webbotauth-httpsig-protocol`, `draft-rescorla-anonymous-webbotauth`
- **Defines:** Bot proves who it operates for via HTTP Message Signatures over its requests. The Signature Agent Card is a delegation artifact — it asserts *"this key represents this operator's bot,"* which is delegation from operator to bot expressed at the HTTP layer.
- **Composition with RFC 8693:** Precondition. WebBotAuth answers *"is this bot legitimate?"* before OAuth answers *"is this bot authorized?"* Distinct concerns; clean handoff.
- **Layer:** WebBotAuth
- **Notes:** The anonymous path (`draft-rescorla-anonymous-webbotauth`) and the signed identity path represent a WG-internal design fork over whether delegation identity is required for web-facing agents at all.

---

## Category 4: Cross-Cutting Concerns

Three surfaces where delegation is observed, evidenced, or escalated by adjacent systems rather than declared or issued.

### 4A. Audit-record delegation context (AUDIT — proposed)

- **Key drafts:** `draft-kuehlewind-audit-architecture` (informational architecture underpinning the AUDIT BoF), AUDIT charter deliverables (see dedicated section below)
- **Defines:** Data model for representing delegation context in an audit trail. Interaction, Action, Delegation, and Authorization Transition are the four record types framed by user-intent that give the AUDIT acronym its expansion.
- **Composition with RFC 8693:** *Depends on WG posture — Observer or Arbiter.* Charter is Observer-leaning; see AUDIT Charter Analysis section for the specific deliverables where drift risk lives.
- **Layer:** Cross-layer (no single home; kuehlewind-audit-architecture is a HUB but not a stack layer)
- **Notes:** This is the surface that motivated this document. Discussed in detail below.

### 4B. Verifiable credentials for delegation (W3C)

- **Key drafts:** W3C VC 2.0, VC delegation types
- **Defines:** Signed delegation credentials as portable authority artifacts, independent of any specific issuer or protocol.
- **Composition with RFC 8693:** External to OAuth; can be presented as a subject token in Token Exchange (RFC 8693 §2.1.1) or as a bearer credential in a JWT authorization grant (RFC 7523).
- **Layer:** External (W3C)
- **Notes:** Semantically the most portable delegation representation — a VC delegation credential can flow across every layer in the Protocol Boundary Map. Currently underused in the IETF drafts corpus; likely to gain adoption as VC 2.0 stabilizes.

### 4C. AuthZEN Access Request and Approval Profile (ARAP)

- **Key drafts:** OpenID AuthZEN Access Request and Approval Profile Draft 1 (McGuinness, adopted as AuthZEN WG draft May 2026)
- **Defines:** The escalation semantics when a PDP returns `decision: false` but the requested authority could be granted via workflow. Introduces `evaluation_id` binding, JWS `binding_token`, and re-evaluation after workflow completion.
- **Composition with RFC 8693:** Precedes token issuance rather than modifying it. Composes with any of the Category 1 mechanics and any of the Category 2 semantics — ARAP handles the deny-then-escalate boundary and hands the eventual token issuance back to normal OAuth flows.
- **Layer:** OpenID Foundation / adjacent to OAuth
- **Notes:** Explicitly positioned against CIBA — CIBA solves authentication freshness, ARAP solves authorization escalation. Adds a new state ("requestable denial") that doesn't map cleanly onto the delegation lifecycle of any Category 1 or 2 model without profiling.

---

## AUDIT Charter Analysis

The AUDIT BoF charter (`mirjak/audit-bof-preparation/audit-charter.md`) resolves substantially in favor of the Observer posture. The relevant reassuring text:

> "The working group will **compose** existing IETF building blocks for identity (WIMSE), attestation (RATS), authorization (**OAuth family**), transparency (SCITT), context propagation (W3C Trace Context), and conversation containers (vCon), and will define only the additional protocol elements, data models, and best practices needed to make these compose coherently for the AI agent case."

> "The working group will **not define auditing policies or compliance frameworks**, but instead provide the technical building blocks needed to support them."

This is exactly the right framing to avoid becoming the seventh definitional surface. Delegation semantics belong to OAuth (and, by the boundary map, to WIMSE / AGTP / DMSC where those layers own the delegation event). AUDIT observes what those layers produce.

However, two of the four deliverables have latent drift risk. These are the specific texts to watch during the BoF discussion and any subsequent WG work:

### Drift risk in Deliverable 2 — Audit Data Models and Semantics

> "One or more Standards Track RFCs defining data models for representing audit information, including interaction records, agent identity, **delegation context**, authorization state over time, and action provenance."

The phrase "delegation context" is where semantic drift can occur without anyone intending it. A safe formulation is:

> *"A delegation-context record contains whatever act-chain, actor-chain, mission reference, gateway task ID, or protocol authority header the source layer produced, carried verbatim in a source-typed envelope. AUDIT does not require the source layer to reshape its delegation representation to fit an AUDIT-specific schema."*

A drift-risk formulation to watch for and push back on:

> *"A delegation-context record MUST contain: delegator identity, delegatee identity, delegation type ∈ {impersonation, on-behalf-of, capability, coordination}, delegation scope, delegation purpose, delegation attenuation..."*

The second formulation looks innocuous but forces every source layer to normalize its delegation representation to a canonical AUDIT schema. That is definitional — it defines what delegation *is* by defining what its audit record *must* contain. Once such a schema is normatively required, every OAuth extension, AGTP profile, and DMSC gateway becomes obligated to fill it in, and the enum values in `delegation type` become a de-facto controlled vocabulary for what counts as delegation. This is how AUDIT could inadvertently become the seventh definitional surface.

### Drift risk in Deliverable 3 — Protocol Extensions or Profiles

> "One or more Standards Track RFCs specifying extensions to existing IETF protocols (e.g., HTTP, OAuth, or token formats) to convey audit-related information."

If an AUDIT-defined OAuth extension introduces new claims (e.g., `audit_delegation_id`, `audit_delegator_evidence`) that must be populated at token issuance, those claims can subtly encode a delegation semantic model. Safe path: any AUDIT-introduced claim is opaque to OAuth semantics — a correlation identifier only. Risk path: AUDIT claims carry structured delegation metadata.

### Recommended watch list for the BoF and early WG work

1. Does the "delegation context" data model normatively prescribe fields that don't exist in the source layers, or does it accept source-layer representations verbatim?
2. Do the enum values in any delegation-related field function as a controlled vocabulary, or are they source-declared?
3. Do AUDIT-introduced OAuth claims carry only correlation identifiers, or do they carry structured delegation metadata?
4. Does the "authorization state over time" data model prescribe a state machine, or does it observe whatever state machine the source layer uses?

If the answers land on the observer side of these four questions, AUDIT is unifying and additive — a genuine benefit. If any land on the arbiter side, AUDIT becomes a definitional surface and the count moves from 15 to 16 with a governance problem attached.

---

## Composition Patterns

Not all of the 15 surfaces compose. Some are additive; some conflict; some are silently incompatible.

### Additive (compose without semantic change)

- **1A ↔ 1B ↔ 1C:** Actor Profile + verifiable chain + attenuation. Each addresses a different property of the same underlying delegation event.
- **2C + 1E + 2B:** Mission-Bound OAuth uses Transaction Token Chaining and ID-JAG as its cross-AS handoff mechanisms.
- **3C → 1A:** WIMSE SVID → OAuth client_assertion → OAuth token with `act` claim. Clean handoff.
- **3D → 1A:** WebBotAuth Signature Agent Card → OAuth authorization decision. Clean handoff.
- **4C + Category 1/2:** ARAP handles the escalation boundary and defers to normal OAuth for eventual issuance.

### Conflicting (define competing semantics for the same event)

- **1A vs. 1D:** McGuinness Actor Profile uses `act`; Mishra DAAP uses new claims. Not composable — a token cannot be both simultaneously.
- **1A vs. 2C:** Actor Profile treats the token as authoritative; Mission-Bound treats the token as a projection of a durable AS record. Compatible only if 2C is layered above 1A rather than replacing it.
- **3A vs. Category 1/2:** AGTP `Agent-Authority-Scope` header has normative precedence over OAuth scope on AGTP hops. Composition is defined asymmetrically — OAuth-native consumers don't see AGTP, AGTP-native consumers preemptively override OAuth.
- **3B vs. Category 1/2:** DMSC gateway task delegation happens above the OAuth layer; no explicit composition profile exists between DMSC coordination decisions and OAuth token issuance for the underlying sub-agent calls.

### Silently incompatible (no defined composition)

- **1C vs. 1D:** Attenuating tokens and DAAP both propose budget-bounded grants but with structurally different claim sets. No composition profile.
- **3A vs. 3B:** AGTP and DMSC could plausibly co-exist (AGTP as transport under a DMSC gateway) but no draft addresses how AGTP authority headers relate to DMSC task delegation records.
- **4A vs. everything:** Depends on AUDIT WG posture (see charter analysis above).

---

## Open Tensions and Definitional Forks

Beyond the four boundary tensions in `protocol_boundaries_analysis.md`, the delegation surface has three additional forks worth tracking:

### Fork 1: Which OAuth-layer mechanic wins for agents?

The OAuth WG will need to consolidate at least three of {`mcguinness-actor-profile`, `mw-oauth-actor-chain`, `mishra-oauth-agent-grants`, `niyikiza-attenuating-tokens`} before advancing agent-delegation work to WG documents. All four address the same problem space with distinct designs. The recharter's "Complex Delegation" milestone is where this consolidation will happen or fail to happen.

### Fork 2: Is delegation an issuance-time event or a runtime object?

Category 1 and 2A models treat delegation as fully specified at issuance — the token is the authority, the record is the log. Model 2C (Mission-Bound) treats delegation as a runtime object with a lifecycle — the token is a projection, the authority record is durable and mutable. These are architecturally distinct choices; each has downstream implications for revocation, evidence, and audit. The two can coexist but the corpus has not converged on which is the default.

### Fork 3: Does delegation belong to the token layer, the protocol layer, or the coordination layer?

- Category 1/2 answer: token layer (OAuth owns it).
- Category 3A answer: protocol layer (AGTP header owns it).
- Category 3B answer: coordination layer (DMSC gateway owns it).
- Category 4A (AUDIT) answer, if it takes Arbiter posture: cross-layer audit format owns it.

The Protocol Boundary Map is careful not to prescribe on this fork — it documents where each family claims delegation lives. But the fork is real and shapes every downstream consolidation conversation.

---

## Summary Table

| # | Model | Category | Key drafts | Composition with RFC 8693 | Layer |
|---|---|---|---|---|---|
| 1A | Informational actor chain | 1 | RFC 8693, `mcguinness-actor-profile` | IS the baseline | OAuth |
| 1B | Verifiable actor chain | 1 | `mw-oauth-actor-chain` | Extends | OAuth |
| 1C | Attenuating capabilities | 1 | `niyikiza-attenuating-agent-tokens` | Extends (orthogonal) | OAuth |
| 1D | Cascade-revocation grants | 1 | `mishra-oauth-agent-grants` (DAAP) | Replaces | OAuth |
| 1E | Transaction Token chaining | 1 | `ietf-oauth-transaction-tokens`, `araut-txn-tokens-for-agents`, `fletcher-txn-token-chaining-profile` | Composes | OAuth |
| 2A | On-behalf-of user grant | 2 | `oauth-ai-agents-on-behalf-of-user`, `li-oauth-delegated-authorization` | Extends | OAuth |
| 2B | Cross-domain identity chaining | 2 | `ietf-oauth-identity-chaining` (WG), `ietf-oauth-identity-assertion-authz-grant` (WG) | Extends (cross-AS) | OAuth |
| 2C | Mission (durable authority record) | 2 | McGuinness Mission-Bound target I-Ds; blog series | Additive | OAuth (conceptually above) |
| 3A | Protocol-header authority | 3 | `hood-independent-agtp`, `hood-agtp-composition`, `bu-agentproto-security-principal-binding` | Parallel / preemptive | AgentProtocol |
| 3B | Gateway task delegation | 3 | DMSC family (6+ drafts) | Orthogonal; defers | DMSC |
| 3C | Workload identity assertion | 3 | WIMSE core drafts, `ietf-oauth-spiffe-client-auth` | Feeds via SPIFFE→client_assertion | WIMSE |
| 3D | Web-facing bot authentication | 3 | WebBotAuth WG drafts | Precondition | WebBotAuth |
| 4A | Audit-record delegation context | 4 | `kuehlewind-audit-architecture`, AUDIT charter deliverables | *Depends on WG posture* | Cross-layer |
| 4B | Verifiable credentials | 4 | W3C VC 2.0 | External; via 8693 subject token | External |
| 4C | AuthZEN escalation (ARAP) | 4 | OIDF AuthZEN ARAP Draft 1 | Precedes; composes with any Category 1/2 model | OIDF |

---

## What This Means for Corpus Curation

- **Track OAuth WG Complex Delegation recharter closely.** The Category 1 consolidation happens here or not at all. If four distinct mechanics ship in parallel as WG documents, the definitional fragmentation calcifies.

- **Track AUDIT BoF outcome and early WG deliverable text.** The four watch-list questions in the AUDIT Charter Analysis section are the specific ones to raise at the side meeting. Charter is well-scoped; the risk is in the deliverables.

- **Track the Fletcher / McGuinness composition path.** Transaction Token Chaining Profile (1E) and Mission-Bound OAuth (2C) are the two most architecturally-integrated proposals in the corpus, and they are explicitly designed to compose. Whether the OAuth WG accepts that composition as the reference model, or forks between them, is a signal to watch.

- **Do not add a corpus row for each planned McGuinness target I-D.** The Mission-Bound minimum profile and runtime enforcement profile are named in the blog posts but not yet on Datatracker; they remain on the Pending Watch List in `CLAUDE.md` per existing policy.

- **Consider whether the Protocol Boundary Map should be updated to acknowledge Category 4A explicitly.** The current map treats audit as absent from the stack; the AUDIT BoF's arrival gives audit a home even if it's cross-cutting. A footnote or a "cross-cutting concerns" callout would reflect current reality without disrupting the six-layer structure.

- **This document should be revisited after IETF 126.** The AUDIT BoF outcome and any OAuth Complex Delegation recharter milestones will materially change the surface count. A dated re-issue (v2, `2026-08-XX`) after IETF 126 concludes would be the natural cadence.

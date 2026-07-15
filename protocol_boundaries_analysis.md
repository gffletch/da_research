# Protocol Boundaries: DMSC · AgentProtocol · DAWN · WIMSE · OAuth · WebBotAuth

**Date:** 2026-07-13  
**Corpus:** 177 sources; 117 Active IETF Drafts

## Purpose

Six distinct protocol families are active in the IETF agent authorization space. They are not in competition — each owns a distinct layer of the agent interaction stack. This document proposes clean boundaries, identifies the handoff points, and flags the places where boundary ambiguity creates consolidation pressure.

---

## The Stack

```
┌─────────────────────────────────────────────────────────────────┐
│  TASK / APPLICATION                                             │
│  Agent receives a goal; determines what it needs to do          │
├─────────────────────────────────────────────────────────────────┤
│  MULTI-AGENT COORDINATION       ← DMSC / A2A (AgentProtocol)   │
│  Team assembly, task delegation, capability negotiation         │
├─────────────────────────────────────────────────────────────────┤
│  DISCOVERY                      ← DAWN                          │
│  Finding agents, workloads, and services before connecting      │
├─────────────────────────────────────────────────────────────────┤
│  AGENT TRANSPORT / SESSION      ← AgentProtocol (AGTP)         │
│  Agent-to-agent and agent-to-resource communication             │
├─────────────────────────────────────────────────────────────────┤
│  WORKLOAD IDENTITY              ← WIMSE                         │
│  Cryptographic identity for the running agent process           │
├─────────────────────────────────────────────────────────────────┤
│  WEB-FACING AGENT AUTH          ← WebBotAuth                    │
│  Authenticating bots/agents to origin servers on the public web │
├─────────────────────────────────────────────────────────────────┤
│  AUTHORIZATION                  ← OAuth                         │
│  Tokens, delegation chains, scopes, and resource access control │
└─────────────────────────────────────────────────────────────────┘
```

---

## Layer-by-Layer Boundaries

### OAuth — Authorization Layer

**What it owns:** The complete authorization lifecycle — token issuance, delegation chains (RFC 8693 token exchange), scope attenuation, resource server interaction, and revocation. OAuth is the **authority infrastructure**: it answers "is this agent permitted to perform this action on this resource?"

**What it explicitly does not own:**
- How agents find each other (DAWN)
- How agent processes prove they are running on attested hardware (WIMSE)
- How bots authenticate to websites (WebBotAuth handles the web-facing subset)
- How multi-agent teams are assembled (DMSC/A2A)
- What communication protocol carries agent-to-agent messages (AgentProtocol)

**Handoffs:**
- **→ WIMSE:** Agent identity credentials from WIMSE feed into OAuth's `client_assertion` flow (draft-ietf-oauth-spiffe-client-auth). WIMSE proves *who the process is*; OAuth decides *what it can do*.
- **→ WebBotAuth:** WebBotAuth authenticates bots to origin servers, then hands off to OAuth for resource-level access decisions. Bot authentication is a precondition for, not a replacement of, OAuth authorization.
- **→ DAWN:** DAWN discovers available agents; OAuth then authorizes requests to those agents.
- **→ AgentProtocol:** AGTP carries an authority scope declaration in protocol headers; OAuth issues the underlying token that populates that scope.

**Core corpus drafts:** RFC 6749, RFC 8693, RFC 9396, draft-ietf-oauth-transaction-tokens, draft-ietf-oauth-identity-chaining, draft-ietf-oauth-identity-assertion-authz-grant, and the 90+ individual extensions.

---

### WIMSE — Workload Identity Layer

**What it owns:** Cryptographic identity for *running agent processes* within and across service mesh boundaries. WIMSE answers "what is this workload, and can I cryptographically verify that claim?" It provides the identity substrate that OAuth and WebBotAuth use to bind credentials to specific running processes rather than just software identities.

**What it explicitly does not own:**
- What the workload is authorized to do (OAuth)
- How workloads discover each other (DAWN, though draft-schwenkschuster-wimse-trust-domain-discovery is adjacent)
- Application-layer communication between agents (AgentProtocol)

**Handoffs:**
- **→ OAuth:** WIMSE SVIDs feed into OAuth client authentication (draft-ietf-oauth-spiffe-client-auth, WG-adopted). WIMSE identity → OAuth authorization token.
- **→ WebBotAuth:** WebBotAuth's httpsig-protocol (HTTP message signatures) and WIMSE's mTLS profile solve similar problems at different layers. WebBotAuth is web-origin-facing; WIMSE is internal service-mesh-facing. An agent operating in both domains needs both.
- **→ AGTP:** draft-hood-agtp-agent-cert binds AGTP agent identity to X.509 credentials, creating an AGTP-layer analogue to WIMSE's PKI binding.

**Core corpus drafts:** draft-ietf-wimse-arch, draft-ietf-wimse-identifier, draft-ietf-wimse-workload-identity-use-cases, draft-ietf-oauth-spiffe-client-auth, and the WIMSE agent extension family (ni-wimse, reece, jiang, schwenkschuster, winmagic, munoz).

---

### WebBotAuth — Web-Facing Agent Authentication Layer

**What it owns:** Authentication of bots and AI agents to **origin servers on the public web** — websites built for humans that agents access programmatically. WebBotAuth answers "who is this automated client and is it a legitimate operator?" at the HTTP layer, replacing IP allowlisting and User-Agent strings.

**What it explicitly does not own:**
- Service-mesh workload identity (WIMSE)
- Resource-level access control (OAuth)
- Multi-agent coordination (DMSC/A2A)
- Internal agent-to-agent communication (AgentProtocol)

**Handoffs:**
- **→ OAuth:** WebBotAuth establishes bot identity at the HTTP level; OAuth authorization decisions can then condition on that identity. The Signature Agent Card (draft-meunier-webbotauth-registry) is analogous to an OAuth client registration — both assert who the client is before authorization proceeds.
- **→ WIMSE:** WIMSE is the internal identity layer; WebBotAuth is the external (web-facing) identity layer. An agent crawling the public web needs WebBotAuth; the same agent calling internal services needs WIMSE. They are not competing — they address different trust perimeters.
- **Tension:** The anonymous path (draft-rescorla-anonymous-webbotauth) and the signed identity path (draft-meunier-webbotauth-httpsig-protocol) represent a genuine WG design fork. The WG must resolve where on the identity/anonymity spectrum the core spec lands.

**Core corpus drafts:** charter-ietf-webbotauth, draft-meunier-webbotauth-registry, draft-meunier-webbotauth-httpsig-protocol, draft-meunier-webbotauth-httpsig-directory, draft-rescorla-anonymous-webbotauth, draft-nottingham-webbotauth-use-cases.

---

### DAWN — Discovery Layer

**What it owns:** Finding agents, workloads, and named entities **before** any communication or authorization begins. DAWN answers "where are the agents that can help with this task, and what are their capabilities?" It operates as a prerequisite step — you must discover before you can connect, authenticate, or authorize.

**What it explicitly does not own:**
- Authentication or authorization of discovered entities (explicitly out of scope per draft-king-dawn-requirements)
- The communication protocol used after discovery (AgentProtocol, HTTP, AGTP)
- The authorization framework for the discovered resource (OAuth)

**Handoffs:**
- **→ AgentProtocol:** DAWN provides the endpoint; AgentProtocol (AGTP or A2A) provides the connection. AGTP's DISCOVER method (draft-hood-agtp-discovery) is an AGTP-native alternative discovery mechanism that competes with DAWN for the same slot.
- **→ OAuth:** DAWN discovers the agent endpoint; the client then initiates an OAuth token request to interact with it.
- **→ DMSC:** DMSC embeds discovery inside the Agent Gateway (via draft-sz-dmsc-iaip's intent-based routing), effectively conflating the discovery and coordination layers. This is the sharpest DMSC/DAWN boundary tension.

**Boundary tension with DMSC:** DMSC's gateway does discovery internally (semantic routing matches intents to capabilities at the gateway); DAWN treats discovery as a standalone, protocol-neutral layer. These are competing architectural philosophies: centralized gateway routing (DMSC) vs. federated query-based discovery (DAWN). The DAWN gap analysis (draft-moussa-dawn-gap-analysis) does not yet address DMSC directly.

**Core corpus drafts:** draft-king-dawn-requirements, draft-farrel-dawn-terminology, draft-akhavain-moussa-dawn-problem-statement, draft-moussa-dawn-gap-analysis, draft-jimenez-dawn-discovery-landscape, draft-aiendpoint-ai-discovery, draft-serra-mcp-discovery-uri.

---

### AgentProtocol (AGTP / A2A) — Transport and Session Layer

**What it owns:** The communication protocol between agents, and between agents and resources — the equivalent of HTTP but purpose-built for agent intent-driven traffic. Two distinct proposals exist:

- **AGTP (draft-hood-independent-agtp):** A new dedicated protocol on port 4480 with a 18-method vocabulary (cognitive + mechanics verbs), mandatory agent identity headers, and protocol-level authority scope declaration. Full protocol stack replacement.
- **A2A (Google Agent2Agent):** An HTTP-based protocol for agent-to-agent communication. No Google-authored IETF I-Ds found; community submissions reference the protocol but Google has not filed normative documents.

**What it explicitly does not own:**
- Authorization decisions (OAuth)
- Workload identity credentials (WIMSE)
- Discovery of which agents to contact (DAWN)
- Multi-agent team assembly and task orchestration (DMSC)

**Handoffs:**
- **→ OAuth:** AGTP's authority scope header carries the OAuth token scope. AGTP-composition (draft-hood-agtp-composition) explicitly defines how AGTP transports OAuth/OIDC tokens.
- **→ WIMSE / WebBotAuth:** AGTP-cert (draft-hood-agtp-agent-cert) binds AGTP identity to X.509 PKI — the same infrastructure that WIMSE and WebBotAuth use.
- **→ DAWN:** AGTP has its own discovery mechanism (DISCOVER method, draft-hood-agtp-discovery); DAWN is an alternative. These compete for the discovery slot.

**Boundary tension with DMSC:** AGTP is a transport-layer replacement; DMSC's gateway-centric model uses existing transports but adds a gateway coordination layer on top. DMSC does not require AGTP; AGTP does not require DMSC gateways. They can compose but are designed independently.

**Core corpus drafts:** draft-hood-independent-agtp, draft-hood-agtp-ard, draft-hood-agtp-api, draft-hood-agtp-trust, draft-hood-agtp-agent-cert, draft-fane-opena2a-aap, draft-ni-a2a-ai-agent-security-requirements.

---

### DMSC — Multi-Agent Coordination Layer

**What it owns:** The orchestration layer above transport — how multi-agent teams are assembled, how task intents are routed to capable agents across administrative domains, and how the coordination contract (capability negotiation, session binding, provenance audit) is established. DMSC explicitly addresses what MCP and A2A do not: **cross-organizational governance and policy enforcement** at the coordination layer.

**What it explicitly does not own:**
- End-to-end authorization tokens (OAuth)
- Workload identity credentials (WIMSE)
- Web-facing bot authentication (WebBotAuth)

**Handoffs:**
- **→ OAuth:** DMSC's gateway enforces access control within its scope; for cross-domain authorization decisions, it defers to or triggers OAuth token requests. The dunbar-dmsc-gw-scenarios-gap-analysis draft explicitly states that A2A and MCP lack the governance and policy enforcement that regulated environments require — positioning DMSC as the governance orchestration layer above OAuth's authorization primitives.
- **→ DAWN:** DMSC embeds discovery in the gateway (intent-based routing via draft-sz-dmsc-iaip). DAWN treats discovery as a separate layer. These represent competing architectural positions: DMSC says discovery and coordination belong together in the gateway; DAWN says discovery should be protocol-neutral and separate.
- **→ AgentProtocol:** DMSC is transport-agnostic; the MACP architecture uses HTTP and existing transports. AGTP is one possible transport below DMSC, but the DMSC family does not reference AGTP.

**Key design choices distinguishing DMSC:**
1. **Gateway-centric:** a mediation gateway is the normative coordination point, not a peer-to-peer protocol
2. **Semantic routing:** capability-based routing at the gateway rather than address-based routing
3. **Network-infrastructure integration:** draft-li-dmsc-inf-architecture proposes capability-awareness at the IP forwarding layer
4. **Regulated-environment focus:** cross-organizational trust, audit receipts, and governance policy are first-class requirements

**Core corpus drafts:** draft-li-dmsc-macp, draft-li-dmsc-inf-architecture, draft-sz-dmsc-iaip, draft-yang-dmsc-ioa-task-protocol, draft-dunbar-dmsc-gw-scenarios-gap-analysis, draft-somoza-dmsc-atn-agent-trust-negotiation.

---

## Boundary Tensions and Open Questions

### 1. Discovery: DAWN vs. DMSC gateway vs. AGTP DISCOVER

Three approaches exist for the same slot:

| Approach | Where discovery lives | Who owns the result |
|---|---|---|
| DAWN | Standalone federated protocol layer | Any client |
| DMSC gateway | Inside the gateway's intent-routing function | Gateway assigns agents to requests |
| AGTP DISCOVER method | Inside the AGTP protocol | AGTP clients |

**Open question:** Does discovery belong in a dedicated layer (DAWN) or embedded in the coordination gateway (DMSC)? The DAWN WG's answer is the former; the DMSC family's answer is the latter. These positions are architecturally incompatible at scale — a decision is needed before either can serve as a global standard.

### 2. Web-facing identity: WebBotAuth vs. WIMSE mTLS

For agents that straddle the internal/external boundary:

| Context | Protocol |
|---|---|
| Internal service-to-service | WIMSE mTLS |
| External web origin | WebBotAuth httpsig |
| Signed HTTP requests (both contexts) | HTTP Message Signatures (RFC 9421) |

**Open question:** Should WebBotAuth and WIMSE converge on a shared credential format, or is the internal/external distinction sufficient justification for separate designs? RFC 9421 HTTP Message Signatures is the common substrate both use — the WGs liaise but have not specified interoperability.

### 3. OAuth scope vs. AGTP authority scope

AGTP's mandatory `Agent-Authority-Scope` header declares the agent's authority at the protocol level. OAuth access tokens declare the same information in their `scope` or `authorization_details` claims. When both are present:

**Open question:** Which is authoritative when they diverge? AGTP-composition (draft-hood-agtp-composition) specifies that AGTP headers take precedence over adjacent-layer fields — but OAuth's resource server does not speak AGTP. This creates a potential split between AGTP-native infrastructure (which enforces AGTP authority) and OAuth-native resource servers (which enforce token claims). The AGTP family does not currently address this split.

### 4. DMSC governance vs. OAuth authorization

The dunbar gap analysis identifies that MCP and A2A lack cross-organizational governance. OAuth also lacks this — OAuth authorizes access, it does not orchestrate multi-party policy negotiation. DMSC fills this gap with the gateway mediation layer (draft-yang-dmsc-gateway-mediation-layer).

**Open question:** Should the OAuth WG extend its scope to cover cross-organizational governance orchestration (e.g., via the Complex Delegation recharter milestone), or does DMSC own this problem? Currently DMSC and OAuth do not compose explicitly — there is no DMSC profile of OAuth delegation, and no OAuth extension that references DMSC gateways.

---

## Proposed Boundary Assignments (Summary)

| Protocol family | Owns | Hands off to |
|---|---|---|
| **OAuth** | Authorization tokens, delegation chains, scopes, revocation | WIMSE for workload identity; WebBotAuth for web-facing auth |
| **WIMSE** | Cryptographic workload identity within and across service meshes | OAuth for authorization; WebBotAuth for web-facing perimeter |
| **WebBotAuth** | Bot/agent authentication to public web origin servers | OAuth for resource authorization; WIMSE for internal identity |
| **DAWN** | Federated protocol-neutral agent/workload/service discovery | AgentProtocol for connection; OAuth for authorization of discovered entity |
| **AgentProtocol (AGTP/A2A)** | Agent-to-agent and agent-to-resource communication protocol | WIMSE/WebBotAuth for identity; OAuth for authorization; DAWN for discovery |
| **DMSC** | Cross-organizational multi-agent coordination, gateway orchestration, governance policy | OAuth for token-level authorization; transport layer below the gateway |

---

## What This Means for Corpus Curation

- **DMSC family** is an independent coordination layer. Track the core architectural docs; skip purely internal plumbing specs.
- **AGTP family** is a self-contained transport ecosystem from one author shop. Track the core protocol + trust + identity specs; the 18-draft suite need not all be individually catalogued.
- **DAWN** is the most likely candidate for formal WG adoption in the near term (IETF 126 BoF). Track the framework docs actively.
- **WebBotAuth** WG protocol drafts are now tracked. The identity/anonymity design fork is the key decision to watch.
- **A2A** has no Google-authored IETF drafts. Community submissions reference A2A but Google has not engaged with IETF normatively. Track as "industry reference protocol" rather than "IETF work item."

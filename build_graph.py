"""
Build the IETF AI Agent Authorization knowledge graph.
Outputs:
  - agent_authz_graph.json   (the data, RAG-ready)
  - agent_authz_graph.html   (interactive D3 visualization)
"""
import json
from datetime import date

# ============================================================
# SCHEMA
# ============================================================
SCHEMA = {
    "schema_version": "1.0",
    "generated_at": str(date.today()),
    "title": "IETF AI Agent Authorization & Delegation Knowledge Graph",
    "description": (
        "Knowledge graph of IETF specifications and individual drafts concerned with "
        "delegated authorization for AI agents, as of May 2026. Each node is a "
        "specification (RFC, working-group draft, individual draft, or external spec). "
        "Each edge is a typed relationship between specifications. The graph is "
        "designed to be queryable by a graph database, ingestible by a RAG system "
        "(each node carries a long_description usable as a retrieval chunk), and "
        "renderable as a node-link visualization."
    ),
    "node_types": {
        "rfc": "Published IETF RFC.",
        "wg-draft": "IETF working group draft (active, in-progress).",
        "individual-draft": "IETF individual-submission draft (not WG-adopted).",
        "external-spec": "Non-IETF specification (W3C, 3GPP, OpenID Foundation, etc.).",
        "external-impl": "Non-IETF implementation, open-source project, or vendor spec.",
    },
    "edge_types": {
        "depends_on": "Source normatively or informatively references target.",
        "profiles": "Source is a profile / specialization of target.",
        "extends": "Source extends target with new functionality (claims, params, errors).",
        "composes": "Source assembles target with other specs into a unified architecture.",
        "supersedes": "Source replaces target (a published successor of an older work).",
        "superseded_by": "Inverse of supersedes.",
        "replaces": "Source replaces target via re-slugging (same content, new draft handle).",
        "replaced_by": "Inverse of replaces.",
        "name_collides_with": "Source and target use the same short name with different content.",
        "surveys": "Source surveys / indexes target.",
        "related_to": "Source is part of the same author cluster or thematic group as target.",
    },
    "categories": {
        "delegation": "Delegation mechanics — how authority moves down a chain of actors.",
        "identity": "Agent identity — who the agent is and how it proves it.",
        "discovery-transport": "Discovery and transport — plumbing before authentication.",
        "audit": "Audit and compliance — making agent behaviour verifiably auditable.",
        "cross-cutting": "Adjacent or cross-cutting work that doesn't fit the four main clusters.",
    },
    "rag_guidance": (
        "For RAG ingestion: treat each node's 'long_description' as a primary retrieval "
        "chunk and supplement it with name, summary, and key_mechanism. For graph-aware "
        "retrieval, follow outbound 'depends_on' / 'composes' edges to recover the "
        "specification stack the node builds on; follow inbound 'depends_on' to find "
        "what builds on it. The 'name_collides_with' edges mark the AIP-naming conflict; "
        "the 'replaces' edges mark active re-slugging moves."
    ),
}

# ============================================================
# NODES
# ============================================================
nodes = []

def add(n):
    nodes.append(n)

# ---------- RFCs (foundation) ----------
add({
    "id": "rfc-6749",
    "type": "rfc",
    "name": "The OAuth 2.0 Authorization Framework",
    "short_name": "OAuth 2.0",
    "summary": "The original OAuth 2.0 framework defining authorization-code, implicit, ROPC, and client-credentials grants.",
    "long_description": (
        "RFC 6749 establishes the OAuth 2.0 authorization framework: how clients obtain "
        "access tokens from authorization servers on behalf of resource owners. It defines "
        "the four canonical grant types and the basic protocol endpoints. Nearly every "
        "draft in the AI-agent authorization corpus inherits from RFC 6749 either directly "
        "or through OAuth 2.1, which obsoletes it while preserving most of its surface."
    ),
    "status": "published",
    "year": 2012,
    "url": "https://www.rfc-editor.org/rfc/rfc6749",
})
add({
    "id": "rfc-7521",
    "type": "rfc",
    "name": "Assertion Framework for OAuth 2.0 Client Authentication and Authorization Grants",
    "summary": "Generic framework for using assertions (signed claim documents) as OAuth grants or for client authentication.",
    "long_description": (
        "RFC 7521 defines the generic assertion framework that OAuth uses whenever an "
        "external proof — a SAML assertion, a JWT, a SPIFFE SVID — replaces an interactive "
        "user consent step. SPIFFE client authentication and the Identity Assertion JWT "
        "Authorization Grant both profile this framework."
    ),
    "status": "published", "year": 2015,
    "url": "https://www.rfc-editor.org/rfc/rfc7521",
})
add({
    "id": "rfc-7523",
    "type": "rfc",
    "name": "JWT Profile for OAuth 2.0 Client Authentication and Authorization Grants",
    "summary": "Profiles RFC 7521 specifically for JWT assertions.",
    "long_description": (
        "RFC 7523 specifies how JSON Web Tokens are used as OAuth 2.0 client-authentication "
        "credentials and as authorization grants. It's the substrate on which "
        "draft-ietf-oauth-identity-chaining and draft-ietf-oauth-spiffe-client-auth build."
    ),
    "status": "published", "year": 2015,
    "url": "https://www.rfc-editor.org/rfc/rfc7523",
})
add({
    "id": "rfc-7636",
    "type": "rfc",
    "name": "Proof Key for Code Exchange by OAuth Public Clients (PKCE)",
    "short_name": "PKCE",
    "summary": "Defines a code-verifier/code-challenge mechanism to bind an authorization request to the same client instance that initiated it.",
    "long_description": (
        "RFC 7636 was originally about mobile public clients but is now mandatory for all "
        "OAuth 2.1 authorization-code flows. It prevents authorization-code injection. "
        "Several agent-delegation drafts cite it as the baseline for proving the same "
        "client that asked for the code is the one redeeming it."
    ),
    "status": "published", "year": 2015,
    "url": "https://www.rfc-editor.org/rfc/rfc7636",
})
add({
    "id": "rfc-7519",
    "type": "rfc", "name": "JSON Web Token (JWT)",
    "summary": "Defines the JWT format.",
    "long_description": "RFC 7519 specifies JSON Web Tokens — the signed, claim-bearing tokens used as access tokens, ID tokens, assertions, and transaction tokens across nearly every spec in this corpus.",
    "status": "published", "year": 2015,
    "url": "https://www.rfc-editor.org/rfc/rfc7519",
})
add({
    "id": "rfc-8615", "type": "rfc",
    "name": "Well-Known Uniform Resource Identifiers (URIs)",
    "summary": "Defines the /.well-known/ URI registry mechanism.",
    "long_description": "RFC 8615 standardizes /.well-known/ URIs for service discovery. Every discovery draft in the corpus — draft-serra-mcp-discovery-uri, draft-aiendpoint-ai-discovery, the WorkOS auth.md protocol — registers a new .well-known suffix under this RFC's framework.",
    "status": "published", "year": 2019,
    "url": "https://www.rfc-editor.org/rfc/rfc8615",
})
add({
    "id": "rfc-8693", "type": "rfc",
    "name": "OAuth 2.0 Token Exchange",
    "short_name": "Token Exchange",
    "summary": "Defines subject_token/actor_token exchange flows including nested 'act' claims for delegation chains.",
    "long_description": (
        "RFC 8693 is the canonical OAuth mechanism for delegation. A client presents a "
        "subject_token (identifying the principal) and optionally an actor_token "
        "(identifying the entity acting on the principal's behalf) and receives a new "
        "token that carries an 'act' claim. The 'act' claim can be nested, recording "
        "the entire delegation chain. The corpus is split between drafts that extend "
        "RFC 8693 (McGuinness Actor Profile, mw-oauth-actor-chain) and drafts that work "
        "around its weaknesses, especially the fact that prior actors in a nested 'act' "
        "are informational only and not cryptographically validated — the 'chain "
        "splicing' weakness."
    ),
    "status": "published", "year": 2020,
    "url": "https://www.rfc-editor.org/rfc/rfc8693",
})
add({
    "id": "rfc-8785", "type": "rfc",
    "name": "JSON Canonicalization Scheme (JCS)",
    "summary": "Canonical serialization of JSON for cryptographic signing.",
    "long_description": "RFC 8785 specifies a canonical form for JSON so that two encoders produce byte-identical output, which is necessary when computing hashes or signatures over JSON. draft-sharif-agent-audit-trail uses it for tamper-evident audit records.",
    "status": "published", "year": 2020,
    "url": "https://www.rfc-editor.org/rfc/rfc8785",
})
add({
    "id": "rfc-9068", "type": "rfc",
    "name": "JSON Web Token (JWT) Profile for OAuth 2.0 Access Tokens",
    "summary": "Standardizes the claim set of JWT-format OAuth access tokens.",
    "long_description": "RFC 9068 makes JWT access tokens interoperable across implementations by pinning down the required claim names and values. The transaction-tokens drafts inherit its claim conventions.",
    "status": "published", "year": 2021,
    "url": "https://www.rfc-editor.org/rfc/rfc9068",
})
add({
    "id": "rfc-9334", "type": "rfc",
    "name": "Remote ATtestation procedureS (RATS) Architecture",
    "short_name": "RATS",
    "summary": "Defines the Attester/Verifier/Relying Party architecture for remote attestation.",
    "long_description": "RFC 9334 defines the vocabulary of remote attestation: Attester, Verifier, Evidence, Endorsements, Reference Values, Attestation Results. The Kuehlewind audit architecture and attestation-based client auth both invoke this vocabulary, though attestation-based-client-auth deliberately keeps the attestation procedures themselves out of scope.",
    "status": "published", "year": 2023,
    "url": "https://www.rfc-editor.org/rfc/rfc9334",
})
add({
    "id": "rfc-9396", "type": "rfc",
    "name": "OAuth 2.0 Rich Authorization Requests",
    "short_name": "RAR",
    "summary": "Introduces the authorization_details parameter for structured fine-grained permissions.",
    "long_description": (
        "RFC 9396 lets OAuth clients request structured, transaction-level permissions "
        "(e.g., 'pay EUR 123.50 to merchant X') instead of flat scope strings. RAR is "
        "foundational to draft-niyikiza-oauth-attenuating-agent-tokens (monotonic "
        "attenuation), draft-araut-oauth-transaction-tokens-for-agents (agentic_ctx "
        "carries RAR details), and the OVID/OVID-ME mandate model. It's becoming the "
        "canonical carrier for agent mandates."
    ),
    "status": "published", "year": 2023,
    "url": "https://www.rfc-editor.org/rfc/rfc9396",
})
add({
    "id": "rfc-9421", "type": "rfc",
    "name": "HTTP Message Signatures",
    "summary": "Standardizes signing of HTTP messages.",
    "long_description": "RFC 9421 is used by draft-sharif-attp for binding trust-transport claims to specific HTTP request/response messages.",
    "status": "published", "year": 2024,
    "url": "https://www.rfc-editor.org/rfc/rfc9421",
})
add({
    "id": "rfc-9449", "type": "rfc",
    "name": "OAuth 2.0 Demonstrating Proof of Possession (DPoP)",
    "short_name": "DPoP",
    "summary": "Binds an access token to a public key the client controls.",
    "long_description": "RFC 9449 makes access tokens sender-constrained: only the holder of the proof-of-possession key can present the token. draft-singla-agent-identity-protocol uses DPoP as one of its credential-binding mechanisms; the Hardt AAuth Protocol deliberately rejects DPoP in favor of resource-signed challenges.",
    "status": "published", "year": 2023,
    "url": "https://www.rfc-editor.org/rfc/rfc9449",
})
add({
    "id": "rfc-9562", "type": "rfc", "name": "Universally Unique IDentifiers (UUIDs)",
    "summary": "Updates RFC 4122 with new UUID versions including v7 (time-ordered).",
    "long_description": "RFC 9562 is referenced by draft-sharif-agent-audit-trail for audit-record identifiers.",
    "status": "published", "year": 2024,
    "url": "https://www.rfc-editor.org/rfc/rfc9562",
})
add({
    "id": "rfc-9635", "type": "rfc",
    "name": "Grant Negotiation and Authorization Protocol (GNAP)",
    "short_name": "GNAP",
    "summary": "A next-generation delegation protocol where clients can present a key on first contact.",
    "long_description": "RFC 9635 is the IETF's 'OAuth 3' alternative — a clean-sheet delegation protocol that removes pre-registration. The Hardt AAuth Protocol explicitly compares itself to (and differentiates from) GNAP.",
    "status": "published", "year": 2024,
    "url": "https://www.rfc-editor.org/rfc/rfc9635",
})
add({
    "id": "rfc-9700", "type": "rfc",
    "name": "Best Current Practice for OAuth 2.0 Security",
    "summary": "The BCP that codifies modern OAuth security requirements (PKCE, exact redirects, sender-constrained tokens).",
    "long_description": "RFC 9700 is the security baseline that OAuth 2.1 conformance effectively asserts. draft-ietf-oauth-security-topics-update extends it.",
    "status": "published", "year": 2025,
    "url": "https://www.rfc-editor.org/rfc/rfc9700",
})

# ---------- WG drafts ----------
add({
    "id": "draft-ietf-oauth-v2-1", "type": "wg-draft",
    "name": "The OAuth 2.1 Authorization Framework",
    "short_name": "OAuth 2.1",
    "summary": "Consolidates RFC 6749/6750 with mandatory PKCE, no implicit/ROPC, exact redirect-URI matching.",
    "long_description": "draft-ietf-oauth-v2-1 is the baseline that MCP, FAPI 2.0, and most agent specs profile against. Revision -15, March 2026. Milestone for IESG submission Dec 2026 per the OAuth WG recharter.",
    "status": "active", "revision": "-15", "wg": "oauth",
    "url": "https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/",
})
add({
    "id": "draft-ietf-oauth-identity-chaining", "type": "wg-draft",
    "name": "OAuth Identity and Authorization Chaining Across Domains",
    "summary": "Preserves identity context across trust domains via RFC 8693 + RFC 7521/7523.",
    "long_description": "The canonical multi-domain delegation pattern referenced by most agent and zero-trust drafts. Revision -12, May 2026.",
    "status": "active", "revision": "-12", "wg": "oauth",
    "url": "https://datatracker.ietf.org/doc/draft-ietf-oauth-identity-chaining/",
})
add({
    "id": "draft-ietf-oauth-identity-assertion-authz-grant", "type": "wg-draft",
    "name": "Identity Assertion JWT Authorization Grant (ID-JAG)",
    "summary": "How an app uses an identity assertion to obtain a third-party access token via a shared enterprise IdP.",
    "long_description": "Parecki/McGuinness/Campbell. The cross-IdP SSO-to-API bridge. WorkOS's auth.md uses it as one of three discovery flows.",
    "status": "active", "revision": "-03", "wg": "oauth",
    "url": "https://datatracker.ietf.org/doc/draft-ietf-oauth-identity-assertion-authz-grant/",
})
add({
    "id": "draft-ietf-oauth-transaction-tokens", "type": "wg-draft",
    "name": "Transaction Tokens (Txn-Tokens)",
    "summary": "Short-lived signed JWTs that propagate immutable user identity and authorization context through internal call chains.",
    "long_description": "Tulshibagwale/Fletcher/Kasselman. Pairs with AuthZEN/CAEP for zero-trust microservices. Revision -08, March 2026; milestone for IESG submission Dec 2026.",
    "status": "active", "revision": "-08", "wg": "oauth",
    "url": "https://datatracker.ietf.org/doc/draft-ietf-oauth-transaction-tokens/",
})
add({
    "id": "draft-ietf-oauth-attestation-based-client-auth", "type": "wg-draft",
    "name": "OAuth 2.0 Attestation-Based Client Authentication",
    "summary": "Client Attestation JWT + Client Attestation PoP JWT carried in HTTP headers, so public clients can authenticate without a shared secret.",
    "long_description": "Looker/Bastian/Bormann. Relates to the RATS Passport Model, though attestation procedures themselves are out of scope. The substrate the McGuinness Client Instance Assertion builds on.",
    "status": "active", "revision": "-08", "wg": "oauth",
    "url": "https://datatracker.ietf.org/doc/draft-ietf-oauth-attestation-based-client-auth/",
})
add({
    "id": "draft-ietf-oauth-spiffe-client-auth", "type": "wg-draft",
    "name": "OAuth SPIFFE Client Authentication",
    "summary": "Profiles RFC 7521/7523 + attestation-based-client-auth so SPIFFE workloads can authenticate to OAuth ASes using their SVID credentials.",
    "long_description": "Schwenkschuster/Kasselman/Rose(NIST)/Thorgersen(IBM). The protocol bridge between SPIFFE/WIMSE workload identity and the OAuth client-auth surface. Re-slugged from draft-schwenkschuster-oauth-spiffe-client-auth on WG adoption.",
    "status": "active", "revision": "-01", "wg": "oauth",
    "url": "https://datatracker.ietf.org/doc/draft-ietf-oauth-spiffe-client-auth/",
})
add({
    "id": "draft-ietf-oauth-first-party-apps", "type": "wg-draft",
    "name": "OAuth 2.0 for First-Party Applications",
    "summary": "Authorization Challenge Endpoint for first-party native apps to drive a browserless OAuth flow.",
    "long_description": "Parecki/Fletcher/Kasselman. Revision -03, Feb 2026. Explicitly excluded for third-party use because it requires high AS↔client trust.",
    "status": "active", "revision": "-03", "wg": "oauth",
    "url": "https://datatracker.ietf.org/doc/draft-ietf-oauth-first-party-apps/",
})
add({
    "id": "draft-ietf-oauth-browser-based-apps", "type": "wg-draft",
    "name": "OAuth 2.0 for Browser-Based Applications",
    "summary": "Establishes BFF and related patterns as current best practice for SPAs.",
    "long_description": "Revision -26, Dec 2025. Codifies why pure-browser refresh tokens are deprecated.",
    "status": "active", "revision": "-26", "wg": "oauth",
    "url": "https://datatracker.ietf.org/doc/draft-ietf-oauth-browser-based-apps/",
})
add({
    "id": "draft-ietf-oauth-security-topics-update", "type": "wg-draft",
    "name": "Updates to OAuth 2.0 Security Best Current Practice",
    "summary": "Extends RFC 9700 with new countermeasures including rules against audience-injection.",
    "long_description": "Co-authored by the University of Stuttgart FAPI formal-analysis team, so the recommendations are formally grounded.",
    "status": "active", "revision": "-01", "wg": "oauth",
    "url": "https://datatracker.ietf.org/doc/draft-ietf-oauth-security-topics-update/",
})
add({
    "id": "draft-ietf-wimse-arch", "type": "wg-draft",
    "name": "Workload Identity in a Multi System Environment (WIMSE) Architecture",
    "summary": "The WIMSE architectural document defining workload identity, attestation, and credential exchange across systems.",
    "long_description": "Salowey/Rosomakho/Tschofenig. The architectural anchor for the entire WIMSE WG work program. Intentionally compatible with SPIFFE.",
    "status": "active", "revision": "-07", "wg": "wimse",
    "url": "https://datatracker.ietf.org/doc/draft-ietf-wimse-arch/",
})
add({
    "id": "draft-ietf-scitt-architecture", "type": "wg-draft",
    "name": "Supply Chain Integrity, Transparency, and Trust (SCITT) Architecture",
    "summary": "Defines the architecture for transparency services that publish signed statements with non-repudiable receipts.",
    "long_description": "Birkholz et al. The transparency-log substrate used by the Kuehlewind audit architecture for non-repudiable audit-record registration.",
    "status": "active", "revision": "-22", "wg": "scitt",
    "url": "https://datatracker.ietf.org/doc/draft-ietf-scitt-architecture/",
})

print(f"After WG drafts: {len(nodes)} nodes")

# ---------- Individual drafts: Delegation cluster ----------
add({
    "id": "draft-mcguinness-oauth-actor-profile", "type": "individual-draft",
    "category": "delegation",
    "name": "OAuth Actor Profile for Delegation",
    "authors": ["Karl McGuinness"],
    "summary": "Profiles the RFC 8693 'act' claim with required iss, optional sub_profile entity classification, and uniform processing across JWT assertion grants, JWT access tokens, and Transaction Tokens.",
    "long_description": (
        "draft-mcguinness-oauth-actor-profile-00 (April 30, 2026) is the most complete "
        "actor-representation profile to date. It defines depth-1+ chain validation, "
        "cycle-aware construction, and bearer-to-PoP upgrade. The sub_profile field is "
        "the vocabulary slot that distinguishes AI Agent, Sub-Agent, Tool, Service, and "
        "Human entities — making it possible to enforce per-actor-class policy. The "
        "draft is designed to apply uniformly across the JWT assertion grant flow, "
        "JWT access tokens (RFC 9068), and Transaction Tokens. It complements rather "
        "than competes with draft-mw-oauth-actor-chain, which takes a cryptographic-"
        "validation approach to the same problem."
    ),
    "status": "active", "revision": "-00", "date": "2026-04-30",
    "url": "https://datatracker.ietf.org/doc/draft-mcguinness-oauth-actor-profile/",
    "tags": [],
})
add({
    "id": "draft-mw-oauth-actor-chain", "type": "individual-draft",
    "category": "delegation",
    "name": "Cryptographically Verifiable Actor Chains for OAuth 2.0 Token Exchange",
    "authors": ["A. Prasad (Oracle)", "R. Krishnan (JPMorgan Chase)", "D. Lopez (Telefonica)", "S. Addepalli (Aryaka)"],
    "summary": "Defines six actor-chain profiles (Declared/Verified × Full/Subset/Actor-Only Disclosure) for RFC 8693 that cryptographically validate the delegation path across successive token exchanges.",
    "long_description": (
        "draft-mw-oauth-actor-chain-00 (May 1, 2026; 97 pages; re-slugged from "
        "draft-mw-spice-actor-chain-05) is the most direct attack on RFC 8693's "
        "chain-splicing weakness. Where RFC 8693 leaves prior actors in nested act "
        "claims as informational only, this draft makes the chain itself cryptographically "
        "verifiable through step proofs and hop acknowledgments. Six profiles support "
        "different disclosure preferences. A complementary alternative to the McGuinness "
        "Actor Profile — Prasad et al. solve chain integrity with cryptography; "
        "McGuinness solves it with structural processing rules."
    ),
    "status": "active", "revision": "-00", "date": "2026-05-01",
    "url": "https://datatracker.ietf.org/doc/draft-mw-oauth-actor-chain/",
    "tags": [],
})
add({
    "id": "draft-niyikiza-oauth-attenuating-agent-tokens", "type": "individual-draft",
    "category": "delegation",
    "name": "Attenuating Authorization Tokens for Agentic Delegation Chains",
    "authors": ["Niyikiza"],
    "summary": "Extends RFC 9396 Rich Authorization Requests with monotonic attenuation at each delegation hop, offline chain verification, and a typed constraint vocabulary for tool-level argument restrictions.",
    "long_description": (
        "draft-niyikiza-oauth-attenuating-agent-tokens-00 (March 2026) is arguably the "
        "strongest purely-OAuth-grounded delegation draft. Monotonic attenuation means "
        "scopes only narrow as delegation deepens, never widen. The 'offline chain "
        "verification' property — being able to verify the full delegation chain without "
        "round-trip to the AS — is a key scalability win that no other delegation draft "
        "currently delivers cleanly. Overlaps significantly with draft-mishra-oauth-agent-"
        "grants; OAuth WG will likely expect consolidation. Good path to WG adoption "
        "after the OAuth recharter."
    ),
    "status": "active", "revision": "-00", "date": "2026-03-01",
    "url": "https://datatracker.ietf.org/doc/draft-niyikiza-oauth-attenuating-agent-tokens/",
    "tags": [],
})
add({
    "id": "draft-mishra-oauth-agent-grants", "type": "individual-draft",
    "category": "delegation",
    "name": "Delegated Agent Authorization Protocol (DAAP)",
    "authors": ["Mishra"],
    "summary": "Runtime agent identity for dynamically-spawned agents, multi-agent sub-delegation with depth-limiting, and cascade revocation of an entire delegation subtree.",
    "long_description": (
        "draft-mishra-oauth-agent-grants-01 (March 2026) introduces new JWT claims "
        "(agt, dev, grnt, scp, bdg) — a more aggressive alternative to RFC 8693 with "
        "budget-bounded grants. Three practical innovations: runtime identity for "
        "dynamically-spawned agents (not registered ahead of time), depth-limiting that "
        "caps how deep a sub-delegation tree can go, and cascade revocation that "
        "invalidates an entire subtree when any ancestor is revoked. Overlaps with "
        "draft-niyikiza-oauth-attenuating-agent-tokens; the OAuth WG will likely "
        "expect consolidation."
    ),
    "status": "active", "revision": "-01", "date": "2026-03-01",
    "url": "https://datatracker.ietf.org/doc/draft-mishra-oauth-agent-grants/",
    "tags": [],
})
add({
    "id": "draft-araut-oauth-transaction-tokens-for-agents", "type": "individual-draft",
    "category": "delegation",
    "name": "Transaction Tokens For Agents",
    "authors": ["Ashay Raut (Amazon)"],
    "summary": "Profiles Transaction Tokens for agent workflows: adds 'act' for agent identity, 'agentic_ctx' for agent metadata, RFC 9396 RAR integration, and 'actchain' for multi-agent delegation lineage.",
    "long_description": (
        "draft-araut-oauth-transaction-tokens-for-agents-01 (May 2026; re-slugged from "
        "draft-oauth-transaction-tokens-for-agents-06) extends the WG Transaction Tokens "
        "draft for agent workflows. The 'agentic_ctx' claim carries agent_type, intent, "
        "allowed_actions, and environment_constraints. The 'actchain' claim adds a "
        "cryptographic trace of the delegation path with chain-progression rules. The "
        "Transaction Token Service explicitly checks that the workload requesting a "
        "replacement token matches the prior 'act' claim — a structural block against "
        "chain-splicing attacks. One of the easier paths to standardization because it's "
        "a conservative extension of already-published Transaction Token work."
    ),
    "status": "active", "revision": "-01", "date": "2026-05-01",
    "url": "https://datatracker.ietf.org/doc/draft-araut-oauth-transaction-tokens-for-agents/",
    "tags": [],
})
add({
    "id": "draft-oauth-ai-agents-on-behalf-of-user", "type": "individual-draft",
    "category": "delegation",
    "name": "OAuth 2.0 Extension: On-Behalf-Of User Authorization for AI Agents",
    "summary": "Adds requested_actor and actor_token parameters to the OAuth authorization-code flow so the user gives explicit consent per agent.",
    "long_description": (
        "draft-oauth-ai-agents-on-behalf-of-user-02 (August 2025; likely due for -03 "
        "refresh). One of the most IETF-ready delegation drafts because it builds naturally "
        "on RFC 6749 + RFC 8693 + RFC 7636 PKCE without inventing new primitives. The "
        "agent is treated as a distinct identity in token exchange, separate from the "
        "delegating user, and the resulting delegation chain is documented in the access "
        "token claims. Strong candidate for WG adoption after the OAuth recharter."
    ),
    "status": "active", "revision": "-02", "date": "2025-08-01",
    "url": "https://datatracker.ietf.org/doc/draft-oauth-ai-agents-on-behalf-of-user/",
    "tags": [],
})
add({
    "id": "draft-li-oauth-delegated-authorization", "type": "individual-draft",
    "category": "delegation",
    "name": "OAuth 2.0 Delegated Authorization",
    "authors": ["Huawei"],
    "summary": "Hierarchical 'delegation token' model where a client mints subordinate, narrowly-scoped access tokens for delegated parties.",
    "long_description": "draft-li-oauth-delegated-authorization-01 (March 2026; Informational track). One of the few drafts using the literal term 'delegated authorization'. Addresses over-privileged access tokens by letting a client issue subordinate scoped tokens to delegatees.",
    "status": "active", "revision": "-01", "date": "2026-03-01",
    "url": "https://datatracker.ietf.org/doc/draft-li-oauth-delegated-authorization/",
    "tags": [],
})

# ---------- Individual drafts: Identity cluster ----------
add({
    "id": "draft-klrc-aiagent-auth", "type": "individual-draft",
    "category": "identity",
    "name": "AI Agent Authentication and Authorization",
    "summary": "Composes WIMSE/SPIFFE workload identity, OAuth 2.x, and OpenID SSF to authenticate and delegate authority to AI agents — does not invent new protocols.",
    "long_description": (
        "draft-klrc-aiagent-auth-00 (March 2026) introduces the term 'Agent Identity "
        "Management System (AIMS)'. The cleanest standards-based framing of agent-as-"
        "workload. Importantly, it doesn't propose new protocols; it explicitly composes "
        "existing IETF building blocks. Presented at IETF 125 hotrfc and dispatch by "
        "Yaroslav Rosomakho."
    ),
    "status": "active", "revision": "-00", "date": "2026-03-01",
    "url": "https://datatracker.ietf.org/doc/draft-klrc-aiagent-auth/",
    "tags": [],
})
add({
    "id": "draft-ni-wimse-ai-agent-identity", "type": "individual-draft",
    "category": "identity",
    "name": "WIMSE Applicability for AI Agents",
    "authors": ["Ni", "Liu"],
    "summary": "Maps the WIMSE workload-identity architecture to AI-agent use cases and establishes credential-management mechanisms for agentic AI.",
    "long_description": "draft-ni-wimse-ai-agent-identity-02 (February 2026). Essential bridge between the WIMSE WG and the AI-agent space. If an AI-agent WG is ever chartered, this applicability statement is essential groundwork. Co-authored by Ni and Liu, who also lead the related security-requirements draft.",
    "status": "active", "revision": "-02", "date": "2026-02-01",
    "url": "https://datatracker.ietf.org/doc/draft-ni-wimse-ai-agent-identity/",
    "tags": [],
})
add({
    "id": "draft-mcguinness-oauth-client-instance-assertion", "type": "individual-draft",
    "category": "identity",
    "name": "OAuth Client Instance Assertion",
    "authors": ["Karl McGuinness"],
    "summary": "Represents a specific running instance of an OAuth client (not just the client registration) so authorization servers can bind grants to a concrete instance.",
    "long_description": "Companion to McGuinness's Actor Profile draft. The 'client instance' concept lets the AS distinguish between two running copies of the same registered client — critical for binding mandates and PoP keys to specific instances in agent scenarios.",
    "status": "active", "revision": "-00", "date": "2026-05-01",
    "url": "https://datatracker.ietf.org/doc/draft-mcguinness-oauth-client-instance-assertion/",
    "tags": [],
})
add({
    "id": "draft-singla-agent-identity-protocol", "type": "individual-draft",
    "category": "identity",
    "name": "AIP: Decentralized Identity and Delegation for AI Agents",
    "authors": ["Singla"],
    "summary": "Six-layer model (identity → reputation) with W3C DID anchoring, Delegation Depth counter, three Grant ceremony tiers (G1/G2/G3), DPoP, and an MCP integration layer.",
    "long_description": (
        "draft-singla-agent-identity-protocol-00 (April 17, 2026). The most comprehensive "
        "identity framework in the individual-drafts corpus — but at 75+ pages with a "
        "W3C DID dependency that will face IETF pushback, scope reduction is needed. "
        "The 'AIP' name collision with draft-prakash-aip and draft-aip-agent-identity-"
        "protocol is a blocking issue for WG adoption."
    ),
    "status": "active", "revision": "-00", "date": "2026-04-17",
    "url": "https://datatracker.ietf.org/doc/draft-singla-agent-identity-protocol/",
    "tags": ["name-collision"],
})
add({
    "id": "draft-prakash-aip", "type": "individual-draft",
    "category": "identity",
    "name": "AIP: Verifiable Delegation for AI Agent Systems",
    "authors": ["Prakash"],
    "summary": "Invocation-Bound Capability Tokens (IBCTs) in two modes: compact (JWT/Ed25519) for single-hop and chained (Biscuit + Datalog) for multi-hop. Bindings for MCP, A2A, HTTP APIs.",
    "long_description": (
        "draft-prakash-aip-00 (March 27, 2026). Technically strong — Biscuit + Datalog "
        "is genuinely well-suited to scope attenuation. The 'AIP' name collision with "
        "draft-singla-agent-identity-protocol and draft-aip-agent-identity-protocol is "
        "a blocking issue for WG adoption."
    ),
    "status": "active", "revision": "-00", "date": "2026-03-27",
    "url": "https://datatracker.ietf.org/doc/draft-prakash-aip/",
    "tags": ["name-collision"],
})
add({
    "id": "draft-aip-agent-identity-protocol", "type": "individual-draft",
    "category": "identity",
    "name": "AIP: Agentic Authentication and Authorized Policy Enforcement",
    "summary": "AIP Token signed per tool call (agent ID, tool, nonce, timestamp, signature); AgentPolicy YAML for per-tool argument constraints + DLP rules; HITL proxy enforcement.",
    "long_description": "draft-aip-agent-identity-protocol-00 (March 16, 2026). Implementation-focused. YAML policy approach is pragmatic but not interoperable-by-design. HITL integration is a valuable safety feature. Third member of the 'AIP' name-collision triple — must be resolved before any can progress.",
    "status": "active", "revision": "-00", "date": "2026-03-16",
    "url": "https://datatracker.ietf.org/doc/draft-aip-agent-identity-protocol/",
    "tags": ["name-collision"],
})
add({
    "id": "draft-sharif-agent-identity-framework", "type": "individual-draft",
    "category": "identity",
    "name": "Agent Identity Framework: Trust and Identity for Autonomous AI Agents",
    "authors": ["Sharif"],
    "summary": "Five-layer model (identity, authorization, attestation, evidence, trust) with a gap analysis between current Internet standards and autonomous-agent requirements.",
    "long_description": "draft-sharif-agent-identity-framework-00 (April 6, 2026). More gap-analysis than protocol spec. Useful as a problem statement. Five-layer model is a reasonable decomposition but insufficient as a standalone contribution. Part of the broader Sharif cluster of drafts (audit-trail, attp, transport-protocol, payment-trust).",
    "status": "active", "revision": "-00", "date": "2026-04-06",
    "url": "https://datatracker.ietf.org/doc/draft-sharif-agent-identity-framework/",
    "tags": ["sharif-cluster"],
})

# ---------- Individual drafts: Discovery & Transport cluster ----------
add({
    "id": "draft-king-dawn-requirements", "type": "individual-draft",
    "category": "discovery-transport",
    "name": "Requirements for the Discovery of Agents, Workloads, and Named Entities (DAWN)",
    "authors": ["Daniel King", "Adrian Farrel"],
    "summary": "Solution-neutral requirements for discovering AI agents, services, and workloads across administrative boundaries — what must be discoverable, what trust properties apply, what architectural constraints exist.",
    "long_description": "draft-king-dawn-requirements-01 (April 28, 2026). Intentionally NOT a protocol — sits one layer below auth. Authentication and authorization of discovered entities are out of scope, but DAWN discovery happens BEFORE auth/authz can begin. Adrian Farrel of Old Dog Consulting is the architect.",
    "status": "active", "revision": "-01", "date": "2026-04-28",
    "url": "https://datatracker.ietf.org/doc/draft-king-dawn-requirements/",
    "tags": [],
})
add({
    "id": "draft-serra-mcp-discovery-uri", "type": "individual-draft",
    "category": "discovery-transport",
    "name": "The mcp URI Scheme and MCP Server Discovery Mechanism",
    "summary": "Defines an mcp:// URI scheme plus /.well-known/mcp-server (RFC 8615) plus a DNS TXT fallback for Model Context Protocol server discovery.",
    "long_description": "draft-serra-mcp-discovery-uri-04 (March 2026). Already at revision -04 suggesting active iteration; narrow scope, clean design, and the strongest IANA-registration candidate in the agent-spec corpus. OAuth 2.1 for auth is deliberately out of scope.",
    "status": "active", "revision": "-04", "date": "2026-03-01",
    "url": "https://datatracker.ietf.org/doc/draft-serra-mcp-discovery-uri/",
    "tags": [],
})
add({
    "id": "draft-aiendpoint-ai-discovery", "type": "individual-draft",
    "category": "discovery-transport",
    "name": "The AI Discovery Endpoint",
    "summary": "/.well-known/ai URI suffix for programmatic service-capability discovery by AI agents without parsing human-oriented docs.",
    "long_description": "draft-aiendpoint-ai-discovery-00 (March 2026). Complementary to MCP discovery but broader (not MCP-specific). Needs differentiation from OpenAPI/service-description work to gain traction.",
    "status": "active", "revision": "-00", "date": "2026-03-24",
    "url": "https://datatracker.ietf.org/doc/draft-aiendpoint-ai-discovery/",
    "tags": [],
})
add({
    "id": "draft-sharif-attp", "type": "individual-draft",
    "category": "discovery-transport",
    "name": "ATTP: Agent Trust Transport Protocol",
    "authors": ["Sharif"],
    "summary": "Trust levels L0–L4 mapped to PSD2 Strong Customer Authentication requirements; bindings for MCP (MCPS), REST, A2A, gRPC, GraphQL.",
    "long_description": "draft-sharif-attp-00 (April 2026). Regulatory mapping appendices (PSD2, PCI DSS) are notable — one of the few drafts engaging financial regulation directly. Supersedes draft-sharif-agent-payment-trust. Ambitious scope. Part of the Sharif cluster.",
    "status": "active", "revision": "-00", "date": "2026-04-01",
    "url": "https://datatracker.ietf.org/doc/draft-sharif-attp/",
    "tags": ["sharif-cluster"],
})
add({
    "id": "draft-sharif-agent-transport-protocol", "type": "individual-draft",
    "category": "discovery-transport",
    "name": "Agent Transport Protocol (ATP): Async Store-and-Forward for AI Agents",
    "authors": ["Sharif"],
    "summary": "Async store-and-forward messaging with cryptographic identity per relay hop, trust scoring at ingress, capability negotiation, interop with A2A/MCP/FIPA ACL; transport-agnostic over TCP/TLS/QUIC.",
    "long_description": "draft-sharif-agent-transport-protocol-00 (March 28, 2026). Addresses a real gap — most agent protocols assume synchronous availability, and store-and-forward is appropriate for long-running agentic tasks. Scope is broad and needs narrowing. Part of the Sharif cluster.",
    "status": "active", "revision": "-00", "date": "2026-03-28",
    "url": "https://datatracker.ietf.org/doc/draft-sharif-agent-transport-protocol/",
    "tags": ["sharif-cluster"],
})

# ---------- Individual drafts: Audit cluster ----------
add({
    "id": "draft-kuehlewind-audit-architecture", "type": "individual-draft",
    "category": "audit",
    "name": "An Architecture for Auditing AI Agent Delegation and Interactions",
    "authors": ["Mirja Kühlewind (Ericsson)", "Henk Birkholz (Fraunhofer SIT)"],
    "summary": "Defines four record types (Interaction, Action, Delegation, Authorization Transition) and an Audit Context that propagates across OAuth + WIMSE + RATS + SCITT.",
    "long_description": (
        "draft-kuehlewind-audit-architecture-00 (May 18, 2026). The cross-layer "
        "integrator — explicitly composes the McGuinness Actor Profile, mw-oauth-actor-"
        "chain, Transaction Tokens, identity-chaining, ID-JAG, WIMSE, RATS, SCITT, and "
        "Verifiable Agent Conversations into a single auditable architecture with 11 "
        "proposed work items. The 'treats Agent as untrusted' threat model is what "
        "regulators (SOX, PSD2, EU AI Act) actually need. The most interconnected node "
        "in the entire corpus."
    ),
    "status": "active", "revision": "-00", "date": "2026-05-18",
    "url": "https://datatracker.ietf.org/doc/draft-kuehlewind-audit-architecture/",
    "tags": ["hub"],
})
add({
    "id": "draft-birkholz-verifiable-agent-conversations", "type": "individual-draft",
    "category": "audit",
    "name": "Verifiable Agent Conversation Records",
    "authors": ["Henk Birkholz", "T. Heldt", "O. Steele"],
    "summary": "CDDL data format with JSON and CBOR encodings for tamper-evident verifiably-signed records of agent conversations, reasoning traces, tool calls, and system events.",
    "long_description": "draft-birkholz-verifiable-agent-conversations-00 (February 25, 2026). The canonical Interaction-Record format for the Kuehlewind audit architecture. Motivating examples are concrete: agents acting beyond authorized scope, chain-of-thought outputs that don't match the reasoning that actually produced actions, and 'sandbagging' — agents underperforming during capability evaluations while operating at full capacity in deployment. Presented at IETF 125 dispatch and hotrfc.",
    "status": "active", "revision": "-00", "date": "2026-02-25",
    "url": "https://datatracker.ietf.org/doc/draft-birkholz-verifiable-agent-conversations/",
    "tags": [],
})
add({
    "id": "draft-sharif-agent-audit-trail", "type": "individual-draft",
    "category": "audit",
    "name": "Agent Audit Trail (AAT): Standard Logging Format for Autonomous AI Systems",
    "authors": ["Sharif"],
    "summary": "JSON-based audit record with mandatory fields (agent identity, action classification, outcome tracking, trust level) using RFC 8785 JSON Canonicalization and RFC 9562 UUIDs.",
    "long_description": "draft-sharif-agent-audit-trail-00 (March 29, 2026). Orthogonal to delegation but important for compliance — standardized audit-log format is a genuine gap. A pragmatic single-layer alternative to the Kuehlewind cross-layer architecture. Part of the Sharif cluster.",
    "status": "active", "revision": "-00", "date": "2026-03-29",
    "url": "https://datatracker.ietf.org/doc/draft-sharif-agent-audit-trail/",
    "tags": ["sharif-cluster"],
})

# ---------- Individual drafts: Cross-cutting cluster ----------
add({
    "id": "draft-hardt-aauth-protocol", "type": "individual-draft",
    "category": "cross-cutting",
    "name": "AAuth Protocol",
    "authors": ["Dick Hardt"],
    "summary": "A clean-sheet authorization protocol with proof-of-possession by default, resource-signed challenges, agent identity without pre-registration, deferred 202 responses, and AS-to-AS federation.",
    "long_description": "draft-hardt-aauth-protocol-00 (April 2026). Dick Hardt is the original author of OAuth. AAuth is explicitly NOT an OAuth or GNAP extension — section 20.11 of the draft spends a full page explaining why resource-signed challenges, multi-hop interaction chaining, AS-to-AS federation, and clarification chat are architectural changes that warrant a new protocol rather than extensions to an existing one. The deliberate outlier in the corpus.",
    "status": "active", "revision": "-00", "date": "2026-04-01",
    "url": "https://datatracker.ietf.org/doc/draft-hardt-aauth-protocol/",
    "tags": ["outlier"],
})
add({
    "id": "draft-kahrer-oauth-client-challenge-protocol", "type": "individual-draft",
    "category": "cross-cutting",
    "name": "OAuth Client Challenge Protocol",
    "authors": ["Judith Kahrer (Curity)"],
    "summary": "Defines a new insufficient_client_authorization error so the authorization server can dynamically challenge the client mid-flow for an additional assertion, verifiable presentation, or proof-of-possession material.",
    "long_description": "draft-kahrer-oauth-client-challenge-protocol-00 (May 19, 2026). Enables just-in-time and step-up client authorization. Deliberately distinct from first-party-apps (which challenges the USER through the client); this draft challenges the CLIENT itself and works for both first- and third-party clients. Cites Mastercard Verifiable Intent as a use case — connects directly to the agent-mandate pattern.",
    "status": "active", "revision": "-00", "date": "2026-05-19",
    "url": "https://datatracker.ietf.org/doc/draft-kahrer-oauth-client-challenge-protocol/",
    "tags": [],
})
add({
    "id": "draft-goswami-agentic-jwt", "type": "individual-draft",
    "category": "cross-cutting",
    "name": "Secure Intent Protocol: JWT-Compatible Agentic Identity and Workflow Management",
    "authors": ["Goswami"],
    "summary": "Agentic JWT extension to OAuth 2.0 with a Supervisor Agent role for sub-agent coordination, addressing the intent-execution separation gap.",
    "long_description": "draft-goswami-agentic-jwt-00 (December 2025). The intent-execution separation framing is insightful and distinguishing — recognizing that 'what the user wanted' and 'what got executed' are different things and need separate verification. Workflow-step authorization approach is novel but may face skepticism in the OAuth WG.",
    "status": "active", "revision": "-00", "date": "2025-12-01",
    "url": "https://datatracker.ietf.org/doc/draft-goswami-agentic-jwt/",
    "tags": [],
})
add({
    "id": "draft-chen-oauth-roadmap", "type": "individual-draft",
    "category": "cross-cutting",
    "name": "A Comprehensive Roadmap for OAuth 2.0 Standards and Drafts",
    "authors": ["Chen"],
    "summary": "Informational draft that maps the entire OAuth 2.0 ecosystem of RFCs, BCPs, and active drafts into functional layers from core to extensions to industry profiles.",
    "long_description": "draft-chen-oauth-roadmap-00 (May 2026). The single most useful index document when starting work in this area. Surveys ~30 active OAuth drafts.",
    "status": "active", "revision": "-00", "date": "2026-05-01",
    "url": "https://datatracker.ietf.org/doc/draft-chen-oauth-roadmap/",
    "tags": [],
})
add({
    "id": "draft-rosenberg-aiproto-framework", "type": "individual-draft",
    "category": "cross-cutting",
    "name": "Framework, Use Cases and Requirements for AI Agent Protocols",
    "authors": ["Jonathan Rosenberg (Five9)", "Cullen Jennings (Cisco)"],
    "summary": "Comprehensive AI-agent communications framework covering user↔agent, agent↔API, and agent↔agent interactions; surveys MCP, A2A, Agntcy.",
    "long_description": "draft-rosenberg-aiproto-framework-00 (October 2025). Rosenberg (Five9) and Jennings (Cisco) are credible long-time IETF contributors. Important landscape document but likely expired April 2026; worth tracking for -01 refresh.",
    "status": "active", "revision": "-00", "date": "2025-10-22",
    "url": "https://datatracker.ietf.org/doc/draft-rosenberg-aiproto-framework/",
    "tags": ["expired-likely"],
})
add({
    "id": "draft-rosenberg-aiproto-cheq", "type": "individual-draft",
    "category": "cross-cutting",
    "name": "CHEQ: A Protocol for Confirmation of AI Agent Decisions (HITL)",
    "authors": ["Jonathan Rosenberg (Five9)", "Cullen Jennings (Cisco)"],
    "summary": "Out-of-band user confirmation of agent tool calls; eliminates LLM-hallucination risk for consequential actions; enables sensitive operations (banking) without exposing data to the agent.",
    "long_description": "draft-rosenberg-aiproto-cheq-00 (October 2025). The out-of-band HITL confirmation model is valuable and complements delegation frameworks. Likely expired April 2026.",
    "status": "active", "revision": "-00", "date": "2025-10-22",
    "url": "https://datatracker.ietf.org/doc/draft-rosenberg-aiproto-cheq/",
    "tags": ["expired-likely"],
})
add({
    "id": "draft-ni-a2a-ai-agent-security-requirements", "type": "individual-draft",
    "category": "cross-cutting",
    "name": "Security Requirements for AI Agents",
    "authors": ["Ni", "Liu"],
    "summary": "Enumerates security requirements for AI agents covering identity, authorization chaining across domains; references WIMSE, OAuth identity chaining, A2A OAuth profile.",
    "long_description": "draft-ni-a2a-ai-agent-security-requirements-01 (February 2026). Essential scaffolding for an eventual AI-agent WG. Well-connected to existing IETF work. Authors Ni and Liu also lead the WIMSE AI-agent identity draft.",
    "status": "active", "revision": "-01", "date": "2026-02-01",
    "url": "https://datatracker.ietf.org/doc/draft-ni-a2a-ai-agent-security-requirements/",
    "tags": [],
})
add({
    "id": "draft-stephan-ai-agent-6g", "type": "individual-draft",
    "category": "cross-cutting",
    "name": "AI Agent Protocols for 6G Systems",
    "authors": ["Stephan et al."],
    "summary": "Use cases and service requirements from 3GPP TR 22.870 extrapolated to IETF agent-protocol requirements; covers autonomous vehicles, privacy preservation, anomaly detection.",
    "long_description": "draft-stephan-ai-agent-6g-02 (October 2025). Strong operator backing (Orange, Deutsche Telekom, Telefonica, China Mobile, Huawei). Requirements-oriented. Important for 3GPP/IETF coordination. May be expired April 2026; watch for update.",
    "status": "active", "revision": "-02", "date": "2025-10-22",
    "url": "https://datatracker.ietf.org/doc/draft-stephan-ai-agent-6g/",
    "tags": ["expired-likely"],
})
add({
    "id": "draft-jimenez-t2trg-iot-agent", "type": "individual-draft",
    "category": "cross-cutting",
    "name": "Agentic AI Operation of Constrained RESTful Environments",
    "authors": ["Jimenez"],
    "summary": "Agentic AI (ReAct/smolagents) operating on CoAP/CoRE IoT environments; reference implementation provided.",
    "long_description": "draft-jimenez-t2trg-iot-agent-00 (April 14, 2026). Unique in targeting constrained IoT environments. T2TRG affiliation and reference implementation are positive signals. Niche but fills an unaddressed gap.",
    "status": "active", "revision": "-00", "date": "2026-04-14",
    "url": "https://datatracker.ietf.org/doc/draft-jimenez-t2trg-iot-agent/",
    "tags": [],
})
add({
    "id": "draft-sharif-agent-payment-trust", "type": "individual-draft",
    "category": "cross-cutting",
    "name": "Trust Scoring and Identity Verification for AI Agent Payment Transactions",
    "authors": ["Sharif"],
    "summary": "Agent Passport (cryptographic delegation certificate as PSD2 'something you have'); trust scoring for payment transactions; maps to PCI DSS v4.0.1.",
    "long_description": "draft-sharif-agent-payment-trust-00 (March 2026). SUPERSEDED by draft-sharif-attp-00 (April 2026). Retained for historical context — the Agent Passport concept is interesting but needs formal grounding; the ATTP successor generalizes it across transport bindings.",
    "status": "superseded", "revision": "-00", "date": "2026-03-26",
    "url": "https://datatracker.ietf.org/doc/draft-sharif-agent-payment-trust/",
    "tags": ["superseded", "sharif-cluster"],
})

# ---------- Re-slugged predecessors as nodes ----------
add({
    "id": "draft-oauth-transaction-tokens-for-agents", "type": "individual-draft",
    "category": "delegation",
    "name": "Transaction Tokens For Agents (predecessor slug)",
    "summary": "Predecessor slug of draft-araut-oauth-transaction-tokens-for-agents. Last revision -06 (April 2026) before rename.",
    "long_description": "This slug is now marked 'Replaced Internet-Draft' on the IETF Datatracker. Content continues under draft-araut-oauth-transaction-tokens-for-agents. Listed in this graph to provide a continuity record for citations that refer to the old slug.",
    "status": "replaced", "revision": "-06", "date": "2026-04-11",
    "url": "https://datatracker.ietf.org/doc/draft-oauth-transaction-tokens-for-agents/",
    "tags": ["replaced"],
})
add({
    "id": "draft-mw-spice-actor-chain", "type": "individual-draft",
    "category": "delegation",
    "name": "Cryptographically Verifiable Actor Chains (predecessor slug)",
    "summary": "Predecessor slug of draft-mw-oauth-actor-chain. Last revision -05 (April 25, 2026) before rename.",
    "long_description": "This slug was under the SPICE namespace; content continues under draft-mw-oauth-actor-chain in the OAuth namespace. Listed for citation continuity.",
    "status": "replaced", "revision": "-05", "date": "2026-04-25",
    "url": "https://datatracker.ietf.org/doc/draft-mw-spice-actor-chain/",
    "tags": ["replaced"],
})

# ---------- External specs / implementations ----------
add({
    "id": "ext-w3c-did", "type": "external-spec",
    "name": "W3C Decentralized Identifiers (DIDs)",
    "summary": "W3C Recommendation defining a decentralized identifier system independent of any centralized registry.",
    "long_description": "Used by draft-singla-agent-identity-protocol as the identity anchor. The DID dependency is one reason that draft faces IETF pushback.",
    "url": "https://www.w3.org/TR/did-core/",
})
add({
    "id": "ext-w3c-vc", "type": "external-spec",
    "name": "W3C Verifiable Credentials Data Model",
    "summary": "W3C Recommendation defining a cryptographically-signed claim structure with issuer/holder/verifier roles.",
    "url": "https://www.w3.org/TR/vc-data-model-2.0/",
})
add({
    "id": "ext-mcp", "type": "external-spec",
    "name": "Model Context Protocol (MCP)",
    "summary": "Anthropic-originated open protocol for connecting AI assistants to external data sources and tools.",
    "long_description": "Referenced by draft-serra-mcp-discovery-uri (defines mcp:// URIs), draft-aiendpoint-ai-discovery (complement), draft-singla-agent-identity-protocol (integration), draft-prakash-aip (binding), and draft-sharif-attp (MCPS variant).",
    "url": "https://modelcontextprotocol.io/",
})
add({
    "id": "ext-a2a", "type": "external-spec",
    "name": "Google A2A (Agent-to-Agent) Protocol",
    "summary": "Google-originated protocol for inter-agent communication.",
    "url": "https://google.github.io/A2A/",
})
add({
    "id": "ext-biscuit", "type": "external-spec",
    "name": "Biscuit Authorization Tokens",
    "summary": "Open token format with built-in Datalog-based authorization logic.",
    "long_description": "Used by draft-prakash-aip as the multi-hop chained token format. The Datalog logic provides a clean way to express scope attenuation.",
    "url": "https://www.biscuitsec.org/",
})
add({
    "id": "ext-fipa-acl", "type": "external-spec",
    "name": "FIPA ACL (Agent Communication Language)",
    "summary": "Foundation for Intelligent Physical Agents standard for agent communication, originating in the late 1990s.",
    "url": "http://www.fipa.org/specs/fipa00061/",
})
add({
    "id": "ext-spiffe", "type": "external-spec",
    "name": "SPIFFE (Secure Production Identity Framework For Everyone)",
    "summary": "CNCF project defining a workload-identity system with SPIFFE Verifiable Identity Documents (SVIDs).",
    "long_description": "SPIFFE is intentionally interoperable with WIMSE — existing SPIFFE deployments map cleanly onto WIMSE standards. SVIDs come in JWT, WIT, and X.509 forms; all three are usable as OAuth client credentials per draft-ietf-oauth-spiffe-client-auth.",
    "url": "https://spiffe.io/",
})
add({
    "id": "ext-openid-ssf", "type": "external-spec",
    "name": "OpenID Shared Signals Framework (SSF)",
    "summary": "OpenID Foundation specification defining transport for Security Event Tokens between cooperating identity providers.",
    "long_description": "Underlies CAEP (session/access changes) and RISC (account-compromise signals). Used by draft-klrc-aiagent-auth for revocation propagation.",
    "url": "https://openid.net/wg/sharedsignals/specifications/",
})
add({
    "id": "ext-cddl-cose", "type": "external-spec",
    "name": "CDDL / COSE / CBOR",
    "summary": "Concise Data Definition Language, CBOR Object Signing and Encryption, and Concise Binary Object Representation — the binary-friendly counterpart to JSON/JOSE.",
    "url": "https://datatracker.ietf.org/doc/rfc8949/",
})
add({
    "id": "ext-3gpp-22870", "type": "external-spec",
    "name": "3GPP TR 22.870",
    "summary": "3GPP Technical Report on study of AI-aided services for 6G.",
    "url": "https://www.3gpp.org/",
})
add({
    "id": "ext-coap", "type": "external-spec",
    "name": "CoAP (Constrained Application Protocol, RFC 7252)",
    "summary": "RESTful protocol for constrained IoT environments.",
    "url": "https://www.rfc-editor.org/rfc/rfc7252",
})
add({
    "id": "ext-mastercard-vi", "type": "external-spec",
    "name": "Mastercard Verifiable Intent (VI)",
    "summary": "Mastercard specification for verifiable agent intent in payment contexts.",
    "url": "https://verifiableintent.dev/",
})
add({
    "id": "ext-cae", "type": "external-spec",
    "name": "OpenID Continuous Access Evaluation Profile (CAEP)",
    "summary": "OpenID Foundation specification for asynchronous notification of session/credential/posture changes.",
    "url": "https://openid.net/specs/openid-caep-1_0-final.html",
})

print(f"Total nodes: {len(nodes)}")


# ============================================================
# EDGES
# ============================================================
edges = []
def e(src, dst, rel, label=""):
    edge = {"source": src, "target": dst, "type": rel}
    if label: edge["label"] = label
    edges.append(edge)

# ---------- WG drafts depend on RFCs ----------
e("draft-ietf-oauth-v2-1", "rfc-6749", "supersedes", "Consolidates and obsoletes")
e("draft-ietf-oauth-v2-1", "rfc-7636", "depends_on", "Mandates PKCE")
e("draft-ietf-oauth-v2-1", "rfc-9700", "depends_on", "Asserts security BCP conformance")
e("draft-ietf-oauth-identity-chaining", "rfc-8693", "depends_on", "Built on token exchange")
e("draft-ietf-oauth-identity-chaining", "rfc-7521", "depends_on")
e("draft-ietf-oauth-identity-chaining", "rfc-7523", "depends_on")
e("draft-ietf-oauth-identity-assertion-authz-grant", "rfc-7521", "depends_on")
e("draft-ietf-oauth-identity-assertion-authz-grant", "rfc-7523", "depends_on")
e("draft-ietf-oauth-transaction-tokens", "rfc-7519", "depends_on", "JWT format")
e("draft-ietf-oauth-transaction-tokens", "rfc-9068", "depends_on")
e("draft-ietf-oauth-attestation-based-client-auth", "rfc-9334", "depends_on", "RATS Passport Model")
e("draft-ietf-oauth-attestation-based-client-auth", "rfc-7519", "depends_on")
e("draft-ietf-oauth-spiffe-client-auth", "rfc-7521", "depends_on")
e("draft-ietf-oauth-spiffe-client-auth", "rfc-7523", "depends_on")
e("draft-ietf-oauth-spiffe-client-auth", "draft-ietf-oauth-attestation-based-client-auth", "depends_on")
e("draft-ietf-oauth-spiffe-client-auth", "ext-spiffe", "depends_on", "SVID credentials")
e("draft-ietf-oauth-spiffe-client-auth", "draft-ietf-wimse-arch", "related_to")
e("draft-ietf-oauth-first-party-apps", "rfc-6749", "extends")
e("draft-ietf-oauth-browser-based-apps", "rfc-6749", "depends_on")
e("draft-ietf-oauth-security-topics-update", "rfc-9700", "extends")
e("draft-ietf-wimse-arch", "rfc-8693", "depends_on", "Token exchange substrate")
e("draft-ietf-wimse-arch", "ext-spiffe", "related_to", "Intentionally compatible")

# ---------- Individual delegation drafts ----------
e("draft-mcguinness-oauth-actor-profile", "rfc-8693", "profiles", "Profiles the act claim")
e("draft-mcguinness-oauth-actor-profile", "draft-ietf-oauth-transaction-tokens", "depends_on")
e("draft-mcguinness-oauth-actor-profile", "rfc-9068", "depends_on")
e("draft-mcguinness-oauth-actor-profile", "draft-ietf-oauth-identity-assertion-authz-grant", "depends_on")

e("draft-mw-oauth-actor-chain", "rfc-8693", "extends", "Cryptographically validates chains")
e("draft-mw-oauth-actor-chain", "draft-mw-spice-actor-chain", "replaces", "Re-slugged from SPICE namespace")
e("draft-mw-spice-actor-chain", "draft-mw-oauth-actor-chain", "replaced_by")

e("draft-niyikiza-oauth-attenuating-agent-tokens", "rfc-9396", "extends", "Monotonic attenuation of RAR details")
e("draft-niyikiza-oauth-attenuating-agent-tokens", "draft-mishra-oauth-agent-grants", "related_to", "Overlaps; WG will expect consolidation")
e("draft-mishra-oauth-agent-grants", "rfc-8693", "depends_on")
e("draft-mishra-oauth-agent-grants", "draft-niyikiza-oauth-attenuating-agent-tokens", "related_to")

e("draft-araut-oauth-transaction-tokens-for-agents", "draft-ietf-oauth-transaction-tokens", "extends", "Adds agent context to Txn-Tokens")
e("draft-araut-oauth-transaction-tokens-for-agents", "rfc-8693", "depends_on")
e("draft-araut-oauth-transaction-tokens-for-agents", "rfc-9396", "depends_on", "agentic_ctx carries RAR details")
e("draft-araut-oauth-transaction-tokens-for-agents", "draft-oauth-transaction-tokens-for-agents", "replaces", "Re-slugged from old name")
e("draft-oauth-transaction-tokens-for-agents", "draft-araut-oauth-transaction-tokens-for-agents", "replaced_by")

e("draft-oauth-ai-agents-on-behalf-of-user", "rfc-6749", "extends", "Adds requested_actor/actor_token params")
e("draft-oauth-ai-agents-on-behalf-of-user", "rfc-7636", "depends_on", "PKCE")
e("draft-oauth-ai-agents-on-behalf-of-user", "rfc-8693", "depends_on")

e("draft-li-oauth-delegated-authorization", "rfc-6749", "extends")

# ---------- Individual identity drafts ----------
e("draft-klrc-aiagent-auth", "draft-ietf-wimse-arch", "composes")
e("draft-klrc-aiagent-auth", "rfc-6749", "composes")
e("draft-klrc-aiagent-auth", "ext-openid-ssf", "composes")
e("draft-klrc-aiagent-auth", "ext-spiffe", "composes")

e("draft-ni-wimse-ai-agent-identity", "draft-ietf-wimse-arch", "profiles", "Applies WIMSE to AI agents")
e("draft-ni-wimse-ai-agent-identity", "draft-ni-a2a-ai-agent-security-requirements", "related_to", "Same author cluster")

e("draft-mcguinness-oauth-client-instance-assertion", "draft-ietf-oauth-attestation-based-client-auth", "depends_on")
e("draft-mcguinness-oauth-client-instance-assertion", "draft-mcguinness-oauth-actor-profile", "related_to", "Same author, companion drafts")

# AIP name collision triangle
e("draft-singla-agent-identity-protocol", "draft-prakash-aip", "name_collides_with")
e("draft-singla-agent-identity-protocol", "draft-aip-agent-identity-protocol", "name_collides_with")
e("draft-prakash-aip", "draft-aip-agent-identity-protocol", "name_collides_with")
e("draft-prakash-aip", "draft-singla-agent-identity-protocol", "name_collides_with")
e("draft-aip-agent-identity-protocol", "draft-singla-agent-identity-protocol", "name_collides_with")
e("draft-aip-agent-identity-protocol", "draft-prakash-aip", "name_collides_with")

e("draft-singla-agent-identity-protocol", "ext-w3c-did", "depends_on")
e("draft-singla-agent-identity-protocol", "rfc-9449", "depends_on", "DPoP")
e("draft-singla-agent-identity-protocol", "ext-mcp", "depends_on", "Integration layer")

e("draft-prakash-aip", "ext-biscuit", "depends_on", "Multi-hop chained mode")
e("draft-prakash-aip", "rfc-7519", "depends_on", "Compact single-hop mode")
e("draft-prakash-aip", "ext-mcp", "depends_on")
e("draft-prakash-aip", "ext-a2a", "depends_on")

e("draft-aip-agent-identity-protocol", "rfc-7519", "depends_on")

e("draft-sharif-agent-identity-framework", "draft-sharif-agent-audit-trail", "related_to", "Sharif cluster")
e("draft-sharif-agent-identity-framework", "draft-sharif-attp", "related_to", "Sharif cluster")

# ---------- Individual discovery & transport drafts ----------
e("draft-king-dawn-requirements", "rfc-8615", "related_to", "Discovery substrate")
e("draft-king-dawn-requirements", "rfc-9334", "related_to", "RATS for attestation in discovery")
e("draft-king-dawn-requirements", "draft-ietf-wimse-arch", "related_to", "Specializes discovery for workloads")

e("draft-serra-mcp-discovery-uri", "rfc-8615", "depends_on", ".well-known/mcp-server")
e("draft-serra-mcp-discovery-uri", "ext-mcp", "depends_on")

e("draft-aiendpoint-ai-discovery", "rfc-8615", "depends_on", ".well-known/ai")
e("draft-aiendpoint-ai-discovery", "draft-serra-mcp-discovery-uri", "related_to", "Complementary discovery")

e("draft-sharif-attp", "draft-sharif-agent-payment-trust", "supersedes")
e("draft-sharif-agent-payment-trust", "draft-sharif-attp", "superseded_by")
e("draft-sharif-attp", "rfc-9421", "depends_on", "HTTP Message Signatures")
e("draft-sharif-attp", "ext-mcp", "depends_on", "MCPS binding")
e("draft-sharif-attp", "ext-a2a", "depends_on")

e("draft-sharif-agent-transport-protocol", "ext-mcp", "depends_on")
e("draft-sharif-agent-transport-protocol", "ext-a2a", "depends_on")
e("draft-sharif-agent-transport-protocol", "ext-fipa-acl", "depends_on")

# ---------- Individual audit drafts ----------
# The big one — kuehlewind composes ~10 specs
e("draft-kuehlewind-audit-architecture", "draft-mcguinness-oauth-actor-profile", "composes")
e("draft-kuehlewind-audit-architecture", "draft-mw-oauth-actor-chain", "composes")
e("draft-kuehlewind-audit-architecture", "draft-ietf-oauth-transaction-tokens", "composes")
e("draft-kuehlewind-audit-architecture", "draft-ietf-oauth-identity-chaining", "composes")
e("draft-kuehlewind-audit-architecture", "draft-ietf-oauth-identity-assertion-authz-grant", "composes")
e("draft-kuehlewind-audit-architecture", "draft-ietf-wimse-arch", "composes")
e("draft-kuehlewind-audit-architecture", "rfc-9334", "composes", "RATS")
e("draft-kuehlewind-audit-architecture", "draft-ietf-scitt-architecture", "composes")
e("draft-kuehlewind-audit-architecture", "draft-birkholz-verifiable-agent-conversations", "composes")
e("draft-kuehlewind-audit-architecture", "rfc-9396", "depends_on", "RAR for authorization details")
e("draft-kuehlewind-audit-architecture", "rfc-8693", "depends_on")

e("draft-birkholz-verifiable-agent-conversations", "ext-cddl-cose", "depends_on")

e("draft-sharif-agent-audit-trail", "rfc-8785", "depends_on", "JSON Canonicalization")
e("draft-sharif-agent-audit-trail", "rfc-9562", "depends_on", "UUIDs")
e("draft-sharif-agent-audit-trail", "draft-sharif-agent-identity-framework", "related_to")

# ---------- Individual cross-cutting drafts ----------
# Hardt explicitly does NOT depend on OAuth/GNAP/DPoP — no edges
# But it's adjacent to GNAP conceptually
e("draft-hardt-aauth-protocol", "rfc-9635", "related_to", "Explicitly differentiates from GNAP")

e("draft-kahrer-oauth-client-challenge-protocol", "rfc-6749", "extends", "New error code")
e("draft-kahrer-oauth-client-challenge-protocol", "draft-ietf-oauth-attestation-based-client-auth", "related_to")
e("draft-kahrer-oauth-client-challenge-protocol", "draft-ietf-oauth-first-party-apps", "related_to", "Distinct but similar pattern")
e("draft-kahrer-oauth-client-challenge-protocol", "ext-mastercard-vi", "related_to", "Cited use case")

e("draft-goswami-agentic-jwt", "rfc-6749", "extends")
e("draft-goswami-agentic-jwt", "rfc-7519", "depends_on")

e("draft-chen-oauth-roadmap", "rfc-6749", "surveys")
e("draft-chen-oauth-roadmap", "draft-ietf-oauth-v2-1", "surveys")
e("draft-chen-oauth-roadmap", "draft-ietf-oauth-transaction-tokens", "surveys")
e("draft-chen-oauth-roadmap", "draft-ietf-oauth-identity-chaining", "surveys")

e("draft-rosenberg-aiproto-cheq", "draft-rosenberg-aiproto-framework", "extends")
e("draft-rosenberg-aiproto-framework", "ext-mcp", "surveys")
e("draft-rosenberg-aiproto-framework", "ext-a2a", "surveys")

e("draft-ni-a2a-ai-agent-security-requirements", "draft-ietf-wimse-arch", "depends_on")
e("draft-ni-a2a-ai-agent-security-requirements", "draft-ietf-oauth-identity-chaining", "depends_on")
e("draft-ni-a2a-ai-agent-security-requirements", "draft-ni-wimse-ai-agent-identity", "related_to")

e("draft-stephan-ai-agent-6g", "ext-3gpp-22870", "depends_on")
e("draft-stephan-ai-agent-6g", "draft-rosenberg-aiproto-framework", "related_to")

e("draft-jimenez-t2trg-iot-agent", "ext-coap", "depends_on")

print(f"Total edges: {len(edges)}")

# ============================================================
# ASSEMBLE AND WRITE JSON
# ============================================================
graph = {
    "@meta": SCHEMA,
    "nodes": nodes,
    "edges": edges,
}

with open('/home/claude/agent_authz_graph.json', 'w') as f:
    json.dump(graph, f, indent=2, ensure_ascii=False)

print(f"Wrote agent_authz_graph.json: {len(nodes)} nodes, {len(edges)} edges")


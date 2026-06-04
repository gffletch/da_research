from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = Workbook()
wb.remove(wb.active)

HEADER_FONT = Font(name='Arial', size=11, bold=True, color='FFFFFF')
BODY_FONT   = Font(name='Arial', size=10)
LINK_FONT   = Font(name='Arial', size=10, color='0563C1', underline='single')
HEADER_ALIGN = Alignment(horizontal='center', vertical='center', wrap_text=True)
BODY_ALIGN   = Alignment(vertical='top', wrap_text=True)
THIN = Side(border_style='thin', color='BFBFBF')
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

COLORS = {
    'RFC':       '1F4E78',
    'Drafts':    'C0504D',
    'OpenID':    '7030A0',
    'Other':     '548235',
    'Academic':  'BF8F00',
    'Industry':  '404040',
    'Summary':   '305496',
}

COLS = ["#", "Title", "One-Sentence Summary", "Link", "Standards Organization", "Comments"]
WIDTHS = {1: 5, 2: 44, 3: 70, 4: 56, 5: 26, 6: 62}

def make_sheet(title, color, rows):
    ws = wb.create_sheet(title)
    fill = PatternFill('solid', start_color=color)
    for col, h in enumerate(COLS, 1):
        c = ws.cell(row=1, column=col, value=h)
        c.font, c.fill, c.alignment, c.border = HEADER_FONT, fill, HEADER_ALIGN, BORDER
    for i, (t, s, link, org, comment) in enumerate(rows, start=2):
        ws.cell(row=i, column=1, value=i-1)
        ws.cell(row=i, column=2, value=t)
        ws.cell(row=i, column=3, value=s)
        link_cell = ws.cell(row=i, column=4, value=link)
        ws.cell(row=i, column=5, value=org)
        ws.cell(row=i, column=6, value=comment)
        for col in range(1, 7):
            cell = ws.cell(row=i, column=col)
            cell.alignment = BODY_ALIGN
            cell.border = BORDER
            cell.font = BODY_FONT
        link_cell.hyperlink = link
        link_cell.font = LINK_FONT
    for col, w in WIDTHS.items():
        ws.column_dimensions[get_column_letter(col)].width = w
    ws.row_dimensions[1].height = 32
    ws.freeze_panes = "A2"
    return ws

# ============================================================
# TAB 1: PUBLISHED RFCs
# ============================================================
rfc_rows = [
    ("RFC 9635 — Grant Negotiation and Authorization Protocol (GNAP)",
     "An IETF standards-track RFC for a next-generation delegation protocol that removes pre-registration by letting clients present a key on first contact with the AS.",
     "https://www.rfc-editor.org/rfc/rfc9635",
     "IETF (concluded GNAP WG)",
     "Often called 'OAuth 3'; published Oct 2024, working group concluded so the spec is in maintenance mode."),

    ("RFC 9396 — OAuth 2.0 Rich Authorization Requests (RAR)",
     "An IETF RFC introducing the authorization_details JSON parameter so OAuth clients can request structured fine-grained permissions instead of flat scopes.",
     "https://datatracker.ietf.org/doc/html/rfc9396",
     "IETF",
     "Foundational to FAPI 2.0, open-banking PSD2/PSD3, and increasingly used as the policy carrier for MCP and agent transaction tokens."),

    ("RFC 8693 — OAuth 2.0 Token Exchange",
     "An IETF RFC defining a token-exchange grant with subject_token and actor_token parameters, providing the canonical mechanism for impersonation and delegation in OAuth.",
     "https://www.rfc-editor.org/rfc/rfc8693",
     "IETF",
     "The 'actor_token' chain is the basis for almost every multi-hop agent-delegation proposal but is itself subject to the 'delegation chain splicing' attack."),

    ("RFC 9700 — Best Current Practice for OAuth 2.0 Security",
     "The IETF BCP that codifies current OAuth security requirements such as PKCE, exact redirect matching, and sender-constrained tokens.",
     "https://www.rfc-editor.org/rfc/rfc9700",
     "IETF",
     "Published January 2025; companion to OAuth 2.1 — implementations claiming OAuth 2.1 conformance are essentially asserting RFC 9700 conformance."),
]
make_sheet("Published RFCs", COLORS['RFC'], rfc_rows)

# ============================================================
# TAB 2: ACTIVE IETF DRAFTS
# ============================================================
draft_rows = [
    # ---- IETF Working Group Charters (scope-defining documents) ----
    ("Charter: OAuth WG Proposed Recharter (charter-ietf-oauth-05-05)",
     "The OAuth WG's proposed recharter (currently under External Review, on the 2026-06-04 IESG telechat agenda) that formally adds 'Complex Delegation' to the work program — new mechanisms and extensions for authorization of automated agents acting on behalf of users, including cross-administrative-domain scenarios.",
     "https://datatracker.ietf.org/doc/charter-ietf-oauth/05-05/",
     "IETF (OAuth WG charter)",
     "★ Hugely significant: the OAuth WG is formally re-chartering around agent delegation. Milestones include Transaction Tokens and OAuth 2.1 to IESG by Dec 2026, SD-JWT VC by Jul 2026. Coordinates with WIMSE on multi-hop workload identity."),

    ("Charter: Web Bot Auth WG (charter-ietf-webbotauth-01)",
     "The formal IETF charter for the newly-approved Web Bot Auth WG, standardizing methods for bots (search crawlers, AI training crawlers, AI agents retrieving content for end users) to cryptographically authenticate themselves to websites built for humans.",
     "https://datatracker.ietf.org/doc/charter-ietf-webbotauth/01/",
     "IETF (WebBotAuth WG charter)",
     "Approved Oct 2025; complements but does not duplicate OAuth delegation work — authenticates the bot/agent itself, not the end user. Liaises with AIPREF, HTTPBIS, OAuth, TLS, and WIMSE."),

    ("Charter: AI Preferences WG (charter-ietf-aipref-01)",
     "The formal IETF charter for the AIPREF WG, standardizing vocabulary and protocol mechanisms (e.g., extending the Robots Exclusion Protocol and HTTP headers) for content owners to express preferences about AI training, deployment, and use of their content.",
     "https://datatracker.ietf.org/doc/charter-ietf-aipref/01/",
     "IETF (AIPREF WG charter)",
     "Approved April 2025; the charter explicitly puts 'authenticating or authorizing clients and/or crawlers' out of scope — included here for ecosystem context, not because it's delegated-authz work per se. Sibling WG to WebBotAuth."),

    ("draft-king-dawn-requirements — Requirements for Discovery of Agents, Workloads, and Named Entities (DAWN)",
     "An individual IETF draft from Adrian Farrel and Daniel King setting out solution-neutral requirements for discovering AI agents, services, and workloads across administrative boundaries — what must be discoverable, what trust properties apply, and what architectural constraints exist.",
     "https://datatracker.ietf.org/doc/draft-king-dawn-requirements/01/",
     "IETF (individual)",
     "Revision -01, April 2026; intentionally NOT a protocol — sits one layer below auth. Authentication and authorization of discovered entities are out of scope, but DAWN discovery happens *before* auth/authz can begin."),

    # ---- WG drafts (more weight, closer to standardization) ----
    ("draft-ietf-oauth-v2-1 — The OAuth 2.1 Authorization Framework",
     "An IETF WG draft that obsoletes RFC 6749/6750 by mandating PKCE for the authorization code grant, removing implicit and ROPC, and requiring exact redirect-URI matching.",
     "https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/",
     "IETF (OAuth WG)",
     "Revision -15 (March 2026) is the current baseline that MCP, FAPI 2.0, and most agent specs profile against."),

    ("draft-ietf-oauth-identity-chaining — OAuth Identity and Authorization Chaining Across Domains",
     "An IETF WG draft that defines how to preserve identity and authorization context across trust domains by combining RFC 8693 token exchange with RFC 7521/7523 JWT assertions.",
     "https://datatracker.ietf.org/doc/draft-ietf-oauth-identity-chaining/",
     "IETF (OAuth WG)",
     "Active WG draft (-08, expires Aug 2026); the canonical multi-domain delegation pattern referenced by most agent and zero-trust drafts."),

    ("draft-ietf-oauth-identity-assertion-authz-grant — Identity Assertion JWT Authorization Grant (ID-JAG)",
     "An IETF WG draft (Parecki/McGuinness/Campbell) defining how an app uses an identity assertion to obtain an access token for a third-party API by coordinating through a shared enterprise IdP.",
     "https://datatracker.ietf.org/doc/draft-ietf-oauth-identity-assertion-authz-grant/",
     "IETF (OAuth WG)",
     "Revision -03, April 2026; the cross-IdP SSO-to-API bridge that the McGuinness Actor Profile draft layers on top of, and that WorkOS's auth.md uses as one of its three discovery flows."),

    ("draft-ietf-oauth-transaction-tokens — Transaction Tokens (Txn-Tokens)",
     "An IETF WG draft defining short-lived signed JWTs that propagate immutable user identity and authorization context through internal call chains within a trust domain.",
     "https://datatracker.ietf.org/doc/draft-ietf-oauth-transaction-tokens/",
     "IETF (OAuth WG)",
     "Revision -08 published March 2026; co-authored by Tulshibagwale (CAEP inventor), Fletcher, and Kasselman — pairs with AuthZEN/CAEP for zero-trust microservices."),

    ("draft-ietf-oauth-first-party-apps — OAuth 2.0 for First-Party Applications",
     "An IETF WG draft defining an Authorization Challenge Endpoint that lets first-party native apps drive a browserless OAuth flow while still supporting step-up authentication via RFC 9470.",
     "https://datatracker.ietf.org/doc/draft-ietf-oauth-first-party-apps/",
     "IETF (OAuth WG)",
     "Revision -03, published 28 Feb 2026; explicitly excluded for third-party use because it requires high AS↔client trust."),

    ("draft-ietf-oauth-attestation-based-client-auth — OAuth 2.0 Attestation-Based Client Authentication",
     "An IETF WG draft (Looker/Bastian/Bormann) introducing two JWTs — a Client Attestation issued by a Client Attester and a Client Attestation PoP signed by the client instance — that travel in HTTP headers to let traditionally-public clients authenticate to the AS without a shared secret.",
     "https://datatracker.ietf.org/doc/draft-ietf-oauth-attestation-based-client-auth/",
     "IETF (OAuth WG)",
     "Revision -08, March 2026; relates to the RATS Passport Model per RFC 9334, but RATS attestation procedures themselves are deliberately out of scope. The 'client instance' framing pairs naturally with the McGuinness Client Instance Assertion draft."),

    ("draft-ietf-oauth-spiffe-client-auth — OAuth SPIFFE Client Authentication",
     "An IETF WG draft (Schwenkschuster/Kasselman/Rose-NIST/Thorgersen-IBM) profiling RFC 7521, RFC 7523, and OAuth attestation-based client auth so that SPIFFE-enabled workloads can authenticate to OAuth ASes using JWT-SVID, WIT-SVID, or X.509-SVID credentials instead of shared client secrets.",
     "https://datatracker.ietf.org/doc/draft-ietf-oauth-spiffe-client-auth/",
     "IETF (OAuth WG)",
     "Revision -01, March 2026 (re-slugged from draft-schwenkschuster-oauth-spiffe-client-auth after WG adoption); the protocol bridge between SPIFFE/WIMSE workload identity and the OAuth client-auth surface."),

    ("draft-kahrer-oauth-client-challenge-protocol — OAuth Client Challenge Protocol",
     "An IETF individual draft from Judith Kahrer (Curity) defining a new 'insufficient_client_authorization' error code so the authorization server can dynamically challenge the client mid-flow for an additional assertion, verifiable presentation, or proof-of-possession material — enabling just-in-time and step-up client authorization.",
     "https://datatracker.ietf.org/doc/draft-kahrer-oauth-client-challenge-protocol/",
     "IETF (individual)",
     "Revision -00 published 19 May 2026; deliberately distinct from first-party-apps (challenges the CLIENT, not the user) and works for both first- and third-party clients. Cites Mastercard Verifiable Intent as a use case, linking it directly to the mandate/RAR pattern OVID implements."),

    ("draft-ietf-oauth-browser-based-apps — OAuth 2.0 for Browser-Based Applications",
     "An IETF WG draft establishing the Backend-for-Frontend (BFF) and other architectural patterns as current best practice for SPAs given browser-resident token-storage limitations.",
     "https://datatracker.ietf.org/doc/draft-ietf-oauth-browser-based-apps/",
     "IETF (OAuth WG)",
     "Revision -26 (Dec 2025); critical for any delegated-authorization design touching SPAs because it codifies why pure-browser refresh tokens are deprecated."),

    ("draft-ietf-oauth-security-topics-update — Updates to OAuth 2.0 Security BCP",
     "An IETF WG draft that extends RFC 9700 with new countermeasures, notably rules against audience-injection attacks where a client authenticates to multiple authorization servers.",
     "https://datatracker.ietf.org/doc/draft-ietf-oauth-security-topics-update/",
     "IETF (OAuth WG)",
     "Revision -01, March 2026; co-authored by University of Stuttgart (FAPI formal-analysis team) so the recommendations are formally grounded."),

    ("draft-mcguinness-oauth-actor-profile — OAuth Actor Profile for Delegation",
     "Karl McGuinness's individual draft profiling the RFC 8693 'act' claim with required iss, optional sub_profile entity classification, and uniform processing across JWT assertion grants, JWT access tokens, and Transaction Tokens.",
     "https://datatracker.ietf.org/doc/html/draft-mcguinness-oauth-actor-profile-00",
     "IETF (individual)",
     "Revision -00 published 30 April 2026; defines depth-1+ chain validation, cycle-aware construction, and bearer-to-PoP upgrade — the most complete actor-representation profile to date."),

    ("draft-mw-oauth-actor-chain — Cryptographically Verifiable Actor Chains for OAuth 2.0 Token Exchange",
     "An IETF individual draft (Prasad/Krishnan/Lopez/Addepalli) defining six actor-chain profiles for RFC 8693 — Declared/Verified × Full/Subset/Actor-Only Disclosure — that preserve and cryptographically validate delegation-path continuity across successive token exchanges instead of relying on RFC 8693's informational-only nested act claims.",
     "https://datatracker.ietf.org/doc/draft-mw-oauth-actor-chain/",
     "IETF (individual)",
     "97-page -00 submitted 1 May 2026 (re-slugged from draft-mw-spice-actor-chain-05); a complementary alternative to the McGuinness Actor Profile that directly addresses RFC 8693's chain-splicing weakness by making the chain itself cryptographically verifiable rather than just informational."),

    ("draft-mcguinness-oauth-client-instance-assertion — OAuth Client Instance Assertion",
     "Karl McGuinness's individual draft for representing a specific running instance of an OAuth client (rather than just the client registration) so authorization servers can bind grants to a concrete instance.",
     "https://datatracker.ietf.org/doc/draft-mcguinness-oauth-client-instance-assertion/",
     "IETF (individual)",
     "Note: full draft text was not retrievable through automated fetch at time of writing — recommend reading directly. Companion to the Actor Profile draft and to attestation-based client auth."),

    ("draft-mcguinness-oauth-resource-token-resp — OAuth 2.0 Resource Parameter in Access Token Response",
     "A McGuinness/Skokan individual draft adding a 'resource' parameter to the OAuth access token response so clients can confirm which resource the issued token is valid for, mitigating resource mix-up attacks especially in deployments that use RFC 8707 Resource Indicators.",
     "https://datatracker.ietf.org/doc/draft-mcguinness-oauth-resource-token-resp/",
     "IETF (individual)",
     "Revision -03 (March 2026). Filip Skokan added as co-author in -03. Complements RFC 8707 / RFC 9700 / RFC 9207 by adding issuance-time confirmation to the discovery-time mechanisms. Notable for the agent-authz corpus because dynamic resource discovery is a core agent pattern and resource-mix-up attacks are amplified when agents juggle many short-lived tokens."),

    ("draft-mcguinness-oauth-rfc9728bis — Update to OAuth 2.0 Protected Resource Metadata Resource Identifier Validation",
     "A McGuinness individual draft updating Section 3.3 of RFC 9728 (Protected Resource Metadata) so the resource value can be any URI sharing the same TLS origin as the requested URL whose path is a prefix of it — broadening the set of WWW-Authenticate response use cases without changing the rest of RFC 9728.",
     "https://datatracker.ietf.org/doc/draft-mcguinness-oauth-rfc9728bis/",
     "IETF (individual)",
     "Revision -01 (Feb 2026). A small targeted correction to the PRM validation rule. Notable as supporting infrastructure for the McGuinness Mission-Bound OAuth work — PRM is the substrate for Resource AS / Resource Server discovery of required RAR types under that profile."),

    ("draft-mcguinness-token-xchg-target-svc-disco — OAuth 2.0 Token Exchange Target Service Discovery",
     "A McGuinness/Parecki individual draft defining a discovery endpoint that, given a subject token, returns the set of available target services (audiences, resources, scopes) the holder can request via RFC 8693 Token Exchange — accepting any registered subject_token_type so it supports advanced flows including identity chaining and cross-domain delegation.",
     "https://datatracker.ietf.org/doc/draft-mcguinness-token-xchg-target-svc-disco/",
     "IETF (individual)",
     "Revision -01 (Feb 2026), co-authored with Aaron Parecki (Okta). Fills a discovery gap that ID-JAG and the Transaction Token Chaining Profile both implicitly assume — clients today must know which audience to request, which doesn't compose with open-world agentic flows where the right downstream service is determined at runtime."),

    ("draft-mcguinness-oauth-actor-receipts — OAuth Actor Receipts for Delegation Provenance",
     "A McGuinness companion draft to the Actor Profile, aiming to provide per-hop signed receipts as the verifiable provenance layer that the Actor Profile (which keeps the 'act' chain informational) deliberately leaves out. Pulls over the provenance gap from the core profile so each principal in a delegation chain can produce independent cryptographic evidence.",
     "https://mcguinness.github.io/draft-mcguinness-oauth-actor-profile/draft-mcguinness-oauth-actor-receipts.html",
     "Pre-publication (author's GitHub)",
     "NOT YET ON DATATRACKER. McGuinness described it on the OAUTH-WG list on 1 May 2026 as 'a very early work in progress'. Recommended companion to the Actor Profile when a deployment needs Verified Full Disclosure mode (per the Mission-Bound OAuth Runtime Enforcement Profile's Actor Provenance Module). Watch for an IETF submission later in 2026."),

    ("draft-mishra-oauth-agent-grants — Delegated Agent Authorization Protocol (DAAP)",
     "An IETF individual draft addressing runtime agent identity for dynamically-spawned agents, multi-agent sub-delegation with depth-limiting, and cascade revocation of an entire delegation subtree when any ancestor is revoked.",
     "https://datatracker.ietf.org/doc/draft-mishra-oauth-agent-grants/",
     "IETF (individual)",
     "Revision -01 (March 2026); registers new JWT claims (agt, dev, grnt, scp, bdg) — a more aggressive alternative to RFC 8693 with budget-bounded grants. Overlaps with draft-niyikiza-oauth-attenuating-agent-tokens; OAuth WG will likely expect consolidation."),

    ("draft-kuehlewind-audit-architecture — Architecture for Auditing AI Agent Delegation and Interactions",
     "An IETF individual draft from Mirja Kühlewind (Ericsson, former IETF TSV-AD) and Henk Birkholz (Fraunhofer SIT, lead author of RFC 9334 RATS and SCITT architecture) defining four record types — Interaction, Action, Delegation, and Authorization Transition — and an Audit Context that propagates across OAuth + WIMSE + RATS + SCITT to make agent behaviour verifiably auditable end-to-end.",
     "https://datatracker.ietf.org/doc/draft-kuehlewind-audit-architecture/",
     "IETF (individual)",
     "Revision -00 published 18 May 2026; the cross-layer integration piece — explicitly composes the McGuinness Actor Profile, Transaction Tokens, identity-chaining, ID-JAG, WIMSE, RATS, and SCITT into a single auditable architecture with 11 proposed work items. The treats-Agent-as-untrusted threat model is what regulators (SOX, PSD2, EU AI Act) actually want."),

    ("draft-birkholz-verifiable-agent-conversations — Verifiable Agent Conversation Records",
     "An IETF individual draft (Birkholz/Heldt/Steele) defining a CDDL data format — with both JSON and CBOR encodings — for tamper-evident, verifiably-signed records of agent conversations, agent reasoning traces, tool calls, and system events that support long-term evidentiary value across chains of custody.",
     "https://datatracker.ietf.org/doc/draft-birkholz-verifiable-agent-conversations/",
     "IETF (individual)",
     "Revision -00 published 25 Feb 2026; presented at IETF 125 dispatch and hotrfc. The canonical Interaction-Record format for the Kuehlewind audit architecture. Motivating examples are concrete: agents acting beyond scope, CoT divergence, and 'sandbagging' during evaluations."),

    ("draft-klrc-aiagent-auth — AI Agent Authentication and Authorization",
     "An IETF individual draft that does not invent new protocols but composes WIMSE/SPIFFE workload identity, OAuth 2.x, and OpenID SSF to authenticate and delegate authority to AI agents.",
     "https://datatracker.ietf.org/doc/html/draft-klrc-aiagent-auth-00",
     "IETF (individual)",
     "Revision -00, March 2026; introduces 'Agent Identity Management System (AIMS)' and is the cleanest standards-based framing of agent-as-workload."),

    # ---- Individual drafts: Identity / Authorization / Delegation cluster ----
    ("draft-niyikiza-oauth-attenuating-agent-tokens — Attenuating Authorization Tokens for Agentic Delegation Chains",
     "An IETF individual draft extending RFC 9396 Rich Authorization Requests with monotonic attenuation at each delegation hop, offline chain verification, and a typed constraint vocabulary for tool-level argument restrictions.",
     "https://datatracker.ietf.org/doc/draft-niyikiza-oauth-attenuating-agent-tokens/",
     "IETF (individual)",
     "Revision -00, March 2026; arguably the strongest purely-OAuth-grounded delegation draft — offline verification is a key scalability property. Good path to OAuth WG adoption; overlaps with draft-mishra-oauth-agent-grants and will likely need to be consolidated with it."),

    ("draft-singla-agent-identity-protocol — AIP: Decentralized Identity and Delegation for AI Agents",
     "An IETF individual draft proposing a six-layer model (identity through reputation) for AI agents with W3C DID anchoring, a Delegation Depth counter, three Grant ceremony tiers (G1/G2/G3), DPoP proof-of-possession, and an MCP integration layer.",
     "https://datatracker.ietf.org/doc/draft-singla-agent-identity-protocol/",
     "IETF (individual)",
     "Revision -00, 17 April 2026; the most comprehensive identity framework in the set. The W3C DID dependency will face IETF pushback, the 75+ page scope needs reduction, and the 'AIP' name collision with two other drafts (draft-prakash-aip, draft-aip-agent-identity-protocol) must be resolved."),

    ("draft-prakash-aip — AIP: Verifiable Delegation for AI Agent Systems",
     "An IETF individual draft introducing Invocation-Bound Capability Tokens (IBCTs) in two modes — compact (JWT/Ed25519) for single-hop and chained (Biscuit + Datalog) for multi-hop — with bindings for MCP, A2A, and HTTP APIs.",
     "https://datatracker.ietf.org/doc/draft-prakash-aip/",
     "IETF (individual)",
     "Revision -00, 27 March 2026; technically strong — Biscuit + Datalog is well-suited to scope attenuation. The 'AIP' name collision with draft-singla-agent-identity-protocol and draft-aip-agent-identity-protocol is a blocking issue for WG adoption."),

    ("draft-goswami-agentic-jwt — Secure Intent Protocol: JWT-Compatible Agentic Identity and Workflow Management",
     "An IETF individual draft defining an Agentic JWT extension to OAuth 2.0 with a Supervisor Agent role for sub-agent coordination, explicitly addressing the 'intent-execution separation' gap and adding workflow-step authorization.",
     "https://datatracker.ietf.org/doc/draft-goswami-agentic-jwt/",
     "IETF (individual)",
     "Revision -00, December 2025; the intent-execution-separation framing is insightful and distinguishing. The workflow-step authorization approach is novel but may face skepticism in the OAuth WG."),

    ("draft-ni-wimse-ai-agent-identity — WIMSE Applicability for AI Agents",
     "An IETF individual draft mapping the WIMSE workload-identity architecture to AI-agent use cases and establishing credential-management mechanisms for agentic AI within the WIMSE framework.",
     "https://datatracker.ietf.org/doc/draft-ni-wimse-ai-agent-identity/",
     "IETF (individual)",
     "Revision -02, February 2026; an important bridge between the WIMSE WG and the AI agent space. If an AI-agent WG is ever chartered, this applicability statement is essential groundwork. Co-authored with Liu, who also leads the related security-requirements draft."),

    ("draft-sharif-agent-identity-framework — Agent Identity Framework: Trust and Identity for Autonomous AI Agents",
     "An IETF individual draft proposing a five-layer model (identity, authorization, attestation, evidence, trust) for autonomous AI agents, with a gap analysis between current Internet standards and agent requirements.",
     "https://datatracker.ietf.org/doc/draft-sharif-agent-identity-framework/",
     "IETF (individual)",
     "Revision -00, 6 April 2026; more gap-analysis than protocol spec. Useful as problem statement. Five-layer model is a reasonable decomposition but insufficient as a standalone contribution. Part of the Sharif cluster (with -agent-audit-trail, -attp, etc.)."),

    ("draft-aip-agent-identity-protocol — AIP: Agentic Authentication and Authorized Policy Enforcement",
     "An IETF individual draft defining an AIP Token signed per tool call (agent ID, tool, nonce, timestamp, signature), an AgentPolicy YAML format for per-tool argument constraints and DLP rules, and a Human-in-the-Loop proxy enforcement model.",
     "https://datatracker.ietf.org/doc/draft-aip-agent-identity-protocol/",
     "IETF (individual)",
     "Revision -00, 16 March 2026; implementation-focused. YAML policy approach is pragmatic but not interoperable-by-design. HITL integration is a valuable safety feature. Third member of the 'AIP' name-collision triple — must be resolved before any can progress."),

    # ---- Individual drafts: Transport / Infrastructure / Discovery cluster ----
    ("draft-serra-mcp-discovery-uri — The mcp URI Scheme and MCP Server Discovery Mechanism",
     "An IETF individual draft defining an 'mcp://' URI scheme combined with /.well-known/mcp-server (RFC 8615) and a DNS TXT fallback for discovery of Model Context Protocol servers.",
     "https://datatracker.ietf.org/doc/draft-serra-mcp-discovery-uri/",
     "IETF (individual)",
     "Already at revision -04 (March 2026), suggesting active iteration; narrow scope, clean design, and the strongest IANA-registration candidate in the set. OAuth 2.1 for auth is deliberately out of scope."),

    ("draft-sharif-attp — ATTP: Agent Trust Transport Protocol",
     "An IETF individual draft defining trust levels L0–L4 mapped to PSD2 Strong Customer Authentication requirements, with bindings for MCP (MCPS), REST, A2A, gRPC, and GraphQL; supersedes draft-sharif-agent-payment-trust.",
     "https://datatracker.ietf.org/doc/draft-sharif-attp/",
     "IETF (individual)",
     "Revision -00, April 2026; regulatory mapping appendices (PSD2, PCI DSS) are notable — one of the few drafts engaging financial regulation directly. Ambitious scope. Part of the Sharif cluster."),

    ("draft-sharif-agent-transport-protocol — Agent Transport Protocol (ATP): Async Store-and-Forward for AI Agents",
     "An IETF individual draft defining async store-and-forward messaging semantics with cryptographic identity per relay hop, trust scoring at ingress, capability negotiation, and interop with Google A2A, MCP, and FIPA ACL; transport-agnostic over TCP/TLS/QUIC.",
     "https://datatracker.ietf.org/doc/draft-sharif-agent-transport-protocol/",
     "IETF (individual)",
     "Revision -00, 28 March 2026; addresses a real gap — most agent protocols assume synchronous availability, and store-and-forward is appropriate for long-running agentic tasks. Scope is broad and needs narrowing."),

    ("draft-sharif-agent-audit-trail — Agent Audit Trail (AAT): Standard Logging Format for Autonomous AI Systems",
     "An IETF individual draft defining a JSON-based audit record with mandatory fields (agent identity, action classification, outcome tracking, trust level) using RFC 8785 JSON Canonicalization and RFC 9562 UUIDs.",
     "https://datatracker.ietf.org/doc/draft-sharif-agent-audit-trail/",
     "IETF (individual)",
     "Revision -00, 29 March 2026; orthogonal to delegation but important for compliance — standardized audit-log format is a genuine gap. Complements identity frameworks well. A sibling/alternative to the Kuehlewind audit architecture which takes a far more ambitious cross-layer approach."),

    ("draft-aiendpoint-ai-discovery — The AI Discovery Endpoint",
     "An IETF individual draft defining a /.well-known/ai URI suffix for programmatic service capability discovery by AI agents — letting agents discover what an endpoint supports without having to parse human-oriented documentation; requests IANA well-known URI registration.",
     "https://datatracker.ietf.org/doc/draft-aiendpoint-ai-discovery/",
     "IETF (individual)",
     "Revision -00, March 2026; complementary to MCP discovery but broader (not MCP-specific). Needs differentiation from OpenAPI/service-description work to gain traction."),

    # ---- Individual drafts: Security Requirements / Frameworks cluster ----
    ("draft-ni-a2a-ai-agent-security-requirements — Security Requirements for AI Agents",
     "An IETF individual draft enumerating security requirements for AI agents, covering identity, authorization chaining across domains, and integration points with WIMSE, OAuth identity chaining, and the A2A OAuth profile.",
     "https://datatracker.ietf.org/doc/draft-ni-a2a-ai-agent-security-requirements/",
     "IETF (individual)",
     "Revision -01, February 2026; essential scaffolding for an eventual AI-agent WG. Well-connected to existing IETF work and authored by Ni and Liu, who also lead the WIMSE AI-agent identity draft."),

    ("draft-rosenberg-aiproto-framework — Framework, Use Cases and Requirements for AI Agent Protocols",
     "An IETF individual draft providing a comprehensive AI-agent communications framework that covers user↔agent, agent↔API, and agent↔agent interactions; surveys MCP, A2A, and Agntcy; and sets the stage for IETF standards activity.",
     "https://datatracker.ietf.org/doc/draft-rosenberg-aiproto-framework/",
     "IETF (individual)",
     "Revision -00, October 2025; Rosenberg (Five9) and Jennings (Cisco) are credible long-time IETF contributors. Important landscape document but likely expired (April 2026); watch for a -01 refresh post-IETF 123."),

    ("draft-rosenberg-aiproto-cheq — CHEQ: A Protocol for Confirmation of AI Agent Decisions (HITL)",
     "An IETF individual draft defining an out-of-band Human-in-the-Loop confirmation protocol for agent tool calls, eliminating LLM-hallucination risk for consequential actions and enabling sensitive operations (e.g., banking) without exposing data to the agent.",
     "https://datatracker.ietf.org/doc/draft-rosenberg-aiproto-cheq/",
     "IETF (individual)",
     "Revision -00, October 2025; out-of-band HITL confirmation model is valuable and complements delegation frameworks. Likely expired (April 2026); worth tracking for a -01 refresh."),

    ("draft-sharif-agent-payment-trust — Trust Scoring and Identity Verification for AI Agent Payment Transactions (SUPERSEDED)",
     "An IETF individual draft introducing an Agent Passport — a cryptographic delegation certificate intended to serve as the PSD2 'something you have' factor — and a trust-scoring model for payment transactions mapped to PCI DSS v4.0.1.",
     "https://datatracker.ietf.org/doc/draft-sharif-agent-payment-trust/",
     "IETF (individual, superseded)",
     "SUPERSEDED by draft-sharif-attp-00 (April 2026). Retained for historical context — the Agent Passport concept is interesting but needs formal grounding; the ATTP successor generalizes it across transport bindings."),

    ("draft-stephan-ai-agent-6g — AI Agent Protocols for 6G Systems",
     "An IETF individual draft translating use cases and service requirements from 3GPP TR 22.870 into IETF agent-protocol requirements, covering autonomous vehicles, privacy preservation, and anomaly detection.",
     "https://datatracker.ietf.org/doc/draft-stephan-ai-agent-6g/",
     "IETF (individual)",
     "Revision -02, October 2025; strong operator backing (Orange, Deutsche Telekom, Telefonica, China Mobile, Huawei). Requirements-oriented and important for 3GPP/IETF coordination. May be expired (April 2026); watch for an update."),

    ("draft-jimenez-t2trg-iot-agent — Agentic AI Operation of Constrained RESTful Environments",
     "An IETF individual draft (T2TRG affiliated) describing agentic AI (ReAct, smolagents) operating on CoAP/CoRE constrained-IoT environments, with a reference implementation provided.",
     "https://datatracker.ietf.org/doc/draft-jimenez-t2trg-iot-agent/",
     "IETF (individual)",
     "Revision -00, 14 April 2026; unique in targeting constrained IoT environments. T2TRG affiliation and reference implementation are positive signals. Niche but fills an unaddressed gap."),

    ("draft-li-oauth-delegated-authorization — OAuth 2.0 Delegated Authorization",
     "An IETF individual draft from Huawei authors that extends OAuth 2.0 with a hierarchical 'delegation token' model so a client can mint subordinate, narrowly-scoped access tokens for delegated parties.",
     "https://datatracker.ietf.org/doc/draft-li-oauth-delegated-authorization/",
     "IETF (individual)",
     "Revision -01, March 2026 (Informational); directly addresses over-privileged tokens and is one of the few drafts using the literal term 'delegated authorization'."),

    ("draft-araut-oauth-transaction-tokens-for-agents — Transaction Tokens For Agents",
     "An IETF individual draft from Ashay Raut (Amazon) profiling Transaction Tokens for agent-based workflows by adding 'act' for the agent identity, an 'agentic_ctx' claim carrying agent_type/intent/allowed_actions/environment_constraints, RFC 9396 RAR integration, and an 'actchain' claim for multi-agent delegation lineage.",
     "https://datatracker.ietf.org/doc/draft-araut-oauth-transaction-tokens-for-agents/",
     "IETF (individual)",
     "Revision -01 (May 2026) under the new slug — re-slugged from draft-oauth-transaction-tokens-for-agents-06; the -06 added the actchain delegation lineage, RAR-driven agentic_ctx, and a TTS check that blocks chain-splicing attacks. Conservative extension of the WG Transaction Tokens draft and an easier path to standardization."),

    ("draft-oauth-ai-agents-on-behalf-of-user — On-Behalf-Of User Authorization for AI Agents",
     "An IETF individual draft adding requested_actor and actor_token parameters to the OAuth authorization-code flow so the user gives explicit consent per agent, with the resulting delegation chain documented in the access-token claims.",
     "https://datatracker.ietf.org/doc/draft-oauth-ai-agents-on-behalf-of-user/",
     "IETF (individual)",
     "Revision -02 was submitted August 2025; likely due for -03 refresh. Builds naturally on RFC 6749 + RFC 8693 + RFC 7636 PKCE — one of the most 'IETF-ready' delegation drafts and a strong WG-adoption candidate after the OAuth recharter."),

    ("draft-hardt-aauth-protocol — AAuth Protocol",
     "A new clean-sheet authorization protocol from Dick Hardt (original OAuth author) defining proof-of-possession by default, resource-signed challenges, agent identity without pre-registration, deferred 202 responses, and AS-to-AS federation for the agent ecosystem.",
     "https://datatracker.ietf.org/doc/draft-hardt-aauth-protocol/",
     "IETF (individual)",
     "Revision -00, April 2026; the design rationale section explicitly explains why AAuth is not GNAP, not OAuth, not DPoP and not mTLS — important read for anyone planning a new agent-auth stack."),

    ("draft-chen-oauth-roadmap — Comprehensive Roadmap for OAuth 2.0 Standards and Drafts",
     "An IETF informational draft that maps the entire OAuth 2.0 ecosystem of RFCs, BCPs, and active drafts into functional layers from core to extensions to industry profiles.",
     "https://www.ietf.org/archive/id/draft-chen-oauth-roadmap-00.html",
     "IETF (individual)",
     "Brand-new -00 draft (May 2026); the single most useful index when starting work in this area."),

    ("Charter: WIMSE — Workload Identity in Multi-System Environments (charter-ietf-wimse-01)",
     "The formal IETF charter for the WIMSE WG covering architecture, JOSE-based WIMSE tokens for service-to-service traffic, local token issuance, and token exchange profiles (likely based on RFC 8693) for cross-trust-domain workload identity.",
     "https://datatracker.ietf.org/doc/charter-ietf-wimse/01/",
     "IETF (WIMSE WG charter)",
     "Approved 18 March 2026 (v01); explicitly liaises with OAuth, SCIM, SCITT, RATS, the OpenID Foundation, and CNCF/SPIFFE — the formal scope statement that anchors all WIMSE draft work."),
]
make_sheet("Active IETF Drafts", COLORS['Drafts'], draft_rows)

# ============================================================
# TAB 3: OpenID Foundation
# ============================================================
oidf_rows = [
    ("OpenID Foundation — Identity Management for Agentic AI (Whitepaper, Oct 2025)",
     "An OpenID Foundation whitepaper arguing that user impersonation by agents should be replaced by delegated authority, requiring explicit 'on-behalf-of' flows where agents prove their delegated scope while remaining identifiable as distinct from the user they represent.",
     "https://openid.net/wp-content/uploads/2025/10/Identity-Management-for-Agentic-AI.pdf",
     "OpenID Foundation",
     "The industry's most-cited problem statement for agent identity; ZeroID and other reference implementations explicitly position themselves against this document."),

    ("OpenID AuthZEN Authorization API 1.0 (Final)",
     "An OpenID Foundation Final Specification that standardizes the request/response between Policy Enforcement Points and Policy Decision Points, often described as 'OIDC for authorization'.",
     "https://openid.net/specs/authorization-api-1_0.html",
     "OpenID Foundation (AuthZEN WG)",
     "Approved as Final 12 January 2026 by 81–1–25 vote; complements OAuth's delegation by externalizing the runtime allow/deny decision."),

    ("OpenID AuthZEN Profile for MCP Tool Authorization",
     "An OpenID AuthZEN profile that maps MCP tool-invocation authorization onto the AuthZEN PDP/PEP API so MCP servers can externalize per-tool decisions.",
     "https://github.com/openid/authzen",
     "OpenID Foundation (AuthZEN WG)",
     "Among the first standards-body responses to the agent/MCP authorization problem; lives in the AuthZEN GitHub alongside the core spec."),

    ("OpenID AuthZEN Access Request and Approval Profile (ARAP) — Draft 1",
     "An AuthZEN WG draft (adopted May 2026, Draft 1 published 3 June 2026, sole author Karl McGuinness) that lets a PDP return decision:false with a structured 'access_request' context object pointing at an Access Request Endpoint. The PEP submits the request, gets an opaque Task Handle, polls or receives callbacks, and re-evaluates against the PDP after the workflow completes — denial remains denial; the PDP stays authoritative.",
     "https://openid.github.io/authzen/authzen-access-request-approval-profile-1_0.html",
     "OpenID Foundation (AuthZEN WG)",
     "The standardization of 'deny, but escalate' as a runtime primitive. Concepts: evaluation_id binding, JWS binding_token, approval.state (also JWS), bulk items[] submissions, catalog references for entitlement enumeration, multi-step approval progress, cancellation, idempotency. Single completion mode in the base profile (reevaluate); other modes deferred to follow-on profiles. AI agents are a primary use case in the worked examples (the 'Agent Tool Discovery' end-to-end appendix). Composes with McGuinness's Actor Profile draft for the act-chain shape. Explicitly positioned against CIBA: ARAP solves authorization escalation, CIBA solves authentication freshness — different problems."),

    ("OpenID Continuous Access Evaluation Profile (CAEP) 1.0",
     "An OpenID Foundation specification that defines event types over the Shared Signals Framework so transmitters can asynchronously notify receivers of session, credential, or device-posture changes.",
     "https://openid.net/specs/openid-caep-1_0-final.html",
     "OpenID Foundation (Shared Signals WG)",
     "Pairs with AuthZEN to give continuous (not just point-in-time) authorization — the async layer of the 'continuous authorization loop'."),

    ("OpenID Shared Signals Framework (SSF) 1.0",
     "An OpenID Foundation specification that defines a generic transport for Security Event Tokens (RFC 8417) between cooperating identity providers and relying parties.",
     "https://openid.net/wg/sharedsignals/specifications/",
     "OpenID Foundation (Shared Signals WG)",
     "Underlies both CAEP (session/access changes) and RISC (account-compromise signals); 9-vendor interop demonstrated at Gartner IAM London 2025."),

    ("CAEP Interoperability Profile 1.0",
     "An OpenID profile that pins down concrete bindings, OAuth 2.0 usage, and minimal event-type support so independent SSF/CAEP implementations can actually interoperate.",
     "https://openid.github.io/sharedsignals/openid-caep-interoperability-profile-1_0.html",
     "OpenID Foundation (Shared Signals WG)",
     "Critical because the CAEP base spec leaves enough optionality that vendors weren't truly interoperable until this profile."),

    ("FAPI 2.0 Security Profile (Final)",
     "The OpenID Foundation Final Specification that defines a high-security OAuth 2.0 profile requiring sender-constrained tokens (DPoP/mTLS), PAR, and formally analyzed properties.",
     "https://openid.net/specs/fapi-security-profile-2_0-final.html",
     "OpenID Foundation (FAPI WG)",
     "Approved Final Feb 2025; formally verified by University of Stuttgart and now the de-facto baseline for open banking/open data globally."),

    ("FAPI 2.0 Message Signing",
     "An OpenID FAPI extension that adds non-repudiation by requiring signatures over authorization requests, responses, and resource-server messages on top of the FAPI 2.0 baseline.",
     "https://openid.net/specs/fapi-2_0-message-signing-ID1.html",
     "OpenID Foundation (FAPI WG)",
     "Final conformance tests launched August 2025; required where regulators or schemes demand non-repudiation."),

    ("OpenID FAPI Grant Management for OAuth 2.0",
     "An OpenID FAPI specification that standardizes how clients create, query, update, and revoke long-lived consent grants, born from PSD2 and Australian CDR experience.",
     "https://openid.net/wg/fapi/specifications/",
     "OpenID Foundation (FAPI WG)",
     "Solves the recurring 'where do I see and revoke what I've delegated?' UX problem at scale."),

    ("Health Relationship Trust Profile for UMA 2.0 (HEART UMA2)",
     "An OpenID HEART profile of UMA 2.0 that tightens cryptographic and consent-management requirements for healthcare/HIPAA-style multi-party API scenarios.",
     "https://openid.net/specs/openid-heart-uma2-1_0.html",
     "OpenID Foundation (HEART WG)",
     "Reference for any patient-mediated data-sharing implementation, including 21st Century Cures Act deployments."),
]
make_sheet("OpenID Foundation", COLORS['OpenID'], oidf_rows)

# ============================================================
# TAB 4: Other standards bodies
# ============================================================
other_rows = [
    ("User-Managed Access (UMA) 2.0 Grant for OAuth 2.0 Authorization",
     "A Kantara Initiative recommendation defining an OAuth 2.0 extension grant for asynchronous, party-to-party delegation where the resource owner pre-configures policy on the AS.",
     "https://docs.kantarainitiative.org/uma/wg/rec-oauth-uma-grant-2.0.html",
     "Kantara Initiative",
     "The original 'Alice-to-Bob' delegated-authorization standard; broadly supported by Keycloak, ForgeRock/Ping, WSO2."),

    ("W3C Verifiable Credentials Data Model v2.0 (Recommendation)",
     "The W3C Recommendation defining a tamper-evident, cryptographically-signed claim structure with an issuer/holder/verifier model and support for selective disclosure.",
     "https://www.w3.org/TR/vc-data-model-2.0/",
     "W3C (VC WG)",
     "Reached Recommendation status 15 May 2025; underlies EUDI Wallet, mDL, and most agent-attestation proposals."),

    ("W3C Verifiable Credentials Data Model v2.1 (First Public Working Draft)",
     "The W3C VC Working Group's First Public Working Draft of the next data-model revision, refining v2.0 alignment with JOSE/COSE and Data Integrity proofs.",
     "https://www.w3.org/news/2026/first-public-working-draft-verifiable-credentials-data-model-v2-1/",
     "W3C (VC WG)",
     "Published April 2026; planned EU recognition target April 2027 per VC WG charter."),

    ("W3C Verifiable Credentials Working Group Charter (2026)",
     "The current W3C charter for the VC WG that schedules upcoming Recommendations on Confidence Method, Rendering Methods, and an HTTP API for issuance and presentation.",
     "https://w3c.github.io/vc-charter-2026/",
     "W3C",
     "Confidence Method and Rendering Methods exclusion periods ended 29 March 2026 — these are the v2.1 sibling specs to watch."),

    ("NIST AI Agent Standards Initiative — Center for AI Standards and Innovation",
     "A NIST initiative within the Center for AI Standards and Innovation aimed at accelerating adoption of software and AI-agent identity and authorization standards.",
     "https://www.nist.gov/ai",
     "NIST (US government)",
     "February 2026 NCCoE concept paper on 'Accelerating the Adoption of Software and AI Agent Identity and Authorization' is the key entry point."),

    ("EU AI Act broader enforcement (high-risk AI systems audit trails, August 2026)",
     "EU regulation requiring auditable trails for high-risk AI systems, which in practice mandates the kind of cryptographic delegation chains being standardized in IETF agent drafts.",
     "https://artificialintelligenceact.eu/",
     "European Union (regulation)",
     "Compliance deadline shapes urgency for delegation-chain standardization; many vendors target Aug 2026 readiness."),
]
make_sheet("Other Standards & Govt", COLORS['Other'], other_rows)

# ============================================================
# TAB 5: Academic
# ============================================================
academic_rows = [
    ("Authenticated Delegation and Authorized AI Agents (South et al., arXiv:2501.09674)",
     "An academic paper from MIT, Anthropic, and collaborators proposing an OAuth/OIDC-compatible framework for authenticated, scoped, auditable delegation of authority from humans to AI agents.",
     "https://arxiv.org/abs/2501.09674",
     "Academic (arXiv preprint)",
     "Highly cited 2025 paper that re-framed agent authorization as 'delegation with chains of accountability' and influenced subsequent IETF drafts."),

    ("Delegated Authorization for Agents Constrained to Semantic Task-to-Scope Matching (arXiv:2510.26702)",
     "An academic paper introducing a model in which the AS semantically inspects an agent's intended task and grants the minimal scope set, plus the ASTRA benchmark dataset.",
     "https://arxiv.org/abs/2510.26702",
     "Academic (arXiv preprint)",
     "Published Oct 2025; one of the first works giving researchers a public benchmark for semantically-grounded delegated authorization."),

    ("Establishing Workload Identity for Zero Trust CI/CD (Avirneni, arXiv:2504.14760)",
     "An academic paper describing the migration from static CI/CD secrets through OIDC federation to runtime SPIFFE-issued workload identities for non-human actors.",
     "https://arxiv.org/abs/2504.14760",
     "Academic (arXiv preprint)",
     "Concrete enterprise-grade reference implementation tying SPIFFE/SPIRE to OIDC federation in GitHub Actions/AWS/GCP/Azure."),

    ("Identity Control Plane: The Unifying Layer for Zero Trust Infrastructure (arXiv:2504.17759)",
     "An academic position paper proposing an Identity Control Plane that unifies SPIFFE workload identity, OIDC/SAML human identity, and broker-issued transaction tokens under one policy plane.",
     "https://arxiv.org/abs/2504.17759",
     "Academic (arXiv preprint)",
     "Useful conceptual framing because most enterprises already have all three identity types but no unified plane."),

    ("Formal Security Analysis of the OpenID Financial-grade API 2.0 (Hosseyni, Kuesters, Würtele, IEEE CSF 2024)",
     "An academic paper providing the formal-methods proof of FAPI 2.0's security properties under the FAPI 2.0 attacker model, performed by the University of Stuttgart team.",
     "https://doi.ieeecomputersociety.org/10.1109/CSF61375.2024.00002",
     "IEEE CSF (Academic conference)",
     "The proof underpinning FAPI 2.0's claim of being formally verified; the same authors now drive the OAuth Security Topics Update draft."),
]
make_sheet("Academic Papers", COLORS['Academic'], academic_rows)

# ============================================================
# TAB 6: Industry & Implementations — with ZeroID and auth.md
# ============================================================
industry_rows = [
    # ---- Reference implementations of the standards stack ----
    ("OVID-ME — Cedar Policy Evaluation for OVID Agent Mandates",
     "A reference implementation that enforces attenuated multi-hop agent-delegation mandates by evaluating Cedar policies embedded as RFC 9396 authorization_details inside signed OVID JWTs.",
     "https://github.com/clawdreyhepburn/ovid-me",
     "Open-source (Apache-2.0)",
     "Companion to the OVID identity package; provides AuthZEN-compliant PDP, dry-run/shadow/enforce modes, and SMT-based subset proof at issuance time. Pairs with Carapace as a two-layer enforcement stack."),

    ("OVID — Cryptographic Agent Identity (npm @clawdreyhepburn/ovid)",
     "An Ed25519 JWT package giving each agent a signed cryptographic identity with walkable delegation chains back to the human, designed to compose with OVID-ME at evaluation time.",
     "https://www.npmjs.com/package/@clawdreyhepburn/ovid",
     "Open-source (Apache-2.0)",
     "Implements the SPIFFE-style 'spawner is the attestor' model for agents; conceptual sibling of WIMSE workload tokens for the agent-delegation use case."),

    ("ZeroID — Autonomous Agent Identity Management System (AAIMS)",
     "A Go-based open-source identity service from Highflame that issues short-lived agent credentials over OAuth 2.1 with WIMSE/SPIFFE URIs, RFC 8693 delegation with automatic scope attenuation, configurable max delegation depth, and CAEP/SSF cascading real-time revocation.",
     "https://github.com/highflame-ai/zeroid",
     "Open-source (Apache-2.0)",
     "v1.1.11 released March 2026; one of the most complete production-grade reference implementations of the agent-identity stack — explicitly cites the OpenID Foundation's Oct 2025 Agentic AI whitepaper as its design north-star."),

    ("auth.md — Agentic Registration Protocol (WorkOS)",
     "A reference implementation of a 'robots.txt for agent authentication': an AUTH.md skill manifest at a service's domain that tells agents how to register via three discovery-driven flows — identity assertion (ID-JAG), verified-email assertion, or anonymous OTP claim.",
     "https://github.com/workos/auth.md",
     "Open-source (MIT, WorkOS)",
     "Composes directly with draft-ietf-oauth-identity-assertion-authz-grant; the discovery and onboarding piece that the IETF stack doesn't define, exposed via /.well-known/oauth-authorization-server with an agent_auth block."),

    ("ATP — Agent Trust Protocol Core (atp-sdk)",
     "A TypeScript/Node SDK plus multi-service Docker stack providing quantum-safe (hybrid Ed25519 + NIST ML-DSA) agent identity over a did:atp DID method, with continuous trust scoring, zero-knowledge trust-level proofs, and first-class adapters for LangChain, Motleycrew, MCP, Swarm, ADK, and A2A.",
     "https://github.com/agent-trust-protocol/atp-core",
     "Open-source (Apache-2.0, Larry Lewis)",
     "Specification implicit in implementation — no separate spec doc. Differentiators: PQ hybrid signatures via FIPS 204 ML-DSA, ZK proofs for trust-level predicates (prove trust ≥ 0.7 without revealing the score), multi-framework adapters as a first-class concern. Acronym near-collides with draft-sharif-attp (Agent Trust Transport Protocol) — same problem space, distinct designs: discrete L0-L4 trust levels there, continuous 0.0-1.0 trust scoring here. Early-stage (1 star, 2 contributors, one of whom is Claude); README ships a real Context7 API key, a 'ship-fast' signal worth noting."),

    # ---- LinkedIn-style and analyst articles ----
    ("AI Agents and the Multi-Hop Delegation Problem (WorkOS)",
     "A WorkOS engineering blog post that catalogs the open IETF drafts and RFCs addressing multi-hop AI-agent delegation including identity chaining, attenuating tokens, and actor chains.",
     "https://workos.com/blog/oauth-multi-hop-delegation-ai-agents",
     "Industry blog (WorkOS)",
     "Particularly useful index of currently-active drafts (April 2026) on the agent-delegation problem with NIST and EU AI Act compliance context."),

    # ---- McGuinness "Mission-Bound OAuth" blog series (May–Jun 2026) ----
    # Karl McGuinness (former Okta SVP & Chief Product Architect) — a four-post architectural argument
    # for treating the user-approved task itself as a first-class OAuth object (the "Mission"). Companion
    # to draft-mcguinness-oauth-actor-profile, draft-mcguinness-oauth-client-instance-assertion, and the
    # AuthZEN ARAP profile listed in the OpenID Foundation tab. Listed in publication order.

    ("Mission-Bound OAuth MVP (McGuinness, 22 May 2026)",
     "The protocol-level proposal. Five wire additions on top of existing OAuth: a 'mission_intent' RAR envelope (purpose, mission_expiry, context), a generic 'resource_access' RAR type, a durable Mission record at the Authorization Server, an opaque 'mission' claim (id + origin) on access tokens, and a Mission-state enforcement gate on refresh / exchange / introspection / assertion validation. Seven-state Mission lifecycle (pending_approval, active, suspended, revoked, expired, completed, rejected). proposal_hash (SHA-256 over JCS-canonical authorization_details) and consent_rendering_hash anchor what was approved versus what the user saw.",
     "https://notes.karlmcguinness.com/notes/mission-bound-oauth-mvp/",
     "Architect blog (Karl McGuinness)",
     "76-min read; the substrate post for the whole series. Target I-D name: draft-mcguinness-oauth-mission-bound-minimum-profile. Conformance Ladder L0–L5 (L0 baseline OAuth → L5 verifiable governance with portable receipts). Cross-AS handoff uses ID-JAG for user-rooted flows or the Fletcher Transaction Token Chaining Profile for Txn-Token-rooted flows. Mission Expansion creates a successor Mission with 'mission.supersedes' rather than mutating in place. Three Resource Server tiers (RS-A OAuth-only → RS-D Mission-state aware via introspection or SSF/CAEP events). Architectural challenges acknowledged honestly: state-sync at scale, unknown-constraint brittleness, lethal-trifecta boundary."),

    ("The Mission is the Missing OAuth Abstraction (McGuinness, 1 Jun 2026)",
     "The architectural frame: OAuth has no first-class object for 'the task the user approved' — only tokens, scopes, prompts, and logs that are downstream projections of it. The Mission is that durable, AS-stored, user-approved authority record. Argues this is what closes the gap that five prior bodies of his work (Power of Attorney, Mission Shaping, Open-World OAuth, Sessions Are Not Missions, the Mission-Bound architecture series) have circled from different angles. Two layers, one object: issuance-bound authority (MVP) plus runtime-enforced authority (the IBAC profile).",
     "https://notes.karlmcguinness.com/notes/the-mission-is-the-missing-oauth-abstraction/",
     "Architect blog (Karl McGuinness)",
     "Short (9-min) framing post that ties the whole programme together. The argument for why IBAC becomes practical when intent is compiled from an AS-validated Mission at consent time rather than inferred post-hoc from agent behaviour (where it's adversarial-input territory and the PDP has no user to ask). Best entry point for someone new to the series."),

    ("Mission-Bound OAuth Runtime Enforcement Profile (McGuinness, 1 Jun 2026)",
     "The IBAC layer layered on the MVP. Core (required for compliance): Intent-to-Policy Compilation (AS deterministically compiles approved authorization_details to an evaluable artifact at activation, stores policy_version on the Mission), Resource-Side Enforcement Contract (RS-B minimum, PDP evaluates every consequential request), Standard Subset Semantics per RAR Type with strict-refuse on unknown constraints (stricter than MVP's 'preserve or refuse'), Mission Introspection Profile (extended response with act chain, tenant, subject, policy_version), Runtime Denial and Escalation via ARAP (MUST), Local-Action Boundary requiring AuthZEN Access Evaluation for non-OAuth actions, Parameter Binding / TOCTOU Protection (parameter_digest bound to the permit), Decision Evidence Records (per-decision audit record bound to mission.id, proposal_hash, policy_version, decision, constraint clauses, act chain). Six Optional Modules: Tool Binding Profile, Decision Receipt Profile (W3C VC 2.0), Actor Provenance Profile, Purpose Registry Profile, Attestation Profile (RATS PTV + WIMSE), Policy Projection Profile (Cedar carriage).",
     "https://notes.karlmcguinness.com/notes/mission-bound-oauth-runtime-enforcement-profile/",
     "Architect blog (Karl McGuinness)",
     "37-min read; target I-D name: draft-mcguinness-oauth-mission-bound-runtime-enforcement-profile. Six-class action classification (non-consequential → consequential read → consequential write → irreversible → external commitment → privileged administration) determines PDP-gate requirement and parameter binding. Four PDP deployment modes (AS-hosted, RS-hosted, tenant governance, federated). Goal pair: 'execution continuity' (every in-bounds action succeeds; every out-of-bounds becomes governed Mission Expansion) plus 'proof of authority' (per-decision cryptographic receipts). Acknowledges PDP latency overhead and tool-manifest fracturing as real challenges."),

    ("Authorization Denied Is No Longer Enough (McGuinness, 2 Jun 2026)",
     "The framing post for ARAP. In closed-world authorization, 'decision:false' was the end of the interaction. In open-world agentic systems with runtime discovery, sub-agent delegation, and evolving missions, denial is increasingly the beginning of a governance escalation — and the missing protocol primitive is a 'requestable denial': a deny that names where to ask and binds the request to the exact evaluation it remediates. Why CIBA isn't the answer (CIBA solves authentication freshness; this is about governance state). Why approvals aren't authority (reevaluation against current state, not standing entitlement).",
     "https://notes.karlmcguinness.com/notes/authorization-denied-is-no-longer-enough/",
     "Architect blog (Karl McGuinness)",
     "Confirms that the AuthZEN ARAP profile was adopted as a working group draft in May 2026 — material maturity signal. Useful as the 'why' read alongside the ARAP spec itself. Also positions the work against AARM (Autonomous Action Runtime Management, aarm.dev/spec) which intercepts every agent action and resolves to allow/deny/modify/step-up/defer — ARAP standardizes the deny+escalate boundary at the AuthZEN layer."),

    ("Solving the Identity Crisis for AI Agents (Uber Engineering)",
     "A production engineering post from Uber describing their agent identity architecture: an Agent Registry (workload-to-agent mapping), a SPIRE-backed STS that issues short-lived JWTs with embedded actor chains at P99 below 40ms, an MCP Gateway as policy enforcement point, and an AI Agent Mesh for agent-to-agent communication. A standardized A2A client automates token exchange and chain propagation across agent hops.",
     "https://www.uber.com/us/en/blog/solving-the-agent-identity-crisis/",
     "Industry blog (Uber Engineering)",
     "Published 21 May 2026; six-author post (Mathew, Borole, Huang, Burykin, Goel, Walsh) from Uber's platform engineering team. Architecture aligns with WIMSE workload identity (SPIRE as the credential foundation), RFC 8693 actor-chain propagation, and single-hop short-lived JWTs with audience-scoped claims. One of the few public disclosures of a production-grade agent identity system at hyperscaler scale — a real-world reference point for the corpus's delegation-chain design patterns."),

    ("AI Agent Authentication Gets the Hard Part Right. Authorization Is Still Your Problem. (Rock Cyber Musings)",
     "An analyst article arguing the new IETF agent-auth draft solves authentication via SPIFFE+WIMSE+OAuth but leaves authorization and policy enforcement as an unsolved open problem.",
     "https://www.rockcybermusings.com/p/i-agent-authentication-authorization-gap",
     "Industry analysis blog",
     "Maps the IETF draft against MCP and the Colorado AI Act 'reasonable care' standard; pragmatic implementer perspective."),

    ("Agent Authentication & Delegated Access (Zylos Research, April 2026)",
     "A research-style industry article surveying OAuth flows, scoped tokens, and identity patterns specifically for AI agents, covering OAuth 2.1 baselines and chain-splicing risks.",
     "https://zylos.ai/research/2026-04-11-agent-authentication-delegated-access-oauth-scoped-tokens",
     "Industry research blog",
     "Documents the 'delegation chain splicing' attack against RFC 8693 actor-token chains formally raised on the OAuth WG list in early 2026."),

    ("AuthZEN + Shared Signals Framework Series (Andrew Doering)",
     "A multi-part technical blog walking through how AuthZEN (synchronous PDP/PEP) and SSF/CAEP (asynchronous events) combine into a continuous-authorization loop in real Microsoft Entra/M365 deployments.",
     "https://andrewdoering.org/blog/2026/authzen-shared-signals-framework-part-1-fundamentals/",
     "Industry blog",
     "Documents the 2026 asymmetry where Microsoft Entra is a CAEP transmitter for closed-loop CAE but not an external SSF receiver."),

    ("Just-in-Time Authorization with OpenID SSE and CAEP (The New Stack, Tulshibagwale)",
     "An article from CAEP's original inventor explaining how SSE+CAEP enable just-in-time authorization decisions instead of long-lived session-based access.",
     "https://thenewstack.io/just-in-time-authorization-with-openid-sse-and-caep/",
     "Industry article (The New Stack)",
     "Background piece by Atul Tulshibagwale (SGNL CTO, CAEP inventor) explaining the architectural intent."),

    ("How AuthZEN, Shared Signals & CAEP Complement Each Other (OpenID Foundation)",
     "An OpenID Foundation explainer arguing that AuthZEN and SSF/CAEP are complementary — sync access decisions vs async session updates — not competing standards.",
     "https://openid.net/how-authzen-and-shared-signals-caep-complement-each-other/",
     "OpenID Foundation",
     "Useful when explaining the layering to stakeholders confused by the OpenID alphabet soup."),

    ("OAuth 2.1 Features You Can't Ignore in 2026 (Gutierrez, Medium)",
     "A practitioner article summarizing why OAuth 2.1 — mandated PKCE, exact redirect matching, sender-constrained tokens — is the 2026 minimum bar for delegated authorization.",
     "https://rgutierrez2004.medium.com/oauth-2-1-features-you-cant-ignore-in-2026-a15f852cb723",
     "Industry blog (Medium)",
     "Author is Cyber Intelligence Lead — IAM/AI at Oracle; concise piece suitable for executive briefings."),

    ("RFC 9396: OAuth 2.0 Rich Authorization Requests (CIAM Weekly)",
     "A practitioner deep-dive on RAR explaining why scopes alone don't carry transaction-level intent and how authorization_details is being adopted in payments and verifiable credentials.",
     "https://ciamweekly.substack.com/p/rfc-9396-oauth-20-rich-authorization",
     "Industry newsletter",
     "Captures the current (March 2026) state of RAR adoption, including CAMARA telco APIs and DPV-purpose binding proposals."),

    ("Technical Deconstruction of MCP Authorization (kane.mx, Nov 2025)",
     "A long-form technical article showing that the Model Context Protocol's authorization spec is, in practice, an OAuth 2.1 profile combined with RFC 9728 protected-resource metadata and RFC 7591 dynamic registration.",
     "https://kane.mx/posts/2025/mcp-authorization-oauth-rfc-deep-dive/",
     "Independent technical blog",
     "Calls out RFC 8707 (Resource Indicators) as the critical compatibility bottleneck since most major IdPs use proprietary audience parameters."),

    ("AI Agents Authentication: How Autonomous Systems Prove Identity (GitGuardian)",
     "A GitGuardian engineering article arguing that delegated, short-lived OAuth grants are structurally safer than the static API keys that produced 28.65M secret leaks in 2025.",
     "https://blog.gitguardian.com/ai-agents-authentication-how-autonomous-systems-prove-identity/",
     "Industry blog (GitGuardian)",
     "Useful for the 'why delegated authorization > shared secrets' business case with concrete 2025 incident data."),

    ("Workload Identity – Key Takeaways from IETF 122 (Defakto)",
     "A practitioner recap of IETF 122 covering the WIMSE Workload Identity Token, Credential Exchange, and side-meeting work on bot/agent web authentication.",
     "https://www.defakto.security/blog/workload-identity-key-takeaways-from-ietf-122/",
     "Industry blog (Defakto)",
     "Author Pieter Kasselman is co-author of multiple key drafts (Transaction Tokens, First-Party Apps); strong primary-source view."),

    ("User-Managed Access (UMA) 2.0 Comprehensive Guide (SSOJet, Feb 2026)",
     "A 2026 industry guide reframing UMA 2.0 for current CIAM contexts, covering resource-set registration, permission tickets, requesting-party tokens (RPTs), and policy externalization gains.",
     "https://ssojet.com/blog/user-managed-access-uma-2-0-comprehensive-guide",
     "Industry blog (SSOJet)",
     "Cites Kantara analysis showing centralized-policy moves can cut authorization code 80% — useful pitch material."),

    ("Decentralized Identity and Verifiable Credentials: The Enterprise Playbook 2026",
     "An enterprise-oriented guide explaining how W3C VCs, DIDs, and OpenID4VC enable the issuer-holder-verifier delegation model for digital credentials and EUDI Wallet acceptance.",
     "https://securityboulevard.com/2026/03/decentralized-identity-and-verifiable-credentials-the-enterprise-playbook-2026/",
     "Industry article (Security Boulevard)",
     "Critical 2027 EU compliance dates: banks, telecom, healthcare, and very-large platforms must accept EUDI Wallet."),

    ("OAuth 2.0 & OpenID Connect: The Complete Guide to What the Standards Actually Say (Patil, Medium)",
     "A practitioner-friendly synthesis covering OAuth 2.0 core, the OAuth 2.1 draft, RFC 9068 JWT access tokens, RFC 8252 native apps, and RFC 8628 device authorization.",
     "https://mrutyunjaypatil.medium.com/oauth-2-0-openid-connect-the-complete-guide-to-what-the-standards-actually-say-e92f040a4251",
     "Industry blog (Medium)",
     "Good handoff document for engineers new to the area; cites the current standards rather than legacy patterns."),

    ("LinkedIn Engineering — OpenID Connect Authentication for Sign In with LinkedIn V2",
     "LinkedIn's own engineering write-up on adopting OpenID Connect on top of OAuth 2.0, explicitly distinguishing OAuth's delegated-access role from OIDC's identity-assertion role.",
     "https://www.linkedin.com/developers/news/featured-updates/openid-connect-authentication",
     "Industry (LinkedIn Engineering)",
     "Real-world example from LinkedIn explaining why they layered OIDC over an existing OAuth 2.0 delegated-access stack."),

    ("Rich Authorization Requests (RAR) — Authlete Knowledge Base",
     "A vendor knowledge-base article giving worked examples of RAR's authorization_details object, including locations, actions, datatypes, and identifier fields with their Authlete bindings.",
     "https://www.authlete.com/kb/oauth-and-openid-connect/authorization-requests/rich-authorization-requests/",
     "Vendor documentation (Authlete)",
     "Authlete is one of the few certified FAPI 2.0 + RAR implementations; useful reference for concrete request bodies."),

    ("An Introduction to Authorization Exchange (AuthZEN) — Curity",
     "A vendor explainer comparing externalized-authorization patterns (OPA, Cedar, XACML, Zanzibar) and showing how AuthZEN's API normalizes the PDP/PEP wire protocol across them.",
     "https://curity.io/resources/learn/authzen/",
     "Vendor blog (Curity)",
     "Curity is a member of the AuthZEN WG; positions AuthZEN as 'OpenID Connect for authorization' which has become the common framing."),
]
make_sheet("Industry & Implementations", COLORS['Industry'], industry_rows)

# ============================================================
# Index tab
# ============================================================
ws_idx = wb.create_sheet("Index", 0)
fill = PatternFill('solid', start_color=COLORS['Summary'])
ws_idx['A1'] = "Delegated Authorization Research — Index"
ws_idx['A1'].font = Font(name='Arial', size=14, bold=True)
ws_idx.merge_cells('A1:D1')

ws_idx['A2'] = "Research compiled May 2026. Sources separated by maturity so it's clear where active work is happening."
ws_idx['A2'].font = Font(name='Arial', size=10, italic=True, color='595959')
ws_idx.merge_cells('A2:D2')

hdr = ["Tab", "What's in it", "Count", "Where the action is"]
for col, h in enumerate(hdr, 1):
    c = ws_idx.cell(row=4, column=col, value=h)
    c.font, c.fill, c.alignment, c.border = HEADER_FONT, fill, HEADER_ALIGN, BORDER

idx_data = [
    ("Published RFCs", "Settled IETF standards-track and BCP RFCs — the foundation everything else builds on.",
     len(rfc_rows), "Stable. These are the primitives, not where the debate is."),
    ("Active IETF Drafts", "IETF WG charters, requirements drafts, and active WG/individual drafts — including the OAuth WG recharter formally adding 'Complex Delegation' for agents and a six-draft McGuinness individual-submission cluster.",
     len(draft_rows), "★ THIS IS WHERE THE CURRENT WORK IS HAPPENING ★  OAuth recharter on 4 Jun 2026 IESG telechat."),
    ("OpenID Foundation", "Final and draft OIDF specs and the Oct 2025 Agentic AI whitepaper: AuthZEN (incl. the new ARAP profile), Shared Signals/CAEP, FAPI 2.0, HEART.",
     len(oidf_rows), "Mostly Final. AuthZEN Access Request & Approval Profile (ARAP) was adopted as a WG draft May 2026, Draft 1 published 3 Jun 2026."),
    ("Other Standards & Govt", "Kantara UMA 2.0, W3C VCs, NIST AI initiative, EU AI Act compliance dates.",
     len(other_rows), "VC v2.1 First Public Working Draft is the active piece."),
    ("Academic Papers", "arXiv preprints and IEEE conference papers on delegated authz and workload identity.",
     len(academic_rows), "Mostly settled; the 2025 South et al. paper is the most-cited foundation."),
    ("Industry & Implementations", "Vendor blogs, LinkedIn-style articles, reference implementations (OVID/OVID-ME, ZeroID, WorkOS auth.md, Agent Trust Protocol), and the McGuinness Mission-Bound OAuth blog series.",
     len(industry_rows), "Practitioner content; the five implementations at the top of the tab show what an implementable agent-delegation stack looks like today. The four McGuinness Mission-Bound OAuth posts (May–Jun 2026) form a coherent architectural argument."),
]

for i, (tab, what, count, action) in enumerate(idx_data, start=5):
    ws_idx.cell(row=i, column=1, value=tab).font = Font(name='Arial', size=10, bold=True)
    ws_idx.cell(row=i, column=2, value=what).font = BODY_FONT
    ws_idx.cell(row=i, column=3, value=count).font = BODY_FONT
    ws_idx.cell(row=i, column=4, value=action).font = BODY_FONT
    for col in range(1, 5):
        cell = ws_idx.cell(row=i, column=col)
        cell.alignment = BODY_ALIGN
        cell.border = BORDER

total_row = 5 + len(idx_data)
total_count = sum(count for _, _, count, _ in idx_data)
ws_idx.cell(row=total_row, column=1, value="TOTAL").font = Font(name='Arial', size=10, bold=True)
ws_idx.cell(row=total_row, column=3, value=total_count).font = Font(name='Arial', size=10, bold=True)
for col in range(1, 5):
    ws_idx.cell(row=total_row, column=col).border = BORDER

ws_idx.column_dimensions['A'].width = 30
ws_idx.column_dimensions['B'].width = 70
ws_idx.column_dimensions['C'].width = 8
ws_idx.column_dimensions['D'].width = 60
ws_idx.row_dimensions[1].height = 22
ws_idx.row_dimensions[4].height = 30

wb.save('/Users/gffletch/Develop/Authorization/da_research/delegated_authorization_research.xlsx')
print("OK - workbook saved")
print(f"Tab counts: RFCs={len(rfc_rows)}, Drafts={len(draft_rows)}, OIDF={len(oidf_rows)}, Other={len(other_rows)}, Academic={len(academic_rows)}, Industry={len(industry_rows)}")
print(f"Total: {len(rfc_rows)+len(draft_rows)+len(oidf_rows)+len(other_rows)+len(academic_rows)+len(industry_rows)}")

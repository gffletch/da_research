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
    'Mission':   'B65C1E',
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
    ("RFC 10017 — OAuth 2.0 for Browser-Based Applications",
     "An IETF BCP establishing the Backend-for-Frontend (BFF) and other architectural patterns as current best practice for SPAs given browser-resident token-storage limitations.",
     "https://www.rfc-editor.org/rfc/rfc10017",
     "IETF (OAuth WG)",
     "Published as RFC 10017 on 21 Aug 2026, from draft-ietf-oauth-browser-based-apps -27. Moved here from the Active IETF Drafts tab on 26 Aug 2026. **Peripheral to delegated authorization** — tracked for OAuth WG completeness rather than for agent delegation, which is the maintainer's own framing. Still relevant to any delegated-authorization design touching SPAs, since it codifies why pure-browser refresh tokens are deprecated. A 26 Aug 2026 audit of all 251 tracked Datatracker drafts confirmed this is the only one that has reached RFC status."),

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

    ("draft-nottingham-webbotauth-use-cases — Use Cases for Authentication of Web Bots",
     "Frames the key questions for WebBotAuth WG scope: what sites need (mitigating bot abuse, access control for human-gated content), what bot operators need (IP mobility, non-IP-based identity), and the tension between them when a bot operator wants to be recognized but not tracked.",
     "https://datatracker.ietf.org/doc/draft-nottingham-webbotauth-use-cases/",
     "IETF (WebBotAuth WG)",
     "Revision -02, Apr 2026; author: Mark Nottingham (Melbourne). The foundational use-case framing for the WG; scopes out the design space that the registry, httpsig-protocol, and anonymous-auth drafts are responding to."),

    ("draft-meunier-webbotauth-registry — Registry and Signature Agent Card for Web Bot Auth",
     "Defines the 'Signature Agent Card,' a JSON metadata document enabling bots to publish their identity, capabilities, and public keys; establishes a IANA registry drawing from OAuth client metadata extended with bot-specific fields including crawl-rate declarations and data-use purpose.",
     "https://datatracker.ietf.org/doc/draft-meunier-webbotauth-registry/",
     "IETF (WebBotAuth WG)",
     "Revision -03, Jun 26 2026 (most mature WG document); authors: Maxime Guerreiro, Thibault Meunier (Cloudflare), Ulas Kirazci (Amazon). The Agent Card is the identity artifact that the httpsig-protocol references; together they form the core WebBotAuth authentication architecture."),

    ("draft-meunier-webbotauth-httpsig-protocol — HTTP Message Signatures for Automated Traffic",
     "Defines the core WebBotAuth authentication architecture: automated agents sign HTTP requests with private keys bound to their Agent Card; origin servers verify agent identity through public key discovery via the registry. Intended to replace IP allowlisting and User-Agent string matching as the primary bot identification mechanism.",
     "https://datatracker.ietf.org/doc/draft-meunier-webbotauth-httpsig-protocol/",
     "IETF (WebBotAuth WG)",
     "Revision -02, 19 Aug 2026 (was -01, 6 Aug 2026) (was -00, Jun 26 2026); authors: Thibault Meunier (Cloudflare), Sandor Major (Google). Replaces draft-meunier-web-bot-auth-architecture. Pairs with draft-meunier-webbotauth-httpsig-directory for key discovery. **SUPERSEDES draft-meunier-webbotauth-httpsig-directory**, which Datatracker marks Replaced by this draft. That older row was removed from the corpus on 26 Aug 2026 — it was tracked separately and had become a duplicate of this one under the pre-rename slug."),


    ("draft-rescorla-anonymous-webbotauth — Anonymous Bot Authentication: Authorization and Rate Limiting for Web Agents",
     "Proposes Anonymous Bot Authentication (ABA) using Privacy Pass tokens and Anonymous Rate-Limited Credentials, enabling sites to enforce rate limits and access controls on bots without identifying individual operators. Decouples 'is this a legitimate bot' from 'which bot is this,' preserving privacy while preventing abuse.",
     "https://datatracker.ietf.org/doc/draft-rescorla-anonymous-webbotauth/",
     "IETF (WebBotAuth WG)",
     "Revision -00, Apr 7 2026; authors: Eric Rescorla (Independent), Richard L. Barnes (Cisco). Proposes the privacy-preserving counterpart to the httpsig identity approach — the WG will need to decide where the identity/anonymity balance lies."),

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

    ("draft-farrel-dawn-terminology — Terminology for the Discovery of Agents, Workloads, and Named Entities (DAWN)",
     "Establishes standardized vocabulary across DAWN specifications: agents, workloads, named entities, capabilities, discovery processes, and registration functions. Defines the entities-to-be-discovered and the properties discovery must convey, without specifying protocol mechanics.",
     "https://datatracker.ietf.org/doc/draft-farrel-dawn-terminology/",
     "IETF (individual)",
     "Revision -04, Jul 26 2026; authors: Adrian Farrel (Old Dog Consulting), Kehan Yao (China Mobile), Roland Schott (Deutsche Telekom), Nic Williams (Infoblox). Updated immediately ahead of IETF 126 DAWN BoF. At rev 04 the most mature DAWN document after the requirements draft; Farrel/Williams authorship signals serious WG momentum."),

    ("draft-akhavain-moussa-dawn-problem-statement — Problem Statement for the Discovery of Agents, Workloads, and Named Entities (DAWN)",
     "Articulates cross-domain discovery challenges for the DAWN problem space: scalability across administrative boundaries, trust in discovered information, and the absence of a unified discovery model for heterogeneous AI agents and workloads. Establishes functional requirements that protocol proposals must satisfy.",
     "https://datatracker.ietf.org/doc/draft-akhavain-moussa-dawn-problem-statement/",
     "IETF (individual)",
     "Revision -05, Jul 19 2026; authors: Arashmid Akhavain, Hesham Moussa (Huawei Canada), Daniel King (Old Dog Consulting). King co-authorship ties this to draft-king-dawn-requirements already in corpus; together they are the two foundational DAWN framing documents. Updated ahead of IETF 126 DAWN BoF."),

    ("draft-moussa-dawn-gap-analysis — Gap Analysis and Applicability Statement for Discovery Protocols of DAWN",
     "Evaluates DNS, mDNS/DNS-SD, SSDP/UPnP, and other existing discovery protocols against DAWN requirements, identifying security gaps (no agent-specific trust model), privacy gaps (broadcast exposure), and applicability limits (local-scope vs. global cross-domain scenarios); proposes hybrid patterns and mitigations.",
     "https://datatracker.ietf.org/doc/draft-moussa-dawn-gap-analysis/",
     "IETF (individual)",
     "Revision -01, Jun 12 2026; authors: Hesham Moussa, Arashmid Akhavain (Huawei Canada). Directly informs which existing protocol building blocks DAWN can reuse vs. what must be specified fresh. Key input for understanding why a new WG is needed rather than profiling DNS or mDNS."),

    ("draft-jimenez-dawn-discovery-landscape — A Survey of AI Agent Discovery Mechanisms",
     "Surveys discovery mechanisms across standardization bodies and open-source projects (MCP, A2A, robots.txt, Well-Known URIs, registry services), comparing approaches by model, scope, and semantic capability, and identifying remaining standardization gaps that DAWN must address.",
     "https://datatracker.ietf.org/doc/draft-jimenez-dawn-discovery-landscape/",
     "IETF (individual)",
     "Revision -00, Jul 3 2026; authors: Jaime Jimenez, Jim Feng, Jari Arkko, Mirja Kühlewind, Rajat Kandoi (all Ericsson). Kühlewind co-authorship (same as kuehlewind-audit-architecture in corpus) is notable — the audit architecture team is tracking the discovery space. Useful as the landscape reference for the boundaries analysis."),

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
     "Revision -17, Jul 22 2026 — rapid iteration signal heading into IETF 126. IESG-approved and in the RFC Editor queue (rfceditor state 'In Progress', IANA actions acknowledged); still no RFC number assigned as of 21 Aug 2026. The canonical multi-domain delegation pattern referenced by most agent and zero-trust drafts."),

    ("draft-ietf-oauth-identity-assertion-authz-grant — Identity Assertion JWT Authorization Grant (ID-JAG)",
     "An IETF WG draft (Parecki/McGuinness/Campbell) defining how an app uses an identity assertion to obtain an access token for a third-party API by coordinating through a shared enterprise IdP.",
     "https://datatracker.ietf.org/doc/draft-ietf-oauth-identity-assertion-authz-grant/",
     "IETF (OAuth WG)",
     "Revision -03, April 2026; the cross-IdP SSO-to-API bridge that the McGuinness Actor Profile draft layers on top of, and that WorkOS's auth.md uses as one of its three discovery flows."),

    ("draft-sharma-oauth-identity-propagation-context — Identity Propagation Context for Multi-Hop Delegation in OAuth 2.0",
     "Defines a signed JSON Identity Propagation Context (IPC) that carries per-hop cryptographic re-signing of delegation chain metadata at trust boundaries, complementing RFC 8693 Token Exchange by enabling identity propagation through multi-service chains without requiring a Security Token Service interaction at every hop.",
     "https://datatracker.ietf.org/doc/draft-sharma-oauth-identity-propagation-context/",
     "IETF (individual)",
     "Revision -01, Jul 23 2026 (first filed -00 Jul 23 2026); author: Sharma. Cluster B (cross-domain identity chaining) companion to draft-ietf-oauth-identity-chaining. HTTP, gRPC, and Kafka protocol bindings specified — the first explicit event-streaming protocol binding in this family. The per-hop re-signing model is a structural alternative to token-based chains, trading token bloat for per-hop cryptographic commitment."),

    ("draft-ietf-oauth-transaction-tokens — Transaction Tokens (Txn-Tokens)",
     "An IETF WG draft defining short-lived signed JWTs that propagate immutable user identity and authorization context through internal call chains within a trust domain.",
     "https://datatracker.ietf.org/doc/draft-ietf-oauth-transaction-tokens/",
     "IETF (OAuth WG)",
     "Revision -11, 4 Aug 2026 (was -09, published 6 Jul 2026 (was -08 Mar 2026)); co-authored by Tulshibagwale (CAEP inventor), Fletcher, and Kasselman. -09 reorganized the Request Context section, changed JWT body claims from OPTIONAL to RECOMMENDED, and enhanced security considerations for invalidated access tokens. Advanced past WGLC: as of 21 Aug 2026 the stream state is 'WG Consensus: Waiting for Write-Up'. IESG submission milestone Dec 2026, and Transaction Tokens is one of only three active OAuth WG milestones under the approved rev-06 charter."),

    ("draft-ietf-oauth-first-party-apps — OAuth 2.0 for First-Party Applications",
     "An IETF WG draft defining an Authorization Challenge Endpoint that lets first-party native apps drive a browserless OAuth flow while still supporting step-up authentication via RFC 9470.",
     "https://datatracker.ietf.org/doc/draft-ietf-oauth-first-party-apps/",
     "IETF (OAuth WG)",
     "Revision -04, published 1 Jul 2026; explicitly excluded for third-party use because it requires high AS↔client trust."),

    ("draft-ietf-oauth-attestation-based-client-auth — OAuth 2.0 Attestation-Based Client Authentication",
     "An IETF WG draft (Looker/Bastian/Bormann) introducing two JWTs — a Client Attestation issued by a Client Attester and a Client Attestation PoP signed by the client instance — that travel in HTTP headers to let traditionally-public clients authenticate to the AS without a shared secret.",
     "https://datatracker.ietf.org/doc/draft-ietf-oauth-attestation-based-client-auth/",
     "IETF (OAuth WG)",
     "Revision -10, Jul 2026 (was -08 Mar 2026). -10 added a 'client_attestation_pop_methods_supported' metadata parameter, created a new 'OAuth Client Attestation Proof-of-Possession Methods' registry, clarified that PoP mechanisms from other specs are permitted, and refined DPoP combined-mode handling. Relates to the RATS Passport Model per RFC 9334; RATS attestation procedures themselves are deliberately out of scope. The 'client instance' framing pairs naturally with the McGuinness Client Instance Assertion and AI Agent Instance drafts."),

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

    ("draft-ietf-oauth-security-topics-update — Updates to OAuth 2.0 Security BCP",
     "An IETF WG draft that extends RFC 9700 with new countermeasures, notably rules against audience-injection attacks where a client authenticates to multiple authorization servers.",
     "https://datatracker.ietf.org/doc/draft-ietf-oauth-security-topics-update/",
     "IETF (OAuth WG)",
     "Revision -01, March 2026; co-authored by University of Stuttgart (FAPI formal-analysis team) so the recommendations are formally grounded."),

    ("draft-ietf-oauth-client-id-metadata-document — OAuth Client ID Metadata Document",
     "Defines a mechanism for OAuth clients to identify themselves to authorization servers via a URL as the client_id, pointing to a published JSON document containing client metadata — enabling dynamic client identification without prior registration.",
     "https://datatracker.ietf.org/doc/draft-ietf-oauth-client-id-metadata-document/",
     "IETF (OAuth WG)",
     "Revision -02, Jul 2026; OAuth WG-adopted. Directly relevant to AI agent deployments where agents may be registered via discoverable metadata documents rather than static registrations. Complements draft-king-dawn-requirements (discovery layer) by providing the OAuth-layer registration artifact."),

    ("draft-ietf-oauth-refresh-token-expiration — OAuth 2.0 Refresh Token and Authorization Expiration",
     "Extends OAuth 2.0 with new token endpoint response parameters specifying refresh token expiration and user authorization expiration, making expiry semantics explicit and interoperable across implementations.",
     "https://datatracker.ietf.org/doc/draft-ietf-oauth-refresh-token-expiration/",
     "IETF (OAuth WG)",
     "Revision -03, Jul 2026; OAuth WG-adopted. Relevant to long-running agent sessions: explicit authorization expiration addresses the gap where refresh tokens survive past the user's intended authorization window — a known risk in agentic delegation scenarios."),

    ("draft-mcguinness-oauth-actor-profile — OAuth Actor Profile for Delegation",
     "Karl McGuinness's individual draft profiling the RFC 8693 'act' claim with required iss, optional sub_profile entity classification, and uniform processing across JWT assertion grants, JWT access tokens, and Transaction Tokens.",
     "https://datatracker.ietf.org/doc/html/draft-mcguinness-oauth-actor-profile-00",
     "IETF (individual)",
     "Revision -00 published 30 April 2026; defines depth-1+ chain validation, cycle-aware construction, and bearer-to-PoP upgrade — the most complete actor-representation profile to date."),

    ("draft-mw-oauth-actor-chain — Cryptographically Verifiable Actor Chains for OAuth 2.0 Token Exchange",
     "An IETF individual draft (Prasad/Krishnan/Lopez/Addepalli) defining six actor-chain profiles for RFC 8693 — Declared/Verified × Full/Subset/Actor-Only Disclosure — that preserve and cryptographically validate delegation-path continuity across successive token exchanges instead of relying on RFC 8693's informational-only nested act claims.",
     "https://datatracker.ietf.org/doc/draft-mw-oauth-actor-chain/",
     "IETF (individual)",
     "Revision -01, 30 Jun 2026 (was -00 May 2026; re-slugged from draft-mw-spice-actor-chain-05); a complementary alternative to the McGuinness Actor Profile that directly addresses RFC 8693's chain-splicing weakness by making the chain itself cryptographically verifiable rather than just informational."),

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
     "https://datatracker.ietf.org/doc/draft-mcguinness-oauth-actor-receipts/",
     "IETF (individual)",
     "Revision -00, 4 Jul 2026; now formally on IETF Datatracker (was GitHub-only pre-publication through Jun 2026). Recommended companion to the Actor Profile when a deployment needs Verified Full Disclosure mode (per the Mission-Bound OAuth Runtime Enforcement Profile's Actor Provenance Module). Completes a triad with actor-profile and actor-proofs — receipts provide provenance, proofs provide cryptographic per-hop accountability."),

    ("draft-mcguinness-oauth-actor-proofs — OAuth Actor-Signed Hop Proofs",
     "Introduces the 'actor_proofs' claim — a signed per-hop proof chain where each actor signs its own participation and the target binding it authorized for that hop; proofs are hash-chained and validated using actor verification keys from trusted sources, with optional references to sibling actor receipts.",
     "https://datatracker.ietf.org/doc/draft-mcguinness-oauth-actor-proofs/",
     "IETF (individual)",
     "Revision -00, 4 Jul 2026. Completes the actor triad with actor-profile (chain structure) and actor-receipts (provenance) — actor-proofs closes the cryptographic accountability gap. Filed the same day as ai-agent-instance, id-assertion-framework, and domain-authorized-issuer — McGuinness submitted four new I-Ds on Jul 4-6, bringing his total to 11 individual I-Ds on Datatracker."),

    ("draft-mcguinness-oauth-insufficient-claims — OAuth 2.0 Insufficient Claims Challenge",
     "A McGuinness individual draft defining an insufficient_claims error code and required_claims parameter enabling authorization servers and protected resources to signal precisely which claims are missing from a presented credential. Allows resource servers to request enriched credentials carrying specific missing attributes rather than returning a generic 401.",
     "https://datatracker.ietf.org/doc/draft-mcguinness-oauth-insufficient-claims/",
     "IETF (individual)",
     "Revision -00, 27 May 2026. Enables just-in-time claim negotiation in multi-agent delegation chains where the acting party must assemble claims from multiple sources. Natural companion to the Actor Profile and Client Instance Assertion — those drafts define the identity structure; this one provides the feedback loop when that structure is incomplete at the RS."),

    ("draft-mcguinness-oauth-ai-agent-instance — OAuth 2.0 AI Agent Instance Profile",
     "Profiles OAuth 2.0 for deployments where a single client ID represents an agent platform running many concurrent agent instances; defines claims conveying attested agent instance identity and provenance from an agent attester to the AS, with delegation-chain semantics for sub-agents. Claims are carrier-independent, compatible with both Client Instance Assertions and Client Attestation JWT.",
     "https://datatracker.ietf.org/doc/draft-mcguinness-oauth-ai-agent-instance/",
     "IETF (individual)",
     "Revision -00, 4 Jul 2026. Fills the gap between a registered OAuth client ID (platform-level) and a running agent instance (runtime-level) — the level at which delegation chains, attestation, and revocation actually operate. Companion to draft-mcguinness-oauth-client-instance-assertion (general instance framing) and draft-mcguinness-oauth-actor-profile (chain representation)."),

    ("draft-mcguinness-oauth-id-assertion-framework — OAuth Identity Assertion Trust Framework",
     "Addresses the gap where issuer authentication alone does not prove AS authority over subject namespaces; defines an Authority Delegation Model with independent trust-evaluation categories and an Identity Assertion Issuer Trust Policy (JSON document declaring required trust methods) that Resource ASes evaluate before accepting identity assertions.",
     "https://datatracker.ietf.org/doc/draft-mcguinness-oauth-id-assertion-framework/",
     "IETF (individual)",
     "Revision -00, 4 Jul 2026. Directly motivates and companions draft-mcguinness-oauth-domain-authorized-issuer (below) which provides a DNS-based trust method. Addresses the 'who is allowed to assert identities in this namespace?' question that ID-JAG and the identity-chaining WG draft assume resolved but do not specify."),

    ("draft-mcguinness-oauth-domain-authorized-issuer — OAuth Domain-Authorized Issuer Trust Method",
     "DNS domain owners publish a policy (DNS TXT record at _oauth-issuer-policy.{domain} or HTTPS well-known fallback) listing the OAuth ASes authorized to assert identities in that namespace; Resource ASes use this to validate assertion issuers before accepting identity assertions or chaining tokens. Pattern echoes CAA/SPF/DKIM. Non-transitive — flat authorization, no delegation chains.",
     "https://datatracker.ietf.org/doc/draft-mcguinness-oauth-domain-authorized-issuer/",
     "IETF (individual)",
     "Revision -00, 4 Jul 2026. Implements one trust method for draft-mcguinness-oauth-id-assertion-framework. DNS-based approach is lightweight and operationally familiar; the non-transitive design avoids the amplification risks of transitive trust chains. Closes the 'how do you know the AS is allowed to speak for this domain?' gap that cross-domain identity chaining has always assumed away."),

    ("draft-mcguinness-oauth-mission — Mission-Bound Authorization for OAuth 2.0",
     "Introduces 'Mission' — a durable, integrity-bound artifact stored at the AS representing an approved task; clients submit Mission Intent via PAR, ASes derive concrete permissions, and approvers grant consent via integrity anchors. Access tokens carry a 'mission' claim; issuance is gated by the Mission's lifecycle state, enabling revocation governance and audit trails for multi-step agent operations.",
     "https://datatracker.ietf.org/doc/draft-mcguinness-oauth-mission/",
     "IETF (individual)",
     "Revision -00, 6 Jul 2026. This is the formal I-D target for the 'Mission-Bound OAuth MVP' blog post (May 2026, Industry tab) — the five-wire-addition protocol that makes the user-approved task a first-class OAuth object. Paired with the runtime enforcement profile (still not on Datatracker as of Jul 10). The Mission lifecycle (pending_approval → active → suspended → revoked → expired → completed → rejected) and the proposal_hash/consent_rendering_hash binding anchor what was approved versus what the user saw."),

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
     "Revision -03, 6 Jul 2026 (was -00, March 2026); introduces 'Agent Identity Management System (AIMS)' and is the cleanest standards-based framing of agent-as-workload."),

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
     "Revision -01, 19 Aug 2026 (was -00, 27 March 2026); technically strong — Biscuit + Datalog is well-suited to scope attenuation. The 'AIP' name collision with draft-singla-agent-identity-protocol and draft-aip-agent-identity-protocol is a blocking issue for WG adoption."),

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

    ("draft-sharif-x509-agent-identity-profile — X.509 Certificate Profile for Autonomous AI Agent Identity",
     "Defines a new X.509v3 AgentIdentity extension encoding graduated trust levels (0–4), operational capabilities, delegation constraints, and revocation endpoints for autonomous AI agent certificates. Maintains backward compatibility with standard X.509v3 parsers (extension marked non-critical) and integrates with SPIFFE workload identity frameworks.",
     "https://datatracker.ietf.org/doc/draft-sharif-x509-agent-identity-profile/",
     "IETF (individual)",
     "Revision -03, 31 Jul 2026 (was -02, Jul 26 2026 (first filed Jul 20 2026)); part of the Sharif cluster. Fills the PKI-layer identity gap that draft-ietf-wimse-workload-creds left open — workload-creds specifies credential issuance, this profiles X.509v3 for the agent-specific certificate case. Graduated trust taxonomy (0–4) and kill-switch revocation are referenced by draft-sweeney-wimse-credential-delegation."),

    ("draft-aip-agent-identity-protocol — AIP: Agentic Authentication and Authorized Policy Enforcement",
     "An IETF individual draft defining an AIP Token signed per tool call (agent ID, tool, nonce, timestamp, signature), an AgentPolicy YAML format for per-tool argument constraints and DLP rules, and a Human-in-the-Loop proxy enforcement model.",
     "https://datatracker.ietf.org/doc/draft-aip-agent-identity-protocol/",
     "IETF (individual)",
     "Revision -00, 16 March 2026; implementation-focused. YAML policy approach is pragmatic but not interoperable-by-design. HITL integration is a valuable safety feature. Third member of the 'AIP' name-collision triple — must be resolved before any can progress."),

    ("draft-liu-oauth-chain-delegation — Delegation Chain for OAuth 2.0",
     "Introduces a delegation_chain JWT claim as a structured companion to RFC 8693's act claim; delegation_chain records the complete delegation history as an ordered array with per-hop authorization constraints and optional cryptographic confirmation from each delegating agent. Supports cross-domain delegation with integrated user consent interaction.",
     "https://datatracker.ietf.org/doc/draft-liu-oauth-chain-delegation/",
     "IETF (individual)",
     "Revision -00, 6 Jun 2026; authors: Dapeng Liu, Judy Zhu, Suresh Krishnan (Ericsson), Aaron Parecki (Okta). Provides the structured delegation lineage that act alone cannot express; strong overlap with draft-mw-oauth-actor-chain and draft-niyikiza-oauth-attenuating-agent-tokens — OAuth WG will likely expect consolidation across these three."),

    ("draft-fletcher-transaction-token-chaining-profile — Transaction Token Authorization Grant Profile for OAuth Identity and Authorization Chaining",
     "Establishes a framework for using Transaction Tokens as subject credentials in OAuth 2.0 Token Exchange requests (RFC 8693), enabling services within one trust domain to obtain JWT authorization grants for accessing resources across domain boundaries without exposing internal token formats.",
     "https://datatracker.ietf.org/doc/draft-fletcher-transaction-token-chaining-profile/",
     "IETF (individual)",
     "Revision -02, 6 Jul 2026 (was -01 Jun 2026); authors: George Fletcher (Practical Identity LLC), Pieter Kasselman (Defakto Security), Sean O'Dell (CVS Health). Directly bridges draft-ietf-oauth-transaction-tokens and draft-ietf-oauth-identity-chaining (both in corpus), closing the 'how do TX Tokens actually cross domains' gap. Note: lead author is the corpus maintainer."),

    ("draft-zhu-oauth-async-delegation — Sender-Constrained Delegation Handle for Asynchronous OAuth 2.0 Identity Chaining",
     "Introduces a Delegation Handle — a sender-constrained, audience-locked JWT issued by authorization servers — enabling acting clients to refresh chained access tokens without re-prompting an offline end user while maintaining strict policy bounds and identity chains.",
     "https://datatracker.ietf.org/doc/draft-zhu-oauth-async-delegation/",
     "IETF (individual)",
     "Revision -05, 3 Aug 2026 (was -04, Jul 23 2026 (first filed -00, 22 May 2026)); authors: Larry Zhu, Sam Currie (Atlassian). Addresses a concrete gap in agent delegation: what happens when the delegating human is not present to re-authorize. Directly relevant to long-running agentic workflows using draft-ietf-oauth-identity-chaining. Active revision pace — -04 within ~2 months of initial filing."),

    ("draft-emerson-oauth-user-mediated-delivery — User-Mediated Credential Delivery for AI Agents",
     "Proposes user-mediated credential delivery as a complementary OAuth authorization primitive for AI agent frameworks: rather than delivering credentials through automated channels controlled by the agent or its platform, places the authorization decision and credential delivery step in the user's hands even when the agent is autonomous.",
     "https://datatracker.ietf.org/doc/draft-emerson-oauth-user-mediated-delivery/",
     "IETF (individual)",
     "Revision -00, Jul 2026; author: Matt Emerson. Novel complement to draft-zhu-oauth-async-delegation — where Zhu handles the case of offline delegation continuation, Emerson argues some credential deliveries should always route through the user even in automated pipelines. Addresses prompt-injection and social-engineering risks in agent credential chains."),

    ("draft-gerber-oauth-deferred-token-response — Deferred Token Response",
     "Defines an OAuth 2.1 extension enabling authorization servers to defer access-token issuance by returning a deferral code the client polls or receives via callback; designed for use cases including fraud review, identity verification, autonomous agent approvals, and enterprise governance workflows where immediate token issuance is not appropriate.",
     "https://datatracker.ietf.org/doc/draft-gerber-oauth-deferred-token-response/",
     "IETF (individual)",
     "Revision -00, Jun 23 2026; presented at IETF 126 OAuth WG. May be the closest current Datatracker analog to the still-pending draft-mcguinness-oauth-deferred-code-processing — note in comments if the McGuinness variant eventually files, as the two may need consolidation. The async issuance pattern directly enables human-approval workflows in agentic pipelines without requiring the agent to remain connected while awaiting the authorization decision."),

    ("draft-chen-oauth-agent-revocation — OAuth 2.0 Agent Authorization Explicit Revocation",
     "Extends RFC 7009 token revocation for agent-based scenarios: introduces batch revocation by agent ID, cascading revocation across delegation chains, conditional revocation options, and verifiable audit trails.",
     "https://datatracker.ietf.org/doc/draft-chen-oauth-agent-revocation/",
     "IETF (individual)",
     "Revision -00, 27 Apr 2026; authors: Meiling Chen, Li Su (China Mobile). Fills the lifecycle management gap — existing RFC 7009 revocation is single-token and client-centric, but agent delegation chains require cascade semantics. Natural companion to draft-ietf-oauth-transaction-tokens and draft-niyikiza-oauth-attenuating-agent-tokens."),

    ("draft-jiang-oauth-intent-admission — Intent Admission Assertions for Agentic Systems",
     "Defines a signed, verifiable Intent Admission Assertion (IAA) that an admission point creates after verifying agent identity, evaluating permissions against policy, and — when required — obtaining explicit user consent; the IAA is transmitted to the execution endpoint which re-validates before proceeding. Leverages OAuth and RFC 9396 Rich Authorization Requests.",
     "https://datatracker.ietf.org/doc/draft-jiang-oauth-intent-admission/",
     "IETF (individual)",
     "Revision -00, 23 Jun 2026; authors: Yuning Jiang, Lun Li, Yurong Song, Faye Liu (Huawei). The required_consent path maps directly to the HITL pattern central to the corpus. Companion to draft-jiang-intent-security (threat model) from the same Huawei group."),

    ("draft-ni-oauth-batch-authorization-delegation — Batch Authorization Delegation",
     "Defines a mechanism for delegating a batch of fine-grained, actor-bound permissions in a single request across multiple collaborating actors; uses RFC 9396 RAR to carry per-actor authorization_details and RFC 8693 Token Exchange for sub-agent delegation, targeting multi-agent orchestration where a leader-agent receives batch permissions and delegates subsets to sub-agents.",
     "https://datatracker.ietf.org/doc/draft-ni-oauth-batch-authorization-delegation/",
     "IETF (individual)",
     "Revision -00, 3 Jul 2026; authors: Ni Yuan, Peter Chunchi Liu (Huawei). Addresses the round-trip overhead problem in large-scale multi-agent orchestration — individual delegation exchanges per sub-agent don't scale. Complements draft-song-oauth-ai-agent-collaborate-authz (same Huawei group, coordination focus) and draft-niyikiza-oauth-attenuating-agent-tokens (attenuation semantics). The RAR-based batch approach aligns well with the OAuth WG's RAR investment. **SUPERSEDES draft-ni-batch-authorization-delegation**, which Datatracker marks Replaced by this draft. That older row was removed from the corpus on 26 Aug 2026 — it was tracked separately and had become a duplicate of this one under the pre-rename slug."),

    ("draft-liu-oauth-a2a-profile — Agent-to-Agent (A2A) Profile for OAuth Transaction Tokens",
     "Defines a profile for using OAuth Transaction Tokens in distributed agent-to-agent communication scenarios; specifies mechanisms for embedding call-chain context within tokens to preserve agent identity, authorization information, and operational flow across agent workloads in trusted environments.",
     "https://datatracker.ietf.org/doc/draft-liu-oauth-a2a-profile/",
     "IETF (individual)",
     "EXPIRED. Revision -00, Oct 2025; authors: Peter Chunchi Liu, Ni Yuan (Huawei) — same author pair as draft-ni-oauth-batch-authorization-delegation. Directly profiles draft-ietf-oauth-transaction-tokens for A2A use; overlaps significantly with draft-araut-oauth-transaction-tokens-for-agents. Never revised; likely deferred rather than abandoned given both authors remain active in the corpus through Jul 2026."),

    ("draft-song-oauth-ai-agent-collaborate-authz — OAuth 2.0 Extension for Multi-AI Agent Collaboration",
     "Extends OAuth 2.0 for coordinated multi-agent task groups: defines a collaborative authorization flow allowing a lead agent to obtain delegation tokens for sub-agents, with shared task context, coordinated scope attenuation, and cross-agent session binding.",
     "https://datatracker.ietf.org/doc/draft-song-oauth-ai-agent-collaborate-authz/",
     "IETF (individual)",
     "Revision -02, Jun/Jul 2026; authors: Yurong Song (Huawei) and colleagues. Addresses the multi-agent coordination gap at the OAuth layer — complements draft-jiang-oauth-intent-admission from the same Huawei group. Distinct from single-hop delegation drafts in explicitly modeling lead-agent-to-sub-agent scope sharing."),

    ("draft-kroehl-agentic-trust-aae — Agent Authorization Envelope (AAE)",
     "Specifies the AAE, a structured authorization container with three mandatory components — MANDATE, CONSTRAINTS, and VALIDITY — providing a machine-evaluable, cryptographically verifiable authorization assertion using W3C DIDs and Verifiable Credentials.",
     "https://datatracker.ietf.org/doc/draft-kroehl-agentic-trust-aae/",
     "IETF (individual)",
     "Revision -01, 11 Aug 2026 (was -00, 21 May 2026); author: Lars Kersten Kroehl (CryptoKRI GmbH). Occupies similar design space to draft-mcguinness-oauth-actor-profile but uses a DID/VC substrate rather than OAuth — provides a useful alternative approach for non-OAuth deployments."),

    ("draft-pidlisnyi-aps — Agent Passport System (APS)",
     "Specifies Ed25519-based agent passports, scoped delegation chains with constraints across seven dimensions (a lattice model where delegation monotonically narrows capabilities), cascade revocation, a three-signature policy chain, signed receipts, and MCP bindings; includes reference implementations in TypeScript and Python.",
     "https://datatracker.ietf.org/doc/draft-pidlisnyi-aps/",
     "IETF (individual)",
     "Revision -01, 14 May 2026; author: Tymofii Pidlisnyi (AEOESS). Among the most comprehensive standalone agent authz specs in the wave — the seven-dimension constraint lattice and MCP binding make it directly implementable against Model Context Protocol deployments alongside draft-serra-mcp-discovery-uri."),

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
     "Revision -01, 3 Jun 2026 (was -00, April 2026); regulatory mapping appendices (PSD2, PCI DSS) are notable — one of the few drafts engaging financial regulation directly. Ambitious scope. Part of the Sharif cluster."),

    ("draft-sharif-agent-transport-protocol — Agent Transport Protocol (ATP): Async Store-and-Forward for AI Agents",
     "An IETF individual draft defining async store-and-forward messaging semantics with cryptographic identity per relay hop, trust scoring at ingress, capability negotiation, and interop with Google A2A, MCP, and FIPA ACL; transport-agnostic over TCP/TLS/QUIC.",
     "https://datatracker.ietf.org/doc/draft-sharif-agent-transport-protocol/",
     "IETF (individual)",
     "Revision -00, 28 March 2026; addresses a real gap — most agent protocols assume synchronous availability, and store-and-forward is appropriate for long-running agentic tasks. Scope is broad and needs narrowing."),

    ("draft-sharif-agent-audit-trail — Agent Audit Trail (AAT): Standard Logging Format for Autonomous AI Systems",
     "An IETF individual draft defining a JSON-based audit record with mandatory fields (agent identity, action classification, outcome tracking, trust level) using RFC 8785 JSON Canonicalization and RFC 9562 UUIDs.",
     "https://datatracker.ietf.org/doc/draft-sharif-agent-audit-trail/",
     "IETF (individual)",
     "Revision -01, 19 Aug 2026 (was -00, 29 March 2026); orthogonal to delegation but important for compliance — standardized audit-log format is a genuine gap. Complements identity frameworks well. A sibling/alternative to the Kuehlewind audit architecture which takes a far more ambitious cross-layer approach."),

    ("draft-aiendpoint-ai-discovery — The AI Discovery Endpoint",
     "An IETF individual draft defining a /.well-known/ai URI suffix for programmatic service capability discovery by AI agents — letting agents discover what an endpoint supports without having to parse human-oriented documentation; requests IANA well-known URI registration.",
     "https://datatracker.ietf.org/doc/draft-aiendpoint-ai-discovery/",
     "IETF (individual)",
     "Revision -01, 28 Jul 2026 (was -00, March 2026); complementary to MCP discovery but broader (not MCP-specific). Needs differentiation from OpenAPI/service-description work to gain traction."),

    ("draft-hood-independent-agtp — Agent Transfer Protocol (AGTP)",
     "An IETF individual draft proposing a dedicated application-layer protocol for AI agent traffic on port 4480 (TCP/TLS and QUIC) with an agtp:// URI scheme, arguing that HTTP is insufficient because agent-generated intent-driven traffic is indistinguishable from human-initiated requests. Defines a Runtime Contract Negotiation Substrate (RCNS) with eighteen methods split into cognitive verbs (QUERY, DISCOVER, DESCRIBE, SUMMARIZE, PLAN, PROPOSE) and mechanics verbs (EXECUTE, DELEGATE, ESCALATE, CONFIRM, SUSPEND, NOTIFY), mandatory agent identity headers, and protocol-level authority scope declaration.",
     "https://datatracker.ietf.org/doc/draft-hood-independent-agtp/",
     "IETF (individual)",
     "Revision -09, 28 Jun 2026 (was -08 May 2026); supersedes draft-hood-independent-atp. Companion specs in the same family: AGTP-API, AGTP-CERT, AGTP-MERCHANT, AGTP-IDENTIFIERS, AGTP-TRUST. Mandatory TLS 1.3+. Ambitious scope — a new transport layer rather than an HTTP profile. The cognitive/mechanics verb split is a distinctive design choice; contrasts with draft-sharif-agent-transport-protocol which layers async store-and-forward on top of existing transports rather than replacing them."),

    ("draft-hood-agtp-ard — ARD Binding for AGTP: Agentic Resource Discovery over the Agent Transfer Protocol",
     "Specifies how Agentic Resource Discovery (ARD) composes with AGTP, defining a catalog entry type for ARD manifests, aligning AGTP's identity model with ARD's trustManifest, and providing an AGTP-native binding for publishing ARD catalogs over AGTP substrate rather than HTTPS.",
     "https://datatracker.ietf.org/doc/draft-hood-agtp-ard/",
     "IETF (individual)",
     "Revision -00, 18 Jun 2026; author: Chris Hood (Nomotic). Extends the AGTP family (draft-hood-independent-agtp in corpus). The trustManifest identity alignment is the piece relevant to the agent identity thread; the rest is transport-layer plumbing for AGTP deployments."),

    ("draft-hood-agtp-api — AGTP-API: Verbs, Paths, Endpoints, and Synthesis",
     "Establishes the full application-layer contract for AGTP agent–server interactions: approved method catalog, path grammar, endpoint primitives, semantic metadata blocks, server manifests, and runtime contract negotiation substrate. Defines how agents and servers negotiate capabilities and authority before action methods are invoked.",
     "https://datatracker.ietf.org/doc/draft-hood-agtp-api/",
     "IETF (individual)",
     "Revision -01, May 26 2026; author: Chris Hood (Nomotic). The normative protocol contract layer for AGTP, complementing draft-hood-independent-agtp (transport) and draft-hood-agtp-trust (trust model). The AGTP family now spans 18 drafts; this is the API-layer anchor."),

    ("draft-hood-agtp-trust — AGTP Trust and Verification Specification",
     "Defines AGTP's three-tier trust model (Tier 1 Verified / Tier 2 Org-Asserted / Tier 3 Experimental) and a continuous behavioral trust score (0.0–1.0) used by infrastructure components for runtime trust-aware routing. Standardizes the evidence substrate, score format, freshness requirements, and consumer-side evaluation rules without mandating the scoring algorithm.",
     "https://datatracker.ietf.org/doc/draft-hood-agtp-trust/",
     "IETF (individual)",
     "Revision -02, Jun 28 2026; author: Chris Hood (Nomotic). The continuous 0.0–1.0 trust score model contrasts with draft-sharif-attp's discrete L0–L4 levels and Larry Lewis's atp-core continuous scoring — three independent designs in the same design space."),

    ("draft-hood-agtp-agent-cert — AGTP Agent Certificate Extension",
     "Specifies an X.509 v3 extension that cryptographically binds AGTP agent identity headers to TLS mutual authentication, enabling infrastructure components (Scope-Enforcement Points, load balancers, governance gateways) to verify agent identity at the network layer without application-layer access. Includes session-level revocation via AGTP NOTIFY broadcast.",
     "https://datatracker.ietf.org/doc/draft-hood-agtp-agent-cert/",
     "IETF (individual)",
     "Revision -03, Jun 28 2026; author: Chris Hood (Nomotic). The PKI-binding companion to the AGTP identity model; positions AGTP agent identity within existing X.509 / TLS infrastructure. Relevant to WebBotAuth comparison — both use PKI for bot/agent identity but at different layers."),

    ("draft-jernalczyk-intentweb-agent-manifest — IntentWeb AgentManifest",
     "Defines a JSON document that websites publish to describe identity, trusted knowledge, agent-facing capabilities, structured bindings, risk levels, consent requirements, authentication expectations, audit rules, and policies — enabling AI agents to comprehend website functionality and safely perform actions without scraping or fragile UI automation.",
     "https://datatracker.ietf.org/doc/draft-jernalczyk-intentweb-agent-manifest/",
     "IETF (individual)",
     "Revision -00, 6 Jul 2026; author: Mariusz Jernalczyk (IntentWeb). Website-side complement to agent identity drafts; sits in the Discovery & Transport cluster alongside draft-hood-agtp-ard and the DAWN/.well-known discovery thread. Single author, no-affiliation submission — early stage but addresses a real discovery gap."),

    ("draft-bu-agentproto-security-principal-binding — Security Principal and Verifier Binding for Agent Communication Protocols",
     "Addresses how agent communication protocols carry claims about user authority, agent instance identity, tool or external-resource identity, delegation state, session continuity, and action evidence; each claim has a different verifier, freshness requirement, failure mode, and security consequence, requiring explicit binding rather than collapsing all claims into a single assertion.",
     "https://datatracker.ietf.org/doc/draft-bu-agentproto-security-principal-binding/",
     "IETF (individual)",
     "Revision -06, 17 Aug 2026 (was -05, 9 Aug 2026) (was -02, Jul 2026). Fills a gap in the AGTP family (draft-hood-independent-agtp in corpus) and is relevant to any agent communication protocol carrying mixed-provenance claims. The verifier-separation model is the missing security architecture layer between protocol transport and authorization enforcement."),

    # ---- Individual drafts: Security Requirements / Frameworks cluster ----
    ("draft-fane-opena2a-aap — OpenA2A Agent Authorization Protocol (AAP)",
     "Establishes authorization mechanisms for AI agent systems through cryptographic identity assertions and scoped capability grants. Introduces a broker layer that separates credentials from the agent's reasoning context, specifically to prevent prompt injection attacks from leaking authorization state while enabling cross-agent delegation.",
     "https://datatracker.ietf.org/doc/draft-fane-opena2a-aap/",
     "IETF (individual)",
     "Revision -01, 23 Jul 2026 (first filed -00 Jul 6 2026); author: Abdel Fane (OpenA2A). Companion draft-fane-opena2a-aip has since moved ahead to -02 (6 Aug 2026) while AAP holds at -01, adding a fourth 'AIP' name collision to the existing Singla/Prakash/aip-agent-identity-protocol triple. The AAP authorization layer is the piece most relevant to OAuth boundary analysis."),

    ("draft-ni-a2a-ai-agent-security-requirements — Security Requirements for AI Agents",
     "An IETF individual draft enumerating security requirements for AI agents, covering identity, authorization chaining across domains, and integration points with WIMSE, OAuth identity chaining, and the A2A OAuth profile.",
     "https://datatracker.ietf.org/doc/draft-ni-a2a-ai-agent-security-requirements/",
     "IETF (individual)",
     "Revision -01, February 2026; essential scaffolding for an eventual AI-agent WG. Well-connected to existing IETF work and authored by Ni and Liu, who also lead the WIMSE AI-agent identity draft."),

    ("draft-chapman-a2a-mls — End-to-End Encryption and Purpose-Bound Governance for Agent-to-Agent Messaging",
     "Extends the Agent2Agent (A2A) protocol with message-level E2E confidentiality using MLS (Messaging Layer Security); defines a Governed Object signed message envelope carrying semantic type, payload, purpose declaration, and expiry; mandates receiver-side processing rules enforcing declared purposes and rejecting expired or replayed messages.",
     "https://datatracker.ietf.org/doc/draft-chapman-a2a-mls/",
     "IETF (individual)",
     "Revision -03, 1 Aug 2026 (was -00, Jul 28 2026); author: Chapman. Adds the transport-security and semantic-governance layer the A2A protocol family was missing. MLS binding anchors agent identity to Ed25519 did:key DIDs. The Governed Object envelope's purpose-declaration mechanism directly addresses the intent-drift threat identified in draft-jiang-intent-security (corpus). Likely to be referenced by other A2A family drafts as the baseline confidentiality profile."),

    ("draft-rosenberg-agentproto-usecases — Framework, Use Cases and Requirements for AI Agent Protocols",
     "AI Agents are software applications that utilize Large Language Models (LLM)s to interact with humans (or other AI Agents) for purposes of performing tasks. AI Agents can make use of resources - including APIs and documents - to perform those tasks, and are capable of reasoning about which resources to use. To facilitate AI agent operation, AI agents need to communicate with users, and then interact with other resources over the Internet, including APIs and other AI agents. This document describes a framework for AI Agent communications on the Internet, identifying the various protocols that come into play. It introduces use cases that motivate features and functions that need to be present in those protocols. It also provides a brief survey of existing work in standardizing AI agent protocols, including the Model Context Protocol (MCP), the Agent to Agent Protocol (A2A) and the Agntcy Framework, and describes how those works fit into this framework. The primary objective of this document is to set the stage for possible standards activity at the IETF in this space.",
     "https://datatracker.ietf.org/doc/draft-rosenberg-agentproto-usecases/",
     "IETF (individual)",
     "Revision -00, checked 26 Aug 2026. **Re-slugged: this draft was tracked as draft-rosenberg-aiproto-framework until 26 Aug 2026**, which Datatracker marks Replaced by this one. Row updated to the current name, URL and abstract; the old slug is recorded here so searches for it still land. Previously filed in the corpus as “draft-rosenberg-aiproto-framework — Framework, Use Cases and Requirements for AI Agent Protocols”."),

    ("draft-rosenberg-aiproto-cheq — CHEQ: A Protocol for Confirmation of AI Agent Decisions (HITL)",
     "An IETF individual draft defining an out-of-band Human-in-the-Loop confirmation protocol for agent tool calls, eliminating LLM-hallucination risk for consequential actions and enabling sensitive operations (e.g., banking) without exposing data to the agent.",
     "https://datatracker.ietf.org/doc/draft-rosenberg-aiproto-cheq/",
     "IETF (individual)",
     "Revision -00, October 2025; out-of-band HITL confirmation model is valuable and complements delegation frameworks. Likely expired (April 2026); worth tracking for a -01 refresh. **EXPIRED on Datatracker** (expired 23 Apr 2026; checked 26 Aug 2026) — kept in the corpus deliberately; an expired draft is still evidence of what was proposed."),

    ("draft-sharif-agent-payment-trust — Trust Scoring and Identity Verification for AI Agent Payment Transactions (SUPERSEDED)",
     "An IETF individual draft introducing an Agent Passport — a cryptographic delegation certificate intended to serve as the PSD2 'something you have' factor — and a trust-scoring model for payment transactions mapped to PCI DSS v4.0.1.",
     "https://datatracker.ietf.org/doc/draft-sharif-agent-payment-trust/",
     "IETF (individual, superseded)",
     "SUPERSEDED by draft-sharif-attp-00 (April 2026). Retained for historical context — the Agent Passport concept is interesting but needs formal grounding; the ATTP successor generalizes it across transport bindings."),

    ("draft-stephan-ai-agent-6g — AI Agent Protocols for 6G Systems",
     "An IETF individual draft translating use cases and service requirements from 3GPP TR 22.870 into IETF agent-protocol requirements, covering autonomous vehicles, privacy preservation, and anomaly detection.",
     "https://datatracker.ietf.org/doc/draft-stephan-ai-agent-6g/",
     "IETF (individual)",
     "Revision -02, October 2025; strong operator backing (Orange, Deutsche Telekom, Telefonica, China Mobile, Huawei). Requirements-oriented and important for 3GPP/IETF coordination. May be expired (April 2026); watch for an update. **EXPIRED on Datatracker** (expired 23 Apr 2026; checked 26 Aug 2026) — kept in the corpus deliberately; an expired draft is still evidence of what was proposed."),

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
     "Revision -02 was submitted August 2025; likely due for -03 refresh. Builds naturally on RFC 6749 + RFC 8693 + RFC 7636 PKCE — one of the most 'IETF-ready' delegation drafts and a strong WG-adoption candidate after the OAuth recharter. **EXPIRED on Datatracker** (expired 27 Feb 2026; checked 26 Aug 2026) — kept in the corpus deliberately; an expired draft is still evidence of what was proposed."),

    ("draft-rosomakho-oauth-txn-challenge — OAuth Transaction Authorization Challenge",
     "An OAuth mechanism enabling protected resources to demand transaction-specific authorization through challenges. When a request involves an agent or automated workflow, the RS returns a challenge to the client; the client presents it to the AS, which validates it, obtains human approval, and issues an access token with RFC 9396 authorization_details describing the approved operation. Positions as complementary to RFC 9470 (Step-Up Authentication) — that spec handles authentication freshness; this one handles authorization specificity.",
     "https://datatracker.ietf.org/doc/draft-rosomakho-oauth-txn-challenge/",
     "IETF (individual)",
     "Revision -00, submitted 25 June 2026. Authors: Yaroslav Rosomakho (Zscaler), Brian Campbell (Ping Identity), Karl McGuinness (Independent), Pieter Kasselman (Defakto). Strong author lineup — Campbell is a prolific OAuth WG contributor, Kasselman co-authored Transaction Tokens and First-Party Apps, McGuinness brings the Mission-Bound OAuth context. The RS-initiated challenge model is distinct from ARAP (which operates at the PDP/PEP layer via AuthZEN) but addresses the same 'denial is not the end' problem — here at the OAuth RS/AS layer rather than the AuthZEN layer."),

    # ---- Individual drafts: Pre-action authorization / permit-before-commit cluster ----
    ("draft-lee-orprg-permit-receipts — Permit Receipts for Permit-Before-Commit Authorization",
     "Defines requirements and an abstract data model for PermitReceipts: a verifier evaluates canonicalized effect requests, action digests, policy epochs, validity intervals, and revocation status before any protected effect is committed at an effect boundary. Covers verifier behavior, failure semantics, and candidate registries.",
     "https://datatracker.ietf.org/doc/draft-lee-orprg-permit-receipts/",
     "IETF (individual)",
     "Revision -00, 4 Jun 2026; author: Yong Bok Lee (Meridian Verity Group). The most complete standalone framework for pre-commit authorization in the current wave; intended to ground IETF discussion on scope and profiles. Seeks guidance on appropriate organizational placement."),

    ("draft-nelson-agent-delegation-receipts — Delegation Receipt Protocol for AI Agent Authorization",
     "Specifies the Delegation Receipt Protocol (DRP) where users sign Authorization Objects (containing scope boundaries, time constraints, instruction hashes, and model state commitments) that are published to an append-only log before the agent runtime gains control. Removes operators as trusted intermediaries by making the user's private key the sole signing authority.",
     "https://datatracker.ietf.org/doc/draft-nelson-agent-delegation-receipts/",
     "IETF (individual)",
     "Revision -10, 13 Jun 2026; author: Ryan Nelson (Authproof). At version 10, the most iterated individual draft in the pre-action authorization space. The commitment-before-execution architecture — sign before the agent runs, not after — is distinctive and directly addresses the prompt-injection attack surface."),

    ("draft-williams-intent-token — The Intent Token: A Cryptographic Authorization Primitive for Autonomous Agents",
     "Specifies a cryptographic authorization primitive that binds an autonomous agent action to a cryptographically signed, human-declared authorization envelope before execution. Addresses the gap in OAuth 2.0 frameworks that govern access to resources but not what agents are permitted to do at the moment of action. Positioned as complementary to OAuth, not a replacement.",
     "https://datatracker.ietf.org/doc/draft-williams-intent-token/",
     "IETF (individual)",
     "Revision -01, 22 Jun 2026; author: Jeffrey Williams (Independent). Overlaps conceptually with draft-kroehl-agentic-trust-aae and draft-nelson-agent-delegation-receipts; worth tracking as a lighter-weight alternative to both."),

    ("draft-pereira-licet-human-intent — LICET: Multi-Modal Physiological Human-Intent Verification for Autonomous AI Agent Authorization",
     "Proposes a biometric HITL protocol fusing ECG, electrodermal activity, and Mahalanobis statistical distance to cryptographically verify genuine human intent — not just credential possession — before authorizing autonomous AI agent actions, with ZK proofs enabling third-party audit without exposing raw biometric data.",
     "https://datatracker.ietf.org/doc/draft-pereira-licet-human-intent/",
     "IETF (individual)",
     "Revision -01, 2 Jul 2026. The most novel and technically niche HITL proposal in the current wave — complements draft-rosenberg-aiproto-cheq (out-of-band HITL confirmation) and draft-sato-soos-hem (kernel-enforced escalation) by grounding human intent in physiological signal rather than credential or UI interaction."),

    # ---- Individual drafts: WIMSE extensions cluster ----
    ("draft-reece-wimse-cross-org-delegation — Cross-Organizational Delegation for Workload and Agent Identity",
     "A problem statement and requirements draft identifying that existing workload and token-based authorization mechanisms were designed for a single trust domain, describing the cross-organizational agent delegation gap, and enumerating requirements for solutions — without proposing specific technical approaches.",
     "https://datatracker.ietf.org/doc/draft-reece-wimse-cross-org-delegation/",
     "IETF (individual)",
     "Revision -01, 30 Jul 2026 (was -00, 25 Jun 2026); author: Morgan Reece (TowerGuardian Consulting). The problem-statement companion to the corpus's operational drafts; likely to feed into WIMSE WG scope expansion and is directly in scope for draft-kuehlewind-audit-architecture's composition graph."),

    ("draft-jiang-wimse-heterogeneous-credential — Heterogeneous Credential Verification for Workload and Agentic Systems",
     "Specifies mechanisms for representing credential sets, identifying credential types, determining appropriate verifiers, normalizing verification results across different formats (workload tokens, OAuth, X.509, attestation), and combining results into a single handling decision.",
     "https://datatracker.ietf.org/doc/draft-jiang-wimse-heterogeneous-credential/",
     "IETF (individual)",
     "Revision -01, 30 Jun 2026 (was -00 Jun 2026); authors: Yuning Jiang, Donghui Wang, Yurong Song, Faye Liu (Huawei). Solves the practical problem of agentic systems receiving credentials in multiple formats from different issuers. Fills a gap left by draft-ni-wimse-ai-agent-identity (corpus) which describes the identity problem but not multi-format credential handling."),

    ("draft-munoz-wimse-authorization-evidence — Signed Authorization-Evidence Records for WIMSE-Authorized AI Agent Actions",
     "Specifies a signed authorization-evidence record (Permit) for WIMSE-authorized AI actions, cryptographically binding to the dispatched request bytes via HTTP Message Signatures, OAuth access tokens, and Shared Signals Framework eventing — without modifying existing standards.",
     "https://datatracker.ietf.org/doc/draft-munoz-wimse-authorization-evidence/",
     "IETF (individual)",
     "Revision -00, 15 May 2026; author: Christian Munoz (Keel API). Profiles WIMSE for AI agent actions and satisfies audit requirements; companion to the SCITT permit profile below. Extends the corpus WIMSE thread (draft-ni-wimse-ai-agent-identity) with a concrete evidence artifact."),

    ("draft-schwenkschuster-wimse-trust-domain-discovery — WIMSE Trust Domain Discovery",
     "Fills a gap in the WIMSE architecture by defining how relying parties obtain cryptographic trust anchors for workload identity credentials; specifies the WIMSE Trust Bundle (a JSON document with freshness metadata) and a well-known HTTPS discovery endpoint resolving trust domain names to their trust bundles, following OpenID Connect Discovery / OAuth 2.0 patterns.",
     "https://datatracker.ietf.org/doc/draft-schwenkschuster-wimse-trust-domain-discovery/",
     "IETF (individual)",
     "Revision -00, 3 Jul 2026; authors: Arndt Schwenkschuster (Defakto Security), Yaroslav Rosomakho (Zscaler). Directly complements draft-schwenkschuster-wimse-credential-exchange (corpus). The kuehlewind-audit-architecture HUB assumes resolvable trust anchors — this provides the discovery mechanism. Rosomakho co-authorship ties it to draft-rosomakho-oauth-txn-challenge."),

    ("draft-winmagic-wimse-condition-bounded-credentials — Condition-Bounded Credentials for Workload and Agent Identity",
     "Proposes hardware-rooted, non-exfiltratable workload credentials whose validity is conditioned on attested runtime posture rather than expiration time — so a credential becomes invalid if the workload's attestation evidence degrades, regardless of the stated expiry.",
     "https://datatracker.ietf.org/doc/draft-winmagic-wimse-condition-bounded-credentials/",
     "IETF (individual)",
     "Revision -01, 6 Jul 2026; author: WinMagic. Extends the WIMSE credential model with posture-conditioned validity — distinct from time-bounded credentials in that security policy changes at the hardware/attestation layer instantly invalidate the credential. Bridges the RATS attestation thread and the WIMSE identity thread in the corpus."),

    ("draft-rampalli-pedigree — PEDIGREE: Per-Hop Cryptographic Delegation for Workload and AI Agent Identity",
     "Extends SPIFFE workload identity with cryptographic per-hop delegation using monotonic scope attenuation enforced at mint and verify; uses Cedar-policy mandates with static-analysis proofs and parent-token re-verification to detect parent-swap attacks. Defines an Operator Ceiling binding all sub-agent authority to the parent's declared mandate.",
     "https://datatracker.ietf.org/doc/draft-rampalli-pedigree/",
     "IETF (individual)",
     "Revision -00, Apr 25 2026; author: Karthik Rampalli (Glyphzero, Inc.) — same author as draft-rampalli-cross-org-delegation-mapping and draft-rampalli-scitt-capsule-provenance-binding (both in corpus). Presented at WIMSE WG as proposed new work at IETF 126 (Bangkok, Jul 2026). Cedar-policy static-analysis attenuation proofs are a unique contribution relative to other delegation-chain drafts. Note: draft-rampalli-cross-org-delegation-mapping (corpus) references the 'PEDIGREE model' — this is the normative definition."),

    ("draft-sweeney-wimse-credential-delegation — Credential Delegation Protocol for AI Agents in Multi-System Environments",
     "Composes RFC 8693 Token Exchange, RFC 9449 DPoP, RFC 9396 Rich Authorization Requests, and OpenID Connect CIBA into a unified delegation flow for autonomous AI agents accessing protected resources across providers; introduces ephemeral agent identities via did:key, capability-shaped attenuated delegation tokens, credential wrapping preventing raw OAuth tokens from reaching agents, synchronous revocation cascading, and tamper-evident audit chains.",
     "https://datatracker.ietf.org/doc/draft-sweeney-wimse-credential-delegation/",
     "IETF (individual)",
     "Revision -00, Jul 28 2026; author: Sweeney. Explicitly designed as a WIMSE companion, citing draft-klrc-aiagent-auth as its target framework. The widest synthesis of OAuth primitives in the WIMSE extension cluster — DPoP + RAR + CIBA + Token Exchange in one flow. The credential-wrapping model (raw tokens never reach the agent) directly addresses the secret-exposure threat formalized in arXiv:2604.24920 (SUDP paper, now in corpus)."),

    # ---- Individual drafts: SCITT / Audit profiles cluster ----
    ("draft-munoz-scitt-permit-profile — A SCITT Profile for Pre-Execution AI Action Authorization Records",
     "SCITT profile for the Pre-Execution Authorization Record (Permit), documenting policy-evaluated decisions before AI agent action dispatch with cryptographic binding proving 'authorized request equals dispatched request.' Composes with adjacent profiles for human-authority binding, post-execution evidence, and content-refusal events via referencing mechanisms.",
     "https://datatracker.ietf.org/doc/draft-munoz-scitt-permit-profile/",
     "IETF (individual)",
     "Revision -00, 15 May 2026; author: Christian Munoz (Keel API). SCITT-anchored analog of the WIMSE evidence record; companion to draft-munoz-wimse-authorization-evidence from the same author. Connects to draft-sharif-agent-audit-trail and draft-kuehlewind-audit-architecture (both in corpus)."),

    ("draft-marques-asqav-compliance-receipts — Compliance Profile of Signed Action Receipts for AI Agents",
     "Establishes a compliance framework for signed action receipts from AI agents, mandating specific fields, cryptographic anchoring, hash-chain linkage, risk/incident classification, cross-agent envelope binding, and enforcement attestation with retention floors tied to EU AI Act, DORA, NIST AI RMF, HIPAA, SEC Rule 17a-4, and CIRCIA.",
     "https://datatracker.ietf.org/doc/draft-marques-asqav-compliance-receipts/",
     "IETF (individual)",
     "Revision -06, 1 Jul 2026 (was -05 May 2026); author: João André Gomes Marques. The most legally grounded receipt profile in the wave — at revision 06, relatively mature. Complements draft-sharif-agent-audit-trail (corpus) with a multi-regulation compliance overlay."),

    ("draft-mih-scitt-agent-action-capsule — An Agent Action Capsule Profile for SCITT",
     "Defines a SCITT statement profile (Agent Action Capsule) documenting agent actions with outcome status (executed, blocked, denied, errored, timed out), evaluated constraints, committed-effect binding, and a human-in-the-loop flag; records a Capsule for every verdict including refusals. COSE Signed Statement format; registrable in SCITT Transparency Services.",
     "https://datatracker.ietf.org/doc/draft-mih-scitt-agent-action-capsule/",
     "IETF (individual)",
     "Revision -02, 6 Jul 2026 (was -01 Jun 2026); author: Steven Mih (Action State Group). -02 added an 'honest human-in-the-loop' flag distinguishing actual HITL from automated policy. Provides auditor-grade evidence that decision gates functioned; the HITL flag directly tracks the corpus theme."),

    ("draft-mih-sato-agent-accountability-composition — Agent Accountability: Composition and Conformance",
     "Addresses how to answer accountability questions about cross-domain autonomous agent actions for auditors and regulators who do not trust the operator; defines a composition model assembling multiple independently verifiable artifacts (workload credentials, delegation tokens, action capsules, attestation results) into a single accountability record with a conformance evaluation framework.",
     "https://datatracker.ietf.org/doc/draft-mih-sato-agent-accountability-composition/",
     "IETF (individual)",
     "Revision -01, 16 Aug 2026 (was -00, Jul 2026); authors: Steven Mih (Action State Group) + Tom Sato (MyAuberge K.K.) — collaboration between the two principal authors of draft-mih-scitt-agent-action-capsule (corpus) and the SOOS governance suite (corpus). Operates above individual SCITT profiles; the accountability-composition layer the kuehlewind-audit-architecture HUB depends on but does not yet specify."),

    ("draft-car-rer-artifact — RER Run Artifact Format: Hash-Chained, Signed Records of AI Inference Execution",
     "Specifies a cryptographically signed JSON record for AI inference runs including a signed envelope declaring permissions and limits, a hash-chained event log covering all model and tool calls, and a runtime signature binding envelope and log to the producing implementation. Enables offline verification by parties uninvolved in the original run.",
     "https://datatracker.ietf.org/doc/draft-car-rer-artifact/",
     "IETF (individual)",
     "Revision -01, 12 Jun 2026; author: Kayla Cardillo (Tech Enrichment). Relevant for post-hoc audit of what permissions an agent claimed during execution; companion to the SCITT profiles but more focused on inference traceability than authorization decisions."),

    ("draft-noa-scitt-ai-agent-receipt — A SCITT Profile for AI-Agent Action Receipts",
     "Defines a minimal SCITT profile: COSE_Sign1 Signed Statements with canonicalized payloads, hash-chained for ordering, registrable in SCITT Transparency Services. Explicitly does NOT assert agent correctness, safety, or real-world outcomes — only tamper-evident, signature-verifiable records of action, principal, policy identity, and verdict.",
     "https://datatracker.ietf.org/doc/draft-noa-scitt-ai-agent-receipt/",
     "IETF (individual)",
     "Revision -01, 15 Aug 2026 (was -00, 23 Jun 2026); author: Tora Toraman (NordenSoft). The minimalist end of the SCITT profile spectrum; useful for corpus completeness alongside the more comprehensive draft-mih-scitt-agent-action-capsule."),

    ("draft-rampalli-scitt-capsule-provenance-binding — Binding Per-Action Authorization and Memory Provenance into Agent Action Capsules",
     "Specifies how to bind three components into AAC records: what was executed ('did'), whether it was authorized ('may'), and the source of the belief that motivated the action ('why-believed'); uses optional payload extensions carrying authorization token references, memory chain roots, and quarantine attestations without modifying AAC core protected-header claims.",
     "https://datatracker.ietf.org/doc/draft-rampalli-scitt-capsule-provenance-binding/",
     "IETF (individual)",
     "Revision -00, 5 Jul 2026; author: Karthik Rampalli (Glyphzero, Inc.). Extends draft-mih-scitt-agent-action-capsule with memory provenance — the 'why-believed' component is novel among SCITT profiles. Includes a defensive publication notice waiving patent claims on the core binding technique."),

    ("draft-rampalli-cross-org-delegation-mapping — A Layered Requirements Mapping for Cross-Organization Agent Delegation",
     "Records a comparative mapping of two evidence layers for cross-organization AI agent delegation — per-hop delegation chains (PEDIGREE model) and named-human authorization roots (EMILIA Protocol binding and evidence-graph drafts) — evaluated against the nine requirements of draft-reece-wimse-cross-org-delegation under a multi-tier organizational architecture.",
     "https://datatracker.ietf.org/doc/draft-rampalli-cross-org-delegation-mapping/",
     "IETF (individual)",
     "Revision -05, Jul 2026; author: Karthik Rampalli (Glyphzero, Inc.) — same author as draft-rampalli-scitt-capsule-provenance-binding (corpus). Rev-05 signals active iteration; the mapping bridges two otherwise disconnected design families and is the first document to formally cross-reference EMILIA Protocol against WIMSE cross-org requirements."),

    ("draft-nobuo-scitt-composite-evidence-verification — Composite Evidence Verification for SCITT Statement Graphs",
     "Defines a composite verifier function for checking collections of SCITT Signed Statements, receipts, object bindings, and relationship edges under a named verification profile; provides structured reporting on validation status, missing evidence, outdated information, and conflicting claims — targeting auditors needing to evaluate multiple interconnected statements.",
     "https://datatracker.ietf.org/doc/draft-nobuo-scitt-composite-evidence-verification/",
     "IETF (individual)",
     "Revision -00, 7 Jul 2026; author: Nobuo Aoki (SOKENDAI). Operates above individual SCITT profiles (AAC, permits, compliance receipts all in corpus) — the 'how do you verify all of them together' layer that draft-kuehlewind-audit-architecture implies but does not yet specify. Watch for Kühlewind/Birkholz pickup."),

    # ---- Individual drafts: EMILIA Protocol family (schrock-ep-*) ----
    # Authorization receipts for high-risk agent actions; five mutually-referencing drafts
    # that together provide pre-action human binding, multi-party quorum, cross-system
    # evidence composition, action evidence graphs, and long-term record preservation.

    ("draft-schrock-ep-authorization-receipts — Authorization Receipts for High-Risk Agent Actions",
     "Defines the EMILIA Protocol (EP) authorization receipt — a COSE_Sign1 artifact that cryptographically binds a named human principal to a specific high-risk agent action before execution, providing auditors and counterparties a tamper-evident record that a real human authorized the consequential step.",
     "https://datatracker.ietf.org/doc/draft-schrock-ep-authorization-receipts/",
     "IETF (individual)",
     "Revision -12, 16 Aug 2026 (was -11, 10 Aug 2026) (was -08, Jul 21 2026). The base artifact for the EMILIA Protocol family; companion drafts draft-schrock-ep-authorization-evidence-chain, draft-schrock-ep-action-evidence-graph, draft-schrock-ep-quorum, and draft-schrock-ep-evidence-record all build on or reference this receipt format. Active iteration pace — -08 by late Jul 2026. Draft-rampalli-cross-org-delegation-mapping (corpus) formally maps EMILIA Protocol receipts against the nine reece-wimse-cross-org-delegation requirements."),


    ("draft-schrock-ep-authorization-evidence-chain — Authorization Evidence Chains: Composing Heterogeneous Agent-Authorization Receipts (EP-AEC)",
     "Defines a mechanism for composing EMILIA Protocol authorization receipts from different systems and issuers into a single authorization evidence chain, enabling auditors to verify a heterogeneous chain of human approvals across organizational boundaries without requiring a common receipt format.",
     "https://datatracker.ietf.org/doc/draft-schrock-ep-authorization-evidence-chain/",
     "IETF (individual)",
     "Revision -05, 3 Aug 2026 (was -02, Jul 2026). The cross-system interoperability layer for EMILIA Protocol receipts; directly addresses the scenario where draft-reece-wimse-cross-org-delegation (corpus) operates and authorization evidence must span administrative domains. Rev-02 indicates active development. **SUPERSEDES draft-schrock-ep-action-evidence-graph**, which Datatracker marks Replaced by this draft. That older row was removed from the corpus on 26 Aug 2026 — it was tracked separately and had become a duplicate of this one under the pre-rename slug."),

    ("draft-schrock-ep-quorum — Multi-Party Quorum Authorization for High-Risk Agent Actions (EP-QUORUM)",
     "Defines EP-QUORUM, a multi-party authorization profile for EMILIA Protocol authorization receipts; extends the base receipt (which binds one human to one action) to require a quorum of named human approvals before an action may proceed, with configurable thresholds, role requirements, and time-bounded approval windows.",
     "https://datatracker.ietf.org/doc/draft-schrock-ep-quorum/",
     "IETF (individual)",
     "Revision -02, Jul 2026. The enterprise governance complement to the base EP receipt; relevant for high-risk regulated workflows (financial transactions, medical orders, critical infrastructure changes) where single-human authorization is insufficient. Rev-02 indicates active iteration."),

    ("draft-schrock-ep-evidence-record — Long-Term, Crypto-Agile Preservation of Authorization Evidence (EP-EVIDENCE-RECORD)",
     "Defines a long-term, crypto-agile record format for preserving EMILIA Protocol authorization evidence under regulatory retention mandates; addresses algorithm deprecation over multi-year retention periods (DORA 5-year, HIPAA 6-year, SEC 17a-4 requirements) using a re-signing model that preserves evidentiary chain of custody.",
     "https://datatracker.ietf.org/doc/draft-schrock-ep-evidence-record/",
     "IETF (individual)",
     "Revision -01, Jul 2026. The regulatory compliance layer for EMILIA Protocol; directly connects to the kuehlewind-audit-architecture HUB (corpus) requirement for audit evidence that survives algorithm sunset. The DORA/HIPAA/SEC citation grounds the spec in concrete regulatory obligations."),

    ("draft-kumaresan-counter-sign — counter-sign: An Open Protocol for Agent-to-Human Authorization",
     "Defines a protocol where agents sign intent objects for consequential actions and humans return cryptographic countersignatures (approve/reject); includes an Enrollment Registry binding actors to signing keys, quorum models for multi-approver scenarios, and tamper-evident receipt logs. Explicitly out of scope for agent-to-service auth — addresses the 'human approval cannot be forged after the fact' problem.",
     "https://datatracker.ietf.org/doc/draft-kumaresan-counter-sign/",
     "IETF (individual)",
     "Revision -00, Jul 21 2026; author: Kumaresan. Human-countersignature model makes it a direct complement to the EMILIA Protocol family (schrock-ep-*) and to draft-sato-soos-hem (HEM) — EMILIA and HEM handle the pre-execution authorization decision, counter-sign handles the cryptographic non-repudiation that the human approval actually happened. The Enrollment Registry is analogous to WebBotAuth's Signature Agent Card registry but for human approvers."),

    ("draft-thallapelly-oasnt — OASNT: Attested Action Authorization Tokens",
     "Defines a JWS-based single-use, short-lived token binding a specific human-approved action to the exact rendered disclosure text the approver saw — 'What You See Is What You Sign' (WYSIWYG) — with optional binding to a concrete HTTP request. Requires hardware-resident secure element signature and device runtime integrity assessment.",
     "https://datatracker.ietf.org/doc/draft-thallapelly-oasnt/",
     "IETF (individual)",
     "Revision -02, 15 Aug 2026 (was -01, Jul 24 2026) (first filed Jul 21 2026); author: Thallapelly. Hardware-bound, WYSIWYG authorization token — distinct from software-only pre-action permit approaches such as draft-kumaresan-counter-sign (above) and the EMILIA Protocol family. The WYSIWYG disclosure binding addresses UI redress attacks where an agent's rendered action description differs from the actual HTTP request being authorized. Hardware PoP requirement makes this the highest-assurance pre-action permit in the current wave."),

    ("draft-tsyrulnikov-rats-attested-inference-receipt — Attested Inference Receipt (AIR): A COSE/CWT Profile for Confidential AI Inference",
     "Defines the Attested Inference Receipt (AIR), a COSE_Sign1 envelope carrying CWT claims profiled per the Entity Attestation Token (EAT) framework; an AIR receipt cryptographically binds model identity, input/output hashes, TEE attestation evidence, and operational telemetry into a single signed artifact verifiable by parties not present at inference time.",
     "https://datatracker.ietf.org/doc/draft-tsyrulnikov-rats-attested-inference-receipt/",
     "IETF (individual)",
     "Revision -02, Jul 2026. The RATS-layer complement to the SCITT profiles in corpus: where SCITT profiles (mih-scitt-agent-action-capsule, marques-asqav-compliance-receipts) record authorization and governance events, AIR records what the model actually computed — model identity, I/O content hashes, and TEE attestation linking the computation to trusted hardware. Together they address the full audit evidence stack."),

    # ---- Individual drafts: SOOS governance suite (Tom Sato, MyAuberge K.K.) ----
    # Five mutually-referencing drafts forming a coherent agent governance family.
    # Analogous integrator role to draft-kuehlewind-audit-architecture but with a
    # Sovereign Object / WIMSE substrate and explicit EU AI Act Article 12/14 alignment.

    ("draft-sato-soos-mjwt — The Mandate JWT (MJWT) for Agentic AI Systems",
     "Introduces the Mandate JWT — a WIMSE workload credential profile binding agent authority to specific Sovereign Object instances under named human principals, with cryptographically enforced delegation ceilings and a six-dimensional Narrowing Property preventing sub-agents from exceeding root authority.",
     "https://datatracker.ietf.org/doc/draft-sato-soos-mjwt/",
     "IETF (individual)",
     "Revision -04, 13 Aug 2026 (was -01, 10 Jun 2026); author: Tom Sato (MyAuberge K.K.). The authorization token primitive for the SOOS governance protocol family. Directly comparable to draft-mcguinness-oauth-client-instance-assertion but uses a WIMSE/Sovereign Object substrate rather than OAuth."),

    ("draft-sato-soos-mad — Multi-Agent Delegation in Sovereign Object Systems",
     "Specifies three core mechanisms for multi-agent delegation accountability: the Narrowing Property (capability non-amplification), five formally defined object topology patterns for runtime relationships, and cluster coordination primitives for parallel execution with aggregation rules. Version 02 adds revocation-during-execution handling and partial-completion routing to human oversight.",
     "https://datatracker.ietf.org/doc/draft-sato-soos-mad/",
     "IETF (individual)",
     "Revision -02, 10 Jun 2026; author: Tom Sato (MyAuberge K.K.). Claims to address gaps the OpenID Foundation identifies as unsolved in multi-agent authorization. The five topology patterns are a useful vocabulary for describing agent-to-agent relationship structures."),

    ("draft-sato-soos-hem — The Human Escalation Mechanism (HEM) for Agentic AI Systems",
     "Defines a kernel-enforced mechanism placing agent sessions in a pending state when human judgment is required, routing structured escalation requests to designated human decision-makers, and prohibiting all state transitions until a human decision is received. Defines five decision types and a dual-layer architecture (LLM-HEM and SOOS-HEM).",
     "https://datatracker.ietf.org/doc/draft-sato-soos-hem/",
     "IETF (individual)",
     "Revision -05, 30 Jun 2026 (was -04 Jun 2026); author: Tom Sato (MyAuberge K.K.). The most normative HITL protocol in the current wave; explicitly aligns with EU AI Act Article 14 requirements for high-risk AI system oversight. Counterpart to ARAP (AuthZEN WG) at the protocol level vs. the OAuth/AuthZEN layer."),

    ("draft-sato-soos-idp — The Intent Declaration Primitive (IDP) for Agentic AI Systems",
     "Specifies a structured declaration mechanism committing AI agent intent to tamper-evident logs before actions are taken, enabling post-hoc review and EU AI Act Article 12 compliance for high-risk systems.",
     "https://datatracker.ietf.org/doc/draft-sato-soos-idp/",
     "IETF (individual)",
     "Revision -05, 30 Jun 2026 (was -04 Jun 2026); author: Tom Sato (MyAuberge K.K.). The log-before-execute pattern mirrors draft-nelson-agent-delegation-receipts but operates at the intent declaration level rather than the user-authorization level. Pairs with GAR (below) to form a complete pre/post audit trail."),

    ("draft-sato-soos-gar — The Governance Audit Record (GAR) for Agentic AI Systems",
     "Defines GAR, an audit framework with five audit types, a Session Audit Record, and an Audit Alert mechanism; collects, signs, and makes governance events from IDP, HEM, and associated SOOS primitives available for regulatory inspection via an append-only, non-suppressible SCITT-anchored audit stream with Authority Lifecycle Events covering the complete revocation-recovery cycle.",
     "https://datatracker.ietf.org/doc/draft-sato-soos-gar/",
     "IETF (individual)",
     "Revision -06, 25 Aug 2026 (was -03, 28 Jun 2026) (was -02 Jun 10). -03 added OpenTelemetry attribute namespace for governance observability, a GAR Processor spec for converting OTel signals to audit records with integrity verification, four new Authority Lifecycle Event categories (policy conflict scenarios, statutory interpretation changes), and mandatory provenance fields for policy evaluation records. The integrator for the SOOS family, analogous to how draft-kuehlewind-audit-architecture integrates the broader IETF agent draft landscape."),

    # ---- Individual drafts: Security analysis / intent / adjacent protocols cluster ----
    ("draft-jiang-intent-security — Security Considerations and Requirements for Intent-Based Requests in Agentic Systems",
     "Solution-agnostic threat analysis covering tampering, privilege escalation, constraint violations, and intent drift in intent-based agentic systems, with a reference model, attack scenarios, and security requirements covering authentication, admission control, constraint validation, and multi-hop integrity.",
     "https://datatracker.ietf.org/doc/draft-jiang-intent-security/",
     "IETF (individual)",
     "Revision -03, 22 Jun 2026; authors: Yuning Jiang, Lun Li, Yurong Song, Faye Liu (Huawei). The threat-model companion to draft-jiang-oauth-intent-admission from the same group; likely intended to inform the broader IETF agentic AI security discussion."),

    ("draft-haberkamp-ipp — Intent Provenance Protocol (IPP)",
     "Specifies a cryptographic infrastructure standard for carrying verified human intent through chains of autonomous AI agent actions; defines the Intent Token, a signed, bounded, and tamper-evident data structure that travels with every agentic action so downstream agents and resource servers can verify that the chain traces to a real human authorization.",
     "https://datatracker.ietf.org/doc/draft-haberkamp-ipp/",
     "IETF (individual)",
     "Revision -01, Jul 2026. Addresses the 'intent drift' threat class from draft-jiang-intent-security (corpus) with a concrete token artifact; complements the EMILIA Protocol receipts (authorization at the action level) with an intent record at the delegation chain level. The traveling Intent Token model is distinct from both SOOS Mandate JWTs (Sato, governance substrate) and McGuinness Actor Profiles (delegation chain encoding in existing OAuth tokens)."),

    ("draft-li-dmsc-macp — Multi-agent Collaboration Protocol Suites Architecture",
     "Defines a protocol suite and architectural framework for secure, scalable multi-agent collaboration covering trusted agent onboarding, capability-based discovery, distributed capability synchronization, and secure agent-to-agent interaction. Specifies a gateway-centric architecture where an Agent Gateway mediates capability negotiation and trust establishment between collaborating agents.",
     "https://datatracker.ietf.org/doc/draft-li-dmsc-macp/",
     "IETF (individual)",
     "Revision -06, Jul 20 2026; active; authors: Xueting Li (China Telecom), Bing Liu (Huawei), Jun Liu (Beijing U of Posts & Telecom), Chenguang Du (Tsinghua), Lianhua Zhang (AsiaInfo). Replaces draft-li-dmsc-mcps-agw. Anchors a DMSC family of companion drafts covering intent-based interconnection, task protocol, gateway directory sync, semantic interaction, and gateway requirements. No explicit OAuth or WIMSE dependencies — operates at the agent coordination layer above transport, below authorization."),

    ("draft-li-dmsc-inf-architecture — Dynamic Multi-agent Secured Collaboration Infrastructure Architecture",
     "Approaches DMSC from the network-infrastructure perspective: proposes capability-based forwarding and semantic routing at the network layer, where agent capability metadata influences packet-forwarding decisions rather than routing based solely on addresses. The most mature DMSC document at rev 07; predates and informs the MACP architecture draft.",
     "https://datatracker.ietf.org/doc/draft-li-dmsc-inf-architecture/",
     "IETF (individual)",
     "Revision -07, May 22 2026; authors: Xueting Li (China Telecom), Aijun Wang (China Telecom), Bing Liu (Huawei), Changwang Lin (New H3C). Infrastructure-layer complement to draft-li-dmsc-macp (protocol suite). The DMSC family now has 14+ companion drafts from Chinese telecom/academic groups — this is the architectural anchor."),

    ("draft-sz-dmsc-iaip — Intent-based Agent Interconnection Protocol at Agent Gateway",
     "Defines semantic capability advertisement and intent-driven routing at DMSC agent gateways: agents publish capability profiles in a structured format and the gateway matches incoming task intents to available agents, replacing fixed-address routing with dynamic semantic matching. The core routing-layer protocol for DMSC inter-agent communication.",
     "https://datatracker.ietf.org/doc/draft-sz-dmsc-iaip/",
     "IETF (individual)",
     "Revision -02, May 2026; authors: Sheng Sun, Xinyi Zhang (CAS/CNIC), Qiangzhou Gao (Huawei), Min Liu, Yuwei Wang (ICT, CAS). The intent-based routing mechanism that distinguishes DMSC from address-based protocols; relevant to the DAWN boundary question — DMSC embeds discovery in the gateway routing layer rather than treating it as a separate protocol."),

    ("draft-yang-dmsc-ioa-task-protocol — Internet of Agents Task Protocol for Heterogeneous Agent Collaboration",
     "Establishes a session and task coordination layer with finite-state-machine-based dialogue management, dynamic team assembly, and nested team hierarchies for distributed heterogeneous agent collaboration. Addresses the multi-agent task lifecycle from assignment through completion and audit across heterogeneous agent implementations.",
     "https://datatracker.ietf.org/doc/draft-yang-dmsc-ioa-task-protocol/",
     "IETF (individual)",
     "Revision -03, Apr 21 2026; authors: Cheng Yang (BUPT), Zhiyuan Liu (Tsinghua), Aijun Wang (China Telecom). The task-coordination layer above the DMSC gateway routing; covers multi-domain and 6G/ITS scenarios. Distinct from OAuth-layer delegation in that it orchestrates task state rather than token issuance."),

    ("draft-dunbar-dmsc-gw-scenarios-gap-analysis — Deployment Scenarios and Gap Analysis for AI Agent Gateway",
     "Surveys single-domain to multi-domain deployment scenarios for AI Agent Gateways and identifies concrete gaps where existing protocols (specifically MCP and Google's A2A) cannot satisfy governance, policy enforcement, and cross-organizational trust requirements — particularly in regulated financial services and telecom environments.",
     "https://datatracker.ietf.org/doc/draft-dunbar-dmsc-gw-scenarios-gap-analysis/",
     "IETF (individual)",
     "Revision -04, 14 Aug 2026 (was -03, 7 Aug 2026) (was -02, Jul 2 2026); authors: Linda Dunbar (Futurewei), YiFei Wang (China Telecom), Bing Liu (Huawei). The most directly useful DMSC document for the boundary analysis: explicitly names MCP and A2A as insufficient and articulates where the DMSC gateway fills the gap. The regulated-environment focus (financial services, telco) distinguishes DMSC's use-case target from OAuth-centric approaches."),

    ("draft-somoza-dmsc-atn-agent-trust-negotiation — Agent Trust Negotiation: Capability, Delegation, and Provenance Binding",
     "Specifies the Agent Trust Negotiation (ATN) protocol, which binds four artifacts — capability manifests, delegation chains, provenance attestations, and session receipts — to agent identities via a handshake state machine producing mutually verified, scope-bounded sessions with SCITT-suitable audit records.",
     "https://datatracker.ietf.org/doc/draft-somoza-dmsc-atn-agent-trust-negotiation/",
     "IETF (individual)",
     "Revision -00, 29 May 2026; author: Enrique Somoza (Independent). Operates above discovery mechanisms and positions itself between the discovery layer (DAWN, MCP) and the authorization layer (WIMSE, OAuth). Relevant as an agent-to-agent trust establishment handshake protocol. **SUPERSEDES draft-somoza-atn-agent-trust-negotiation**, which Datatracker marks Replaced by this draft. That older row was removed from the corpus on 26 Aug 2026 — it was tracked separately and had become a duplicate of this one under the pre-rename slug."),

    ("draft-mcgraw-httpapi-agent-budget — The Delegation HTTP Authentication Scheme for Request-Bound Authority",
     "Defines the 'Delegation' HTTP authentication scheme and response semantics for delegated-authority challenges using HTTP status codes and Problem Details, plus a CBOR/COSE proof format. The initial authority profile is 'Budget,' using post-quantum ML-DSA to prove spending or resource-consumption limits.",
     "https://datatracker.ietf.org/doc/draft-mcgraw-httpapi-agent-budget/",
     "IETF (individual)",
     "Revision -02, 15 Jun 2026; author: John Paul McGraw Jr. (TaskHawk Systems). HTTP-layer bounded delegation with post-quantum crypto; distinct from OAuth-layer delegation in that the authority proof travels in the Authorization header. Complements x401 (Industry tab) at the HTTP challenge-response layer."),

    ("draft-vauban-x402-delegation-binding — x402 Delegation Binding for Agentic HTTP Pipelines",
     "Addresses the security gap where x402 V2 payment grants issued to one agent could be misused by another in the same pipeline, introducing three binding mechanisms: a JCS-derived agent identity pseudonym, a nonce for anti-replay, and a depth-limiting field for transitive delegation.",
     "https://datatracker.ietf.org/doc/draft-vauban-x402-delegation-binding/",
     "IETF (individual)",
     "Revision -01, 25 May 2026; author: Vauban Research. Narrowly scoped to payment pipelines but the delegation-binding pattern (pseudonymous identity + anti-replay + depth-limit) is applicable broadly. Validated across five language runtimes with A2A and MCP integration guidance."),

    ("draft-samal-vap — Verifiable Agent Protocol (VAP): Intent-Bound Admission Control and Audit for Agent Tool Invocation",
     "Specifies VAP as a defense-in-depth layer adding declarations of purpose and session budget commitments to tool invocation requests (targeting MCP-style protocols), enabling servers to perform admission control before execution via four messages carried in existing protocol metadata.",
     "https://datatracker.ietf.org/doc/draft-samal-vap/",
     "IETF (individual)",
     "Revision -00, 3 Jun 2026; author: Kruttidipta Samal (Independent). Lightweight and protocol-agnostic; addresses erroneous agent behavior, cost control, and audit trails without replacing existing auth mechanisms. Practical tool-invocation-level authorization layer for MCP deployments."),

    ("draft-khera-aurora — Agent Unification, Runtime, and Operational Responsibility Attestation (AURORA)",
     "A two-layer framework unifying hardware-enclave-backed Runtime Integrity Attestation with scoped, cryptographically bound Authority Delegation; enables agents to prove both operational authority and runtime integrity simultaneously.",
     "https://datatracker.ietf.org/doc/draft-khera-aurora/",
     "IETF (individual)",
     "Revision -00, 5 Jun 2026; author: Ankur Khera. Addresses the gap where delegation tokens don't prove the runtime environment is trustworthy — relevant where delegation must be paired with platform attestation (enterprise/regulated deployments). Bridges the RATS attestation thread and the OAuth delegation thread."),

    ("draft-borthwick-msebenzi-environment-state — Verifiable Intent — environment.* Constraint Family",
     "Defines the environment.* constraint family for agent-authorization mandate vocabularies, covering external conditions at transaction execution time (venue availability, wallet funding) that existing transactional constraints cannot address. Extends agent authorization mandate frameworks with environmental precondition checking.",
     "https://datatracker.ietf.org/doc/draft-borthwick-msebenzi-environment-state/",
     "IETF (individual)",
     "Revision -01, 13 Jun 2026; authors: Douglas Cameron Borthwick (InsumerAPI), Michael Msebenzi (Headless Oracle). Narrow but practically important for financial and commerce agent workflows; connects to draft-mcgraw-httpapi-agent-budget and draft-vauban-x402-delegation-binding."),

    ("draft-chen-oauth-agent-authz-use-cases — Agent Authorization Use Cases and Gap Analysis for OAuth 2.0",
     "A framework-level analysis enumerating agentic authorization use cases — delegated task execution, multi-agent coordination, long-running workflows, capability attenuation — and mapping each against current OAuth 2.0 mechanisms to identify gaps that require new extensions or profiles.",
     "https://datatracker.ietf.org/doc/draft-chen-oauth-agent-authz-use-cases/",
     "IETF (individual)",
     "Revision -03, 25 Aug 2026 (was -01, 5 Jul 2026); useful problem-statement companion to the OAuth recharter's 'Complex Delegation' milestone. Gap analysis directly motivates several other drafts in this corpus — a natural reference document for the OAuth WG scoping discussion."),

    ("draft-agnihotri-oauth-agent-impl-status — Implementation Status of OAuth Identity Chaining and Transaction Tokens",
     "An RFC 7942–compliant implementation status report tracking open-source implementations of draft-ietf-oauth-identity-chaining and draft-ietf-oauth-transaction-tokens against the relevant spec requirements.",
     "https://datatracker.ietf.org/doc/draft-agnihotri-oauth-agent-impl-status/",
     "IETF (individual)",
     "Revision -02, Jun 2026; provides the implementation evidence required to advance both WG drafts toward IESG submission. Informational companion to the two WG drafts — not a protocol spec but tracking their standardization progress."),

    ("draft-hardt-oauth-aauth-protocol — AAuth Protocol",
     "A new clean-sheet authorization protocol from Dick Hardt (original OAuth author) defining proof-of-possession by default, resource-signed challenges, agent identity without pre-registration, deferred 202 responses, and AS-to-AS federation for the agent ecosystem.",
     "https://datatracker.ietf.org/doc/draft-hardt-oauth-aauth-protocol/",
     "IETF (individual)",
     "Revision -10, 6 Aug 2026 (was -09, Jul 4 2026); slug gained 'oauth' infix at this revision (was draft-hardt-aauth-protocol). Now formally adds four resource access modes including agent governance. The design rationale section explicitly explains why AAuth is not GNAP, not OAuth, not DPoP and not mTLS — important read for anyone planning a new agent-auth stack. OUTLIER: zero OAuth dependencies."),

    ("draft-chen-oauth-roadmap — Comprehensive Roadmap for OAuth 2.0 Standards and Drafts",
     "An IETF informational draft that maps the entire OAuth 2.0 ecosystem of RFCs, BCPs, and active drafts into functional layers from core to extensions to industry profiles.",
     "https://datatracker.ietf.org/doc/draft-chen-oauth-roadmap/",
     "IETF (individual)",
     "Revision -01, 6 May 2026 (was -00, May 2026); the single most useful index when starting work in this area. Link switched from the pinned -00 archive HTML to the Datatracker document page so it tracks the latest revision."),

    ("draft-ietf-wimse-workload-creds — WIMSE Workload Credentials",
     "Defines the credential format and issuance profile for workload credentials in the WIMSE architecture, covering service-to-service authentication token types, local issuance mechanisms, and token exchange profiles for cross-trust-domain workload identity scenarios.",
     "https://datatracker.ietf.org/doc/draft-ietf-wimse-workload-creds/",
     "IETF (WIMSE WG)",
     "Revision -02, Jul 2026; WIMSE WG-adopted. The credential issuance companion to draft-ietf-wimse-arch (architecture) and draft-ietf-wimse-identifier (identifiers) already in corpus. Three WG drafts now cover the full WIMSE stack: arch → identifier → workload-creds. Relevant to the WIMSE agent extension family (ni-wimse, reece, jiang, schwenkschuster) which assumes a credential format this draft now specifies."),

    ("Charter: WIMSE — Workload Identity in Multi-System Environments (charter-ietf-wimse-01)",
     "The formal IETF charter for the WIMSE WG covering architecture, JOSE-based WIMSE tokens for service-to-service traffic, local token issuance, and token exchange profiles (likely based on RFC 8693) for cross-trust-domain workload identity.",
     "https://datatracker.ietf.org/doc/charter-ietf-wimse/01/",
     "IETF (WIMSE WG charter)",
     "Approved 18 March 2026 (v01); explicitly liaises with OAuth, SCIM, SCITT, RATS, the OpenID Foundation, and CNCF/SPIFFE — the formal scope statement that anchors all WIMSE draft work."),

    # ---- Aug 2026 Datatracker sweep — new individual and WG drafts ----

    ("draft-aap-oauth-profile — Agent Authorization Profile (AAP) for OAuth 2.0",
     "This document defines the Agent Authorization Profile (AAP), an authorization profile for OAuth 2.0 and JWT designed for autonomous AI agents. AAP extends existing standards with structured claims and validation rules so that systems can reason about agent identity, task context, operational constraints, delegation chains, and human oversight requirements.",
     "https://datatracker.ietf.org/doc/draft-aap-oauth-profile/",
     "IETF (OAuth-related, individual)",
     "Revision -01, 11 Aug 2026; **now EXPIRED** on Datatracker (checked 26 Aug 2026). Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-ietf-wimse-workload-identity-practices — Workload Identity Practices",
     "This document describes industry practices for providing secure identities to workloads in container orchestration, cloud platforms, and other workload platforms. It explains how workloads obtain credentials for external authentication purposes, without managing long-lived secrets directly.",
     "https://datatracker.ietf.org/doc/draft-ietf-wimse-workload-identity-practices/",
     "IETF (WIMSE WG)",
     "Revision -06, 11 Aug 2026; advanced to IESG **AD Evaluation** as of 18 Aug 2026. WG-adopted draft. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-schrock-ep-bounded-capability-receipts — Bounded Capability Receipts and Durable Spend Control for Agent Actions",
     "Agents sometimes need bounded authority to perform more than one consequential action without obtaining a new human approval for every operation. A signed token alone cannot enforce a shared budget across replicas, survive retries safely, or distinguish an operation that never crossed an effect boundary from one whose outcome is unknown.",
     "https://datatracker.ietf.org/doc/draft-schrock-ep-bounded-capability-receipts/",
     "IETF (individual draft)",
     "Revision -04, 11 Aug 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-chueayen-attestation-receipts — Enforcement Attestation Receipts for AI Inference Decisions",
     "This document specifies a compact JSON attestation receipt for an AI inference decision. A receipt binds an outcome to a request hash under a published Ed25519 public key, so a party that does not trust the issuer's infrastructure can still verify offline what the issuer's signing key attested was decided.",
     "https://datatracker.ietf.org/doc/draft-chueayen-attestation-receipts/",
     "IETF (individual draft)",
     "Revision -02, 8 Aug 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-bezerra-anchors-command-provenance — Anchors: Post-Quantum Command Provenance for Autonomous Machine Links",
     "Autonomous machines such as uncrewed aircraft, ground robots, and spacecraft execute commands issued by human operators and, increasingly, by AI agents.",
     "https://datatracker.ietf.org/doc/draft-bezerra-anchors-command-provenance/",
     "IETF (individual draft)",
     "Revision -01, 7 Aug 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-zehavi-oauth-authz-req-del-chain — OAuth Authorization Request Delegation Chain",
     "Brokered OAuth redirect authorization requests involve intermediary authorization servers between a downstream client and the upstream authorization server that obtains user consent and issues tokens.",
     "https://datatracker.ietf.org/doc/draft-zehavi-oauth-authz-req-del-chain/",
     "IETF (OAuth-related, individual)",
     "Revision -00, 7 Aug 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-gazitt-oauth-authzen-issuance — AuthZEN Profile for OAuth 2.0 Token Issuance",
     "Numerous OAuth 2.0 specifications define a moment at which an authorization server decides whether to issue a security token, and each of them declares the decision itself to be a matter of local policy that is out of scope. The result is that a decision common to every OAuth deployment has no interoperable expression.",
     "https://datatracker.ietf.org/doc/draft-gazitt-oauth-authzen-issuance/",
     "IETF (OAuth-related, individual)",
     "Revision -00, 5 Aug 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-gazitt-oauth-authzen-token-exchange — AuthZEN Binding for OAuth 2.0 Token Exchange",
     "OAuth 2.0 Token Exchange (RFC 8693) defines the moment at which an authorization server decides whether one party may obtain a token to act as, or on behalf of, another. It states that the decision is governed by policy, and does not define that policy.",
     "https://datatracker.ietf.org/doc/draft-gazitt-oauth-authzen-token-exchange/",
     "IETF (OAuth-related, individual)",
     "Revision -00, 5 Aug 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-wang-dmsc-drisac — Distributed Registration and Information Synchronization of Agent Capabilities",
     "The large-scale deployment of autonomous AI Agents introduces challenges to capability description, registration, and discovery. Existing agent communication protocols mainly focus on application- layer interactions and typically rely on centralized registration and discovery mechanisms, which limit scalability, robustness, and semantic extensibility.",
     "https://datatracker.ietf.org/doc/draft-wang-dmsc-drisac/",
     "IETF (DMSC-related, individual)",
     "Revision -01, 18 Aug 2026 (was -00, 5 Aug 2026). Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-diaconu-agents-authz-info-sharing — Cross-Domain AuthZ Information sharing for Agents",
     "Distributed Multi-Agent Systems consist of Agents and MCP Servers operating across multiple administrative domains, each with its own Identity Providers (IdPs) and Authorization Servers (AS).",
     "https://datatracker.ietf.org/doc/draft-diaconu-agents-authz-info-sharing/",
     "IETF (individual draft)",
     "Revision -01, 4 Aug 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-ietf-wimse-http-signature — WIMSE Workload-to-Workload Authentication with HTTP Signatures",
     "The WIMSE architecture defines authentication and authorization for software workloads in a variety of runtime environments, from the most basic ones to complex multi-service, multi-cloud, multi-tenant deployments. This document defines one of the mechanisms to provide workload authentication, using HTTP Signatures.",
     "https://datatracker.ietf.org/doc/draft-ietf-wimse-http-signature/",
     "IETF (WIMSE WG)",
     "Revision -06, 4 Aug 2026. WG-adopted draft. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-carleton-workload-authz-grant — Workload Authorization Grant",
     "This document profiles the Agent Identity Management System (AIMS) framework for agent platforms that host many agent instances per customer.",
     "https://datatracker.ietf.org/doc/draft-carleton-workload-authz-grant/",
     "IETF (individual draft)",
     "Revision -00, 3 Aug 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-helixar-hdp-agentic-delegation — Human Delegation Provenance Protocol (HDP): Cryptographic Chain-of-Custody for Agentic AI Systems",
     "Agentic AI systems operate on behalf of human principals, often delegating tasks through multi-step chains of AI agents. There is currently no standard mechanism to record who authorized an agent to act, under what scope, and through what chain of delegation, in a way that can be verified offline, without a central registry, and without third-party trust anchors.",
     "https://datatracker.ietf.org/doc/draft-helixar-hdp-agentic-delegation/",
     "IETF (individual draft)",
     "Revision -01, 3 Aug 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-mcguinness-oauth-id-continuation-assertion — Identity Continuation Assertion for OAuth 2.0 Token Exchange",
     "This document defines the Identity Continuation Assertion, a short- lived, sender-constrained JWT used as an OAuth 2.0 Token Exchange subject token. It lets an Identity Provider (IdP) issue an onward Identity Assertion JWT Authorization Grant (ID-JAG) when a user's request crosses service boundaries after the user is no longer present.",
     "https://datatracker.ietf.org/doc/draft-mcguinness-oauth-id-continuation-assertion/",
     "IETF (OAuth-related, individual)",
     "Revision -01, 26 Aug 2026 (was -00, 3 Aug 2026). Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-parecki-oauth-jwt-dpop-grant — OAuth 2.0 JWT Authorization Grant with DPoP Binding",
     "This specification defines a new OAuth 2.0 authorization grant type that uses a JSON Web Token (JWT) assertion to request an access token that is bound to a specific key using the Demonstration of Proof-of- Possession (DPoP) mechanism. This provides a higher level of security than a simple bearer token, as the client must prove possession of the key to use the access token.",
     "https://datatracker.ietf.org/doc/draft-parecki-oauth-jwt-dpop-grant/",
     "IETF (OAuth-related, individual)",
     "Revision -01, 3 Aug 2026. Added in the Aug 2026 corpus sweep; not previously tracked. **EXPIRED on Datatracker** (expired 3 Aug 2026; checked 26 Aug 2026) — kept in the corpus deliberately; an expired draft is still evidence of what was proposed."),

    ("draft-mih-agent-accountability-conformance — Agent Accountability: A Conformance and Verification Method",
     "An architecture for auditing agent-driven interactions (draft- kuehlewind-audit-architecture) identifies the record types an auditable agent system produces — interaction, action, delegation, and authorization-transition — and the role of an Auditor that determines whether recorded behaviour matched intent and the authorization in force.",
     "https://datatracker.ietf.org/doc/draft-mih-agent-accountability-conformance/",
     "IETF (individual draft)",
     "Revision -00, 1 Aug 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-okutomi-session-bound-agent-identity — A Verifier-Side Acceptance Profile for Channel-Bound Agent Identity and Authorization",
     "This document defines a verifier-side acceptance profile for channel- bound Agent identity and authorization. It addresses context diversion, where cryptographically valid material is accepted for a different service, tenant, actor, task, target, delegation, or authority boundary than the verifier intended.",
     "https://datatracker.ietf.org/doc/draft-okutomi-session-bound-agent-identity/",
     "IETF (individual draft)",
     "Revision -06, 30 Jul 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-richer-oauth-httpsig — OAuth Proof of Possession Tokens with HTTP Message Signatures",
     "This extension to the OAuth 2.0 authorization framework defines a method for using HTTP Message Signatures to bind access tokens to keys held by OAuth 2.0 clients. Discussion Venues This note is to be removed before publishing as an RFC.",
     "https://datatracker.ietf.org/doc/draft-richer-oauth-httpsig/",
     "IETF (OAuth-related, individual)",
     "Revision -03, 28 Jul 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-schrock-action-remedy-receipts — Action Remedy Receipts for Consequential Agent Effects",
     "Revocation cannot undo an effect that already occurred. A dispute does not authorize a refund, return, reversal, or other remedy. This document defines Action Remedy Receipts for recording a bounded dispute decision and a fresh compensating action without rewriting the original action or effect.",
     "https://datatracker.ietf.org/doc/draft-schrock-action-remedy-receipts/",
     "IETF (individual draft)",
     "Revision -00, 28 Jul 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-tonyai-a2a-trust — Agent-to-Agent Trust, Identity, and Verifiable Provenance",
     "This document defines a trust model for agent-to-agent (A2A) interactions in multi-agent AI systems.",
     "https://datatracker.ietf.org/doc/draft-tonyai-a2a-trust/",
     "IETF (individual draft)",
     "Revision -01, 25 Jul 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-ambekar-oauth-epop — JSON Web Token (JWT) Profile for OAuth 2.0 Enveloped Proof of Possession (EPOP)",
     "This specification defines a profile for OAuth 2.0 sender-constrained credentials in which access tokens and refresh tokens are cryptographically bound to the client's private key as a single inseparable envelope.",
     "https://datatracker.ietf.org/doc/draft-ambekar-oauth-epop/",
     "IETF (OAuth-related, individual)",
     "Revision -03, 24 Jul 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-parecki-oauth-refresh-token-scope-response — OAuth 2.0 Refresh Token Scope",
     "This specification defines a new OAuth 2.0 token response parameter, refresh_token_scope, that indicates the scope authorized for a refresh token when it differs from the scope of the access token issued alongside it.",
     "https://datatracker.ietf.org/doc/draft-parecki-oauth-refresh-token-scope-response/",
     "IETF (OAuth-related, individual)",
     "Revision -00, 24 Jul 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-pro-adp-agent-discovery — Agent Discovery Protocol (ADP) v1.1 -- Well-Known Metadata and Interaction Layer",
     "This document defines the Agent Discovery Protocol (ADP) v1.1, a layered protocol for discovering, verifying, and interacting with AI Agents on the Internet. ADP delegates DNS discovery to DNS-AID (SVCB records) and defines a Well-Known JSON metadata format, an Ed25519-based identity model, and the Agent Gateway Protocol (AGP) for real-time WebSocket messaging.",
     "https://datatracker.ietf.org/doc/draft-pro-adp-agent-discovery/",
     "IETF (individual draft)",
     "Revision -02, 24 Jul 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-ietf-oauth-rfc7523bis — Updates to OAuth 2.0 JSON Web Token (JWT) Client Authentication and Assertion-Based Authorization Grants",
     "This document updates RFC7521, RFC7522, RFC7523 and RFC9126 with respect to the treatment of audience values in OAuth 2.0 Client Assertion Authentication and Assertion-based Authorization Grants to address a security vulnerability identified in the previous requirements for those audience values in multiple OAuth 2.0 specifications.",
     "https://datatracker.ietf.org/doc/draft-ietf-oauth-rfc7523bis/",
     "IETF (OAuth WG)",
     "Revision -11, 23 Jul 2026; entered the RFC Editor queue (touched 13 Aug 2026, rfceditor state 'In Progress'). WG-adopted draft. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-kavian-aep-oauth-session-credential — OAuth Bearer Session Credential Grant Type for the Agent Enrollment Protocol",
     "This document defines the OAuth Bearer session-credential grant type for the Agent Enrollment Protocol (AEP). The grant type lets an AEP Service issue an OAuth-style Bearer access token through the AEP Grant command while preserving baseline AEP client assertion authentication as the root of trust.",
     "https://datatracker.ietf.org/doc/draft-kavian-aep-oauth-session-credential/",
     "IETF (OAuth-related, individual)",
     "Revision -03, 24 Aug 2026 (was -02, 23 Jul 2026). Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-morrison-mcp-dns-discovery — Discovery of Model Context Protocol Servers via DNS TXT Records",
     "This document defines a DNS-based mechanism for discovering Model Context Protocol (MCP) servers, the identity of the organisations that operate them, and a cryptographic identity envelope bound to an individual Sovereign-tier ~handle published under the same zone. Three TXT records are defined.",
     "https://datatracker.ietf.org/doc/draft-morrison-mcp-dns-discovery/",
     "IETF (individual draft)",
     "Revision -05, 23 Jul 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-yossif-agent-mandate-problem — Problem Statement: Verifiable Human Mandates for Autonomous Agent Actions",
     "An autonomous software agent commonly acts under authority a human granted at an earlier moment: the human expresses and authorizes an intent at one time, and the agent executes one or more concrete actions at a later time.",
     "https://datatracker.ietf.org/doc/draft-yossif-agent-mandate-problem/",
     "IETF (individual draft)",
     "Revision -00, 22 Jul 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-araut-oauth-transactiontokens-bcp — OAuth Transaction Tokens Best Current Practice",
     "This document provides best current practices for implementing and deploying OAuth 2.0 Transaction Tokens as specified in draft-ietf- oauth-transaction-tokens. Transaction Tokens (Txn-Tokens) enable workloads in a trusted domain to preserve and propagate user identity and authorization context across service boundaries during the processing of external programmatic requests.",
     "https://datatracker.ietf.org/doc/draft-araut-oauth-transactiontokens-bcp/",
     "IETF (OAuth-related, individual)",
     "Revision -00, 20 Jul 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-ccc-wimse-twi-extensions — WIMSE Extensions for Trustworthy Workload Identity",
     "This document contains a gap analysis that is the output of the Confidential Computing Consortium identifying areas in the IETF WIMSE WG work where the current WIMSE architecture should be extended to accommodate workloads running in Confidential Computing environments. This document contains a high-level outline for these extensions.",
     "https://datatracker.ietf.org/doc/draft-ccc-wimse-twi-extensions/",
     "IETF (WIMSE-related, individual)",
     "Revision -01, 20 Jul 2026. Added in the Aug 2026 corpus sweep; not previously tracked. **EXPIRED on Datatracker** (expired 9 Jul 2026; checked 26 Aug 2026) — kept in the corpus deliberately; an expired draft is still evidence of what was proposed."),

    ("draft-chen-ai-agent-auth-new-requirements — New requirements for Authentication and Authorization in the AI Agents era",
     "AI Agents are rapidly evolving from academic concepts into the core engines driving next-generation applications. However, their autonomy, dynamic nature, and complex delegation relationships pose a fundamental challenge to our existing authentication and authorization frameworks, which were designed for human users and traditional software.",
     "https://datatracker.ietf.org/doc/draft-chen-ai-agent-auth-new-requirements/",
     "IETF (individual draft)",
     "Revision -00, 20 Jul 2026. Added in the Aug 2026 corpus sweep; not previously tracked. **EXPIRED on Datatracker** (expired 10 Jul 2026; checked 26 Aug 2026) — kept in the corpus deliberately; an expired draft is still evidence of what was proposed."),

    ("draft-dellaert-oauth-approval-based-dcr — OAuth 2.0 Approval-Based Dynamic Client Registration",
     "This document specifies an extension to the OAuth 2.0 Dynamic Client Registration Protocol ([RFC7591]) that enables registration of a client with an authorization server through an explicit approval step performed by an approving party, typically the user running the client, without requiring the client to possess an Initial Access Token (IAT) beforehand.",
     "https://datatracker.ietf.org/doc/draft-dellaert-oauth-approval-based-dcr/",
     "IETF (OAuth-related, individual)",
     "Revision -00, 20 Jul 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-hemanth-oauth-ai-scopes — OAuth 2.0 Extension for AI Model Access",
     "This document defines an extension to OAuth 2.0 for delegating scoped access to AI model APIs. It introduces a standardized scope syntax, resource indicators for AI providers, and token constraints suitable for AI workloads including spend limits and model restrictions.",
     "https://datatracker.ietf.org/doc/draft-hemanth-oauth-ai-scopes/",
     "IETF (OAuth-related, individual)",
     "Revision -00, 20 Jul 2026. Added in the Aug 2026 corpus sweep; not previously tracked. **EXPIRED on Datatracker** (expired 10 Jul 2026; checked 26 Aug 2026) — kept in the corpus deliberately; an expired draft is still evidence of what was proposed."),

    ("draft-zhang-dmsc-mas-communication — Security Analysis of Multi-agents Secured Communication and Limitations of Existing Protocols",
     "Multi-agents systems (MAS) increasingly cooperate through workflow, orchestrated, and mesh communication patterns. While existing Internet protocols provide confidentiality and endpoint authentication, they were not designed for agent-native semantics such as dynamic identity, computation-bounded requests, context integrity, and intermediary trust.",
     "https://datatracker.ietf.org/doc/draft-zhang-dmsc-mas-communication/",
     "IETF (DMSC-related, individual)",
     "Revision -00, 20 Jul 2026. Added in the Aug 2026 corpus sweep; not previously tracked. **EXPIRED on Datatracker** (expired 20 Jul 2026; checked 26 Aug 2026) — kept in the corpus deliberately; an expired draft is still evidence of what was proposed."),

    ("draft-aravind-oauth-decision-subject — Decision-Subject Representation for Agent Authorization",
     "This document defines dsub, an OPTIONAL, descriptive claim naming the *decision subject*, the party an automated agent's action is taken _upon_, as distinct from the acting agent (act) and the delegating principal (sub).",
     "https://datatracker.ietf.org/doc/draft-aravind-oauth-decision-subject/",
     "IETF (OAuth-related, individual)",
     "Revision -00, 19 Jul 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-coetzee-oauth-spt-txn-tokens — Transaction-Bound Authorization Tokens for Software and AI Agents (SPT-Txn)",
     "Current authorization is role-scoped: an actor is granted a role whose authority persists across every action it takes. This fails exactly when actors fail -- under compromise, prompt injection, or goal hijacking -- because a compromised actor retains full role authority.",
     "https://datatracker.ietf.org/doc/draft-coetzee-oauth-spt-txn-tokens/",
     "IETF (OAuth-related, individual)",
     "Revision -03, 19 Jul 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-mcguinness-oauth-token-exchange-cnf — Confirmation Response Parameter for OAuth 2.0 Token Exchange",
     "This specification defines a cnf response parameter for the OAuth 2.0 Token Exchange (RFC 8693) response. The parameter carries the confirmation method that the authorization server applied to the issued token, enabling clients to verify that sender-constraint binding (for example a DPoP key or mutual-TLS client certificate) was performed without inspecting the issued token.",
     "https://datatracker.ietf.org/doc/draft-mcguinness-oauth-token-exchange-cnf/",
     "IETF (OAuth-related, individual)",
     "Revision -00, 19 Jul 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-skyfire-oauth-id-verification — Identity Verification Methods Values",
     "Knowing how a person's identity was verified can be important when making trust decisions. This specification defines a claim and values for declaring how the person's identity was verified.",
     "https://datatracker.ietf.org/doc/draft-skyfire-oauth-id-verification/",
     "IETF (OAuth-related, individual)",
     "Revision -01, 19 Jul 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-ietf-wimse-mutual-tls — Workload Authentication Using Mutual TLS",
     "The WIMSE architecture defines authentication and authorization for software workloads in a variety of runtime environments, from the most basic ones to complex multi-service, multi-cloud, multi-tenant deployments. This document profiles a workload authentication based on X.509 workload identity certificates using mutual TLS (mTLS).",
     "https://datatracker.ietf.org/doc/draft-ietf-wimse-mutual-tls/",
     "IETF (WIMSE WG)",
     "Revision -02, 6 Jul 2026. WG-adopted draft. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-liu-ai-agent-authorization-integration — AI Agent Authorization Integration Framework",
     "This document describes how to integrate multiple OAuth 2.0 extensions to enable secure authorization for AI agents acting on behalf of users. It combines cross-domain identity, policy-based authorization, user consent evidence, and multi-hop delegation into a cohesive framework for autonomous agent authorization.",
     "https://datatracker.ietf.org/doc/draft-liu-ai-agent-authorization-integration/",
     "IETF (individual draft)",
     "Revision -00, 6 Jul 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-ni-agent-entity-discovery — DNS-based Entity-Level Discovery and End-to-End Connection for AI Agents",
     "This document defines a new DNS resource record type, Agent Entity Discovery (AED), to publish agent-specific trust anchors or direct match constraints for verifying an agent's certificate or token. This enables the cross-domain users or agents to authenticate, and establish secure, end-to-end connections directly with a private- domain agent entity.",
     "https://datatracker.ietf.org/doc/draft-ni-agent-entity-discovery/",
     "IETF (individual draft)",
     "Revision -00, 6 Jul 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-shang-campus-agent-scope-down — Campus Agent Identification and Scope-Down Access Control",
     "AI agents operating in enterprise campus networks execute user- delegated Tasks by invoking multiple tools and services, often without continuous user supervision. Traditional authorization models assume stable applications and human-driven interactions, creating a mismatch when applied to autonomous agents that can chain actions across heterogeneous systems.",
     "https://datatracker.ietf.org/doc/draft-shang-campus-agent-scope-down/",
     "IETF (individual draft)",
     "Revision -01, 6 Jul 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-yang-dmsc-gateway-mediation-layer — Gateway Mediation Layer for AI Agent Collaboration",
     "Cross-domain and policy-controlled agent collaboration can require mediation decisions that are not always suitable for an agent client or an agent server alone.",
     "https://datatracker.ietf.org/doc/draft-yang-dmsc-gateway-mediation-layer/",
     "IETF (DMSC-related, individual)",
     "Revision -00, 5 Jul 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-cui-dawn-mdi-model — An Information Model for Minimum Discoverable Information (MDI)",
     "The Discovery of Agents, Workloads, and Named Entities (DAWN) terminology document defines Minimum Discoverable Information (MDI) as the minimum information an entity must provide to be discoverable, but does not define its field-level content.",
     "https://datatracker.ietf.org/doc/draft-cui-dawn-mdi-model/",
     "IETF (DAWN-related, individual)",
     "Revision -00, 3 Jul 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-liu-oauth-cross-domain-txn-token — Cross-domain Transaction Tokens",
     "This document describes a mechanism for Cross-Domain Transaction Tokens, which enables the safe maintenance and propagation of user identity, workload identities, and authorization context across multiple trust domains.",
     "https://datatracker.ietf.org/doc/draft-liu-oauth-cross-domain-txn-token/",
     "IETF (OAuth-related, individual)",
     "Revision -00, 3 Jul 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-schrock-action-evidence-boundary — The Action Evidence Boundary for Consequential Agent Effects",
     "Consequential agent actions can cross identity, transport, authorization, policy, and execution systems. Each system can produce a valid artifact while the executor still lacks a safe rule for joining the artifacts to the exact effect, consuming one-time authority, and handling an uncertain outcome. This document defines the Action Evidence Boundary (AEB), an executor-side processing model for that lifecycle. AEB requires native artifact verification, Canonical Action Identifier (CAID) matching, Authorization Evidence Chain (AEC) satisfaction, a separate local authorization decision, durable atomic consumption or reservation, invocation, closed effect outcomes, and authenticated reconciliation. It defines no receipt or token format, no policy language, no universal evidence taxonomy, and no new registry. Native workload credentials, message signatures, attested per-action tokens, permit records, authorization receipts, and status mechanisms retain their own semantics and verifiers.",
     "https://datatracker.ietf.org/doc/draft-schrock-action-evidence-boundary/",
     "IETF (individual draft)",
     "Revision -04, checked 26 Aug 2026. **Re-slugged: this draft was tracked as draft-schrock-agent-action-manifest until 26 Aug 2026**, which Datatracker marks Replaced by this one. Row updated to the current name, URL and abstract; the old slug is recorded here so searches for it still land. Previously filed in the corpus as “draft-schrock-agent-action-manifest — The Agent Action Control Manifest: A Public Effect-Boundary Control Plane for Machine Actions”."),

    ("draft-schrock-human-authorization-binding — Binding Named-Human Authorization Evidence into Agent-Action Records",
     "A recurring pattern spans the agent-action record formats now in development: a record about an agent's action reserves a place for \"the human authorization\" — an approver disposition, an authority context, a human-override field, an actor slot, a signed grant, an approval reference — and leaves its semantics undefined.",
     "https://datatracker.ietf.org/doc/draft-schrock-human-authorization-binding/",
     "IETF (individual draft)",
     "Revision -00, 3 Jul 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-xkumakichi-xaip-receipts — Signed Execution Receipts for AI Agent Tool Calls (XAIP Receipts)",
     "This document defines a wire format for signed execution receipts produced by AI agents when they invoke tools, services, or other agents.",
     "https://datatracker.ietf.org/doc/draft-xkumakichi-xaip-receipts/",
     "IETF (individual draft)",
     "Revision -03, 2 Jul 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-yang-dmsc-gateway-semantic-layer — Gateway Mediation Layer for AI Agent Collaboration",
     "Cross-domain and policy-controlled agent collaboration can require mediation decisions that are not always suitable for an agent client or an agent server alone.",
     "https://datatracker.ietf.org/doc/draft-yang-dmsc-gateway-semantic-layer/",
     "IETF (DMSC-related, individual)",
     "Revision -02, 2 Jul 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),


    ("draft-ayoub-agis-agent-identity-system — AgIS: An Agent Identity System for DNS-Backed Verification of AI and Software Agents",
     "This document specifies AgIS, the Agent Identity System, a DNS-backed identity and verification profile for AI agents, autonomous software agents, and agentic services operating on the existing web.",
     "https://datatracker.ietf.org/doc/draft-ayoub-agis-agent-identity-system/",
     "IETF (individual draft)",
     "Revision -00, 29 Jun 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-vicente-oauth-apm — Authorization Posture Mechanism (APM): Per-Transaction Consistency for OAuth 2.0",
     "This document describes the Authorization Posture Mechanism (APM), a method by which an OAuth 2.0 [RFC6749] authorization server, or a resource server acting on its behalf, re-evaluates the mutual consistency of three bound factors -- the client certificate, the access token, and the device posture -- on a per-request basis for privileged operations, rather than only at session…",
     "https://datatracker.ietf.org/doc/draft-vicente-oauth-apm/",
     "IETF (OAuth-related, individual)",
     "Revision -02, 28 Jun 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-duda-agent-id-framework — Self-Certifying Identity and Capability-Based Delegation for Autonomous AI Agents",
     "We present an identity and delegation framework for secure AI agent communications. The framework introduces a set of entities including Client AI Agents, Service AI Agents, Agent Providers, and Agent Brokers, together with a Trustful Mutable Store responsible for maintaining cryptographically verifiable identity bindings.",
     "https://datatracker.ietf.org/doc/draft-duda-agent-id-framework/",
     "IETF (individual draft)",
     "Revision -00, 26 Jun 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-liu-oauth-authorization-evidence — Authorization Evidence and Audit Trail for OAuth 2.0 Access Tokens",
     "This specification defines an authorization details type for including authorization evidence and audit trail information in OAuth 2.0 access tokens using the Rich Authorization Requests (RAR) framework.",
     "https://datatracker.ietf.org/doc/draft-liu-oauth-authorization-evidence/",
     "IETF (OAuth-related, individual)",
     "Revision -01, 22 Jun 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-vandemeent-tibet-provenance — TIBET: Transaction/Interaction-Based Evidence Trail",
     "This document defines TIBET (Transaction/Interaction-Based Evidence Trail), a data model and protocol for constructing cryptographically linked provenance chains over interactions between autonomous agents, human actors, and automated processes. A TIBET token captures four dimensions of provenance: content (ERIN), references (ERAAN), context (EROMHEEN), and intent (ERACHTER).",
     "https://datatracker.ietf.org/doc/draft-vandemeent-tibet-provenance/",
     "IETF (individual draft)",
     "Revision -02, 17 Jun 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-car-agents-txt-wellknown — AGENTS.TXT: Capability Declarations for Web Agents",
     "This document requests registration of two Well-Known URIs under the \"/.well-known/\" path: \"agents.txt\" and \"agents.json\".",
     "https://datatracker.ietf.org/doc/draft-car-agents-txt-wellknown/",
     "IETF (individual draft)",
     "Revision -00, 12 Jun 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-liu-oauth-rego-policy — Rego Policy Language for OAuth 2.0 Authorization",
     "AI agents exhibit dynamic, unpredictable behavior that cannot be fully described by traditional OAuth 2.0 scopes. This specification defines a behavioral authorization framework that enables clients, particularly AI agents, to propose Rego policy-based behavioral constraint contracts in OAuth 2.0 authorization flows using Rich Authorization Requests (RAR).",
     "https://datatracker.ietf.org/doc/draft-liu-oauth-rego-policy/",
     "IETF (OAuth-related, individual)",
     "Revision -00, 12 Jun 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-ekahraman-oauth-attestation-authz-native-app — OAuth 2.0 Attestation Based Authorization for Native Applications",
     "This document defines an extension to OAuth 2.0 [RFC6749] that enables Authorization Servers to consider Attestation Results presented by Native Applications when issuing access grants.",
     "https://datatracker.ietf.org/doc/draft-ekahraman-oauth-attestation-authz-native-app/",
     "IETF (OAuth-related, individual)",
     "Revision -01, 20 Aug 2026 (was -00, 9 Jun 2026). Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-kay-dawn-use-cases — Use Cases for the Discovery of Agents, Workloads, and Named Entities",
     "This document describes broad categories of use cases for the Discovery of Agents, Workloads, and Named Entities (DAWN). The purpose of the document is to illustrate situations in which entities need to discover other entities. This document does not define a discovery protocol, a registration procedure, a selection algorithm, or an agent-to-agent communication protocol.",
     "https://datatracker.ietf.org/doc/draft-kay-dawn-use-cases/",
     "IETF (DAWN-related, individual)",
     "Revision -00, 7 Jun 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-reddy-wimse-workload-attestation — WIMSE Workload Attestation",
     "This document extends the WIMSE workload-to-workload authentication architecture with a mechanism for conveying attestation across TLS- terminating proxies, a deployment topology where TLS-layer attestation mechanisms lose their end-to-end security properties.",
     "https://datatracker.ietf.org/doc/draft-reddy-wimse-workload-attestation/",
     "IETF (WIMSE-related, individual)",
     "Revision -00, 7 Jun 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-madaras-preauth-receipts — PRE-RCT: Pre-Execution Authorization Receipt Format",
     "This document defines PRE-RCT, the Pre-Execution Authorization Receipt, a cryptographically signed and attestation-aware receipt format used to record high-risk authorization events. PRE-RCT is intended for use with pre-execution authorization protocols such as GNA.",
     "https://datatracker.ietf.org/doc/draft-madaras-preauth-receipts/",
     "IETF (individual draft)",
     "Revision -00, 6 Jun 2026. Added in the Aug 2026 corpus sweep; not previously tracked. **EXPIRED on Datatracker** (expired 6 Jun 2026; checked 26 Aug 2026) — kept in the corpus deliberately; an expired draft is still evidence of what was proposed."),

    ("draft-fulz-oauth-trust-binding — OAuth Trust Binding Extension (OTBE)",
     "This document defines the OAuth Trust Binding Extension (OTBE), a mechanism allowing Resource Owners to explicitly authorize which Authorization Servers may assert their identity towards Relying Parties, mitigating silent impersonation and namespace-based identity capture.",
     "https://datatracker.ietf.org/doc/draft-fulz-oauth-trust-binding/",
     "IETF (OAuth-related, individual)",
     "Revision -00, 30 May 2026. Added in the Aug 2026 corpus sweep; not previously tracked. **EXPIRED on Datatracker** (expired 31 May 2026; checked 26 Aug 2026) — kept in the corpus deliberately; an expired draft is still evidence of what was proposed."),


    ("draft-drake-agent-identity-registry — Agent Identity Registry System: A Federated Architecture for Hardware-Anchored Identity of Autonomous Entities",
     "The Internet's identity infrastructure assumes human principals. As autonomous entities -- AI agents, robotic systems, and other non- human actors -- increasingly participate in both Internet protocols and physical society, no existing standard provides them with persistent, verifiable, hardware-anchored identity.",
     "https://datatracker.ietf.org/doc/draft-drake-agent-identity-registry/",
     "IETF (individual draft)",
     "Revision -03, 22 May 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-iannone-dawn-privacy-considerations — Privacy Considerations for the Discovery of Agents, Workloads, and Named Entities (DAWN)",
     "This document describes the privacy issues associated with the Discovery of Agents, Workloads, and Named Entities (DAWN). It provides general observations about typical current privacy practices in similar domains like, DNS, HTTP, and in general privacy in information retrieval.",
     "https://datatracker.ietf.org/doc/draft-iannone-dawn-privacy-considerations/",
     "IETF (DAWN-related, individual)",
     "Revision -00, 22 May 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-jiang-seat-dynamic-attestation — Dynamic Attestation for AI Agent Communication",
     "This document describes a use case for conveying remote attestation information in association with Transport Layer Security (TLS) sessions in the context of AI agent communication.",
     "https://datatracker.ietf.org/doc/draft-jiang-seat-dynamic-attestation/",
     "IETF (RATS/SEAT-related, individual)",
     "Revision -00, 17 May 2026. Added in the Aug 2026 corpus sweep; not previously tracked. **EXPIRED on Datatracker** (expired 17 May 2026; checked 26 Aug 2026) — kept in the corpus deliberately; an expired draft is still evidence of what was proposed."),

    ("draft-novak-rats-twi-attestation — Remote Attestation for Trustworthy Workload Identity",
     "Trustworthy Workloads are workloads that operate in environments that provide isolation of data in use. This document describes how Trustworthy Workloads can acquire credentials containing stable identifiers, upon proving the trust in the environments in which they operate via Remote Attestation.",
     "https://datatracker.ietf.org/doc/draft-novak-rats-twi-attestation/",
     "IETF (RATS/SEAT-related, individual)",
     "Revision -00, 9 May 2026. Added in the Aug 2026 corpus sweep; not previously tracked. **EXPIRED on Datatracker** (expired 9 May 2026; checked 26 Aug 2026) — kept in the corpus deliberately; an expired draft is still evidence of what was proposed."),

    ("draft-jimenez-agent-directory — Agent Directory",
     "This document defines the Agent Directory (AD), a service where agents register their identity, capabilities, and reachable endpoints and where clients discover them by capability.",
     "https://datatracker.ietf.org/doc/draft-jimenez-agent-directory/",
     "IETF (individual draft)",
     "Revision -01, 8 May 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-hardt-aauth-bootstrap — AAuth Bootstrap Guidance",
     "This document provides informational guidance for agent providers (APs) on enrolling agents and issuing AAuth agent tokens defined in [I-D.hardt-oauth-aauth-protocol]. It covers per-platform key handling, optional platform attestation, agent identifier strategies, and refresh patterns.",
     "https://datatracker.ietf.org/doc/draft-hardt-aauth-bootstrap/",
     "IETF (individual draft)",
     "Revision -01, 6 May 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-abbott-mcp-ax — MCP Aggregation Protocol (MCP-AX): Hierarchical Tool Namespace Delegation for Model Context Protocol Servers",
     "This document specifies MCP-AX, an aggregation protocol for Model Context Protocol (MCP) servers. MCP-AX enables hierarchical composition of tool namespaces across heterogeneous networks of MCP servers, from cloud services to resource-constrained embedded devices.",
     "https://datatracker.ietf.org/doc/draft-abbott-mcp-ax/",
     "IETF (individual draft)",
     "Revision -00, 5 May 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),

    ("draft-hori-agent-quality-graph — Agent Quality Graph (AQG): A Protocol for Evaluating AI Agent Trustworthiness via Delegation Graphs",
     "This document describes the Agent Quality Graph (AQG) protocol, a method for evaluating and ranking AI agent trustworthiness based on delegation transaction graphs. As the number of autonomous AI agents grows rapidly, there is no standardized mechanism for determining which agents reliably complete delegated tasks.",
     "https://datatracker.ietf.org/doc/draft-hori-agent-quality-graph/",
     "IETF (individual draft)",
     "Revision -00, 2 May 2026. Added in the Aug 2026 corpus sweep; not previously tracked."),


    # ---- Reinstated 11 Aug 2026: Skyfire KYA/KYAPay + Hopley x402 receipt clusters ----

    ("draft-hopley-x402-cancellation-receipt — Categorical Mandate Cancellation Receipt Format for Agentic-Payment Flows",
     "This document specifies a categorical mandate cancellation receipt format for agentic-payment flows. The format records that a recurring-payment mandate or other standing payer-to-payee authorisation has been cancelled, by whom, for what reason, and with what effective date.",
     "https://datatracker.ietf.org/doc/draft-hopley-x402-cancellation-receipt/",
     "IETF (individual draft)",
     "Revision -01, 25 May 2026. Hopley x402 agentic-payment receipt cluster (4 drafts: compliance, settlement, refund, cancellation) — categorical receipt formats for agent-initiated payment flows. Reinstated 11 Aug 2026 after initially being filtered out of the Aug 2026 sweep as payments-infra."),

    ("draft-hopley-x402-compliance-receipt — Categorical Compliance Screening Receipt Format for Agentic-Payment Flows",
     "This document specifies a categorical compliance screening receipt format for agentic-payment flows.",
     "https://datatracker.ietf.org/doc/draft-hopley-x402-compliance-receipt/",
     "IETF (individual draft)",
     "Revision -02, 25 May 2026. Hopley x402 agentic-payment receipt cluster (4 drafts: compliance, settlement, refund, cancellation) — categorical receipt formats for agent-initiated payment flows. Reinstated 11 Aug 2026 after initially being filtered out of the Aug 2026 sweep as payments-infra."),

    ("draft-hopley-x402-refund-receipt — Categorical Refund Receipt Format for Agentic-Payment Flows",
     "This document specifies a categorical refund receipt format for agentic-payment flows.",
     "https://datatracker.ietf.org/doc/draft-hopley-x402-refund-receipt/",
     "IETF (individual draft)",
     "Revision -02, 25 May 2026. Hopley x402 agentic-payment receipt cluster (4 drafts: compliance, settlement, refund, cancellation) — categorical receipt formats for agent-initiated payment flows. Reinstated 11 Aug 2026 after initially being filtered out of the Aug 2026 sweep as payments-infra."),

    ("draft-hopley-x402-settlement-attestation — Categorical Settlement Attestation Format for Agentic-Payment Flows",
     "This document specifies a categorical settlement attestation format for agentic-payment flows. The format records that a payment has reached a particular settlement state on a particular chain, at a particular instant, under the attesting party's risk model. The receipt format uses a closed enumeration of categorical outcomes (SETTLED, PENDING_FINALITY, REVERSED).",
     "https://datatracker.ietf.org/doc/draft-hopley-x402-settlement-attestation/",
     "IETF (individual draft)",
     "Revision -01, 25 May 2026. Hopley x402 agentic-payment receipt cluster (4 drafts: compliance, settlement, refund, cancellation) — categorical receipt formats for agent-initiated payment flows. Reinstated 11 Aug 2026 after initially being filtered out of the Aug 2026 sweep as payments-infra."),

    ("draft-skyfire-oauth-aml-methods — Anti-Money Laundering Methods Values",
     "Financial regulations require application of Anti-Money Laundering (AML) and Countering the Financing of Terrorism (CFT) methods in many jurisdictions worldwide. This specification defines a claim and values for declaring what AML/CFT methods were employed.",
     "https://datatracker.ietf.org/doc/draft-skyfire-oauth-aml-methods/",
     "IETF (OAuth-related, individual)",
     "Revision -00, 19 Jul 2026. Skyfire KYA/KYAPay cluster (6 drafts incl. draft-skyfire-oauth-id-verification already in corpus) — agent identity verification and payment claims for OAuth/JWT. Reinstated 11 Aug 2026 after initially being filtered out of the Aug 2026 sweep as payments-infra."),

    ("draft-skyfire-oauth-amr-values — Additional Authentication Method Reference Values",
     "The JWT \"amr\" (Authentication Methods References) claim contains values conveying authentication methods used in the authentication. This specification defines additional Authentication Method Reference values beyond those already registered to represent additional authentication methods in use today.",
     "https://datatracker.ietf.org/doc/draft-skyfire-oauth-amr-values/",
     "IETF (OAuth-related, individual)",
     "Revision -01, 19 Jul 2026. Skyfire KYA/KYAPay cluster (6 drafts incl. draft-skyfire-oauth-id-verification already in corpus) — agent identity verification and payment claims for OAuth/JWT. Reinstated 11 Aug 2026 after initially being filtered out of the Aug 2026 sweep as payments-infra."),

    ("draft-skyfire-oauth-kyapay-token — KYAPay Token",
     "This document defines a token format for agent identity and payment tokens in JSON Web Token (JWT) format. Authorization servers and resource servers from different vendors can leverage this token format to consume identity and payment tokens in an interoperable manner.",
     "https://datatracker.ietf.org/doc/draft-skyfire-oauth-kyapay-token/",
     "IETF (OAuth-related, individual)",
     "Revision -01, 19 Jul 2026. Skyfire KYA/KYAPay cluster (6 drafts incl. draft-skyfire-oauth-id-verification already in corpus) — agent identity verification and payment claims for OAuth/JWT. Reinstated 11 Aug 2026 after initially being filtered out of the Aug 2026 sweep as payments-infra."),

    ("draft-skyfire-oauth-kyapay-token-exchange — KYAPay Token Exchange",
     "This specification describes how KYAPay tokens can be exchanged for OAuth access tokens to dynamically grant agents access to resources they need to accomplish their mission.",
     "https://datatracker.ietf.org/doc/draft-skyfire-oauth-kyapay-token-exchange/",
     "IETF (OAuth-related, individual)",
     "Revision -01, 19 Jul 2026. Skyfire KYA/KYAPay cluster (6 drafts incl. draft-skyfire-oauth-id-verification already in corpus) — agent identity verification and payment claims for OAuth/JWT. Reinstated 11 Aug 2026 after initially being filtered out of the Aug 2026 sweep as payments-infra."),

    ("draft-skyfire-oauth-using-kyapay-tokens — Using KYAPay Tokens",
     "The KYAPay Token is a JSON Web Token (JWT) that carries verified identity (\"Know Your Agent\", KYA) and payment (PAY) information for requests made by software agents on behalf of human principals.",
     "https://datatracker.ietf.org/doc/draft-skyfire-oauth-using-kyapay-tokens/",
     "IETF (OAuth-related, individual)",
     "Revision -00, 19 Jul 2026. Skyfire KYA/KYAPay cluster (6 drafts incl. draft-skyfire-oauth-id-verification already in corpus) — agent identity verification and payment claims for OAuth/JWT. Reinstated 11 Aug 2026 after initially being filtered out of the Aug 2026 sweep as payments-infra."),


    # ---- 26 Aug 2026 Datatracker sweep — new individual + WG drafts ----
    # 68 recently-active candidates found; 39 kept under the 11 Aug 2026 curation bar.
    # Notable: one new OAuth WG draft (rar-metadata-remediation), the six-draft Morrison
    # ~handle identity family, and the NHE / VERA / AgentEnvelope autonomy-gating cluster.

    ("draft-morrison-mcp-tool-surface-names-registry — An IANA Registry for Model Context Protocol Tool Surface Names",
     "This document requests the establishment of an IANA registry for Model Context Protocol [MCP-SPEC] tool surface names. A tool surface name is the wire-level identifier by which a client invokes a typed capability on an MCP server. Existing Morrison- family Internet- Drafts ([ORGALTER]) request IANA registration of specific surface names against a registry that does not yet exist. This document establishes the registry mechanism so that subsequent specifications can register names without restating the registry's structure or registration procedure. The registry uses Specification Required registration with a Designated Expert pool [RFC8126]. Initial contents are the four surface names registered by [ORGALTER]. Vendor-prefix conventions are recommended but not mandated.",
     "https://datatracker.ietf.org/doc/draft-morrison-mcp-tool-surface-names-registry/",
     "IETF (individual)",
     "Revision -01, 11 Aug 2026. Requests an IANA registry for MCP tool surface names. Morrison family plumbing — exists because other Morrison drafts already request registrations against a registry that does not yet exist. Structural, not conceptual, but it is the family's dependency root."),

    ("draft-morrison-identity-pronouns — Identity Pronouns: A Reference-Axis Extension to ~handle Identity Systems",
     "This document defines an identity pronoun grammar as a reference axis orthogonal to the ~handle identity tier taxonomy defined in [MCPDNS] and [IDCOMMITS]. A pronoun is a session-scoped reference that resolves client-side to a concrete handle using local session state before any cryptographic, DNS, or federation operation. The entity- class taxonomy (Sovereign, Bot, Instrument) is unchanged; this specification introduces Absolute vs Pronoun as an orthogonal axis. A pronoun MUST NOT appear in a capability token, in a DNS record, in an Accord signature, or in any inter-organisational protocol payload. The reference implementation defines a single Wave-1 pronoun, ~org, that resolves to the concrete handle of the organisation bound to the caller's current session. An appendix defines a relative-path pronoun grammar (e.g. ~./architect, ~../weaver) as a non-normative design surface for future work. The mechanism is provider-neutral, introduces no new cryptographic primitive, and imposes zero new load on DNS, capability-token issuers, or federated resolvers.",
     "https://datatracker.ietf.org/doc/draft-morrison-identity-pronouns/",
     "IETF (individual)",
     "Revision -02, 11 Aug 2026. Session-scoped 'pronoun' references that resolve client-side to concrete ~handle identities. Morrison family. Kept under the primary-body rule rather than on individual merit: the family is taken in full. Design note worth flagging — a pronoun MUST NOT appear in a capability token, DNS record, or Accord signature, which is an explicit boundary between local reference and wire-visible identity."),

    ("draft-morrison-identity-attributed-commits — Identity-Attributed Git Commits via Tier-Structured Trailers",
     "This document defines a git commit trailer grammar for identity- attributed contributions using the ~handle identity primitive defined in [MCPDNS]. The grammar binds sovereign actors, automated bots, and AI instruments to specific commits via three tier-structured trailers (Acted-By, Executed-By, Drafted-With) and three optional cryptographic trailers (Identity-Signature, Identity-Key-Id, Identity-Anchor). The signature is computed with Ed25519 over the commit's tree hash rather than its commit hash, preserving attribution across rebase, cherry-pick, and squash merge operations. Conformant parsers reject cross-tier category errors (e.g., an Instrument-tier handle in an Acted-By slot) as malformed. The mechanism is provider-neutral, depends only on DNS [RFC1035] and the ~handle resolution algorithm of [MCPDNS], and requires no central authority or platform-specific verification service.",
     "https://datatracker.ietf.org/doc/draft-morrison-identity-attributed-commits/",
     "IETF (individual)",
     "Revision -02, 11 Aug 2026. Git commit trailers (Acted-By / Executed-By / Drafted-With) binding sovereign actors, bots and AI instruments to specific commits. Morrison family. The three-tier actor taxonomy is a direct echo of the actor-chain question in draft-mcguinness-oauth-actor-profile and draft-mw-oauth-actor-chain, expressed in a completely different substrate. Ed25519 over the tree hash rather than the commit hash so attribution survives rebase and squash."),

    ("draft-morrison-agent-channel-fan-out — An Agent-Channel Frame for Identity-Keyed Fan-Out Delivery to Concurrent Sessions",
     "This memo specifies an application-layer frame format and a delivery model by which the several concurrent agentic sessions of a single identity-bound principal, and the recognised members of an organisational identity substrate, exchange short structured messages. The frame, termed the agent-channel frame, is a transport envelope: it carries a closed-catalogue kind discriminator, a structured per-kind payload, an identity attribution pair, and an inline provenance block. Delivery is fan-out: a sender names a recipient scope rather than a single endpoint, and the scope is expanded at delivery time against the recipient's subscriptions. Recipients receive frames over a per-handle Server-Sent Events stream and MAY narrow what they receive with a subscribe-time filter expression. Frames are ephemeral routing units; the memo specifies only the wire envelope, the scope-expansion grammar, the subscribe filter grammar, and the delivery semantics. Frame persistence, where an implementation chooses to retain frames for replay, is out of scope and is not specified. The memo composes with the handle namespace of [IDPRONOUNS], the discovery surface of [MCPDNS], and the cross-organisational ceremony of [IDACCORD]; no new transport and no new handle category is introduced.",
     "https://datatracker.ietf.org/doc/draft-morrison-agent-channel-fan-out/",
     "IETF (individual)",
     "Revision -01, 11 Aug 2026. Application-layer frame for identity-keyed fan-out delivery to the concurrent sessions of one identity-bound principal. Morrison family. Transport-shaped, but kept because the frame carries an identity attribution pair and inline provenance block — it is an identity-binding format, not a routing protocol."),

    ("draft-hillier-certisyn-ai-governance-verified — AI Governance Verified -- A Cryptographic Verification Standard for Agentic AI Governance in Regulated Industries",
     "This document specifies a verification standard for the cryptographic attestation of agentic AI governance in regulated industries. It defines the Verification Reconciliation Object (VRO), the issuing- partner framework, the eight control areas through which AI governance posture is reconciled, three maturity-attestation levels (Documented, Operational, Adversarial-ready), and the cryptographic continuity requirements that together produce deterministic, independently reconstructable, auditor-grade attestations of agentic AI governance. The standard sits beneath ISO/IEC 42001:2023, the NIST AI Risk Management Framework, and other agentic AI governance frameworks, and produces the verifiable artefact those frameworks were designed to imply but do not deliver.",
     "https://datatracker.ietf.org/doc/draft-hillier-certisyn-ai-governance-verified/",
     "IETF (individual)",
     "Revision -02, 12 Aug 2026. Cryptographic attestation of agentic AI governance posture for regulated industries: the Verification Reconciliation Object, eight control areas, three maturity-attestation levels. Positioned beneath ISO/IEC 42001:2023, so it is the compliance-facing counterpart to the audit-architecture work. Hillier has two further drafts in this sweep (scitt-arp, coverage-attestation) that were dropped as non-agent supply-chain work — revisit if the author's direction turns agent-specific."),

    ("draft-winmagic-oauth-condition-bound-keys — Condition-Bound Keys for Mutual-TLS Client Authentication and DPoP",
     "Login and session protection are two markets solving one problem: verify identity before giving access. Online, access is mostly the transaction, so that is where identity should be verified. Done this way, there is no session and no login; identity assurance is embedded in the transaction: it is encrypted by a key only the right identity has. The key that does this exists only where an actor -- human or machine -- a platform, and local policy hold, now. It disappears when the conditions are no longer met. All three are observed on the endpoint. It is hardware-rooted by default and non-exfiltratable, existing nowhere else, and its presence means validity: the identity is live now. This document specifies that key and its uses: under mutual TLS, in a DPoP proof, as a raw public key, in Device Bound Session Credentials, and as a FIDO2 passkey, or in a non-FIDO mode carrying user verification without user interaction.",
     "https://datatracker.ietf.org/doc/draft-winmagic-oauth-condition-bound-keys/",
     "IETF (OAuth-related, individual)",
     "Revision -00, 12 Aug 2026. Binds mTLS client authentication and DPoP keys to conditions rather than to a bare key identity. Files cleanly into the OAuth wiki's **Proof of Possession** cluster, which the 11 Aug 2026 mapping flagged as showing 'Active Drafts: (none)' — this is further evidence that agent-era drafts should be filed by mechanism rather than by being agent-flavoured."),

    ("draft-maintainer-1f916-agent-record — The Agent Record: Transparent, Witness-Countersigned Event Logs for AI Agent Identity, History, and Memory",
     "Autonomous AI agents increasingly act as economic parties: they are hired, they pay, and they make claims about their own past conduct. No deployed standard lets a relying party verify an agent's identity continuity, the integrity of its claimed history, or the intactness of its persisted memory without trusting the agent's operator or platform. This document describes the Agent Record architecture: per-agent append-only event logs bound to Ed25519 keys, checkpointed with signed Merkle tree heads following the RFC 6962 construction, countersigned by independent witnesses, and exported as portable, offline-verifiable dossiers. Memory integrity is anchored by hash commitments recorded in the log, allowing an agent's future sessions, and any third party, to detect tampering with persisted state. The architecture is deployed in production at a founding registry; this document records its wire formats and security model to invite independent implementation and review, and to align terminology with the SCITT architecture, of which this system is an application- specific instance.",
     "https://datatracker.ietf.org/doc/draft-maintainer-1f916-agent-record/",
     "IETF (individual)",
     "Revision -01, 13 Aug 2026. Per-agent append-only event logs bound to Ed25519 keys, checkpointed with signed Merkle tree heads on the RFC 6962 construction and countersigned by independent witnesses. **Unusual authorship signal: the draft's author slug is `maintainer-1f916` — U+1F916 is the robot-face emoji codepoint.** Treat provenance with care. The technical premise is serious and rare: agents as economic parties that make claims about their own past conduct, verifiable without trusting the operator or platform."),

    ("draft-sirkkavaara-vaara-receipt — The Vaara Receipt: A Recomputable Receipt Format for Decisions About Autonomous Actions",
     "This document specifies vaara.receipt/v1, a signed and independently recomputable record that binds a decision about an autonomous action to the evidence the decision was made on, and optionally to one or more external timestamp anchors. The format is canonicalized with the JSON Canonicalization Scheme (JCS) so that any third party can recompute its digests and verify its signature without access to the issuer. A decision and the execution receipt that answers it form one recomputable pair through the envelope's back link. The receipt's trust is root-agnostic: the same record is verifiable with or without a hardware trusted execution environment and is re- expressible as an IETF RATS Entity Attestation Result. Downstream specifications (a payment rail, a compliance regime, a framework integration) define profiles that pin to a version of this document and add only their own evidence schema; they do not redefine the envelope. The format described here is deployed, and its receipts are independently recomputable from public conformance vectors that ship with standalone checkers importing no issuer code. The minimal profile is a governance decision over a single autonomous action, bound to the action's own intent with no external rail; it is the floor of the format, and a reference library offers a matching adoption floor at the API layer as a one-line decorator over the governed function.",
     "https://datatracker.ietf.org/doc/draft-sirkkavaara-vaara-receipt/",
     "IETF (individual)",
     "Revision -07, 13 Aug 2026. A *recomputable* receipt format for decisions about autonomous actions — at -07, one of the more mature individual receipt drafts in the corpus. Recomputability is the distinguishing claim: the receipt is not merely signed evidence but re-derivable, which is a stronger property than the Decision Evidence Records in the Mission-Bound runtime-enforcement profile."),

    ("draft-ruvalcaba-nhe-identity — NHE Identity: A Verifiable Key-Committed Identity and Genesis-Attestation Format for Autonomous Agents",
     "This document specifies how a Non-Human Entity (NHE) is identified and how one party verifies another's identity. An NHE identity is a verifiable cryptographic commitment: control of an identity key, bound by an append-only hash chain to the entity's genesis and to the lineage of its configuration, rather than a mere name. The document defines the identity chain data model (record structure, genesis sentinel, linkage rule, and the no-fork property), a proof-of-control challenge/response, an optional capability attestation that reveals a specific capability without revealing the rest of the configuration, and an optional hardware-rooted genesis-attestation profile. The data model is specified here; the concrete on-the-wire encoding is deferred to the next revision.",
     "https://datatracker.ietf.org/doc/draft-ruvalcaba-nhe-identity/",
     "IETF (individual)",
     "Revision -00, 13 Aug 2026. Verifiable key-committed identity plus genesis-attestation format for autonomous agents. First half of the NHE pair; the genesis attestation (proving how the agent came into existence) is a stronger origin claim than the instance assertions in draft-mcguinness-oauth-ai-agent-instance."),

    ("draft-ruvalcaba-nhe-authz — NHE Backchannel Authorization: Graduated Autonomy and Intent-Scoped Credentials for Autonomous Agent Actions",
     "This document specifies how a consequential action attempted by a Non-Human Entity (NHE) is authorized at the time it is attempted. A security runtime transparently intercepts an entity's outbound action, so the entity holds no standing credentials, and classifies it under graduated autonomy as autonomous, supervised, or denied. A supervised action triggers a backchannel approval flow that presents a human approver with a human-readable rendering of the exact operation; on approval the runtime issues an intent-scoped, single- use, short-lived credential cryptographically bound to that specific action, which an enforcement point verifies against the operation actually being forwarded. The same canonical parameter digest scopes the credential and appears in the human-facing description, so the approver provably authorizes exactly what the credential permits. The flow and credential data model are specified here; the wire encoding is deferred to the next revision.",
     "https://datatracker.ietf.org/doc/draft-ruvalcaba-nhe-authz/",
     "IETF (individual)",
     "Revision -00, 13 Aug 2026. Backchannel authorization with **graduated autonomy** and intent-scoped credentials. Second half of the NHE pair. 'Graduated autonomy' and 'intent-scoped' are close cousins of the Mission-Bound Conformance Ladder (L0–L5) and mission_intent RAR envelope respectively, arrived at independently — worth comparing directly."),

    ("draft-daniel-ai-agent-internet-architecture — Architectural Requirements for Supporting AI Agents on the Internet",
     "Autonomous AI agents are evolving from interactive assistants into networked software workloads that discover services, invoke tools, delegate authority, transact, communicate with other agents, and act asynchronously on behalf of humans and organizations. Existing Internet protocols provide strong foundations, but agent autonomy, dynamic delegation, machine-speed execution, and cross-domain interaction create requirements that span multiple protocol families. This document describes architectural requirements for supporting AI agents on the Internet across naming and discovery, HTTP, authentication, authorization and delegation, TLS and workload identity, asynchronous messaging, capability and intent-based resolution, payments, provenance, auditability, revocation, security, and privacy. It favors profiling and extending existing Internet protocols over defining a monolithic new agent protocol, and identifies the need for IETF-wide architectural coordination.",
     "https://datatracker.ietf.org/doc/draft-daniel-ai-agent-internet-architecture/",
     "IETF (individual)",
     "Revision -00, 13 Aug 2026. Architectural requirements for supporting AI agents on the Internet. A framework document rather than a mechanism — belongs with the adjacent/cross-cutting cluster alongside the other applicability and architecture statements."),

    ("draft-gaikwad-agent-proxy-modes — Proxy Modes for Agent-Tool Protocols",
     "Agent-tool protocols such as the Model Context Protocol (MCP) enable AI applications to discover and invoke external tools, resources, and prompts through a standardized JSON-RPC interface. As deployments scale, intermediaries (proxies, gateways, sidecars) are inserted between clients and servers to provide transport adaptation, capability aggregation, security enforcement, and operational governance. No specification currently defines the behavioral requirements for such intermediaries. This document establishes a taxonomy of proxy modes, a layered architecture for pluggable proxy functionality, and normative requirements for each mode. It is designed to be protocol- agnostic in its architecture while referencing MCP as the primary instantiation.",
     "https://datatracker.ietf.org/doc/draft-gaikwad-agent-proxy-modes/",
     "IETF (individual)",
     "Revision -00, 14 Aug 2026. Proxy modes for agent-tool protocols. Enumerates how an intermediary sits between agent and tool, which is precisely where authority is most often silently laundered — the delegation-mechanics question the actor-chain drafts raise, at the proxy layer."),

    ("draft-cui-dmsc-agent-cdi — Cross-Domain Interoperability Framework for AI Agent Collaboration",
     "This document defines a framework for enabling seamless cross-domain interoperability among AI agents operating across different networks, administrative domains, and heterogeneous platforms. The framework addresses the challenges of identity federation, trust establishment, policy harmonization, and secure communication that arise when AI agents from distinct administrative realms need to collaborate on shared tasks. It specifies mechanisms for agent discovery, capability negotiation, trust delegation, and federated policy enforcement, enabling scalable and secure multi-domain AI collaboration without requiring centralized control.",
     "https://datatracker.ietf.org/doc/draft-cui-dmsc-agent-cdi/",
     "IETF (DMSC-related, individual)",
     "Revision -00, 14 Aug 2026. Cross-domain interoperability framework for AI agent collaboration. DMSC family. Directly on the axis the approved OAuth charter now names — 'automated agents act across multiple administrative domains' — but approached from the DMSC gateway tradition rather than from OAuth. **EXPIRED on Datatracker** (expired 15 Aug 2026; checked 26 Aug 2026) — kept in the corpus deliberately; an expired draft is still evidence of what was proposed."),

    ("draft-jia-oauth-scope-aggregation — OAuth 2.0 Scope Aggregation for Multi-Step AI Agent Workflows",
     "This document describes a scope-aggregated OAuth 2.0 authorization pattern for multi-step AI agent workflows. An AI agent aggregates the scopes required across a workflow and only initiates a single authorization procedure for the aggregated scope. This reduces repeated user consents and multiple authorization round-trips, improving authorization efficiency.",
     "https://datatracker.ietf.org/doc/draft-jia-oauth-scope-aggregation/",
     "IETF (OAuth-related, individual)",
     "Revision -01, 14 Aug 2026. Scope aggregation across multi-step AI agent workflows. Worth reading against the Mission-Bound line, which argues the opposite direction: Mission-Bound attenuates and binds authority to one approved task, while aggregation composes scope across steps. A genuine design fork in how multi-step agent authority should accumulate."),

    ("draft-feng-dmsc-intent-routing-requirements — Requirements for Intent Routing in Multi-Agent Systems at Internet Scale",
     "The rapid proliferation of autonomous AI agents across enterprise and Internet-scale deployments creates a structural challenge that existing agent frameworks cannot address: how to enable any agent to reach and invoke any other agent's capabilities without pre- established bilateral integration, across organizational boundaries, at Internet scale. This document states the normative requirements for that problem. It prescribes no solution, no specific mechanism, no message format, and no assumption of centralized or distributed architecture. Its purpose is to establish a verifiable yardstick against which any claimed \"intent routing\" solution can be judged.",
     "https://datatracker.ietf.org/doc/draft-feng-dmsc-intent-routing-requirements/",
     "IETF (DMSC-related, individual)",
     "Revision -00, 14 Aug 2026. Normative requirements for intent routing in multi-agent systems at Internet scale — deliberately prescribes no mechanism or message format. DMSC family, joining dunbar, wang and cui. Kept despite its routing framing because the problem it states (any agent reaching any other across organizational boundaries without bilateral integration) is the discovery precondition for cross-domain delegation."),

    ("draft-gazitt-oauth-authzen-claims — AuthZEN Profile for Authorization Claims in JWT Access Tokens",
     "RFC 9068 recommends that an authorization server placing group memberships, roles, or entitlements in a JWT access token draw those claims from the SCIM user schema. It says what the claims are named and how their values are encoded, and it does not say where an authorization server obtains them. In deployments today they come from a directory, a database, or a vendor-specific hook, and the question they answer is an authorization question asked of something that is not the authorization system. This document profiles the Resource Search API of the OpenID AuthZEN Authorization API for that purpose. It binds each authorization claim to a search, defines how a search result set becomes a claim value, and requires that a search result never influence whether a token is issued or what authority it conveys. It may be applied on its own, by an authorization server that externalizes claim enrichment but not its issuance decision, or alongside the companion framework document that externalizes the decision.",
     "https://datatracker.ietf.org/doc/draft-gazitt-oauth-authzen-claims/",
     "IETF (OAuth-related, individual)",
     "Revision -00, 14 Aug 2026. AuthZEN profile for carrying authorization claims in JWT access tokens. **Third Gazitt AuthZEN draft** in the corpus after gazitt-oauth-authzen-issuance and gazitt-oauth-authzen-token-exchange. Strengthens the open observation recorded 11 Aug 2026: the Gazitt drafts fit none of the ten OAuth spec clusters because they concern *who decides, on what evidence* rather than how authority moves. That candidate decision/policy cluster is now seven drafts, not six."),

    ("draft-hawkins-scitt-attested-agent-payment — Attested Payment Authorization for Autonomous Agents",
     "Autonomous software agents increasingly initiate payments on behalf of principals. Existing agent-payment mechanisms authenticate the human principal, the operator, or possession of a key; none of them establishes that the software authorized to spend is the software that was reviewed. A key held by a compromised or silently modified agent authenticates exactly as well as one held by an honest agent. This document defines a payment authorization scope bound to a key whose protection properties are attested by hardware, and registers the resulting authorization as a Signed Statement on an SCITT Transparency Service. The binding reuses the EAT confirmation and key-attributes claims without modification; the contribution is the authorization scope, the verification procedure a payment executor performs before settlement, the transparency record that makes the authorization artifact and its registration auditable independently of the agent and of the executor, and an execution-record mechanism that makes the executor's aggregate accounting auditable on challenge. What is registered evidences the authorization; it does not evidence that the verification procedure was performed for any given settlement.",
     "https://datatracker.ietf.org/doc/draft-hawkins-scitt-attested-agent-payment/",
     "IETF (individual)",
     "Revision -01, 15 Aug 2026. Attested payment authorization for autonomous agents, on the SCITT substrate. Kept while the rest of this sweep's SCITT tail was dropped, because the subject is agent payment *authorization* rather than supply-chain transparency. Pairs with draft-hawkins-x402-dns-discovery from the same author."),

    ("draft-xu-mcp-agent-did-framework — DID-Based Service Discovery, Authentication, and Authorization Framework for MCP Agents",
     "This document proposes a DID-based framework for service discovery, authentication, and authorization of MCP (Model Context Protocol) Agents, based on the W3C Decentralized Identifier (DID) standard. The framework uses the did:web and did:key methods to provide verifiable, decentralized identifiers for MCP Clients and Servers. It defines DID method selection, DID Document extensions, service discovery mechanisms (including URL derivation, DNS-based discovery, and directory-based capability queries), and a challenge-response mutual authentication protocol. The framework also describes coexistence with OAuth 2.0 and enables trust establishment, dynamic capability-based service discovery, and fine-grained authorization with portable identities.",
     "https://datatracker.ietf.org/doc/draft-xu-mcp-agent-did-framework/",
     "IETF (individual)",
     "Revision -00, 15 Aug 2026. DID-based service discovery, authentication and authorization for MCP agents. One of the few DID-substrate entries in the corpus; covers all three of discovery, authn and authz in a single framework, which is unusually broad scope for a -00."),

    ("draft-berlinai-vera — VERA: Verifiable Enforcement for Runtime Agents",
     "AI agents take real actions with real data at machine speed. Compromised AI agents pose significant risks including data exfiltration, unauthorized financial transactions, and cascading failures across downstream systems. This document introduces VERA (Verifiable Enforcement for Runtime Agents), a zero trust reference architecture that provides a structured threat model, five enforcement pillars with typed schemas, four formally stated security properties, and an evidence-based maturity runtime where agents earn autonomy through cryptographic proof rather than calendar time.",
     "https://datatracker.ietf.org/doc/draft-berlinai-vera/",
     "IETF (individual)",
     "Revision -00, 16 Aug 2026. VERA: a zero-trust reference architecture with five enforcement pillars, four formally stated security properties, and an evidence-based maturity runtime. The headline design claim — **agents earn autonomy through cryptographic proof rather than calendar time** — is the same instinct as the Mission-Bound runtime-enforcement profile's per-decision evidence records, framed as an architecture rather than an OAuth profile. **EXPIRED on Datatracker** (expired 16 Aug 2026; checked 26 Aug 2026) — kept in the corpus deliberately; an expired draft is still evidence of what was proposed."),

    ("draft-wolfe-faf-agent — FAFA: A Declarative Agent Capability Format",
     "This document specifies the FAF Agent Format (.fafa): a declarative, YAML-based format for an agent's identity, the capabilities it exposes, and the endpoints through which it is reached. A .fafa document describes an agent; it never instructs one. .fafa (application/vnd.fafa+yaml, IANA-registered June 2026 in the vendor tree) is the agent member of the FAF family, alongside .faf (project context) and .fafm (agent memory). It functions as a portable passport that answers four questions: who the agent is, what it may do, where it is reached, and what it must never do. Protocol- native cards (for example A2A Agent Cards and MCP Server Cards) remain useful wire formats; repository instruction files such as AGENTS.md remain the ops briefing; .fafa complements them as a house- neutral source of truth that can be projected into those formats; it does not replace them. This document documents the existing IANA vendor-tree registration. No standards-tree registration is requested. A companion white paper, \"Why Agents Need a Passport,\" provides the production rationale and lifecycle framing.",
     "https://datatracker.ietf.org/doc/draft-wolfe-faf-agent/",
     "IETF (individual)",
     "Revision -01, 16 Aug 2026. FAFA (.fafa): a declarative YAML capability format describing an agent's identity, capabilities and endpoints — explicitly 'describes an agent; it never instructs one'. Maturity signal worth noting: the media type application/vnd.fafa+yaml was **IANA-registered in June 2026** in the vendor tree, which is further than most corpus drafts have got. Includes a 'what it must never do' field, a negative-authority construct that is rare here."),

    ("draft-sahu-agent-action-receipts — Signed, Hash-Chained Action Receipts for AI Agents",
     "This document specifies a format for action receipts: compact, individually signed JSON records that state that a specific AI agent attempted a specific action at a specific time, under a specific policy decision, and what the outcome was. Receipts are linked into an append-only hash chain so that deletion, insertion, reordering, or modification of any previously recorded receipt is detectable by a verifier that holds only the records and the signer's public key. The format is deliberately small and self-contained. Verification requires no network access, no service operated by the producer of the receipts, and no state beyond the records themselves and a trust anchor obtained out of band. This document specifies the record fields, the canonical byte sequence that is signed, the chain linkage rule, the verification procedure, and test vectors.",
     "https://datatracker.ietf.org/doc/draft-sahu-agent-action-receipts/",
     "IETF (individual)",
     "Revision -00, 16 Aug 2026. Signed, hash-chained action receipts for AI agents. Sits in the growing receipts cluster with schrock-ep-authorization-receipts, noa-scitt-ai-agent-receipt, the Hopley x402 receipts and the Vaara receipt. Chaining is the differentiator here — per-action receipts linked into a tamper-evident sequence rather than standalone statements."),

    ("draft-efstathiou-samp-agent-management — Simple Agent Management Protocol (SAMP)",
     "The Simple Agent Management Protocol (SAMP) defines a lightweight management-plane protocol for heterogeneous AI agents. SAMP allows a management system to discover agents, query their state, receive events, subscribe to event streams, and optionally configure or execute explicitly exposed operations under policy control. SAMP is inspired by operational management protocols such as SNMP, but it is designed for AI-agent-specific concepts such as dynamic profiles, autonomy classes, enrollment, trust states, and policy- gated execution. It is not an agent-to-agent communication protocol, an agent tool-use protocol, or an agent framework specification. This document defines SAMP version 0.1 as an Experimental protocol suitable for controlled environments and independent interoperability testing.",
     "https://datatracker.ietf.org/doc/draft-efstathiou-samp-agent-management/",
     "IETF (individual)",
     "Revision -00, 17 Aug 2026. Simple Agent Management Protocol — an SNMP-inspired *management-plane* protocol for heterogeneous agents, carrying autonomy classes, trust states, enrollment and policy-gated execution. **Explicitly not an agent-to-agent protocol**, which is what keeps it in scope here: it is about governing agents, not about them talking."),

    ("draft-mcphillips-agentenvelope-derived-authority — AgentEnvelope: Deterministic Derived Authority for Autonomous Systems",
     "AgentEnvelope defines a deterministic derived-authority model for autonomous and action-performing systems. Instead of issuing bearer credentials or authorization envelopes from a central authority, AgentEnvelope derives scoped action capabilities from customer-held custody material and canonical action envelopes. A verifier can check an action signature against a public action record without receiving roots, seeds, private keys, or hosted service access. This document specifies the v1 derivation model, signing domains, public record structure, mint delegation flow, verification rules, and security considerations.",
     "https://datatracker.ietf.org/doc/draft-mcphillips-agentenvelope-derived-authority/",
     "IETF (individual)",
     "Revision -00, 17 Aug 2026. AgentEnvelope: deterministic derived authority for autonomous systems. Delegation-mechanics cluster. Determinism is the claim to test — derived authority that is reproducible from the envelope rather than looked up in authorization-server state is the architectural opposite of the durable AS-stored Mission object."),

    ("draft-chen-agent-decoupled-authorization-model — A Decoupled Authorization Model for Agent2Agent",
     "This document proposes a framework for dynamic, intent-based authorization for AI Agents. The primary goal is to enable fine- grained, Just-in-Time (JIT) permissions based on an agent's specific intent and behavioral trustworthiness, rather than a long-lived identity or role, achieve decoupling of authorization policies from business operations.",
     "https://datatracker.ietf.org/doc/draft-chen-agent-decoupled-authorization-model/",
     "IETF (individual)",
     "Revision -00, 18 Aug 2026. A decoupled authorization model for Agent2Agent. Same author as draft-chen-oauth-agent-authz-use-cases (also updated in this sweep, now -03) — the use-cases draft states the problem, this one proposes a model, so read them as a pair. **EXPIRED on Datatracker** (expired 18 Aug 2026; checked 26 Aug 2026) — kept in the corpus deliberately; an expired draft is still evidence of what was proposed."),

    ("draft-okutomi-agent-human-interaction — An Agent-Human Interaction Overlay for Task Protocols",
     "This intentionally incomplete design note defines an overlay for Human and Agent participation in existing Task and Action protocols. It separates the responsible Participant from the authenticated Actor, records Human interactions, excludes Humans from Agent discovery, and binds each change to its authorized request. It defines neither a wire protocol nor Humans as Agents.",
     "https://datatracker.ietf.org/doc/draft-okutomi-agent-human-interaction/",
     "IETF (individual)",
     "Revision -00, 18 Aug 2026. An agent-human interaction overlay for task protocols. **Self-described as 'intentionally incomplete'** — an honest caveat worth preserving. Separates the responsible Participant from the authenticated Actor, which is the same distinction draft-mcguinness-oauth-actor-profile draws between principal and actor, and binds each change to its authorizing request."),

    ("draft-das-execution-finality-ai-interoperability — Breaking the Apple-Siri EU DMA Deadlock Without Sacrificing Privacy or Security",
     "The Apple-Siri interoperability debate under the EU Digital Markets Act exposes a difficult technical question: how can third-party AI assistants gain meaningful access to device functions without forcing the platform to surrender privacy, security, or control over consequential actions? This paper proposes an execution-finality architecture in which an AI assistant may request an action, but the request itself has no power to make that action effective. Each consequential operation remains in a Non-Effective State until protected infrastructure validates the requester, resource, destination, user intent where required, freshness, revocation state, and policy conditions. Only then is narrowly scoped, non-bearer execution authority created. At the Finality Sink - the first boundary where the action can become externally effective - the system independently verifies that the real operation still matches what was authorized. Any mismatch, replay, substitution, expiry, or revocation causes fail-closed denial. The key principle is simple: Interoperability should grant participation, not uncontrolled execution authority. This offers a possible technical path through the DMA deadlock: third-party assistants could participate meaningfully without requiring broad reusable permissions, while platforms retain strong privacy, security, revocation, anti-replay, and final-effect controls. Execution-Finality Governance therefore reframes the problem from closed versus open to open participation with bounded, verifiable authority.",
     "https://datatracker.ietf.org/doc/draft-das-execution-finality-ai-interoperability/",
     "IETF (individual)",
     "Revision -00, 19 Aug 2026. An execution-finality architecture in which a third-party AI assistant may *request* an action but the request itself has no power to make it effective — consequential operations stay in a Non-Effective State until protected infrastructure validates requester, resource, destination and user intent. Framed unusually, around the Apple/Siri EU DMA interoperability deadlock, but the underlying primitive (request-without-effect, validate-then-commit) is squarely the permit-before-commit cluster."),

    ("draft-wei-aic-identity-cert — AI Agent Identity Certificate (AIC) Extension for X.509 v3",
     "This document defines the AI Agent Identity Certificate (AIC) Extension for X.509 v3 certificates. The AIC extension enables binding of an AI Agent's cryptographic identity to a natural person (principal), providing cryptographic evidence that can support attribution of AI-autonomous actions to a principal. This specification intentionally separates cryptographic delegation from authorization semantics: AIC defines the cryptographic binding between agent and principal, while all capability and policy semantics are defined externally by vendors, industries, or regulators. The extension is identified by the IANA Private Enterprise Number 66257 assigned to the document author's organization. The AIC extension carries agent identity fields (agentId, delegationMode), a principal identifier (principalUid) linking the agent to the authorizing principal, a container-based capability declaration, authorization boundary constraints, and delegation authorization evidence with replay protection. A companion PrincipalAuthorization extension anchors Principal-side grant declarations and delegation policies. An authorizationConstraints container provides offline-verifiable execution boundaries (IP range, window). An extensibility framework allows vendor-specific and user- specific metadata. This document specifies the ASN.1 module, OID registration, field semantics, delegation model, and extensibility framework. Security considerations for deployment in regulated enterprise environments are discussed.",
     "https://datatracker.ietf.org/doc/draft-wei-aic-identity-cert/",
     "IETF (individual)",
     "Revision -00, 19 Aug 2026. AI Agent Identity Certificate as an X.509 v3 extension. Notable for substrate: nearly all agent-identity work in the corpus is JWT- or DID-shaped, and this puts agent identity in PKI instead. Compare draft-xu-mcp-agent-did-framework for the DID alternative."),

    ("draft-zhao-a2a-dns-sd — DNS-Based Service Discovery for Agent2Agent (A2A) Protocol Agents",
     "The Agent2Agent (A2A) protocol defines how two agents communicate once one knows the other's URL, and how an agent's self-description (the Agent Card) is retrieved from a well-known URI at that URL. It does not define how agents on the same host or local network find each other in the first place. This document profiles DNS-Based Service Discovery (DNS-SD) over Multicast DNS (mDNS) for that purpose: it defines the \"a2a\" service type, the TXT record keys used with it, the discovery procedure, and the security model under which discovery results are treated as hints whose trust is established by Agent Card verification, not by the discovery channel. It also requests IANA registration of the \"a2a\" service name.",
     "https://datatracker.ietf.org/doc/draft-zhao-a2a-dns-sd/",
     "IETF (individual)",
     "Revision -00, 19 Aug 2026. DNS-based service discovery for A2A agents. Discovery-and-transport cluster; the DNS-SD half of a Zhao pair."),

    ("draft-zhao-a2a-webfinger — A WebFinger Profile for Agent2Agent (A2A) Agent Identity Resolution",
     "The Agent2Agent (A2A) protocol retrieves an agent's self-description (the Agent Card) from a fixed well-known URI, which resolves exactly one agent per origin and presumes the client already holds a URL. This document profiles WebFinger for A2A: an agent is named by an \"acct\" URI (agent@domain), and resolution of that name over WebFinger yields a link to the Agent Card of the endpoint that serves the agent -- the agent's own endpoint, or a gateway fronting it. The profile introduces no new link relation, media type, or registry: it composes three deployed standards and states how they fit.",
     "https://datatracker.ietf.org/doc/draft-zhao-a2a-webfinger/",
     "IETF (individual)",
     "Revision -00, 19 Aug 2026. A WebFinger profile for A2A agent identity resolution. The WebFinger half of the Zhao pair — two different resolution substrates for the same problem, filed the same day, which is itself the signal: A2A identity resolution has no settled discovery mechanism."),

    ("draft-feng-agentproto-session-requirements — Requirements for Agent Session Establishment, Capability Negotiation, and Sessionless Interaction",
     "This document defines requirements for session-based and sessionless interactions between entities. For session-based interactions, it covers transport-independent interaction binding, endpoint authentication, capability negotiation, session establishment, authorization, and lifecycle management. It also defines security and state requirements for interactions, such as notifications, probes, and atomic requests, that do not establish a session. It is assumed that the entities involved already know of each other; how they came to know each other is outside the scope of this document. At least one party to an interaction is an agent as defined in Section 3. This document is intended as a contribution to the agentproto working group's use cases, gap analysis, and requirements deliverable. A session is a bilateral association. Protocols and application semantics for coordinating delegation or handoff of work to an entity that is not a peer, and management functions such as cross-entity accountability and audit, are outside the scope of these base session requirements. This document specifies only that such coordination does not, by itself, change the peers or state of an existing session.",
     "https://datatracker.ietf.org/doc/draft-feng-agentproto-session-requirements/",
     "IETF (individual)",
     "Revision -02, 20 Aug 2026. Requirements for agent session establishment, capability negotiation and sessionless interaction, at -02. AgentProtocol family. Same author as draft-feng-dmsc-intent-routing-requirements, filed into a different family in the same week."),

    ("draft-sharif-mcps-secure-mcp — MCPS: Cryptographic Security Layer for the Model Context Protocol",
     "This document specifies MCPS (MCP Secure), a cryptographic security layer for the Model Context Protocol (MCP). MCPS adds agent identity verification, per-message signing, tool definition integrity, and replay protection to MCP communications without modifying the core protocol. MCPS operates as an envelope around existing JSON-RPC messages. It introduces four primitives: (1) Agent Passports for cryptographic identity bound to a specific origin, (2) signed message envelopes for integrity and non-repudiation, (3) tool definition signatures covering the full tool object for detecting poisoning and tampering, and (4) nonce-plus-timestamp replay protection with transcript binding to prevent downgrade attacks. The design is fully backward-compatible. MCPS-unaware clients and servers continue to function normally. MCPS-aware endpoints progressively negotiate security capabilities through trust levels L0 (no verification) through L4 (full mutual authentication with revocation checking). All cryptographic operations use ECDSA P-256 (NIST FIPS 186-5). Signatures use IEEE P1363 fixed-length r||s encoding per RFC 7518 Section 3.4 with low-S normalization to prevent signature malleability. Canonical serialization uses JSON Canonicalization Scheme (JCS) per RFC 8785. The Trust Authority component is self-hostable with no external service dependency.",
     "https://datatracker.ietf.org/doc/draft-sharif-mcps-secure-mcp/",
     "IETF (individual)",
     "Revision -01, 21 Aug 2026. MCPS: a cryptographic security layer for MCP. **Fourth Sharif draft** tracked here, after sharif-attp, sharif-agent-audit-trail (updated -01 in this sweep) and the SUPERSEDED sharif-payment-trust. Sharif is becoming a multi-draft author voice worth tracking as a body of work."),

    ("draft-hawkins-x402-dns-discovery — Discovering x402 Payment Capability via DNS and a Well-Known URI",
     "x402 is an application-level protocol for internet-native payments built on the HTTP 402 (Payment Required) status code. This document defines how a domain publishes its x402 payment capability out-of- band, so that clients, autonomous agents, and indexers can discover it without prior configuration or a central directory. It specifies a JSON capability manifest served at the well-known URI \"/.well- known/x402\" and an optional DNS TXT record at the underscored node name \"_x402\" that points to the manifest. A consumer resolves a bare domain name to verified x402 capability with at most one DNS query and one HTTPS GET.",
     "https://datatracker.ietf.org/doc/draft-hawkins-x402-dns-discovery/",
     "IETF (individual)",
     "Revision -03, 23 Aug 2026. Discovering x402 payment capability via DNS and a well-known URI. Extends the Hopley x402 cluster reinstated on 11 Aug 2026 into the discovery layer. Note the unresolved curation question this sits next to: the Vauban x402 STARK/PQC receipt pair remains deliberately out of the corpus pending a ruling."),

    ("draft-ietf-oauth-rar-metadata-remediation — OAuth 2.0 RAR Metadata and Error Remediation",
     "OAuth 2.0 Rich Authorization Requests (RAR) [RFC9396] standardizes the exchange and processing of authorization details but does not define metadata for describing authorization details types. In addition, no interoperable guidance is offered to clients, to remediate failures by resource servers due to insufficient authorization details. This document addresses this interoperability challenge, allowing clients to dynamically discover metadata instead of relying on out- of-band agreements, as well as standardizes failure signaling including interoperable remediation when insufficient authorization details are the cause of failure.",
     "https://datatracker.ietf.org/doc/draft-ietf-oauth-rar-metadata-remediation/",
     "IETF (OAuth WG)",
     "Revision -00, 23 Aug 2026. **New OAuth WG draft** — the only WG-level addition in this sweep. Defines metadata and error-remediation behaviour for RAR (RFC 9396), the primitive the whole Mission-Bound family builds on: mission_intent is an RAR envelope and the MVP's proposal_hash is computed over canonical authorization_details. A remediation path for RAR errors is the WG-side counterpart to what draft-mcguinness-oauth-insufficient-claims and the ARAP 'requestable denial' work approach from the individual/OIDF side. Watch this one — it is the closest thing yet to Complex Delegation machinery arriving in chartered WG work."),

    ("draft-kavian-agent-enrollment-protocol — The Agent Enrollment Protocol",
     "The Agent Enrollment Protocol (AEP) defines an HTTP-based mechanism for autonomous agents to discover service enrollment requirements, enroll an agent identity, obtain optional session credentials, revoke those credentials, and query enrollment status. AEP uses Decentralized Identifiers, client assertion JWTs, and HTTP Problem Details to provide a narrow machine-first enrollment and authentication substrate for agent-to-service interactions.",
     "https://datatracker.ietf.org/doc/draft-kavian-agent-enrollment-protocol/",
     "IETF (individual)",
     "Revision -03, 24 Aug 2026. The Agent Enrollment Protocol at -03. Companion to draft-kavian-aep-oauth-session-credential, already in the corpus and also updated in this sweep (-03, 24 Aug 2026) — the 'AEP' in that draft's slug is this protocol. Enrollment is the lifecycle stage most corpus drafts assume has already happened."),

    ("draft-agentic-ai-usecases-requirements — Agentic AI Use Cases and Requirements",
     "This document describes use cases for agentic AI communication systems and derives protocol requirements from those use cases. The requirements are intended to guide IETF standardization work on protocols in the context of agent-to-agent communication, agent-to- tool communication, with focus on multimodal communication, session management, discovery, communication security, agent identity and authentication.",
     "https://datatracker.ietf.org/doc/draft-agentic-ai-usecases-requirements/",
     "IETF (individual)",
     "Revision -02, 26 Aug 2026. Agentic AI use cases and requirements, at -02. **Note the slug has no author infix** — unusual for an individual draft and worth watching as a possible sign of intended WG adoption or a group submission."),

    ("draft-morrison-consent-settlement — Consent-Bound Identity Disclosure with Subject Settlement for HTTP-Native Agent Payments",
     "This memo specifies an extension to HTTP-native agent payment protocols by which the disclosure of an identity attribute about a human subject is bound to that subject's recorded consent and settled, in part, to that subject. When an agent pays to read an identity attribute about a person, the extension requires that the read carry a reference to a scoped, revocable consent grant issued by the subject, and it requires that the payment's settlement instruction name the subject as a beneficiary of a share of the read's price greater than the shares of all other parties combined. The extension composes above an identity- attestation envelope (which asserts who a credential is about) and above an HTTP-native payment flow (which moves value for the read); it adds the two functions neither layer provides: consent capture at disclosure time and settlement to the data subject. The wire additions are an advertisement in the server's payment-required response, a consent- grant reference echoed in the client's payment payload, and a settlement instruction enumerating subject beneficiary roles. The extension is settlement-network-agnostic and attestation-format- agnostic. The memo is Informational; the underlying COSE and CBOR formats are normative per [RFC9052] and [RFC8949], and the HTTP semantics are normative per [RFC9110].",
     "https://datatracker.ietf.org/doc/draft-morrison-consent-settlement/",
     "IETF (individual)",
     "Revision -05, 26 Aug 2026. Consent-bound identity disclosure with subject settlement for HTTP-native agent payments. The strongest single draft of the six-draft Morrison family for this corpus: it joins consent, identity disclosure and agent payment settlement in one mechanism. Payments-infra is in scope per the 11 Aug 2026 curation decision."),

    ("draft-morrison-identity-accord — Identity Accord Protocol: A Peer Ceremony for Bilateral Agreements Between Identity-Substrate-Bound Principals",
     "This memo specifies the Identity Accord Protocol, a peer ceremony by which two principals, each represented by an organisational identity substrate and acting under a recorded delegation from a legal entity, execute a bilateral agreement as a portable, self-verifying COSE- signed CBOR document. The protocol composes DNS-based substrate discovery, Ed25519 sovereign signatures, an append-only identity log, and a tamper-evidence descriptor quorum into a single artefact that is verifiable by any third party with access to the public DNS, the parties' identity logs, and an on-chain anchor of the agreement's content hash. The protocol does not require a central registry, a designated verifier, or any infrastructure operated by the specification's author; verification succeeds when the author's reference deployment is offline. The canonical bilateral target is a mutual non-disclosure agreement, but the wire format generalises to any bilateral consent envelope between two legal entities each represented by an identity substrate. An associated MCP tool surface, an associated pre-send enforcement gate, and an associated disclosure-ledger schema are specified, all of which are optional layers above the wire format. The memo is Informational; the underlying COSE and CBOR formats are normative per [RFC9052] and [RFC8949].",
     "https://datatracker.ietf.org/doc/draft-morrison-identity-accord/",
     "IETF (individual)",
     "Revision -02, 26 Aug 2026. A peer ceremony for bilateral agreements between identity-substrate-bound principals. Morrison family. Bilateral peer agreement is an unusual shape in this corpus — most delegation here is asymmetric (principal → agent); this is principal ↔ principal, closer to Hardt's AS-to-AS federation instinct than to OAuth delegation."),

    ("draft-morrison-solo-agent-earn-registration — Registration of Owner-Less Agents as Economic Principals: A Payment-Gated Admission Profile for Transparency Services",
     "This memo describes a profile by which an autonomous agent that has no human or organisational principal at the root of its delegation chain registers itself, on its own behalf, as an economic principal in a transparency service, and by which that registration is the specific act that makes the agent eligible to be paid for subsequent reads of its own identity record. Admission of the agent's Signed Statement to the transparency service is gated on settlement of an HTTP payment challenge returned with the 402 (Payment Required) status. The profile makes no change to the registration semantics of the underlying transparency service: payment is expressed as an operator Registration Policy and authentication-layer concern, and where the payment is authoritative to the admission decision the payment proof is carried as an authenticated input committed to the service's verifiable data structure, so that admission remains a deterministic function of committed inputs and stays replayable by an auditor. The profile is positioned against the current agent- identity drafts, which either require a human principal at the root of the chain or leave the owner-less case undefined; it occupies that undefined seam without contradicting them. This document is Informational.",
     "https://datatracker.ietf.org/doc/draft-morrison-solo-agent-earn-registration/",
     "IETF (individual)",
     "Revision -01, 26 Aug 2026. Registration of **owner-less** agents as economic principals, via a payment-gated admission profile. Morrison family. Notable because almost every other draft in the corpus assumes an agent acts *on behalf of* a human or org principal; this one deliberately addresses the agent with no principal behind it. Read alongside draft-maintainer-1f916-agent-record, which shares that premise."),

    ("draft-li-oauth-policy-based-anonymous-tokens — OAuth 2.0 Policy-Based Anonymous Access Tokens",
     "This document specifies an OAuth 2.0 access-token type that allows a client, after one authorization-server issuance, to derive a policy- bounded set of unlinkable, single-use access tokens locally. Each derived token is bound to one canonical tag, an intended resource server, approved authorization details, a policy epoch, and a validity interval. Resource servers validate the token offline and enforce both policy membership and replay prevention. The protocol defines authorization request semantics, token-endpoint issuance, canonical policy and metadata objects, token derivation and HTTP presentation, resource-server validation, capability discovery, error handling, and IANA registrations. Version 1 requires public verification and the counter-window policy profile. It supports an optional private metadata bit, while private-verification ciphersuites remain optional. Concrete cryptographic algorithms are supplied by separately registered PBAT ciphersuites. The initial mandatory-to-implement ciphersuite is the publicly-verifiable equivalence-class-signature construction over BLS12-381 specified by the companion PBAT ciphersuite document. This specification does not replace OAuth grants, resource-owner consent, client authentication, or audience restriction. — middle",
     "https://datatracker.ietf.org/doc/draft-li-oauth-policy-based-anonymous-tokens/",
     "IETF (OAuth-related, individual)",
     "Revision -00, 26 Aug 2026. Policy-based anonymous access tokens. Also lands in the unclustered decision/policy group alongside the Gazitt and Liu drafts — policy determines issuance, and the token deliberately carries no subject. Relevant to the Privacy Pass / anonymous-path thread already tracked under WebBotAuth."),

    # ---- AIPREF cluster — reinstated 26 Aug 2026 by maintainer decision ----

    ("draft-ietf-aipref-vocab — A Vocabulary For Expressing AI Usage Preferences",
     "This document defines a vocabulary for expressing preferences regarding how digital assets are used by automated processing systems. This vocabulary allows for the declaration of restrictions or permissions for use of digital assets by such systems.",
     "https://datatracker.ietf.org/doc/draft-ietf-aipref-vocab/",
     "IETF (AIPREF WG)",
     "Revision -07, 19 Aug 2026. AIPREF WG draft. Reinstated 26 Aug 2026 after being dropped in the first pass of this sweep: the corpus already tracks the AIPREF WG charter, so tracking the charter while dropping the WG's actual output was inconsistent. The vocabulary itself is the reservation half of a reservation/grant pair — see draft-wallace-aipref-grant-binding for the grant half, which is the piece that behaves like a delegation primitive."),

    ("draft-ietf-aipref-attach — Associating AI Usage Preferences with Content in HTTP",
     "Methods are defined for associating usage preferences with content that is obtained using the HTTP protocol. This document defines attachment methods using the Robots Exclusion Protocol and HTTP header fields. This document updates RFC 9309 to allow for the inclusion of usage preferences.",
     "https://datatracker.ietf.org/doc/draft-ietf-aipref-attach/",
     "IETF (AIPREF WG)",
     "Revision -05, 19 Aug 2026. AIPREF WG draft; the HTTP attachment mechanism for the vocabulary. Reinstated 26 Aug 2026 alongside draft-ietf-aipref-vocab. Relevant to this corpus as the transport question every preference/consent signal eventually faces: how an out-of-band expression of intent is bound to the resource it governs."),

    ("draft-wallace-aipref-grant-binding — A Verifiable-Credential Binding for AI Usage Preferences: Expressing Grants that Lift AIPREF Preferences",
     "The AI Preferences (AIPREF) vocabulary lets those with rights in a digital asset express preferences -- for example, that training of AI models is disallowed -- about how automated systems process that asset. Such a preference expresses a reservation. It does not, by itself, provide a verifiable, revocable record of a specific grant that lifts a preference for a specific party. This document describes that gap and proposes a candidate mechanism: a cryptographically signed, offline-verifiable credential that expresses a grant referencing an AIPREF usage category and a specific asset, that any party can verify without contacting the grantor, and that the grantor can revoke. It is intended as a starting point for discussion, not as a finished specification. The mechanism is preference-general. Training is used throughout as the worked example because it is the reservation most widely discussed, but nothing in the construction is specific to it: the credential binds whichever usage category was reserved to a named party, and the same procedure applies to any other category the vocabulary expresses. What the mechanism establishes is that a grant exists, is authentic, is unrevoked, and was in force at a stated time. It does not adjudicate whether the grantor had standing to grant, and it is not an enforcement or access-control mechanism.",
     "https://datatracker.ietf.org/doc/draft-wallace-aipref-grant-binding/",
     "IETF (individual)",
     "Revision -02, 18 Aug 2026. **The strongest of the four AIPREF entries for this corpus.** A preference expresses a reservation; it does not provide a verifiable, revocable record of a specific grant that lifts that reservation for a specific party. This draft proposes a cryptographically signed, offline-verifiable credential expressing exactly that grant. Party-scoped, revocable, offline-verifiable authority over a named asset is a delegation primitive that happens to be pointed at content rights rather than at API scopes — worth reading against the receipt and consent-evidence drafts."),

    ("draft-hood-aipref-earmark — Earmark: Embedded Attribution and Rights Marks for AI Usage Preferences",
     "This document defines Earmark (Embedded Attribution and Rights Marks), a mechanism by which publishers and rights holders embed signed usage preferences directly into published content. To earmark content is to reserve it for designated uses, and the mark travels with what it covers, surviving republication and aggregation, so the preference remains discoverable wherever the content arrives, including where perimeter signals such as robots.txt no longer apply. Marks carry the identity of the rights holder, the preferences asserted, and a signature, and are verifiable offline by any party. An individual signed statement is a Mark; the mechanism as a whole is Earmark. This document defines the Mark Object, embedding bindings for common content types, and the detection and verification procedure. It reuses the AI Preference vocabulary for preference semantics and the C2PA and CAWG assertion infrastructure for media, defining new machinery only where none exists. Earmarks make ignored preferences observable and attributable. Enforcement remains with law, contract, and the market.",
     "https://datatracker.ietf.org/doc/draft-hood-aipref-earmark/",
     "IETF (individual)",
     "Revision -00, 13 Aug 2026. Embedded attribution and rights marks for AI usage preferences. The weakest of the four AIPREF entries here — marking and attribution rather than authority — kept for completeness of the AIPREF cluster now that the corpus tracks it."),
]
make_sheet("Active IETF Drafts", COLORS['Drafts'], draft_rows)

# ============================================================
# TAB 3: MISSION-BOUND (PRE-PUBLICATION)
# ------------------------------------------------------------
# The 33 GitHub-only drafts of the McGuinness Mission-Bound Authorization
# family. Split out of Active IETF Drafts on 26 Aug 2026: they are neither
# active, nor IETF, nor drafts in any procedural sense — they live in a single
# author's repo and only draft-mcguinness-oauth-mission has been filed on
# Datatracker. That filed draft deliberately stays in the Active IETF Drafts
# tab; this tab is a venue distinction, not a topic one.
# ============================================================
mission_rows = [

    ("draft-mcguinness-mission-harness — Mission-Aware Agent Harnesses",
     "Agent harnesses preserve execution state across restarts, retries, background jobs, tool-connection reuse, and sub-agent orchestration. That continuity is not authority. This document defines an optional Mission-aware harness profile for deployments using Mission-Bound Authorization, with OAuth 2.0 as this version's normative substrate.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-mission-harness.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Agent runtime; maturity: stable; adoption rung: “Recommended for AI agents”. Depends on 10 family draft(s) incl. mission-audit, mission-authzen, mission-discovery. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-mission-orchestration — Mission Orchestration and Unwinding",
     "Mission runtime enforcement can refuse the next consequential action, but Mission termination can occur while an agent workflow is already in flight. This document defines an optional orchestration profile for Mission-governed workflows.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-mission-orchestration.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Agent runtime; maturity: experimental; adoption rung: “Experimental”. Depends on 8 family draft(s) incl. mission-architecture, mission-authzen, mission-harness. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-mission-shaping — Mission Intent Shaping",
     "Mission-Bound Authorization for OAuth 2.0 defines a Mission Intent and the Authority Set an Authorization Server derives from it, but leaves the step that turns an open-ended task request into a candidate Mission Intent to deployment policy.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-mission-shaping.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Approval-time; maturity: informational; adoption rung: “Advanced”. Depends on 10 family draft(s) incl. mission-aauth, mission-architecture, mission-authority-server. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-oauth-mission-approval — Mission Deferred Approval for OAuth 2.0",
     "Mission-Bound Authorization for OAuth 2.0 (the \"issuance profile\") records an approval event at which an Approver consents to a Mission's derived Authority Set, but it treats that event as immediate. A human review of an agent's Proposed Mission is often asynchronous. This document defines an optional Mission Deferred Approval profile. It profiles OAuth Deferred Token Response so a Mission approval can be deferred and polled.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-oauth-mission-approval.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Approval-time; maturity: stable; adoption rung: “Advanced”. Depends on 6 family draft(s) incl. mission-authority-server, mission-shaping, oauth-mission. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-oauth-mission-approval-revision — Mission Approval Revision for OAuth 2.0",
     "Mission Deferred Approval for OAuth 2.0 defers a Mission approval and lets a client poll for the decision. A reviewer commonly approves a narrowed subset of a proposed Mission rather than an all-or-nothing outcome.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-oauth-mission-approval-revision.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Approval-time; maturity: experimental; adoption rung: “Experimental”. Depends on 5 family draft(s) incl. mission-shaping, oauth-mission, oauth-mission-approval. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-oauth-mission-consent-evidence — Mission Consent Evidence for OAuth 2.0",
     "Mission-Bound Authorization for OAuth 2.0 commits the approved Mission Intent and Authority Set, but does not commit the exact consent disclosure shown to the Approver. This document defines an optional Consent Evidence profile.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-oauth-mission-consent-evidence.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Approval-time; maturity: stable; adoption rung: “Recommended for AI agents”. Depends on 11 family draft(s) incl. mission-aauth, mission-audit, mission-authority-server. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-oauth-mission-template — Mission Template for OAuth 2.0",
     "An agent that dispatches work at machine speed cannot pause for a fresh human approval at every run, and a standing Mission broad enough to cover every run over-provisions authority the agent holds the whole time. This document defines an experimental option between those two: the Mission Template.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-oauth-mission-template.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Approval-time; maturity: experimental; adoption rung: “Experimental”. Depends on 9 family draft(s) incl. mission-architecture, mission-runtime, oauth-mission. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-mission-architecture — An Architecture for Mission-Bound Authorization",
     "A Mission is a durable, approval-backed governance object for authorization: the approved task, with a lifecycle, that authority is derived for, bound to, and gated on. It is not a new way to express authority. Read as one system, the Mission model defines a delegated-authority layer: authentication says who is acting, and entitlement governance says what a principal may hold; this layer governs the approved task itself.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-mission-architecture.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Architecture; maturity: informational; adoption rung: “outside-ordering”. Depends on 31 family draft(s) incl. aauth-mission-expiry, mission-aauth, mission-aauth-management. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-mission-aauth — Mission Context Binding for AAuth",
     "AAuth defines missions as optional, immutable authorization contexts for agent governance at a Person Server. A mission is approved through AAuth's native propose, clarify, and approve interaction, is identified by the native `approver` and `s256` reference, and accumulates an ordered mission log.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-mission-aauth.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Bindings / substrate; maturity: stable; adoption rung: “By binding”. Depends on 2 family draft(s) incl. aauth-mission-expiry, mission-substrate. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-mission-authority-server — Mission Authority Server",
     "Mission-Bound Authorization for OAuth 2.0 defines the Mission, a durable, human-approved, integrity-bound authorization artifact, and binds it to OAuth issuance: the Authorization Server derives tokens under the Mission and gates them on its state. Many deployments cannot change their Authorization Server.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-mission-authority-server.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Bindings / substrate; maturity: stable; adoption rung: “By binding”. Depends on 18 family draft(s) incl. mission-architecture, mission-audit, mission-authzen. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-mission-metering — Mission Consumption Metering",
     "Mission-Bound Authorization for OAuth 2.0 bounds an agent's authority by resources, actions, and constraints, and its runtime enforcement profile evaluates each consequential action at the point of use. Neither bounds how much of an approved authority a Mission may consume.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-mission-metering.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Bindings / substrate; maturity: experimental; adoption rung: “Experimental”. Depends on 7 family draft(s) incl. mission-architecture, mission-authzen, mission-orchestration. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-mission-substrate — Mission Substrate Requirements",
     "A Mission binds an actor to approved context under the governance of an identified controller. Authorization substrates realize that relationship in materially different ways. Some carry structured authority in credentials; others keep contextual policy at an online service and use substrate-native authorization at each resource.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-mission-substrate.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Bindings / substrate; maturity: stable; adoption rung: “By binding”. Depends on 12 family draft(s) incl. mission-aauth, mission-architecture, mission-audit. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-mission-uma — Mission-Bound Authorization for UMA 2.0",
     "User-Managed Access (UMA) 2.0 standardized the plumbing of asynchronous, party-asymmetric authorization: a requesting party and client that can only request, a resource owner who approves at the authorization server on their own schedule, a rotating permission ticket carrying the pending request, claims pushing at the token endpoint, a persisted claims token that carries continuity but grants nothing, and per-use introspection at the resource server.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-mission-uma.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Bindings / substrate; maturity: sketch; adoption rung: “Experimental”. Depends on 24 family draft(s) incl. mission-aauth, mission-architecture, mission-audit. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-oauth-mission-issuance-grant — Mission Issuance Grant for OAuth 2.0",
     "The standalone Mission Authority Server binding governs Missions with no change to an estate's Authorization Servers: tokens remain ordinary, and enforcement joins them to Missions at the point of use. That mode provides no Mission-bound credential and no issuance gating.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-oauth-mission-issuance-grant.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Bindings / substrate; maturity: stable; adoption rung: “By binding”. Depends on 8 family draft(s) incl. mission-architecture, mission-authority-server, mission-mandate. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-oauth-mission-continuation — Mission Continuation: Authorization Continuity for Mission-Bound Authorization",
     "This document profiles authorization continuity for Mission-Bound Authorization. A Mission is the durable, grant-anchored record of what work remains authorized, under which constraints, on whose approval.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-oauth-mission-continuation.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Cross-domain projection; maturity: experimental; adoption rung: “Experimental”. Depends on 8 family draft(s) incl. mission-aauth, mission-architecture, mission-authzen. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-oauth-mission-cross-domain — Mission Cross-Domain Projection for OAuth 2.0",
     "The Mission-Bound Authorization for OAuth 2.0 profile binds issued authority to a durable, human-approved Mission held by a single Authorization Server, the Mission Issuer. This document specifies that profile's optional cross-domain projection: a single hop that lets an Authorization Server in another trust domain, a Resource AS, honor a Mission it did not issue.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-oauth-mission-cross-domain.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Cross-domain projection; maturity: stable; adoption rung: “Advanced”. Depends on 8 family draft(s) incl. mission-architecture, mission-mandate, mission-runtime. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-aauth-mission-expiry — AAuth Mission Expiry",
     "AAuth's approved mission blob MAY carry `expires_at`: an immutable, consent-bound lifetime the Person Server enforces on every decision path, capping every token carrying `mission_s256`. This document profiles that member: values are RFC 3339 date-times, deployments document their clock-skew posture, and the Person Server terminates promptly at the deadline.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-aauth-mission-expiry.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Lifecycle; maturity: stable; adoption rung: “By binding”. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-mission-aauth-management — AAuth Mission Management",
     "AAuth defines an immutable mission blob, identifies it by the native `{approver, s256}` mission reference, and gives a mission two states: `active` and `terminated`. It leaves revocation, delegation-tree queries, and administrative interfaces to a companion specification. This document defines that companion.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-mission-aauth-management.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Lifecycle; maturity: stable; adoption rung: “By binding”. Depends on 4 family draft(s) incl. aauth-mission-expiry, mission-aauth, mission-architecture. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-mission-discovery — Mission Open-World Discovery",
     "A Mission commits its authority at approval, but an open-world agent meets resources the approval could not name.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-mission-discovery.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Lifecycle; maturity: experimental; adoption rung: “Experimental”. Depends on 13 family draft(s) incl. mission-aauth, mission-architecture, mission-audit. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-oauth-mission-containment — Mission Containment for OAuth 2.0",
     "Mission-Bound Authorization for OAuth 2.0 commits a Mission's authority at a single approval event: the approved Authority Set and its integrity anchors never change. This document defines Mission Containment, an optional layered extension for narrowing a live Mission without ending it.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-oauth-mission-containment.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Lifecycle; maturity: experimental; adoption rung: “Experimental”. Depends on 15 family draft(s) incl. mission-audit, mission-authzen, mission-discovery. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-oauth-mission-expansion — Mission Expansion for OAuth 2.0",
     "Mission-Bound Authorization for OAuth 2.0 commits a Mission's authority at a single approval event and defers widening: enlarging authority requires a new approval, a successor Mission. This document defines that successor mechanism as an optional, layered extension to the issuance profile.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-oauth-mission-expansion.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Lifecycle; maturity: stable; adoption rung: “Advanced”. Depends on 6 family draft(s) incl. mission-runtime, oauth-mission, oauth-mission-child-delegation. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-oauth-mission-management — Mission Management for OAuth 2.0",
     "The Mission Status and Lifecycle profile observes and changes one Mission at a time and defers fleet-scale management.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-oauth-mission-management.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Lifecycle; maturity: stable; adoption rung: “Advanced”. Depends on 9 family draft(s) incl. mission-architecture, mission-audit, mission-authority-server. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-oauth-mission-progressive — Mission Progressive Authorization for OAuth 2.0",
     "Mission Expansion for OAuth 2.0 widens an agent's authority only through a fresh human approval that creates a successor Mission. An open-ended agentic task often cannot have its full authority enumerated at the initial approval, which leaves a deployment choosing between over-provisioning a broad standing Mission and interrupting the user for a fresh approval at every step.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-oauth-mission-progressive.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Lifecycle; maturity: experimental; adoption rung: “Experimental”. Depends on 11 family draft(s) incl. mission-aauth, mission-architecture, mission-discovery. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-oauth-mission-signals — Mission Lifecycle Signals for OAuth 2.0",
     "The Mission Status and Lifecycle profile names event-driven propagation (Mission state changes reaching consumers over a Shared Signals stream) as one way to bound revocation latency, but leaves the channel itself unspecified.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-oauth-mission-signals.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Lifecycle; maturity: stable; adoption rung: “Advanced”. Depends on 9 family draft(s) incl. mission-aauth, mission-audit, mission-authority-server. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-oauth-mission-status — Mission Status and Lifecycle for OAuth 2.0",
     "The Mission-Bound Authorization for OAuth 2.0 profile binds issued authority to a durable, human-approved Mission and gates issuance on Mission state, but it observes Mission state only through token lifetime and optional token introspection.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-oauth-mission-status.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Lifecycle; maturity: stable; adoption rung: “Implementation minimum”. Depends on 9 family draft(s) incl. mission-aauth, mission-authority-server, mission-runtime. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-mission-audit — Mission Audit Transparency",
     "Mission-Bound Authorization for OAuth 2.0 and its companions produce many evidence records: the approval event, lifecycle transitions, consent evidence, runtime decision and execution evidence, and further evidence types profiles define.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-mission-audit.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Proof portability; maturity: stable; adoption rung: “Advanced”. Depends on 15 family draft(s) incl. mission-aauth, mission-architecture, mission-authority-server. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-mission-mandate — Mission Mandate",
     "A Mission's committed facts (the approved task, the consented authority, the principals, and the expiry) live on the Mission record at its issuer, and a party outside the issuing domain cannot verify what was approved short of a token-exchange hop or trust in the issuer's own records.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-mission-mandate.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Proof portability; maturity: stable; adoption rung: “Advanced”. Depends on 9 family draft(s) incl. mission-aauth, mission-audit, mission-authority-server. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-mission-authzen — Mission-Bound Runtime Enforcement: AuthZEN Profile",
     "Mission-Bound Runtime Enforcement defines a substrate-independent decision contract: before each consequential action runs, a Policy Enforcement Point (PEP) obtains a permit from a Policy Decision Point (PDP) that evaluates the action against the established Mission. This document is the concrete OpenID AuthZEN binding of that contract.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-mission-authzen.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Runtime enforcement; maturity: stable; adoption rung: “Implementation minimum”. Depends on 10 family draft(s) incl. mission-audit, mission-harness, mission-metering. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-mission-runtime — Mission-Bound Runtime Enforcement",
     "This document specifies runtime enforcement for Mission-Bound Authorization: within a declared enforcement scope, no consequential action executes until a policy enforcement point obtains a permit from a policy decision point that evaluates the action and its concrete parameters against the Mission established for the acting credential.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-mission-runtime.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Runtime enforcement; maturity: stable; adoption rung: “Implementation minimum”. Depends on 18 family draft(s) incl. mission-aauth, mission-architecture, mission-audit. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-mission-security-model — Mission Security Model",
     "Mission-Bound Authorization for OAuth 2.0 and its companion profiles spread enforcement across several components: a Mission Issuer, in one of three bindings (OAuth Authorization Server, standalone Mission Authority Server, AAuth Person Server), derives authority and, where it also issues tokens, gates issuance; a Policy Enforcement Point and Policy Decision Point evaluate each action; a harness establishes a mediated execution environment; a consent rendering layer discloses authority to an Approver; an orchestrator unwinds in-flight work; and optional services report Mission state, adjudicate requested authority, meter consumption, manage the Mission fleet, log evidence, and report completion events.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-mission-security-model.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Security model; maturity: informational; adoption rung: “outside-ordering”. Depends on 28 family draft(s) incl. mission-aauth, mission-architecture, mission-audit. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-oauth-mission-work-products — Mission Work Products",
     "Agents produce durable artifacts, files, messages, memory entries, queue events, packages, and directory names, that other agents and Missions later read. An artifact can carry knowledge across a boundary, but it must not carry authority across with it. This document defines, as an experimental companion to Mission-Bound Authorization for OAuth 2.0, how a work product records where it came from without becoming a grant.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-oauth-mission-work-products.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Security model; maturity: experimental; adoption rung: “Experimental”. Depends on 7 family draft(s) incl. mission-architecture, mission-audit, mission-security-model. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-oauth-mission-attenuation — Mission Offline Attenuation for OAuth 2.0",
     "Mission-Bound Authorization for OAuth 2.0 derives delegated authority through the Authorization Server: each narrowing is a derivation at the issuer. For deep sub-agent fan-out, the common agent topology, that puts the Authorization Server in the hot path as a latency and availability dependency. This document defines an optional Mission Offline Attenuation profile.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-oauth-mission-attenuation.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Sub-agents; maturity: experimental; adoption rung: “Experimental”. Depends on 7 family draft(s) incl. mission-harness, mission-runtime, oauth-mission. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

    ("draft-mcguinness-oauth-mission-child-delegation — Mission Child Delegation for OAuth 2.0",
     "Mission-Bound Authorization for OAuth 2.0 defines delegated tokens and the rule that authority narrows down a delegation chain. Agent harnesses, however, can spawn sub-agents whose work outlives a call frame or crosses a different execution boundary. This document defines an optional Mission Child Delegation profile.",
     "https://github.com/mcguinness/mission-bound-authorization/blob/main/draft-mcguinness-oauth-mission-child-delegation.md",
     "IETF (Pre-publication — GitHub)",
     "Mission-Bound Authorization family — group: Sub-agents; maturity: stable; adoption rung: “Advanced”. Depends on 10 family draft(s) incl. mission-architecture, mission-harness, mission-metering. GitHub-only (pre-publication) — not on Datatracker as of 11 Aug 2026. Family is a 34-draft decomposition with a machine-readable family-manifest.json."),

]
make_sheet("Mission-Bound (Pre-pub)", COLORS['Mission'], mission_rows)

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

    ("NIST NCCoE Concept Paper — Accelerating the Adoption of Software and AI Agent Identity and Authorization",
     "US government concept paper proposing a National Cybersecurity Center of Excellence demonstration project for AI agent identity and authorization using OAuth 2.0, SPIFFE/SPIRE, and MCP; explicitly asks whether existing identity standards can serve AI agents without new standards and invites industry collaboration.",
     "https://csrc.nist.gov/pubs/other/2026/02/05/accelerating-the-adoption-of-software-and-ai-agent/ipd",
     "NIST (US government)",
     "Published Feb 5 2026; public comment closed Mar 9 2026. First US government program explicitly addressing interoperability and security standards for agentic AI. Directly references OAuth 2.0, SPIFFE/SPIRE, and MCP — the same stack the IETF corpus is standardizing — as the candidate technology foundation."),

    ("NSA Cybersecurity Information Sheet — MCP Security Design Considerations for AI-Driven Automation",
     "17-page US government guidance on Model Context Protocol security risks and mitigations; identifies uncontrolled automated action escalation, lack of input screening, and overload attack susceptibility as primary risks; recommends filtering proxies and tight resource URL pinning beyond MCP's own documentation.",
     "https://www.nsa.gov/Portals/75/documents/Cybersecurity/CSI_MCP_SECURITY.pdf",
     "NSA (US government)",
     "Published May 20 2026. NSA-tier imprimatur on MCP security; first US government guidance specifically on MCP. The risk categories (escalation, input screening gaps, overload) complement the IETF WebBotAuth and OAuth WG work that addresses the same attack surface from the standards side."),

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

    ("Authorization Propagation in Multi-Agent AI Systems: Identity Governance as Infrastructure (Tallam, arXiv:2605.05440)",
     "Formalizes 'authorization propagation' as a distinct multi-agent security problem irreducible to prompt injection or classical RBAC/ABAC/ReBAC; identifies transitive delegation, aggregation inference, and temporal validity as three distinct sub-problems; derives seven structural requirements for multi-agent authorization architectures.",
     "https://arxiv.org/abs/2605.05440",
     "arXiv",
     "Published May 6 2026; author: Krti Tallam. The formal treatment maps directly onto the delegation-chain and audit-architecture cluster in the corpus. Introduces 'authorization propagation' as a term of art for the multi-hop delegation security problem that RFC 8693 and the Transaction Token family address at the protocol layer."),

    ("Overlaying Governance: A Compositional Authorization Framework for Delegation and Scope in Agentic AI (Ibrahim & Li, arXiv:2606.03518)",
     "Introduces a compositional operator that overlays agentic authorization semantics — recursive delegation chains, time-limited authority, resource scope attenuation — onto existing relational policies without rewriting them; treats scope attenuation as a first-class primitive bounding an agent's access envelope.",
     "https://arxiv.org/abs/2606.03518",
     "arXiv",
     "Published Jun 2 2026; authors: Amjad Ibrahim, Yong Li. 'Resource scope attenuation' is the formal complement to what RAR-for-agents (draft-ietf-oauth-transaction-tokens) and the Mission-Bound OAuth series address at the protocol level. Provides the mathematical framing the IETF drafts reference but do not state."),

    ("SkillScope: Toward Fine-Grained Least-Privilege Enforcement for Agent Skills (Wu et al., arXiv:2605.05868)",
     "Uses graph-based static analysis to identify and constrain over-privileged agent skills (capability bundles packaging instructions and executable resources); validates against 68,312 real-world skills and finds 7,039 over-privileged; constrains over-privilege action instances by 88.56% while preserving task completion.",
     "https://arxiv.org/abs/2605.05868",
     "arXiv",
     "Published May 7 2026; authors: Jiangrong Wu, Yuhong Nan, Yixi Lin, et al. Empirical least-privilege measurement at production scale — the quantitative evidence base the protocol-layer corpus is missing. Graph-static-analysis approach complements the token-attenuation drafts (niyikiza-oauth-attenuating-agent-tokens, rampalli-pedigree) which enforce attenuation at runtime; SkillScope enforces it pre-deployment."),

    ("SUDP: Secret-Use Delegation Protocol for Agentic Systems (Yu et al., arXiv:2604.24920)",
     "Formalizes the 'Agent Secret Use' problem — agents must cause user-authorized secret-backed operations without retaining reusable authority over those secrets — and proposes a three-role protocol (Requester, Authorizer, Custodian) with seven security properties covering authorization integrity and secret confidentiality.",
     "https://arxiv.org/abs/2604.24920",
     "arXiv",
     "Published Apr 27 2026 (v3 May 22 2026); author: Xiaohang Yu et al. Directly formalizes the problem that draft-sweeney-wimse-credential-delegation's credential-wrapping mechanism (raw tokens never reach the agent) addresses at the protocol layer. SUDP is the formal proof that credential-wrapping is necessary; sweeney is a concrete protocol instantiation."),

    ("Before the Tool Call: Deterministic Pre-Action Authorization for Autonomous AI Agents (arXiv:2603.20953)",
     "Proposes Open Agent Passport (OAP), an open specification that intercepts tool calls synchronously before execution, evaluates them against a declarative policy, and produces cryptographically signed audit records; enforces authorization decisions at 53ms median latency.",
     "https://arxiv.org/abs/2603.20953",
     "arXiv",
     "Published Mar 21 2026. Addresses the enforcement gap between token issuance and actual tool execution that OAuth alone cannot close — the protocol-layer corpus focuses on issuance-side mechanisms; OAP is the first empirically validated enforcement-side proposal with latency numbers. Complements draft-munoz-scitt-permit-profile (pre-execution permit) and the EMILIA Protocol family (post-execution receipts)."),

    ("Open Challenges in Multi-Agent Security (de Witt et al., arXiv:2505.02077)",
     "Introduces 'multi-agent security' as a new field distinct from AI safety and traditional cybersecurity; covers threats emerging from agent-to-agent interaction — secret collusion, coordinated swarm attacks, disinformation cascades, and evasion via dispersion; derives a unified research agenda across AI security, multi-agent learning, distributed systems, and governance.",
     "https://arxiv.org/abs/2505.02077",
     "arXiv",
     "Published May 5 2025 (latest version Apr 29 2026); authors: Christian Schroeder de Witt + 23 co-authors (Oxford, DeepMind, MIT, others). 24-author collaboration is a strong legitimacy signal. The inter-agent trust threat model is directly relevant to the audit-architecture and delegation-chain clusters; provides the threat landscape that the IETF drafts respond to."),

    ("Governing Dynamic Capabilities: Cryptographic Binding and Reproducibility Verification for AI Agent Tool Use (Zhou, arXiv:2603.14332)",
     "Identifies the 'capability-identity gap' — agents acquire capabilities at runtime via MCP and A2A post-authorization, enabling silent capability escalation; proposes capability-bound agent certificates (X.509 v3 extensions with skills manifest hash), reproducibility commitments using LLM near-determinism, and a hash-linked verifiable interaction ledger.",
     "https://arxiv.org/abs/2603.14332",
     "arXiv",
     "Published Mar 2026; author: Ziling Zhou (Genupixel Technology). The capability-identity gap concept is distinct from what the current corpus addresses — token-attenuation drafts bound authority at issuance, but this gap occurs post-issuance as agents dynamically load new tools. Thematically adjacent to draft-sharif-x509-agent-identity-profile which also uses X.509v3 extensions for agent capability binding."),
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

    ("ADCS — Agent Delegation Chain Standard v1.0.0 (kahalewai)",
     "A vendor-neutral open specification for managing permissions across multi-agent AI workflows using cryptographic verification at each delegation hop. Core principle: scope can only narrow, never expand (monotonic restriction). Three cumulative conformance levels (core data model → JWT tokens → production infrastructure), a four-phase verification algorithm (structural, cryptographic, temporal, monotonic), seven standardized constraint types, and DID-based signing. Protocol bindings for MCP, A2A, ACP, and HTTP.",
     "https://github.com/kahalewai/adcs/blob/main/spec/ADCS-Standard-v1.0.0.md",
     "Open-source spec (Apache-2.0)",
     "Version 1.0.0 Public Draft for Community Review, dated 2026-04-11. Spec-only repository — no separate reference implementation. Advanced features include chain compaction, CAEP continuous revocation, multi-party quorum, and permission escalation. The monotonic-restriction guarantee is the same invariant as OVID-ME's Cedar-based subset proof and ZeroID's automatic scope attenuation — three independent approaches to the same core security property."),

    ("x401: HTTP Proof Requirement Protocol (Proof / Circle)",
     "A community specification defining an HTTP-native wrapper for credential-based proof requirements, using three dedicated headers — PROOF-REQUIRED, PROOF-PRESENTATION, and PROOF-RESPONSE — to gate access to protected resources. The verifier encodes a W3C Digital Credentials API / OpenID4VP / DCQL request in PROOF-REQUIRED; the agent acquires and presents a verifiable presentation; an optional fourth leg exchanges the VP for a reusable OAuth 2.0 token. Designed to be stateless at the verifier, transport-agnostic, and composable with existing credential protocols rather than replacing them.",
     "https://x401.proof.com/spec/latest",
     "Community spec (Proof / Circle)",
     "Version 0.2.0, Draft. Editors: Daniel Buchner (Proof), Bhushit Agarwal (Circle); contributors from Google, Okta, OpenAI, MATTR. Explicitly does not replace OpenID4VP or the W3C Digital Credentials API — fills the HTTP-layer gap between those protocols and application-level authorization. Analogous positioning to how RFC 9728 (OAuth Protected Resource Metadata) provides the HTTP-layer discovery wrapper for OAuth; x401 provides the HTTP-layer challenge wrapper for VC presentations. Agent authentication and binding are composable add-ons, not mandatory."),

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

    ("Mission-Bound Authorization on the Wire (McGuinness, 22 May 2026, re-issued 22 Jul 2026)",
     "The protocol-level proposal. Five wire additions on top of existing OAuth: a 'mission_intent' RAR envelope (purpose, mission_expiry, context), a generic 'resource_access' RAR type, a durable Mission record at the Authorization Server, an opaque 'mission' claim (id + origin) on access tokens, and a Mission-state enforcement gate on refresh / exchange / introspection / assertion validation. Seven-state Mission lifecycle (pending_approval, active, suspended, revoked, expired, completed, rejected). proposal_hash (SHA-256 over JCS-canonical authorization_details) and consent_rendering_hash anchor what was approved versus what the user saw.",
     "https://notes.karlmcguinness.com/notes/mission-bound-authorization-on-the-wire/",
     "Architect blog (Karl McGuinness)",
     "**RE-SLUGGED — the original /notes/mission-bound-oauth-mvp URL now 404s** (caught in the 26 Aug 2026 sweep). Re-issued 22 Jul 2026 as a chapter of the Mission-Bound Authorization handbook under the new title and slug; content verified equivalent (mission_intent, proposal_hash, resource_access all still present). Part of a site-wide rename of \"Mission-Bound OAuth\" to \"Mission-Bound Authorization\". 76-min read; the substrate post for the whole series. Target I-D name: draft-mcguinness-oauth-mission-bound-minimum-profile. Conformance Ladder L0–L5 (L0 baseline OAuth → L5 verifiable governance with portable receipts). Cross-AS handoff uses ID-JAG for user-rooted flows or the Fletcher Transaction Token Chaining Profile for Txn-Token-rooted flows. Mission Expansion creates a successor Mission with 'mission.supersedes' rather than mutating in place. Three Resource Server tiers (RS-A OAuth-only → RS-D Mission-state aware via introspection or SSF/CAEP events). Architectural challenges acknowledged honestly: state-sync at scale, unknown-constraint brittleness, lethal-trifecta boundary."),

    ("The Mission Is the Missing Abstraction (McGuinness, 1 Jun 2026, re-issued 22 Jul 2026)",
     "The architectural frame: OAuth has no first-class object for 'the task the user approved' — only tokens, scopes, prompts, and logs that are downstream projections of it. The Mission is that durable, AS-stored, user-approved authority record. Argues this is what closes the gap that five prior bodies of his work (Power of Attorney, Mission Shaping, Open-World OAuth, Sessions Are Not Missions, the Mission-Bound architecture series) have circled from different angles. Two layers, one object: issuance-bound authority (MVP) plus runtime-enforced authority (the IBAC profile).",
     "https://notes.karlmcguinness.com/notes/the-mission-is-the-missing-abstraction/",
     "Architect blog (Karl McGuinness)",
     "**RE-SLUGGED — the original URL now 404s** (caught 26 Aug 2026); the word \"OAuth\" was dropped from both title and slug in the 22 Jul 2026 handbook re-issue. Short (9-min) framing post that ties the whole programme together. The argument for why IBAC becomes practical when intent is compiled from an AS-validated Mission at consent time rather than inferred post-hoc from agent behaviour (where it's adversarial-input territory and the PDP has no user to ask). Best entry point for someone new to the series."),

    ("Mission-Bound Runtime Enforcement (McGuinness, 1 Jun 2026, re-issued 22 Jul 2026)",
     "The IBAC layer layered on the MVP. Core (required for compliance): Intent-to-Policy Compilation (AS deterministically compiles approved authorization_details to an evaluable artifact at activation, stores policy_version on the Mission), Resource-Side Enforcement Contract (RS-B minimum, PDP evaluates every consequential request), Standard Subset Semantics per RAR Type with strict-refuse on unknown constraints (stricter than MVP's 'preserve or refuse'), Mission Introspection Profile (extended response with act chain, tenant, subject, policy_version), Runtime Denial and Escalation via ARAP (MUST), Local-Action Boundary requiring AuthZEN Access Evaluation for non-OAuth actions, Parameter Binding / TOCTOU Protection (parameter_digest bound to the permit), Decision Evidence Records (per-decision audit record bound to mission.id, proposal_hash, policy_version, decision, constraint clauses, act chain). Six Optional Modules: Tool Binding Profile, Decision Receipt Profile (W3C VC 2.0), Actor Provenance Profile, Purpose Registry Profile, Attestation Profile (RATS PTV + WIMSE), Policy Projection Profile (Cedar carriage).",
     "https://notes.karlmcguinness.com/notes/mission-bound-runtime-enforcement/",
     "Architect blog (Karl McGuinness)",
     "**RE-SLUGGED — the original URL now 404s** (caught 26 Aug 2026); re-issued 22 Jul 2026 as a handbook chapter, dropping both \"OAuth\" and \"Profile\" from the name. 37-min read; target I-D name: draft-mcguinness-oauth-mission-bound-runtime-enforcement-profile. Six-class action classification (non-consequential → consequential read → consequential write → irreversible → external commitment → privileged administration) determines PDP-gate requirement and parameter binding. Four PDP deployment modes (AS-hosted, RS-hosted, tenant governance, federated). Goal pair: 'execution continuity' (every in-bounds action succeeds; every out-of-bounds becomes governed Mission Expansion) plus 'proof of authority' (per-decision cryptographic receipts). Acknowledges PDP latency overhead and tool-manifest fracturing as real challenges."),

    ("Authorization Denied Is No Longer Enough (McGuinness, 2 Jun 2026)",
     "The framing post for ARAP. In closed-world authorization, 'decision:false' was the end of the interaction. In open-world agentic systems with runtime discovery, sub-agent delegation, and evolving missions, denial is increasingly the beginning of a governance escalation — and the missing protocol primitive is a 'requestable denial': a deny that names where to ask and binds the request to the exact evaluation it remediates. Why CIBA isn't the answer (CIBA solves authentication freshness; this is about governance state). Why approvals aren't authority (reevaluation against current state, not standing entitlement).",
     "https://notes.karlmcguinness.com/notes/authorization-denied-is-no-longer-enough/",
     "Architect blog (Karl McGuinness)",
     "Confirms that the AuthZEN ARAP profile was adopted as a working group draft in May 2026 — material maturity signal. Useful as the 'why' read alongside the ARAP spec itself. Also positions the work against AARM (Autonomous Action Runtime Management, aarm.dev/spec) which intercepts every agent action and resolves to allow/deny/modify/step-up/defer — ARAP standardizes the deny+escalate boundary at the AuthZEN layer."),

    ("Re-Subjecting Is a Mint, Not an Attenuation (McGuinness, 8 Jun 2026)",
     "Argues that crossing subject namespaces — mapping a user's identity from one application's identifier to another's — is a minting operation, not attenuation. Attenuation can narrow authority already represented by an existing artifact; it cannot authoritatively create a target-local identity binding the original issuer never supplied. Only a trusted IdP or broker can perform that translation. Distinguishes two topologies: caller-pushed (intermediate app returns to the IdP for a new assertion) and resource-pulled (destination resolves user identity through a broker). Separates workload identity (which service is calling) from user context (which person delegated the work) as requiring distinct claims.",
     "https://notes.karlmcguinness.com/notes/re-subjecting-is-a-mint-not-an-attenuation/",
     "Architect blog (Karl McGuinness)",
     "Published 8 Jun 2026; a standalone conceptual post outside the four-part Mission-Bound series but thematically continuous with it. Directly relevant to cross-AS delegation flows in the MVP post (ID-JAG for user-rooted re-subjecting) and to the token-exchange-target-service-discovery I-D. Privacy note: every intermediary-visible artifact should minimize identifiers that enable unauthorized cross-context linking."),

    ("Mission Architecture on AAuth (McGuinness, 15 Mar 2026)",
     "Engages directly with Dick Hardt's AAuth protocol, examining whether AAuth's conversational flow and native agent identity could host Mission governance better than OAuth; concludes both architectures require an explicit, durable Mission object for lifecycle governance, approval evidence, and actor continuity — AAuth's strengths are transport-level, not governance-level.",
     "https://notes.karlmcguinness.com/notes/mission-architecture-on-aauth/",
     "Architect blog (Karl McGuinness)",
     "Published Mar 15 2026; the fifth McGuinness blog entry in the corpus (the four-part Mission-Bound series above plus this standalone analysis). Significant because it directly engages draft-hardt-oauth-aauth-protocol (the corpus OUTLIER — zero OAuth dependencies), bridging the two most architecturally influential individual contributors in the corpus. McGuinness argues Mission governance requires a durable object regardless of transport; Hardt argues PoP-by-default and AS-to-AS federation require architectural replacement. These positions are complementary at different layers."),

    ("Enterprise-Managed Authorization for MCP (Paul Carleton, Anthropic MCP Blog, 18 Jun 2026)",
     "Announces Enterprise-Managed Authorization (EMA) extension enabling SSO-based MCP server provisioning through enterprise identity providers, eliminating per-app OAuth friction; explicitly uses the Identity Assertion JWT Authorization Grant (ID-JAG) as the underlying token exchange mechanism. Early adopters include Okta, Claude, VS Code, Asana, Atlassian, Figma, and Supabase.",
     "https://blog.modelcontextprotocol.io/posts/enterprise-managed-auth/",
     "Vendor blog (Anthropic / MCP)",
     "Published Jun 18 2026; author: Paul Carleton (MCP Core Maintainer). One of the first production deployments of draft-ietf-oauth-identity-assertion-authz-grant (ID-JAG, corpus WG draft) at enterprise scale. Multi-vendor adoption (8 platforms at launch) signals ID-JAG is de-facto production-ready even before RFC publication. Cross-App Access from Okta is the identity provider backbone."),

    ("Workload Identity: Key Takeaways from IETF 122 (Kasselman, Defakto Security, 26 Mar 2025)",
     "Reports on WIMSE WG's adoption of three working-group drafts at IETF 122: WIMSE Architecture, Service-to-Service Authentication, and Workload Identity Practices; addresses AI agent identity requirements — credentialing every AI workload, least-privilege scope, and permission escalation mechanisms — within the WIMSE framework.",
     "https://www.defakto.security/blog/workload-identity-key-takeaways-from-ietf-122/",
     "Practitioner blog (Defakto Security)",
     "Published Mar 26 2025; author: Pieter Kasselman (VP Open Standards, Defakto Security) — co-author of draft-klrc-aiagent-auth, draft-fletcher-transaction-token-chaining-profile, and draft-ietf-oauth-first-party-apps (all in corpus). Documents the WIMSE WG milestone that provides the workload-identity substrate for the AI agent extension family; useful primary-source account of the IETF milestone from the author who subsequently filed klrc-aiagent-auth."),

    ("Whither User-Managed Access in the AI Agent Era? (Eve Maler, Venn Factory, 10 Jul 2025)",
     "Examines whether UMA 2.0 remains relevant for AI agent delegation, distinguishing whether agents function as OAuth client apps or as requesting parties with their own legal standing; argues UMA 'basically exists for this' but identifies gaps: dynamic resource discovery, multi-level delegation tracking, and the need for standardized infrastructure analogous to Microsoft's On-Behalf-Of flow.",
     "https://workshop.vennfactory.com/p/whither-user-managed-access-in-the",
     "Practitioner blog (Venn Factory)",
     "Published Jul 10 2025; author: Eve Maler (primary author of UMA 2.0, former VP Innovation at ForgeRock, W3C TAG). The UMA specification is in the Other Standards & Govt tab; this is the spec author's own analysis of its applicability to AI agents. Identifies the same gaps (dynamic resource discovery, multi-level delegation) that the DAWN and identity-chaining IETF work addresses — useful bridge between the Kantara UMA entry and the active IETF corpus."),

    ("Tangled Tokens and Authorized Agents (Justin Richer, 15 May 2025)",
     "Examines how MCP's proxy model creates two distinct authorization contexts (agent-to-MCP-server and server-to-upstream-resource) that OAuth's pre-registration assumptions don't accommodate cleanly; argues for credential-mapping strategies adapted from email IMAP patterns and identifies unresolved tensions around static OAuth registration and MCP server allowlisting.",
     "https://justinsecurity.medium.com/tangled-tokens-and-authorized-agents-331e4db02fb4",
     "Practitioner blog (Justin Richer)",
     "Published May 15 2025; author: Justin Richer (independent OAuth expert, co-author of OAuth 2.0 in Action, former GNAP WG co-chair). The IMAP credential-mapping analogy is the most concrete prior-art framing for the MCP authorization problem. Complements the Dan Moore Stack Overflow Blog post (below) which covers the MCP OAuth 2.1 spec detail; this post covers the architectural gap the spec doesn't resolve."),

    ("Is That Allowed? Authentication and Authorization in Model Context Protocol (Dan Moore, Stack Overflow Blog, 21 Jan 2026)",
     "Technical walkthrough of MCP's OAuth 2.1 implementation: Authorization Code grant with mandatory PKCE, RFC 9728 protected resource metadata for server discovery, and the RFC 8707 resource parameter; explicitly names the gap that MCP spec does not mandate how servers authenticate with backend services.",
     "https://stackoverflow.blog/2026/01/21/is-that-allowed-authentication-and-authorization-in-model-context-protocol/",
     "Practitioner blog (Stack Overflow Blog)",
     "Published Jan 21 2026; author: Dan Moore (Head of Developer Relations, FusionAuth). Directly references RFC 8414 (OAuth Server Metadata), RFC 8707 (Resource Indicators), RFC 9728 (Protected Resource Metadata) — all IETF corpus entries. Stack Overflow Blog platform gives this mainstream engineering reach. The gap identified (server-to-backend auth unspecified by MCP) is the same gap that draft-ietf-oauth-identity-assertion-authz-grant and klrc-aiagent-auth address."),

    ("AI Agent Authentication Gets the Hard Part Right. Authorization Is Still Your Problem. (Rock Lambros, RockCyber Musings, 17 Mar 2026)",
     "Analyzes draft-klrc-aiagent-auth-00 in depth, praising its identity layer (WIMSE + SPIFFE composition) but flagging that the Security Considerations section contains only 'TODO Security'; recommends layering OPA or Cedar policy engines for actual authorization and names AuthZEN as a candidate gap-filler.",
     "https://www.rockcybermusings.com/p/i-agent-authentication-authorization-gap",
     "Practitioner blog (RockCyber Musings)",
     "Published Mar 17 2026; author: Rock Lambros. One of the few practitioner posts that analyzes a specific IETF draft (draft-klrc-aiagent-auth, corpus) in depth and names the authorization gap that authentication alone doesn't close. The 'TODO Security' observation was accurate as of the -00 filing; draft-klrc-aiagent-auth has since reached -03 (6 Jul 2026) — re-check whether Security Considerations were filled in."),

    ("Least Privilege for AI Agents: Identity, Access, and Tool Binding (Microsoft Security Blog, 16 Jul 2026)",
     "Microsoft's blueprint for applying least-privilege to agentic workloads: unique dedicated agent principals with named owners and explicit purpose statements, task-based roles scoped to specific resources, controlled tool access allowlists, and end-to-end auditability requirements; positions agent identity as a first-class security principal requiring the same governance as human identities.",
     "https://www.microsoft.com/en-us/security/blog/2026/07/16/least-privilege-for-ai-agents-identity-access-and-tool-binding/",
     "Vendor blog (Microsoft Security)",
     "Published Jul 16 2026. Microsoft's most recent major position on least-privilege for agents; extends the earlier Azure and Microsoft Entra entries in the corpus with specific tool-binding guidance. The named-owner and explicit-purpose-statement requirements align directly with Mission-Bound OAuth's proposal_hash and consent_rendering_hash binding. First Microsoft Security Blog entry to use 'tool binding' as a security term of art."),

    ("Solving the Identity Crisis for AI Agents (Uber Engineering)",
     "A production engineering post from Uber describing their agent identity architecture: an Agent Registry (workload-to-agent mapping), a SPIRE-backed STS that issues short-lived JWTs with embedded actor chains at P99 below 40ms, an MCP Gateway as policy enforcement point, and an AI Agent Mesh for agent-to-agent communication. A standardized A2A client automates token exchange and chain propagation across agent hops.",
     "https://www.uber.com/us/en/blog/solving-the-agent-identity-crisis/",
     "Industry blog (Uber Engineering)",
     "Published 21 May 2026; six-author post (Mathew, Borole, Huang, Burykin, Goel, Walsh) from Uber's platform engineering team. Architecture aligns with WIMSE workload identity (SPIRE as the credential foundation), RFC 8693 actor-chain propagation, and single-hop short-lived JWTs with audience-scoped claims. One of the few public disclosures of a production-grade agent identity system at hyperscaler scale — a real-world reference point for the corpus's delegation-chain design patterns."),

    ("Agents Are Not Just Workloads (Patrick Parker, LinkedIn)",
     "Argues that classifying AI agents as 'workloads' is a category error that corrupts identity architecture: workloads are a what-runs-where concept, agents are a who-acts-on-whose-authority concept. Identifies five breakdown areas where workload-identity patterns fail for agents: intent captured as static token claims, delegation gaps (no purpose binding or revocation paths), overlooked tool-catalog authorization surface, bearer-credential custody ambiguity under prompt injection, and mutable logs insufficient as tamper-evident authorization evidence.",
     "https://www.linkedin.com/pulse/agents-just-workloads-patrick-parker-0qxte/",
     "Industry blog (LinkedIn)",
     "Published 9 Jun 2026. Proposes signature-based receipts binding relationships, authority, tasks, and bounds; runtime validation of generated task intent; and AuthZEN gateway-based enforcement. A principled counterpoint to the WIMSE-as-sufficient-for-agents framing — pairs well with the Uber Engineering post (which uses SPIRE/WIMSE as the credential foundation but adds actor chains and MCP gateway enforcement on top)."),

    ("Creating a Relationship Binding (Tom Jones)",
     "A community whitepaper proposing a signed 'Consent to Create Binding' JWT/JWS message that establishes a subject-bound relationship identifier (UUID or DID) between a user and a set of agents or service providers. The message carries 16 mandatory/optional fields: issuer, subject, subject role, context (trust framework), permissions, device statement, identity proof, purpose of use, key material, and signature. Includes a lifecycle termination model (session, cookie, transaction, relationship, and legal-based retention scopes) and a companion 'Consent Receipt with Binding' response. A second section argues that relationship-based governance — binding actors through mutual obligations, escalation paths, and accountability chains — is more resilient for AI agent systems than representational approaches (policies, classifications, static maps).",
     "https://docs.google.com/document/d/1CwBDRbw147YlNld-UOlJ4lGvmpDIOCSI/edit#heading=h.kp911j18z01y",
     "Community whitepaper",
     "No publication date in the document; primary use case is healthcare (NIST IAL2/AAL2). Draws on Kantara's Distribute Assurance Specification for identity assurance levels and references OpenID Connect id_token as the closest existing message shape. The Consent to Create Binding message adds purpose of use, device statement, and lifecycle termination semantics that id_token lacks. Companion doc 'Digital Contracts Made Legally Valid' (separate Google Doc) covers giving the binding legal status. Relationship-governance argument is thematically aligned with Parker's 'Agents Are Not Just Workloads' — both argue that accountability chains and mutual obligations are the right governance primitive for agentic systems."),

    ("Intent Agent Native Authorization for Agentic Profiles (IANA-AP) (Martin Besozzi, Jul 2026)",
     "Proposes a four-phase runtime authorization lifecycle for AI agents: discovery (agent capabilities + API authorization mappings), intent computation (agent generates planned operations), review/approval (user provides explicit phishing-resistant consent via WebAuthn/FIDO2 passkeys before execution), and enforcement (every runtime invocation validated against the approved authorization artifact). Composes RFC 9396 RAR, OAuth FiPA, OpenID AuthZEN, MCP, SPIFFE JWT-SVIDs, and CEL policy mappings into a single coherent framework.",
     "https://embesozzi.github.io/posts/martin-besozzi/intent-agent-native-authorization-agentic-profiles/",
     "Architect blog (Martin Besozzi)",
     "Updated July 2026; includes open specification and reference implementation on GitHub. The SARC (Subject, Action, Resource, Context) model and 'x-authz-mapping' Agentic Profile extension are novel additions. The four-phase pre-execution approval requirement directly parallels draft-nelson-agent-delegation-receipts and draft-sato-soos-idp — but grounds it in existing OAuth standards rather than new protocol primitives. One of the few practitioner-level posts that explicitly composes AuthZEN, RAR, and FiPA into a working agent authorization flow."),

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

    ("ACLX — AI Output Governance (Proprietary)",
     "A proprietary enforcement layer that intercepts AI-generated content between inference and delivery, evaluating it against OPA/Cedar policies, identity context, and a three-phase sensitivity detection stack: deterministic regex rules → ontology-based compilation-risk scoring → semantic LLM evaluation for novel synthesis. Four enforcement outcomes: ALLOW, REDACT, BLOCK, or ESCALATE to human review. Treats agents as first-class principals evaluated at the output boundary regardless of whether a session or IDP exists.",
     "https://aclx.ai/",
     "Proprietary product",
     "No published specification. Identifies a gap the corpus standards map does not yet cover: identity (OIDC/SCIM/SPIFFE), signals (CAEP/SSF), policy (OAuth/AuthZEN/OPA), and enforcement (ZTA/RATS/SCITT) all have standards, but output evaluation — governing what the AI synthesizes rather than what the user was authorized to ask — has none. The synthesis-detection layer (AI compiling across individually-authorized sources to produce content crossing a higher sensitivity boundary) is a novel problem the corpus's existing standards do not address."),

    # ---- Karl McGuinness / Control Plane blog backfill — Aug 2026 sweep ----

    ("McGuinness — Kerberos Won Because Nobody Had to Implement It",
     "The question worth asking about AAuth is not only whether the protocol is good. Kerberos won because of everything around the protocol: SSPI and GSS-API hid the mechanism from application developers, the LSA owned keys and ticket lifecycle, machine accounts existed as a side effect of domain join, Active Directory shipped the KDC by default, and SPNEGO made rollout incremental.",
     "https://notes.karlmcguinness.com/notes/kerberos-won-because-nobody-had-to-implement-it/",
     "Industry blog (Independent)",
     "Published 10 Aug 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — The Runtime Mints the Identity. That Does Not Make It the Authority.",
     "Agent runtimes naturally create the first trustworthy evidence about an instance, which gives them the default position in agent identity. Runtime proof and enterprise binding are still separate jobs. In heterogeneous enterprises, a binding layer can map evidence from many runtimes into durable Agent and Agent Deployment records and supply that governed context to credential issuers and resources.",
     "https://notes.karlmcguinness.com/notes/the-runtime-mints-the-identity/",
     "Industry blog (Independent)",
     "Published 10 Aug 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — Agent Authority Has No General System of Record",
     "Agent task authority is scattered across four de facto records: harness permission prompts, OAuth grants, IAM roles, and change tickets. Each performs a real job, but none is a general, portable system of record for approved work. An action click is not task approval, a grant is not a task lifecycle, and an identity role is not a reason for one undertaking.",
     "https://notes.karlmcguinness.com/notes/agent-authority-has-no-system-of-record/",
     "Industry blog (Independent)",
     "Published 10 Aug 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — The MCP Lesson",
     "The control-points series argues that distribution determines defaults and standard seams determine whether those defaults remain contestable. MCP adds the clock. It launched with a specification, SDKs, a distributed host, and reference servers, and one developer could run the whole loop before the ecosystem coordinated. Mature authorization and governance followed the adoption pressure.",
     "https://notes.karlmcguinness.com/notes/the-mcp-lesson/",
     "Industry blog (Independent)",
     "Published 10 Aug 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — Cross App Access Shows How the Layered Play Ships",
     "Cross App Access is not twenty-five generally available integrations. It is three different things at three different stages: a stable MCP authorization extension, a live Claude and Okta beta, and a partner graph whose broader product rollout is still under way. That distinction makes the strategic result clearer.",
     "https://notes.karlmcguinness.com/notes/cross-app-access-is-the-layered-play-shipping/",
     "Industry blog (Independent)",
     "Published 10 Aug 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — A Blocked Agent Is a Captive Client",
     "Long-running agents discover mid-task that they need a destination their egress proxy does not allow, and the block comes back as an opaque connection failure with no machine-actionable way to ask for access and no human standing by. That block is a requestable denial, and the egress proxy is a policy enforcement point.",
     "https://notes.karlmcguinness.com/notes/a-blocked-agent-is-a-captive-client/",
     "Industry blog (Independent)",
     "Published 10 Aug 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — The Company's Memory Must Be an Enterprise Record",
     "Model routers and customer-controlled agent state are now concrete product architectures, but they do not make every model interchangeable or every memory store strategic. The important boundary is narrower. Task checkpoints are operational state, transcripts are evidence, embeddings are derived indexes, and model-generated memories are untrusted proposals.",
     "https://notes.karlmcguinness.com/notes/the-companys-memory-is-an-enterprise-record/",
     "Industry blog (Independent)",
     "Published 10 Aug 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — Continuity Is Not One Thing",
     "Delegated work forces four separate continuity questions: request provenance, identity attribution, target-applicable authority, and continuing work justification. Their answers compose through a common boundary contract: authoritative sources, bound and correlated evidence, explicit lifecycle semantics, local decisions, and declared failure behavior.",
     "https://notes.karlmcguinness.com/notes/continuity-is-not-one-thing/",
     "Industry blog (Independent)",
     "Published 10 Aug 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — The Continuity Evaluation Kit",
     "Continuity Is Not One Thing argues that delegated work poses four independently governed continuity questions.",
     "https://notes.karlmcguinness.com/notes/continuity-evaluation-kit/",
     "Industry blog (Independent)",
     "Published 10 Aug 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — The Enterprise Agent Control Stack",
     "The enterprise agent control stack is not one product or one call chain. It is a set of independently governed answers: which instance is running, whose Agent it is, which deployment was approved, why its current work remains authorized, what an issuer may project, how credentials are acquired and presented, whether a resource permits one concrete action, and which evidence proves the joins afterward.",
     "https://notes.karlmcguinness.com/notes/the-enterprise-agent-stack/",
     "Industry blog (Independent)",
     "Published 10 Aug 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — Least-Privilege MCP Tool Calls Need a Mission",
     "The least-privilege MCP series ends on a gap: token-side and resource-side authorization both work per call, and neither names the task the user approved. This essay applies Mission-Bound Authorization at the MCP boundary.",
     "https://notes.karlmcguinness.com/notes/least-privilege-mcp-tool-calls-need-a-mission/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — Least Exposure Is Broader Than Least Privilege",
     "Least privilege scopes what an agent may do, one tool call at a time. But a perfectly authorized agent can still be compromised by what it is allowed to see. Least exposure is the broader control: task-scoped minimal disclosure for prompt context, retrieved documents, tool schemas, secrets, business rules, approval context, memory, and downstream responses.",
     "https://notes.karlmcguinness.com/notes/least-exposure-is-broader-than-least-privilege/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — The Question Authorization Never Answered",
     "Authorization looks the way it does because each generation solved the question its era made urgent, and deferred one question that someone else was always carrying: what approved work is this, and is it still on? Purpose was not absent. A second stack of tickets, purchase orders, workflows, and approval systems held it locally, and people carried it between systems.",
     "https://notes.karlmcguinness.com/notes/the-question-authorization-never-answered/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — Weighing Mission-Bound Authorization",
     "A handbook that ends on its own argument has not concluded, it has just stopped.",
     "https://notes.karlmcguinness.com/series/weighing-mission-bound-authorization/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); series index. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — Testing Mission-Bound Authorization",
     "An architecture that only answers its own questions is untested. This chapter runs the handbook against five outside framings: Simon Willison’s lethal trifecta, the threat model that defines what makes agents dangerous. Patrick Parker’s Seven Laws of AIdentity, mapped law by law with coverage and caveats stated rather than claimed whole.",
     "https://notes.karlmcguinness.com/series/testing-mission-bound-authorization/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); series index. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — Building Mission-Bound Authorization",
     "Designing Mission-Bound Authorization establishes the architecture: the object, the laws, the framework, and the staged adoption path. This chapter is the build.",
     "https://notes.karlmcguinness.com/series/building-mission-bound-authorization/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); series index. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — Designing Mission-Bound Authorization",
     "The AI agent auth best-practices draft names the Mission and declares its translation into authorization out of scope. This chapter is that translation, at architecture depth: the problem in one screen, the vocabulary, the missing layer, the five laws, the reference security architecture, and the canonical picture. Part 1 is the joint between the card model and the protocol. Part 2 defines the Mission.",
     "https://notes.karlmcguinness.com/series/designing-mission-bound-authorization/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); series index. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — What the Corporate Card Already Solved",
     "Enterprises already run a mature delegated-authority architecture. It is called expense governance, and payments spent fifty years hardening it: purpose-issued instruments, approvals bound to what the approver was shown, delegation that only narrows, a network that authorizes every transaction, and cancellations, disputes, and statements that close the loop.",
     "https://notes.karlmcguinness.com/series/what-the-corporate-card-already-solved/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); series index. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — The Identity Continuation Assertion",
     "Re-subjecting across a SaaS boundary is a mint, not an attenuation, so the IdP must issue each onward grant. ID-JAG covers the first hop, where an application holds the user’s ID Token or SAML assertion to exchange. Subsequent hops hold no end-user credential, which leaves a gap: the intermediate has nothing to present to the IdP to continue the chain. The Identity Continuation Assertion fills it.",
     "https://notes.karlmcguinness.com/notes/identity-continuation-assertion/",
     "Industry blog (Independent)",
     "Published 8 Jul 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — Trusting Issuers in Open-World OAuth",
     "Self-service agent sign-up exposes a first-contact trust problem: a Resource Authorization Server can verify a perfectly valid JWT and still not know whether the issuer is allowed to assert identities for the user’s domain. That is two questions, not one.",
     "https://notes.karlmcguinness.com/notes/trusting-issuers-in-open-world-oauth/",
     "Industry blog (Independent)",
     "Published 5 Jul 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — Closing the Gaps in Least-Privilege MCP Tool Calls",
     "Part one laid out two ways to lock down a single tool call an agent makes through the Model Context Protocol: carry a narrow token, or let the resource decide each call. This part walks the standards that close the gaps.",
     "https://notes.karlmcguinness.com/notes/closing-the-gaps-least-privilege-mcp-tool-calls/",
     "Industry blog (Independent)",
     "Published 26 Jun 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — Two Models for Least-Privilege MCP Tool Calls",
     "There are two natural ways to lock an agent’s Model Context Protocol (MCP) tool calls down to least privilege. The agent can carry a narrow token scoped to the action, or the server can decide each call as it happens. Carrying a token gives portable proof of what the agent may do, but pushes domain knowledge onto the authorization server and token management onto the client.",
     "https://notes.karlmcguinness.com/notes/least-privilege-mcp-tool-calls/",
     "Industry blog (Independent)",
     "Published 25 Jun 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — Authorization Is the Other Half of Executable Intent",
     "Microsoft’s ASSERT compiles written behavior requirements into executable evaluations: intent made executable for verification. That answers what the agent did, not what it was allowed to do: an eval produces a verdict, not a binding authorization decision, and for irreversible actions that is the whole difference.",
     "https://notes.karlmcguinness.com/notes/authorization-is-the-other-half-of-executable-intent/",
     "Industry blog (Independent)",
     "Published 10 Jun 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — SAML at the Post-Quantum Crossroads",
     "OpenID Connect is mature, standardized, and widely deployed, but SAML remains the enterprise SSO default because it is familiar, explicit, and deeply embedded in procurement and operations.",
     "https://notes.karlmcguinness.com/notes/saml-at-the-post-quantum-crossroads/",
     "Industry blog (Independent)",
     "Published 28 May 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — The Agent Provider Is the IdP: A Standards Reading of WorkOS auth.md",
     "WorkOS auth.md is an agent-readable registration document for one-click setup, with Agent Verified, user-claimed, and anonymous paths. In the Agent Verified path, most pieces already exist across OAuth and OpenID standards: ID-JAG, OAuth metadata, dynamic client registration, standard token endpoints, and SSF/CAEP/OPC.",
     "https://notes.karlmcguinness.com/notes/agent-provider-is-the-idp-standards-reading-of-workos-auth-md/",
     "Industry blog (Independent)",
     "Published 22 May 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — Sessions Are Not Missions",
     "Modern agent harnesses make work durable across restarts, devices, background jobs, and sub-agents. That durability is a runtime property, not a governance property. A session answers where the agent can continue working. A mission answers why the agent is allowed to keep working. Conflating them is a central failure mode of long-running autonomous agent systems.",
     "https://notes.karlmcguinness.com/notes/sessions-are-not-missions/",
     "Industry blog (Independent)",
     "Published 11 May 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — Client Instances Are Actors, Not New Clients",
     "Client instances are not new clients. They are actors. With the Actor Profile and the act chain already in place, and an instance_issuers field that fits any client registration channel (static, Dynamic Client Registration, or CIMD), treating instances as first-class actors needs no new grant type, no new client type, and no new claim. It needs a profile that ties them together.",
     "https://notes.karlmcguinness.com/notes/client-instances-are-actors-not-new-clients/",
     "Industry blog (Independent)",
     "Published 5 May 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — Enterprise SaaS Needs OAuth Federation Now",
     "Enterprise SaaS still defaults to app-by-app OAuth islands with their own clients, long-lived artifacts, and revocation paths. The architectural shift is OAuth federation: adopt issuer-mediated federation now for services and workloads, and adopt Cross-App Access (XAA) as the standards direction for user-delegated cross-app access.",
     "https://notes.karlmcguinness.com/notes/enterprise-saas-needs-oauth-federation-now/",
     "Industry blog (Independent)",
     "Published 19 Apr 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — AAuth Now Has a Mission Layer",
     "The new version of AAuth (draft-hardt-aauth-protocol-01, since resubmitted as draft-hardt-oauth-aauth-protocol) materially changes the earlier comparison. Mission is now first-class in the protocol, with PS-mediated approval, mission-aware token choreography, and governance endpoints.",
     "https://notes.karlmcguinness.com/notes/aauth-now-has-a-mission-layer/",
     "Industry blog (Independent)",
     "Published 13 Apr 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — ID-JAG Beyond the Enterprise IdP",
     "ID-JAG, also often called Cross-App Access (XAA), is centered in the current draft on Enterprise IdP trust, but the issuer that matters is the immediate IdP the downstream authorization server already trusts for SSO and subject resolution, not necessarily the top-level workforce IdP.",
     "https://notes.karlmcguinness.com/notes/id-jag-beyond-the-enterprise-idp/",
     "Industry blog (Independent)",
     "Published 5 Apr 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — Open-World OAuth Still Needs Mission Shaping",
     "Open-world OAuth can improve discovery, resource binding, and first-contact trust. That still leaves the harder agent problem: how approved intent becomes bounded authority that stays governed across delegation chains, unfamiliar tools, consent expansion, revocation, and task termination.",
     "https://notes.karlmcguinness.com/notes/open-world-oauth-still-needs-mission-shaping/",
     "Industry blog (Independent)",
     "Published 21 Mar 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — OAuth for Open-World Ecosystems",
     "OAuth was built for closed worlds, and that constraint is why it became mature. Agents expose the limits of that deployment model. This post traces what the newer OAuth standards get right and which substrate gaps still need to close.",
     "https://notes.karlmcguinness.com/notes/oauth-for-open-world-ecosystems/",
     "Industry blog (Independent)",
     "Published 20 Mar 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — Standardize `act` Across Assertion Grants and JWT Access Tokens",
     "The current split between token exchange semantics and JWT access token practice creates avoidable interoperability failures. A common profile for act, grounded in entity profiles, can align JWT assertion grant and JWT access token processing.",
     "https://notes.karlmcguinness.com/notes/standardize-act-across-assertion-grants-and-jwt-access-tokens/",
     "Industry blog (Independent)",
     "Published 18 Mar 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — Mission Shaping Is Not Enough",
     "Part 2 turns from the semantic problem to the runtime one. Quiet expansion, delegation, headless execution, stale state, and open-world execution all push Mission shaping past its strongest domain. Containment and runtime governance carry more of the safety burden.",
     "https://notes.karlmcguinness.com/notes/mission-shaping-is-not-enough/",
     "Industry blog (Independent)",
     "Published 18 Mar 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — The Mission Shaping Problem",
     "This essay picks up from Part 4 of the Mission-Bound OAuth series and focuses on the first hard problem: how approved intent becomes a governable Mission. In structured domains that can look like staged Mission shaping or compilation. Many current deployments still do not do it at all.",
     "https://notes.karlmcguinness.com/notes/the-mission-shaping-problem/",
     "Industry blog (Independent)",
     "Published 17 Mar 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — Why Mission-Bound OAuth Might Be the Wrong Answer",
     "Mission-Bound OAuth is a serious attempt to govern delegated agent authority using existing OAuth infrastructure. This post takes the pessimistic view: it may be the wrong answer because it asks the authorization server to become a governance engine, a lifecycle controller, and a mission ledger all at once.",
     "https://notes.karlmcguinness.com/notes/why-mission-bound-oauth-might-be-the-wrong-answer/",
     "Industry blog (Independent)",
     "Published 15 Mar 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — Client Context and ID-JAG for Mission-Bound OAuth",
     "Rich Authorization Requests are the natural first instinct for agent missions, but audience-bound access tokens and uneven cross-domain interoperability limit how far they can carry a governed task. Mission-Bound OAuth solves that by making the Mission a durable authority object at the authorization server.",
     "https://notes.karlmcguinness.com/notes/client-context-and-id-jag-for-mission-bound-oauth/",
     "Industry blog (Independent)",
     "Published 14 Mar 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — Agents Don't Need Your Passport. They Need Your Authority.",
     "Enterprise IAM was designed for human-paced execution. Agents remove the presence, pacing, and natural scope-limiting that made those controls work. The result is a structural gap that stronger credentials, tighter scopes, and faster JIT provisioning cannot close.",
     "https://notes.karlmcguinness.com/notes/agents-dont-need-your-passport-they-need-your-authority/",
     "Industry blog (Independent)",
     "Published 21 Feb 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — From Passports to Power of Attorney",
     "Tokens, credentials, and scopes tell a system what an agent may do. They say nothing about why execution was authorized or when it should end. The Execution Mandate is the primitive that closes that gap: a signed, inspectable authority record that runtime systems can evaluate and revoke throughout the execution lifecycle.",
     "https://notes.karlmcguinness.com/notes/from-passports-to-power-of-attorney/",
     "Industry blog (Independent)",
     "Published 21 Feb 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — Governing the Stay, Not Just the Entry",
     "An Execution Mandate defines what delegated authority looks like. This post builds the control plane that makes it operational: how mandates are issued and held as authoritative artifacts, how authority is evaluated continuously rather than at gates, how governance crosses organizational boundaries, and where enforcement lands in practice.",
     "https://notes.karlmcguinness.com/notes/governing-the-stay-not-just-the-entry/",
     "Industry blog (Independent)",
     "Published 21 Feb 2026 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),

    ("McGuinness — Welcome to Control Plane",
     "Identity is getting weird again, and in a good way. This blog is where I post hot takes, field notes, and analysis on identity, security, and agentic systems. Some posts will be tactical. Some will be opinionated.",
     "https://notes.karlmcguinness.com/notes/welcome-to-control-plane/",
     "Industry blog (Independent)",
     "Published 28 Apr 2025 on Control Plane (notes.karlmcguinness.com); essay. Part of the Aug 2026 blog backfill — the corpus previously tracked only 6 of 47 posts."),


    # ---- 26 Aug 2026 sweep: pages the 11 Aug RSS pass did not surface ----

    ("Mission-Bound OAuth (McGuinness, 13 Mar 2026)",
     "The original RFC-style specification post: OAuth answers whether a request is permitted right now, while Mission-Bound OAuth asks whether a delegated mission should still be running at all. Proposes a durable Mission object at the Authorization Server governing token derivation, lifecycle, delegation and termination across agent execution. Full document structure — Introduction, Terminology and Roles, Background and Related Work, Architecture Overview, Mission Data Model, Mission Lifecycle, OAuth Protocol Integration, Mission Management, Deployment and Operational Model, Security Considerations, Privacy Considerations.",
     "https://notes.karlmcguinness.com/notes/mission-bound-oauth/",
     "Architect blog (Karl McGuinness)",
     "The genesis document of the entire Mission-Bound programme and, at 13 Mar 2026, the earliest post in it — predating the May-June series by two months and the July handbook by four. Missed by the 11 Aug 2026 sweep despite being in the RSS feed. It is written as a specification rather than an essay, which makes it the closest blog-side analogue of draft-mcguinness-oauth-mission. Note it retains the original \"Mission-Bound OAuth\" name that the July handbook renamed away from."),

    ("Mission-Bound Authorization: The Complete Edition (McGuinness, 22 Jul 2026)",
     "The whole Mission-Bound Authorization handbook on one page in reading order: the cover, the five chapters, the companions and the six appendices, with a print-to-PDF path and a Markdown rendition.",
     "https://notes.karlmcguinness.com/mission-handbook/read/",
     "Architect blog (Karl McGuinness)",
     "The single-page edition of the handbook — roughly 888KB of HTML, by a wide margin the largest single artifact in the corpus. Useful as the one URL to hand someone who wants the entire argument in one place. Its chapter list is also the authoritative index of the 27 individual handbook chapters, which are NOT exposed in the site's RSS feed and are consequently not yet tracked as individual rows."),

    ("About — Control Plane (Karl McGuinness)",
     "Author page for the Control Plane blog: Karl McGuinness, previously SVP and Chief Product Architect at Okta, now writing independently on agent authorization, OAuth, and delegated authority.",
     "https://notes.karlmcguinness.com/about/",
     "Architect blog (Karl McGuinness)",
     "Included for the same reason the series landing pages are: the corpus tracks this author's body of work in full. Useful as the provenance anchor for the 18 individual I-Ds, the 34-draft Mission-Bound family, and the 50 blog entries now attributed to him here."),

    # ---- Mission-Bound handbook chapters + handbook-only series indexes ----
    # Added 26 Aug 2026. These have their own /notes/ and /series/ URLs but are absent
    # from the RSS feed, so the 11 Aug backfill captured the series indexes without their
    # member essays. 24 chapters + 5 series indexes.

    ("McGuinness — Adopting Mission-Bound Authorization",
     "Crawl, Walk, Run. A definitive architecture that ends without a build order is a tour, not a blueprint. Most estates start at the read-only ceiling: agents capped at read access, humans approving or executing the writes, and pilots that never graduate. This closer names what that posture costs and stages the way off it: crawl by shipping the issuance profile (approved, integrity-anchored Missions and a possession-independent kill switch, honestly labeled governance rather than safety), walk by adding the Runtime-Enforced level (per-action enforcement, the AuthZEN binding, and Status freshness, all on substrate that already shipped), and run by climbing to the Governed and High-Assurance Agent levels, each of which makes a broader class of write authority defensible. Plus the ecosystem to compose with, the five operational surfaces you will own, and the pieces the community still has to s.",
     "https://notes.karlmcguinness.com/notes/adopting-mission-bound-authorization/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); chapter of the Mission-Bound Authorization handbook. **Added 26 Aug 2026 — not in the site's RSS feed**, which is why the 11 Aug backfill missed it: the corpus tracked the series index but not its member essays."),

    ("McGuinness — Agents Need a Corporate Card, Not a Blank Check",
     "What Expense Governance Already Knows About Delegated Autonomy. Nobody hands a new hire the company checkbook. In a mature spend program, they get an instrument bound to an approved purpose, checked at each transaction, metered against a budget, and frozen when the reason for the spend goes away. Agent credentials today are blank checks with expiry dates. This part walks the expense-governance loop end to end, maps each control onto agent authority, and is honest about the five places the analogy breaks. Each break is something the agent stack still has to build. In a mature spend program, she gets an instrument with a boundary: a corporate card, a virtual card, or a travel approval that controls what the card can do. It has a limit. It works for travel and software, not for jewelry. It draws against a budget someone approved for a reason, and it can die the day she leaves or the project ends. Inside those bounds, nobody reviews every p.",
     "https://notes.karlmcguinness.com/notes/agents-need-a-corporate-card-not-a-blank-check/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); chapter of the Mission-Bound Authorization handbook. **Added 26 Aug 2026 — not in the site's RSS feed**, which is why the 11 Aug backfill missed it: the corpus tracked the series index but not its member essays."),

    ("McGuinness — Answering the Laws of AIdentity",
     "A Critical Crosswalk from Patrick Parker's Seven Laws to Mission-Bound Authorization. Patrick Parker's Seven Laws of AIdentity describe the dynamics a system must govern when agents act through delegated authority: split actors, generated intent, bounded agency, continuous authorization, least exposure, justifiable action chains, and proof-carrying action. This part maps those laws onto Mission-Bound Authorization without turning resemblance into compliance. The strongest matches are generated intent and bounded agency. Continuous authorization and split-actor attribution require the runtime and identity profiles. Least exposure, chain necessity, policy retention, evidence completeness, and embodied action remain conditional or outside the current wire model. This part is the chapter’s second proof, and the one framing built for identity rather than threats. Patrick Parker published The Laws of AIdentity in May 2026 as a proposed framework for deleg.",
     "https://notes.karlmcguinness.com/notes/answering-the-laws-of-aidentity/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); chapter of the Mission-Bound Authorization handbook. **Added 26 Aug 2026 — not in the site's RSS feed**, which is why the 11 Aug backfill missed it: the corpus tracked the series index but not its member essays."),

    ("McGuinness — Canceling the Card Doesn't Stop the Charges",
     "Endings, Unwindings, and the Statement That Reconciles It All. Cancel a card and watch what refuses to end: the subscription bills the new number the network helpfully forwarded, the pending hotel charge settles days later, and the refund arrives through a process you do not control. Payments learned that ending an instrument is not ending an arrangement, and built machinery for the difference: reversible freezes, terminal cancellations, single-use cards that retire themselves, in-flight states between authorized and settled, chargebacks as governed compensation, and the statement that reconciles everything to one project code. This part maps each ending onto the agent task that must actually stop, and closes with the breaks, including the one where the analogy runs backward. Next month the gym bills you anyway, on the replacement card’s number, which you never gave it. Nothing malfunctioned. The network’s account updater service f.",
     "https://notes.karlmcguinness.com/notes/canceling-the-card-doesnt-stop-the-charges/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); chapter of the Mission-Bound Authorization handbook. **Added 26 Aug 2026 — not in the site's RSS feed**, which is why the 11 Aug backfill missed it: the corpus tracked the series index but not its member essays."),

    ("McGuinness — Closing the Agent Authorization Gaps",
     "The OAuth Community's Gap Catalog, Answered Line by Line. The standards community is converging on a problem statement: agents break OAuth's pre-approval paradigm, tokens cannot represent delegation chains, revocation cannot reach a task, and consent screens cannot survive a thousand scopes. The agent authorization use-case catalog names eleven scenarios and rolls its analysis up to six major gaps, and this part answers the catalog line by line at both grains with machinery that existed before it was published: task-level revocation is the Mission kill switch, bulk revocation is Mission Management, multi-hop chains are act chains and Child Missions, scope explosion dies at Mission-grain consent, and the new grant-versus-execution gap lands on Decision and Execution Evidence. Seven answers are partial and two are delegated, and the tally is stated rather than smoothed. The first four proofs held the model against a threat model.",
     "https://notes.karlmcguinness.com/notes/closing-the-agent-authorization-gaps/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); chapter of the Mission-Bound Authorization handbook. **Added 26 Aug 2026 — not in the site's RSS feed**, which is why the 11 Aug backfill missed it: the corpus tracked the series index but not its member essays."),

    ("McGuinness — Common Objections to Mission-Based Authorization",
     "Answers for the People Who Run Today's Control Planes. A skeptical FAQ for IAM practitioners and architects. Twenty-three objections test mission-based authorization against IdPs, workload identity, OAuth, RAR and UMA, short-lived tokens, PDPs and Zero Trust, Shared Signals, PAM and IGA, workflow engines, internal composition, open-world discovery, semantic misuse, enforcement bypass, lifecycle ownership, and privacy. The answers concede where existing systems are sufficient, identify where a Mission-shaped implementation may already exist under another name, and limit the standards case to the boundaries where private task state no longer reaches. The answer is sometimes yes . Existing products can keep task state, carry purpose attributes, issue task-specific credentials, and gate actions. A system that makes an approval-backed task record the root of authority and enforcement may already implement mission-based authorization with.",
     "https://notes.karlmcguinness.com/notes/common-objections-to-mission-based-authorization/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); chapter of the Mission-Bound Authorization handbook. **Added 26 Aug 2026 — not in the site's RSS feed**, which is why the 11 Aug backfill missed it: the corpus tracked the series index but not its member essays."),

    ("McGuinness — Containing the OWASP Agentic Threats",
     "Fifteen Agentic Threats and the LLM Top 10, Each Given a Verdict. Security reviewers do not arrive with your framing. They arrive with OWASP's: fifteen agentic threats from memory poisoning to human manipulation, plus the LLM Top 10. This part crosswalks both onto the handbook and refuses the move that makes crosswalks worthless, claiming everything. Each threat gets one of three verdicts. Contained means the threat lands on machinery built for it, with a draft behind it. Bounded means the cause is out of authorization's reach but the blast radius is capped at the action gate. Delegated means it is not an authorization problem and a named complement owns it. Six of the fifteen are contained, nine are bounded, and half the LLM Top 10 is honestly someone else's layer. The first two proofs in this chapter answered a threat model and a requirements framework. This one answers the checklist. When a security team reviews an agent deplo.",
     "https://notes.karlmcguinness.com/notes/containing-the-owasp-agentic-threats/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); chapter of the Mission-Bound Authorization handbook. **Added 26 Aug 2026 — not in the site's RSS feed**, which is why the 11 Aug backfill missed it: the corpus tracked the series index but not its member essays."),

    ("McGuinness — From a Request to an Approved Mission",
     "Shaping, Consent Evidence, and Deferred Approval with Revision. A user request is untrusted input. This part covers the integrity of the approval event, the layer before any token exists: the client-side shaper that proposes a candidate Mission Intent, the Consent Evidence that commits the structured consent disclosure the Authorization Server recorded as rendered (not the pixels or the Approver's comprehension), and the deferred and revisable approval that lets a human reviewer narrow a proposal in place. Authority is created only when the Authorization Server validates, narrows, and approves. The Mission Is the Missing Abstraction drew the boundary between Mission Intent (a proposal) and an approved Mission (the governance object). The approval event is the single moment of transition, where the Authorization Server validates the Intent, derives an Authority Set, the Approver consents, and the Mission record is committed by intent_has.",
     "https://notes.karlmcguinness.com/notes/from-a-request-to-an-approved-mission/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); chapter of the Mission-Bound Authorization handbook. **Added 26 Aug 2026 — not in the site's RSS feed**, which is why the 11 Aug backfill missed it: the corpus tracked the series index but not its member essays."),

    ("McGuinness — From the Card to the Architecture",
     "Translating the Corporate-Card Model into Mission-Bound Authorization. What the Corporate Card Already Solved walked a working delegated-authority architecture one control at a time and never mentioned a protocol. This part is the joint between that mental model and this chapter's architecture. The five rules the card world taught become the five laws of delegated authority, stated for any substrate. The corporate-card test becomes the claim gate a vendor claim must pass. And the build lists that closed each card post, the things the agent stack cannot borrow from the expense world, turn out to enumerate the draft family: disclosure integrity, field-speed narrowing, checkpoints per boundary, endings that propagate, and a record that earns trust without a bank. What the Corporate Card Already Solved makes one claim across five posts: enterprise finance independently discovered the governance architecture that agent authorization now requires, a.",
     "https://notes.karlmcguinness.com/notes/from-the-card-to-the-architecture/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); chapter of the Mission-Bound Authorization handbook. **Added 26 Aug 2026 — not in the site's RSS feed**, which is why the 11 Aug backfill missed it: the corpus tracked the series index but not its member essays."),

    ("McGuinness — Making Compliance a By-Product",
     "What NIST AI RMF, the EU AI Act, and ISO/IEC 42001 Ask Agents to Prove. The third kind of outside framing is the one with auditors behind it. NIST AI RMF, the EU AI Act, and ISO/IEC 42001 converge on one demand: show me. Show me who is accountable, what the system is for, how you observe it, and how you stop it. In most agent stacks the honest answer is archaeology through session logs. In this architecture the artifact that enforces is the artifact that documents: the Mission is the documented purpose, the approval is the accountable decision, the evidence family is the log, and Termination is the interrupt. The crosswalk maps eight obligations onto machinery that exists for safety reasons, and then names what compliance still requires, because evidence is not certification. This chapter has held the handbook against a threat model, a requirements framework, and a threat taxonomy. The last framing is the one with auditors behind it. A.",
     "https://notes.karlmcguinness.com/notes/making-compliance-a-by-product/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); chapter of the Mission-Bound Authorization handbook. **Added 26 Aug 2026 — not in the site's RSS feed**, which is why the 11 Aug backfill missed it: the corpus tracked the series index but not its member essays."),

    ("McGuinness — Mission-Based Authorization: The Field Reference",
     "The Category, the Litmus Test, the Landscape, and the Running Example. Mission-based authorization governs the approved task, not just the credential, session, or request. This page is the field reference: the definition and litmus test for what counts as mission-based, a competitive landscape, the adoption stages, threats and non-goals, the canonical diagram and glossary, and the Q3 board-packet example threaded through the handbook. Mission-based authorization governs the approved task , not just the credential, session, or individual request.",
     "https://notes.karlmcguinness.com/notes/mission-based-authorization-field-reference/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); chapter of the Mission-Bound Authorization handbook. **Added 26 Aug 2026 — not in the site's RSS feed**, which is why the 11 Aug backfill missed it: the corpus tracked the series index but not its member essays. Reference apparatus rather than argument; the condensed lookup for the whole model."),

    ("McGuinness — The Mission-Based Authorization Vendor Test",
     "Six Questions for Anyone Claiming Agent Authorization. When a vendor says they support agent authorization, ask six questions: what is the approved task object, what derives authority from it, what keeps authority strictly narrower as work fans out, what checks each action at the moment of use, what happens when it is revoked, and can an auditor pull one identifier and see the whole task. The test is intentionally unforgiving: no approved task object means no category claim, token validation is not runtime enforcement, token expiry is not revocation, and logs are not task evidence. A vendor that passes can write the honest deployment claim with level, enforcement scope, freshness, evidence, and exclusions. Agent auth today can prove who is acting and what credential they hold. It cannot prove the work is still authorized. So when a vendor says they support agent authorization, the evaluation is six questions. Each probes one propert.",
     "https://notes.karlmcguinness.com/notes/mission-based-authorization-vendor-test/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); chapter of the Mission-Bound Authorization handbook. **Added 26 Aug 2026 — not in the site's RSS feed**, which is why the 11 Aug backfill missed it: the corpus tracked the series index but not its member essays. Reference apparatus — an evaluation checklist rather than a design argument."),

    ("McGuinness — Mission-Bound Authority: Instances, Actors, and Delegation",
     "From Authenticated Agent Identity to Bounded, Narrowing Authority. The AI agent auth best practices give an agent workload identity, credentials, and delegated user authority. This part binds Mission authority to that identity. The mission claim projects the approved task into every derived token, attested instance identifiers and actor chains keep every actor attributable, and delegated work gets explicit, narrower, separately revocable authority. A sub-agent that acts because it descends from a parent session is inheriting ambient authority, not delegated authority. Child Missions give durable sub-agents their own revocable handles with strict-subset authority and cascade revocation. Offline attenuation, the experimental roadmap for fan-out at scale, keeps the Authorization Server off the hot path with the runtime state check as the surviving kill switch. The Mission Is the Missing Abstraction defined the Mission and From a Requ.",
     "https://notes.karlmcguinness.com/notes/mission-bound-authority/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); chapter of the Mission-Bound Authorization handbook. **Added 26 Aug 2026 — not in the site's RSS feed**, which is why the 11 Aug backfill missed it: the corpus tracked the series index but not its member essays."),

    ("McGuinness — Mission-Bound Authorization: The Glossary",
     "The Handbook's Vocabulary, A to Z. The handbook's vocabulary in one lookup table, A to Z: the objects, the artifacts, the mechanisms, the roles, and the named constructs, each defined in one to three sentences with a link to its canonical home. The entries are written to be quoted. The canonical homes carry the argument. Delegated work forces four separate continuity questions: request provenance, identity attribution, target-applicable authority, and ….",
     "https://notes.karlmcguinness.com/notes/mission-bound-authorization-glossary/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); chapter of the Mission-Bound Authorization handbook. **Added 26 Aug 2026 — not in the site's RSS feed**, which is why the 11 Aug backfill missed it: the corpus tracked the series index but not its member essays. Reference apparatus rather than argument — but the controlled vocabulary is the useful part: it is the closest thing the Mission-Bound programme has to a normative terminology section."),

    ("McGuinness — Mission-Bound Authorization: The Standards Map",
     "OAuth, WIMSE, and OpenID, Mapped to the Architecture. The Mission is the architecture's new primitive. The rest should compose. This appendix tests that claim against the ratified OAuth substrate, the complete active OAuth and WIMSE working-group queues, selected individual drafts, and the relevant OpenID Foundation specifications. It separates publication status from architectural relationship and states the important deltas and substitution hazards plainly. Statuses follow the public record as of July 15, 2026 . The Reference tracks the family’s own reconciliation date separately. The map is exhaustive for the active OAuth and WIMSE working-group queues on that date. It is intentionally selective for ratified RFCs, individual Internet-Drafts, and OpenID specifications: those sections include documents with a concrete architectural join, a material overlap, or a common substitution hazard. This is a design map, not a registry dump.",
     "https://notes.karlmcguinness.com/notes/mission-bound-authorization-standards-map/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); chapter of the Mission-Bound Authorization handbook. **Added 26 Aug 2026 — not in the site's RSS feed**, which is why the 11 Aug backfill missed it: the corpus tracked the series index but not its member essays. Reference apparatus, and the most directly useful chapter for this corpus: it maps the Mission-Bound programme onto the external specs it composes, so it doubles as an index into the OAuth/OIDF/RATS/WIMSE rows tracked here."),

    ("McGuinness — Mission Lifecycle and Change",
     "Observe, Revoke, Grow, Complete. The issuance profile gives a Mission three states and gates derivation on active. This part adds the surfaces that make state actionable over time: Status for canonical pull freshness with Signals as its push complement, Expansion for governed growth, and Completion for monotonic narrowing. One rule threads through all four. Only active permits reliance, so every state a newer profile adds fails safe for a consumer that predates it. The Mission Is the Missing Abstraction defined the Mission as a durable governance object and gave it a deliberately small lifecycle: active , revoked , expired , with the rule that only active permits new derivation. That issuance profile is complete on its own. But it observes Mission state only through one channel: the lifetime of the tokens it already issued, plus optional token introspection. A consumer that holds a Mission-bound t.",
     "https://notes.karlmcguinness.com/notes/mission-lifecycle-and-change/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); chapter of the Mission-Bound Authorization handbook. **Added 26 Aug 2026 — not in the site's RSS feed**, which is why the 11 Aug backfill missed it: the corpus tracked the series index but not its member essays."),

    ("McGuinness — Splitting the Lethal Trifecta",
     "How Mission-Bound Authorization Contains the Defining Agent Threat Model. Simon Willison named the combination that makes agents dangerous: access to private data, exposure to untrusted content, and the ability to communicate externally, held together in one loop. Any two legs are safe. All three are an exfiltration machine waiting for a poisoned document. This part runs the handbook against that threat model: the three legs become separately typed action classes under one Mission, the external leg becomes a consequential action that needs a fresh parameter-bound permit, mediated custody keeps the egress credential out of the agent's hands, and the harness downgrades egress once untrusted content enters the session. Then the honest residuals: enforcement scope, composition, and the semantic gap. In June 2025, Simon Willison named the pattern that the disclosures keep confirming: an agent that combines access to private data, exposure to untrusted.",
     "https://notes.karlmcguinness.com/notes/splitting-the-lethal-trifecta/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); chapter of the Mission-Bound Authorization handbook. **Added 26 Aug 2026 — not in the site's RSS feed**, which is why the 11 Aug backfill missed it: the corpus tracked the series index but not its member essays."),

    ("McGuinness — The Agent Runtime and Audit",
     "Sessions Are Not Authority, Safe Unwinding, and Tamper-Evident Evidence. The first five layers make the Mission approvable, enforceable, governable, and delegable. This operational close makes them hold up against a real agent: a harness that treats session continuity as recoverable state and not as authority, an orchestrator that unwinds work already in flight when a Mission stops, and a transparency profile that makes the suite's evidence independently verifiable across trust domains. It closes with a synthesis of the six operational layers and the Mission Assurance Levels, the practice-side view of the adoption path the architecture chapter stages. The layers before this one build the Mission as a governance object. It is approved with integrity ( From a Request to an Approved Mission ), bound to instances and delegated under a strict subset ( Mission-Bound Authority ), enforced per action ( Mission-Bound Runtime Enforcement ), and observ.",
     "https://notes.karlmcguinness.com/notes/the-agent-runtime-and-audit/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); chapter of the Mission-Bound Authorization handbook. **Added 26 Aug 2026 — not in the site's RSS feed**, which is why the 11 Aug backfill missed it: the corpus tracked the series index but not its member essays."),

    ("McGuinness — The Authority Control Plane",
     "Where the Layer Sits in the Estate. Issuance gating and runtime enforcement are two independent chokepoints, strictly stronger together: a gap in PEP coverage is still bounded at the token layer, and an outstanding token is still stopped at the action layer. The Mission Authority Server, the issuance grant, the Mandate, and Cross-Domain Projection extend the pattern space. And the structural reading that platform engineers reach for unprompted: the layer is the control plane for delegated authority, mapped concept by concept from desired state to the fleet API, with the disciplines that keep the framing honest. Reading path. ~6 minutes start to finish, or jump to the mapping table for the control-plane reading at a glance.",
     "https://notes.karlmcguinness.com/notes/the-authority-control-plane/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); chapter of the Mission-Bound Authorization handbook. **Added 26 Aug 2026 — not in the site's RSS feed**, which is why the 11 Aug backfill missed it: the corpus tracked the series index but not its member essays."),

    ("McGuinness — The Contractor Gets Their Own Card",
     "Why Delegated Authority Must Narrow, and Never Be Borrowed. Crunch week. The contractor needs materials, and the project manager hands over her own card, just this once. Everything about it is convenient and everything about it is wrong, and every finance team knows exactly why. This part walks delegation the way a mature card program runs it: the contractor's own card with a lower limit, attribution that survives the handoff, cards that die when the project closes, and caps on how many cards a project may issue, not just how big each one is. Then the three places the analogy breaks for AI agents, where the fixes have to be built. Everything about it is convenient. No forms, no waiting, the work keeps moving. And everything about it is wrong, in ways every finance team can recite from memory. The statement will say she bought whatever he buys. Her limit, tuned to her role, is now backing his judgment. If the card number lea.",
     "https://notes.karlmcguinness.com/notes/the-contractor-gets-their-own-card/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); chapter of the Mission-Bound Authorization handbook. **Added 26 Aug 2026 — not in the site's RSS feed**, which is why the 11 Aug backfill missed it: the corpus tracked the series index but not its member essays."),

    ("McGuinness — The Convergence and the Wagers",
     "The Outside Evidence, the Named Bets, and the Handbook's Close. The handbook closes on judgment. First the strongest outside evidence: AAuth, the proposed clean-slate agent protocol, adopted a first-class mission layer in its 01 revision after this model's AAuth mapping circulated: not independent replication, adoption by a designer free to say no, which is its own kind of proof. Then the honest bets: admission grain, issuer home, the price of Termination, the necessity of the object itself, the portability of its authority, and the classification line, each stated with the evidence that would falsify it. The laws and the claim gate are the invariants. The bets are the wagers, and deployment experience, not this handbook, will settle them. The sharpest evidence for the fundamental-versus-accidental split arrived from outside this family. AAuth is Dick Hardt’s proposed agent-native authorization protocol, an active individual draft (.",
     "https://notes.karlmcguinness.com/notes/the-convergence-and-the-wagers/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); chapter of the Mission-Bound Authorization handbook. **Added 26 Aug 2026 — not in the site's RSS feed**, which is why the 11 Aug backfill missed it: the corpus tracked the series index but not its member essays."),

    ("McGuinness — The Network Approves Every Transaction, Not the Card",
     "Per-Action Authorization, and the Escape Hatch Called Cash. A decline at the register is mild embarrassment and a tap of a different card, because the system is working: the network approves transactions, not cards. This part walks per-action authorization the way payments runs it: the plastic that proves almost nothing, the authorization that binds this amount at this merchant now, the hotel hold that expires, the freeze that declines the next swipe wherever the issuer decision is checked, and the ATM, the escape hatch every honest card program names in writing. Then the breaks: agents have no common payment-style network, their false-approval costs are unbounded, and their cardholder can be hypnotized mid-purchase. That boring little moment is the most important design fact in payments. The decline is not a failure of the system. It is the system, doing the one thing it exists to do: deciding this transaction, right now,.",
     "https://notes.karlmcguinness.com/notes/the-network-approves-every-transaction/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); chapter of the Mission-Bound Authorization handbook. **Added 26 Aug 2026 — not in the site's RSS feed**, which is why the 11 Aug backfill missed it: the corpus tracked the series index but not its member essays."),

    ("McGuinness — What Survives Without OAuth",
     "The Substrate-Neutral Model and Its Verb Spine. OAuth is the flagship binding because it is deployment reality, but the model does not depend on it. This part states the framework the profiles realize: four functions (compilation, projection, containment, continuity), a verb spine of ten verbs from propose to analyze, and the fundamental-versus-accidental test. Which ideas survive if OAuth disappears? Nearly all of them: the layer, the laws, the vocabulary, the approved task with an integrity-anchored record, approval evidence, runtime containment. What is accidental is the realization: PAR, RAR, the claim names, the wire shapes. The Mission is the durable, approval-backed record of the task ( The Mission Is the Missing Abstraction ), and the chapters before this one made the argument at every altitude: the intuition, the architecture, the wire, the outside framings. This concluding chapter zooms out to the framework tho.",
     "https://notes.karlmcguinness.com/notes/what-survives-without-oauth/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); chapter of the Mission-Bound Authorization handbook. **Added 26 Aug 2026 — not in the site's RSS feed**, which is why the 11 Aug backfill missed it: the corpus tracked the series index but not its member essays."),

    ("McGuinness — You Approve What You Were Shown",
     "What Spend Approval Knows About Approving an Agent's Task. A manager approves a conference request on their phone between meetings. Months later, the only defensible answer to 'what did you approve?' is the request as rendered on that screen. This part walks the anatomy of a real approval: requests that are proposals and nothing more, reviewers who narrow instead of denying, decisions that take days without losing their place, and the disclosure that binds. Payments turned that last idea into regulation. Then the honest part: three places the analogy breaks for AI agents, and what each break demands. The only defensible answer is not “a trip, roughly.” It is the request as it was rendered on that screen, at that moment: the destination, the dates, the $3,400 estimate, the cost center, the attached quote. If the approval means anything at all, it means that . Not what the requester intended. Not what the system stored somew.",
     "https://notes.karlmcguinness.com/notes/you-approve-what-you-were-shown/",
     "Industry blog (Independent)",
     "Published 22 Jul 2026 on Control Plane (notes.karlmcguinness.com); chapter of the Mission-Bound Authorization handbook. **Added 26 Aug 2026 — not in the site's RSS feed**, which is why the 11 Aug backfill missed it: the corpus tracked the series index but not its member essays."),

    ("McGuinness — Least-Privilege MCP Tool Calls",
     "An agent preparing a board packet reads financials, drafts a document, and notifies a reviewer group: three MCP tool calls across three authorization domains, all behind one sentence of human intent.",
     "https://notes.karlmcguinness.com/series/least-privilege-mcp/",
     "Industry blog (Independent)",
     "Published on Control Plane (notes.karlmcguinness.com); series index. Added 26 Aug 2026: the 11 Aug backfill took series indexes from the RSS feed, but this one is linked only from the handbook and was not in the feed."),

    ("McGuinness — Mission-Bound OAuth",
     "Superseded by the Mission-Bound Authorization draft family, kept as history. A four-part series on Mission-Bound OAuth: the core architecture, the OAuth authentication-layer companion profile, the AAuth mapping, and a final critique of whether OAuth is the right home for the Mission model at all.",
     "https://notes.karlmcguinness.com/series/mission-bound-oauth/",
     "Industry blog (Independent)",
     "Published on Control Plane (notes.karlmcguinness.com); series index. Added 26 Aug 2026: the 11 Aug backfill took series indexes from the RSS feed, but this one is linked only from the handbook and was not in the feed."),

    ("McGuinness — Mission Shaping",
     "Many current agent deployments skip the step that turns approved intent into bounded authority. This two-part series covers the Mission shaping problem and why even a well-shaped Mission is not enough once an agent is running in the world.",
     "https://notes.karlmcguinness.com/series/mission-shaping/",
     "Industry blog (Independent)",
     "Published on Control Plane (notes.karlmcguinness.com); series index. Added 26 Aug 2026: the 11 Aug backfill took series indexes from the RSS feed, but this one is linked only from the handbook and was not in the feed."),

    ("McGuinness — Open-World OAuth",
     "OAuth was built for closed worlds, and that constraint is why it became mature. Agents expose the limits of that deployment model. This post traces what the newer OAuth standards get right and which substrate gaps still need to close. Open-world OAuth can improve discovery, resource binding, and first-contact trust. That still leaves the harder agent problem: how approved intent becomes bounded authority that stays governed across delegation chains, unfamiliar tools, consent expansion, revocation, and task termination.",
     "https://notes.karlmcguinness.com/series/open-world-oauth/",
     "Industry blog (Independent)",
     "Published on Control Plane (notes.karlmcguinness.com); series index. Added 26 Aug 2026: the 11 Aug backfill took series indexes from the RSS feed, but this one is linked only from the handbook and was not in the feed."),

    ("McGuinness — You Don't Give Agents Credentials. You Grant Them Power of Attorney.",
     "Enterprise IAM governs who an agent is and what it may do at each boundary. No widely adopted control governs whether its mission should still be running. This series builds the case for the authority-governance layer that closes that gap.",
     "https://notes.karlmcguinness.com/series/you-dont-give-agents-credentials-you-grant-them-power-of-attorney/",
     "Industry blog (Independent)",
     "Published on Control Plane (notes.karlmcguinness.com); series index. Added 26 Aug 2026: the 11 Aug backfill took series indexes from the RSS feed, but this one is linked only from the handbook and was not in the feed."),
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
    ("Published RFCs", "Settled IETF standards-track and BCP RFCs — the foundation everything else builds on, plus OAuth WG output tracked for completeness.",
     len(rfc_rows), "Stable. Mostly the primitives, not where the debate is. RFC 10017 (browser-based apps, published 21 Aug 2026) is the exception — OAuth WG output that is peripheral to delegation."),
    ("Active IETF Drafts", "IETF WG charters, requirements drafts, and active WG/individual drafts — including the OAuth WG recharter formally adding 'Complex Delegation' for agents, and the 34-draft McGuinness Mission-Bound Authorization family (33 of them GitHub-only pre-publication).",
     len(draft_rows), "★ THIS IS WHERE THE CURRENT WORK IS HAPPENING ★  The 4 Jun 2026 recharter is APPROVED (charter-ietf-oauth rev 06), making Complex Delegation chartered work — though no milestone has been attached to it yet. The 26 Aug 2026 sweep added 39 more drafts, including the first new WG-level entry (draft-ietf-oauth-rar-metadata-remediation), the six-draft Morrison ~handle identity family, and the NHE / VERA / AgentEnvelope autonomy-gating cluster."),
    ("Mission-Bound (Pre-pub)", "The 33 GitHub-only drafts of the McGuinness Mission-Bound Authorization family — a single-repo decomposition with a machine-readable family-manifest.json, carrying group / maturity / adoption-rung per draft.",
     len(mission_rows), "Pre-publication, not IETF documents. Only draft-mcguinness-oauth-mission has been filed on Datatracker and it stays in the Active IETF Drafts tab. Split out of that tab 26 Aug 2026 so 'Active IETF Drafts' means what it says."),
    ("OpenID Foundation", "Final and draft OIDF specs and the Oct 2025 Agentic AI whitepaper: AuthZEN (incl. the new ARAP profile), Shared Signals/CAEP, FAPI 2.0, HEART.",
     len(oidf_rows), "Mostly Final. AuthZEN Access Request & Approval Profile (ARAP) was adopted as a WG draft May 2026, Draft 1 published 3 Jun 2026."),
    ("Other Standards & Govt", "Kantara UMA 2.0, W3C VCs, NIST AI initiative, EU AI Act compliance dates.",
     len(other_rows), "VC v2.1 First Public Working Draft is the active piece."),
    ("Academic Papers", "arXiv preprints and IEEE conference papers on delegated authz and workload identity.",
     len(academic_rows), "Mostly settled; the 2025 South et al. paper is the most-cited foundation."),
    ("Industry & Implementations", "Vendor blogs, LinkedIn-style articles, reference implementations (OVID/OVID-ME, ZeroID, WorkOS auth.md, Agent Trust Protocol), and the McGuinness Mission-Bound Authorization blog corpus.",
     len(industry_rows), "Practitioner content; the five implementations at the top of the tab show what an implementable agent-delegation stack looks like today. The Aug 2026 sweeps backfilled the Control Plane blog to 50 entries — the Agent Control Points series (Aug 2026) and the Mission-Bound Authorization handbook (Jul 2026) are the two most substantial arcs. The 26 Aug sweep repointed three posts the site had re-slugged ('Mission-Bound OAuth' was renamed to 'Mission-Bound Authorization' throughout) and added the handbook single-page edition; the handbook's 27 individual chapters are not in the RSS feed and remain untracked."),
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
print(f"Tab counts: RFCs={len(rfc_rows)}, Drafts={len(draft_rows)}, Mission={len(mission_rows)}, OIDF={len(oidf_rows)}, Other={len(other_rows)}, Academic={len(academic_rows)}, Industry={len(industry_rows)}")
print(f"Total: {len(rfc_rows)+len(draft_rows)+len(mission_rows)+len(oidf_rows)+len(other_rows)+len(academic_rows)+len(industry_rows)}")

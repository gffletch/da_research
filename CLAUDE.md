# Delegated Authorization for AI Agents — Research Corpus

A bibliography + knowledge graph tracking the IETF / OIDF / academic / industry
work on how authority delegates from humans to AI agents. Maintained as a living
research artifact; updated additively as new drafts and blog posts appear.

Maintainer is an IAM/delegated-authz expert. Date context: knowledge cutoff
Jan 2026, current entries dated through Jun 2026.

## Files

**Canonical (the source of truth — update these):**

- `delegated_authorization_research.xlsx` — the bibliography. **101 sources**
  across 7 tabs (Index + 6 content tabs).
- `agent_authz_graph.json` — RAG-ready knowledge graph: 74 nodes, 116 edges.
  Self-describing (node_types, edge_types, categories, RAG guidance embedded).
  **Last synced at the 92-source mark; lags the workbook — see Pending below.**
- `agent_authz_graph.html` — interactive D3 force-directed viz of the JSON,
  D3 inlined for offline use (~391KB).

**Build scripts:**

- `build.py` — the workbook builder. Was named `build_v10.py` in the chat
  session that produced this bundle; renamed to drop the version suffix since
  git history now provides the audit trail. Monolithic (all data inline). Run
  `python build.py` after editing to regenerate the workbook.
- `build_graph.py` — the graph JSON builder. Stale relative to the workbook.

**Helper:**

- `validate.py` — quick sanity check. Run after every edit. Loads workbook,
  prints tab counts, confirms Index total equals row sum, lists any unparseable
  rows, sanity-checks every URL is well-formed.

**Explicitly out of scope for ongoing maintenance** (these are snapshots that
will not be updated as the corpus grows — do not regenerate unless asked):

- `IETF_individual_drafts_infographic.html` — editorial broadsheet (32 drafts)
- `drafting_authority_deck.pptx` — 11-slide presentation

Both still exist from the original session if needed.

## Tab structure

| Tab                        | Count | Notes                                                  |
| -------------------------- | ----- | ------------------------------------------------------ |
| Index                      | cover | Auto-summed; cell `C11` = TOTAL                        |
| Published RFCs             | 4     | Stable. Foundation primitives.                         |
| Active IETF Drafts         | 49    | **★ Where the action is.** WG + individual drafts.     |
| OpenID Foundation          | 11    | Final + draft OIDF specs.                              |
| Other Standards & Govt     | 6     | Kantara, W3C, NIST, EU AI Act.                         |
| Academic Papers            | 5     | arXiv + IEEE.                                          |
| Industry & Implementations | 26    | Vendor blogs + reference implementations.              |

Row schema:

- In `build.py`, each row is a 5-tuple: `(title, summary, url, standards_org, comments)`.
- In the rendered workbook, the builder prepends a `#` column (auto-numbered),
  so the actual layout is 6 columns: `# | Title | Summary | Link | Standards Org | Comments`.
- Headers live at row 1. Data starts at row 2.

## The five thematic clusters (within Active IETF Drafts)

The Active IETF Drafts tab informally groups individual-submission drafts
into five thematic clusters used by the original infographic and the graph.
Still useful as a mental model when placing new drafts:

1. **Delegation mechanics** (7) — actor profiles, chain mechanics, RAR-for-agents
2. **Agent identity** (7) — identity frameworks, instance assertion, three-way
   "AIP" name collision (singla, prakash, aip-protocol)
3. **Discovery & transport** (5) — well-known/.dawn discovery, mcp:// URI,
   agent transport protocols
4. **Audit & compliance** (3) — kuehlewind-audit-architecture is the HUB
   that composes 10+ other specs
5. **Adjacent / cross-cutting** (10) — hardt-aauth (OUTLIER, zero OAuth deps),
   framework documents, vertical-specific applicability statements

## Author voices to track

- **Karl McGuinness** (Independent, former Okta SVP & Chief Product Architect).
  Most concentrated single-author body of work in the corpus — currently:
  - **6 individual I-Ds** on Active IETF Drafts tab (rows 16, 18–22):
    actor-profile, client-instance-assertion, resource-token-resp, rfc9728bis,
    token-xchg-target-svc-disco, actor-receipts (the last is GitHub-only,
    marked "Pre-publication" in standards-org column)
  - **1 OIDF profile** in OpenID Foundation tab: AuthZEN Access Request &
    Approval Profile (ARAP) — adopted as WG draft May 2026, Draft 1 published
    3 Jun 2026
  - **4 blog posts** in Industry & Implementations tab (rows 7–10): the
    "Mission-Bound OAuth" series (May–Jun 2026), in publication order
  - Co-author on `draft-ietf-oauth-identity-assertion-authz-grant` (ID-JAG)
  - **Pending I-Ds** referenced in his blogs but NOT yet on Datatracker —
    see Pending Watch List below

- **Kühlewind / Birkholz** (Ericsson / Fraunhofer SIT). `draft-kuehlewind-audit-architecture`
  is the integrator HUB — composes 10+ other specs into a single auditable
  architecture. When a new draft arrives, ask whether it belongs in that
  draft's composition graph.

- **Dick Hardt**. `draft-hardt-aauth-protocol` is the principled OUTLIER —
  zero OAuth dependencies; argues PoP-by-default, resource-signed challenges,
  and AS-to-AS federation are architectural changes, not extensions. Flag
  any new draft that echoes those design choices.

- **Larry Lewis**. `agent-trust-protocol/atp-core` (Industry tab, row 5).
  Acronym near-collision with `draft-sharif-attp` — different designs:
  discrete L0–L4 trust levels there, continuous 0.0–1.0 trust scoring here.

## How to add a new source

Standard workflow (Claude Code + git):

1. **Edit `build.py` in place.** Locate the right tab section (search for
   `# TAB N:`). Find the right placement within the tab — see Placement Rules
   below. Add the row as a 5-tuple.
2. **Update Index tab description** for the affected tab if the addition
   changes the cluster narrative.
3. **Run the build:** `python build.py`
4. **Validate:** `python validate.py`
5. **Commit:** the git history is now the version trail; no need for `build_v{N+1}.py`.
6. **Decide on graph sync.** Graph rebuild is deliberate, not automatic. If
   the addition is structurally significant (new dependency edge, new cluster
   member, new external composition), update `build_graph.py` and rerun.
   Otherwise leave the graph stale and batch the sync.

## Placement rules within tabs

- **Active IETF Drafts:** loose grouping by author cluster, then by submission
  date. McGuinness cluster occupies rows 16, 18–22 (one slot at row 17 is
  `draft-mw-oauth-actor-chain`, kept there because it's directly responding
  to McGuinness's Actor Profile). New McGuinness drafts go at the end of his
  cluster unless there's an obvious thematic reason to split them.
- **Industry & Implementations:** 5 reference implementations lead (rows 1–5),
  then the McGuinness Mission-Bound blog series (rows 7–10, publication order:
  MVP first as the substrate post), then blogs and analyst articles.
- **OpenID Foundation:** AuthZEN cluster groups together (AuthZEN 1.0 →
  MCP Profile → ARAP), then CAEP/SSF, then FAPI, then HEART.

## Narration style (the `comments` column)

- State the maturity signal — revision number, date, WG adoption status.
- Note structural relationships to other drafts already in the corpus.
- Flag observations that matter — re-slugs, name collisions, supersession.
- Be honest about caveats — early-stage, GitHub-only, leaked credentials,
  unusual authorship signals.
- Don't editorialize the technical content — that's what the `summary`
  column is for.

## Tagging conventions (used in graph + derivatives)

- **HUB** — composes 5+ other drafts. Currently: `kuehlewind-audit-architecture`.
- **OUTLIER** — deliberately depends on nothing else in the corpus.
  Currently: `hardt-aauth-protocol`.
- **COLLISION** — name conflict with another draft. Currently: the three "AIP"
  drafts (singla, prakash, aip-agent-identity-protocol).
- **SUPERSEDED** — replaced by a re-slug. Currently: `sharif-payment-trust`
  (replaced by `sharif-attp`).

## Pending watch list

**McGuinness drafts referenced in his blogs but NOT yet on Datatracker**
(check periodically; add when filed):

- `draft-mcguinness-oauth-deferred-code-processing`
- `draft-mcguinness-oauth-identity-assertion-trust-framework`
- `draft-mcguinness-oauth-domain-authorized-issuer-discovery`
- `draft-mcguinness-oauth-mission-bound-minimum-profile` (target I-D for MVP post)
- `draft-mcguinness-oauth-mission-bound-runtime-enforcement-profile` (target I-D for IBAC post)

**Graph needs rebuild.** Last synced at the 92-source mark; current workbook
is 101. Specifically missing from the graph:

- AuthZEN ARAP profile (OIDF) — should be a new `external-spec` node with
  `composes` edges back to Actor Profile
- 4 McGuinness Mission-Bound blog posts — these are concepts not drafts, so
  may warrant a new node type (`blog-series` or `concept`)
- 4 additional McGuinness drafts (resource-token-resp, rfc9728bis,
  token-xchg-target-svc-disco, actor-receipts) — new `individual-draft` nodes
  with `composes` edges to the Mission-Bound conceptual node

**Other deferred items:**

- User has deferred adding a "maturity/readiness" column to the Active Drafts
  tab. Revisit if the cluster grows past ~60 entries.
- OAuth WG recharter on 4 June 2026 IESG telechat — once outcome is known,
  add formal "Complex Delegation" item under WG drafts.

## Things NOT to do

- **Don't add placeholder rows** for drafts that don't exist yet. If a draft
  is referenced in a blog but Datatracker returns nothing, note it in the
  Pending Watch List above instead.
- **Don't update the snapshot derivatives** (infographic, deck) unless
  explicitly asked. They were one-time deliverables, not living documents.
- **Don't search for `draft-mcguinness-authzen-access-request` on Datatracker.**
  AuthZEN is an OIDF working group, not IETF; the spec lives at
  `openid.github.io/authzen/...` and is the ARAP entry in the OIDF tab.
- **Don't auto-sync the graph** after every workbook addition. Wait for
  user signal — graph updates are deliberate and batched, not automatic.
- **Don't create `build_v11.py`, `build_v12.py`, etc.** That pattern was an
  artifact of working without git. Edit `build.py` in place and commit.

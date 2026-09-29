"""
Build the IETF AI Agent Authorization knowledge graph.

Outputs:
  - agent_authz_graph.json   (the data, RAG-ready)
  - agent_authz_graph.html   (interactive D3 visualization — JSON is spliced into
                              the existing shell between the <script id="graph-data">
                              markers, leaving the inlined D3 bundle untouched)

Design (rewritten 11 Aug 2026)
------------------------------
Previously this script carried every node inline and was hand-maintained, which
is why it drifted 270+ sources behind the workbook. It is now *derived*:

  1. The workbook is the source of truth for WHICH nodes exist.
  2. A curated overlay, read back from the previous agent_authz_graph.json,
     preserves the hand-written analysis (long_description, short_name,
     category, tags, authors...) for nodes that already had it. Curated prose
     always wins over derived text.
  3. Edges come from three places, kept distinguishable on purpose:
       - curated edges from the previous graph (kept if both ends still resolve)
       - `composes` edges from the Mission-Bound Authorization family manifest
         (exact, machine-readable — embedded below so the build stays offline)
       - `references` edges auto-derived from the bibliography annotations
         (a row's text naming another corpus document)

Re-run after a workbook change: `python build_graph.py`. Adding a source no
longer requires editing this file.
"""
import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

import openpyxl

ROOT = Path(__file__).parent
WORKBOOK = ROOT / "delegated_authorization_research.xlsx"
GRAPH_JSON = ROOT / "agent_authz_graph.json"
GRAPH_HTML = ROOT / "agent_authz_graph.html"

# ============================================================
# SCHEMA
# ============================================================
SCHEMA = {
    "schema_version": "2.0",
    "generated_at": str(date.today()),
    "title": "IETF AI Agent Authorization & Delegation Knowledge Graph",
    "description": (
        "Knowledge graph of the delegated-authorization-for-AI-agents corpus. Each node is a "
        "corpus entry (RFC, working-group draft, individual draft, external spec, academic "
        "paper, blog post, or implementation). Each edge is a typed relationship. Derived "
        "from delegated_authorization_research.xlsx, with a curated overlay preserving "
        "hand-written analysis. Designed to be queryable by a graph database, ingestible by "
        "a RAG system (each node carries a long_description usable as a retrieval chunk), "
        "and renderable as a node-link visualization."
    ),
    "node_types": {
        "rfc": "Published IETF RFC.",
        "wg-draft": "IETF working group draft (active, in-progress).",
        "individual-draft": "IETF individual-submission draft (not WG-adopted).",
        "pre-publication-draft": "Draft that exists only in a public repo, not yet on Datatracker.",
        "external-spec": "Non-IETF specification (W3C, 3GPP, OpenID Foundation, etc.).",
        "external-impl": "Non-IETF implementation, open-source project, or vendor spec.",
        "academic-paper": "Peer-reviewed paper or preprint.",
        "blog-post": "Practitioner blog post, analyst article, or essay.",
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
        "references": (
            "Auto-derived: the corpus annotation for source explicitly names target. "
            "Weaker and noisier than the curated edge types above — filter these out "
            "if you want only hand-verified relationships."
        ),
    },
    "categories": {
        "delegation": "Delegation mechanics — how authority moves down a chain of actors.",
        "identity": "Agent identity — who the agent is and how it proves it.",
        "discovery-transport": "Discovery and transport — plumbing before authentication.",
        "audit": "Audit and compliance — making agent behaviour verifiably auditable.",
        "mission-bound": "The Mission-Bound Authorization family — durable approval-backed authority objects.",
        "payments": "Agentic payment authorization, receipts, and settlement evidence.",
        "commentary": "Practitioner commentary, analysis, and academic treatment.",
        "cross-cutting": "Adjacent or cross-cutting work that doesn't fit the other clusters.",
    },
    "rag_guidance": (
        "For RAG ingestion: treat each node's 'long_description' as a primary retrieval chunk "
        "and supplement it with name, summary, and comments. For graph-aware retrieval, follow "
        "outbound 'depends_on' / 'composes' edges to recover the specification stack the node "
        "builds on; follow inbound to find what builds on it. Prefer curated edge types over "
        "'references', which is auto-derived from bibliography text and is advisory only. "
        "The 'name_collides_with' edges mark the AIP-naming conflict; 'replaces' marks re-slugs."
    ),
    "provenance": {
        "derived_from": "delegated_authorization_research.xlsx",
        "origin_field": ("Every node and edge carries `origin`: curated (hand-written analysis, "
            "authoritative), mission-manifest (exact, from the family manifest), or "
            "workbook/derived (regenerated each build). Only `curated` is inherited across rebuilds."),
        "curated_overlay": (
            "Hand-written long_description / short_name / category / tags for the original "
            "74-node graph are preserved by node id and take precedence over derived text."
        ),
    },
}

# ============================================================
# MISSION-BOUND AUTHORIZATION FAMILY
# Mirrored from family-manifest.json in
# github.com/mcguinness/mission-bound-authorization (re-synced 4 Sep 2026; 46 drafts, new role/spec_maturity/maintenance schema).
# Keys and deps are slugs with the shared 'draft-mcguinness-' prefix stripped.
# Refresh by re-reading that manifest when the family changes.
# ============================================================
MISSION_FAMILY = {
    'aauth-mission-expiry': ('lifecycle', 'experimental', 'companion', ['mission-aauth', 'mission-aauth-management']),
    'mission-aam': ('architecture', 'sketch', 'companion', ['mission-architecture', 'mission-audit', 'mission-authzen', 'mission-harness', 'mission-runtime', 'oauth-mission', 'oauth-mission-approval', 'oauth-mission-approval-revision', 'oauth-mission-containment', 'oauth-mission-continuation', 'oauth-mission-expansion', 'oauth-mission-issuance-grant', 'oauth-mission-management', 'oauth-mission-template']),
    'mission-aauth': ('bindings-substrate', 'experimental', 'adapter-binding', ['aauth-mission-expiry', 'mission-aauth-management', 'mission-substrate', 'oauth-mission-transaction-authorization']),
    'mission-aauth-management': ('lifecycle', 'experimental', 'companion', ['aauth-mission-expiry', 'mission-architecture', 'mission-security-model']),
    'mission-approval-governance': ('approval-time', 'experimental', 'companion', ['mission-audit', 'mission-authority-server', 'mission-metering', 'mission-runtime', 'mission-substrate', 'oauth-mission', 'oauth-mission-approval', 'oauth-mission-approval-revision', 'oauth-mission-consent-evidence', 'oauth-mission-progressive', 'oauth-mission-template']),
    'mission-architecture': ('architecture', 'not_applicable', 'guide', ['aauth-mission-expiry', 'mission-aauth', 'mission-aauth-management', 'mission-audit', 'mission-authority-server', 'mission-authzen', 'mission-capability-binding', 'mission-discovery', 'mission-gnap', 'mission-harness', 'mission-mandate', 'mission-metering', 'mission-orchestration', 'mission-runtime', 'mission-runtime-evidence', 'mission-security-model', 'mission-shaping', 'mission-substrate', 'mission-uma', 'oauth-mission', 'oauth-mission-approval', 'oauth-mission-attenuation', 'oauth-mission-child-delegation', 'oauth-mission-consent-evidence', 'oauth-mission-containment', 'oauth-mission-continuation', 'oauth-mission-cross-domain', 'oauth-mission-discharge', 'oauth-mission-expansion', 'oauth-mission-issuance-grant', 'oauth-mission-management', 'oauth-mission-progressive', 'oauth-mission-resource-access', 'oauth-mission-signals', 'oauth-mission-status', 'oauth-mission-status-list', 'oauth-mission-transaction-authorization', 'oauth-mission-work-products']),
    'mission-audit': ('proof-portability', 'experimental', 'companion', ['mission-aauth', 'mission-approval-governance', 'mission-architecture', 'mission-authority-server', 'mission-discovery', 'mission-harness', 'mission-mandate', 'mission-orchestration', 'mission-runtime', 'mission-runtime-evidence', 'mission-shaping', 'mission-substrate', 'oauth-mission', 'oauth-mission-child-delegation', 'oauth-mission-consent-evidence', 'oauth-mission-containment', 'oauth-mission-expansion', 'oauth-mission-signals', 'oauth-mission-template', 'oauth-mission-work-products']),
    'mission-authority-server': ('bindings-substrate', 'experimental', 'adapter-binding', ['mission-approval-governance', 'mission-architecture', 'mission-audit', 'mission-authzen', 'mission-harness', 'mission-mandate', 'mission-runtime', 'mission-runtime-evidence', 'mission-security-model', 'mission-substrate', 'oauth-mission', 'oauth-mission-approval', 'oauth-mission-attenuation', 'oauth-mission-child-delegation', 'oauth-mission-consent-evidence', 'oauth-mission-expansion', 'oauth-mission-issuance-grant', 'oauth-mission-progressive', 'oauth-mission-signals', 'oauth-mission-status']),
    'mission-authzen': ('runtime-enforcement', 'experimental', 'companion', ['mission-architecture', 'mission-capability-binding', 'mission-harness', 'mission-metering', 'mission-runtime', 'mission-runtime-evidence', 'mission-runtime-oauth', 'mission-substrate', 'oauth-mission', 'oauth-mission-containment', 'oauth-mission-cross-domain', 'oauth-mission-expansion', 'oauth-mission-progressive', 'oauth-mission-resource-access', 'oauth-mission-status']),
    'mission-capability-binding': ('agent-runtime', 'experimental', 'companion', ['mission-authzen', 'mission-runtime', 'mission-runtime-evidence', 'mission-substrate', 'oauth-mission']),
    'mission-control-plane': ('lifecycle', 'experimental', 'companion', ['mission-runtime', 'oauth-mission', 'oauth-mission-signals', 'oauth-mission-status']),
    'mission-discovery': ('lifecycle', 'experimental', 'companion', ['mission-aauth', 'mission-architecture', 'mission-audit', 'mission-authority-server', 'mission-capability-binding', 'mission-harness', 'mission-metering', 'mission-runtime', 'mission-substrate', 'oauth-mission', 'oauth-mission-approval', 'oauth-mission-containment', 'oauth-mission-cross-domain', 'oauth-mission-expansion', 'oauth-mission-progressive', 'oauth-mission-work-products']),
    'mission-evidence-envelope': ('proof-portability', 'sketch', 'companion', ['mission-audit', 'mission-mandate', 'mission-runtime-evidence', 'mission-substrate', 'oauth-mission', 'oauth-mission-consent-evidence']),
    'mission-gnap': ('bindings-substrate', 'sketch', 'adapter-binding', ['mission-aauth', 'mission-architecture', 'mission-audit', 'mission-authority-server', 'mission-authzen', 'mission-harness', 'mission-mandate', 'mission-metering', 'mission-runtime', 'mission-security-model', 'mission-shaping', 'mission-substrate', 'mission-uma', 'oauth-mission', 'oauth-mission-approval', 'oauth-mission-approval-revision', 'oauth-mission-attenuation', 'oauth-mission-child-delegation', 'oauth-mission-consent-evidence', 'oauth-mission-containment', 'oauth-mission-cross-domain', 'oauth-mission-expansion', 'oauth-mission-progressive', 'oauth-mission-signals', 'oauth-mission-status']),
    'mission-harness': ('agent-runtime', 'experimental', 'companion', ['mission-audit', 'mission-authority-server', 'mission-authzen', 'mission-discovery', 'mission-orchestration', 'mission-runtime', 'mission-runtime-evidence', 'mission-security-model', 'mission-substrate', 'oauth-mission', 'oauth-mission-child-delegation', 'oauth-mission-containment', 'oauth-mission-expansion', 'oauth-mission-signals', 'oauth-mission-status']),
    'mission-mandate': ('proof-portability', 'experimental', 'companion', ['mission-aauth', 'mission-approval-governance', 'mission-audit', 'mission-authority-server', 'mission-runtime', 'mission-substrate', 'mission-uma', 'oauth-mission', 'oauth-mission-cross-domain', 'oauth-mission-issuance-grant', 'oauth-mission-signals', 'oauth-mission-status']),
    'mission-metering': ('runtime-enforcement', 'experimental', 'companion', ['mission-architecture', 'mission-authzen', 'mission-orchestration', 'mission-runtime', 'mission-runtime-evidence', 'mission-substrate', 'oauth-mission', 'oauth-mission-child-delegation', 'oauth-mission-consent-evidence', 'oauth-mission-containment']),
    'mission-orchestration': ('agent-runtime', 'experimental', 'companion', ['mission-architecture', 'mission-harness', 'mission-runtime', 'mission-runtime-evidence', 'mission-substrate', 'oauth-mission', 'oauth-mission-expansion', 'oauth-mission-signals', 'oauth-mission-status']),
    'mission-runtime': ('runtime-enforcement', 'experimental', 'companion', ['mission-aauth', 'mission-architecture', 'mission-audit', 'mission-authority-server', 'mission-authzen', 'mission-capability-binding', 'mission-control-plane', 'mission-harness', 'mission-mandate', 'mission-metering', 'mission-orchestration', 'mission-runtime-evidence', 'mission-runtime-oauth', 'mission-security-model', 'mission-shaping', 'mission-substrate', 'oauth-mission', 'oauth-mission-attenuation', 'oauth-mission-consent-evidence', 'oauth-mission-containment', 'oauth-mission-cross-domain', 'oauth-mission-discharge', 'oauth-mission-signals', 'oauth-mission-transaction-authorization']),
    'mission-runtime-evidence': ('runtime-enforcement', 'experimental', 'companion', ['mission-audit', 'mission-authority-server', 'mission-authzen', 'mission-capability-binding', 'mission-harness', 'mission-runtime', 'mission-substrate', 'oauth-mission', 'oauth-mission-containment', 'oauth-mission-continuation', 'oauth-mission-cross-domain', 'oauth-mission-resource-access']),
    'mission-runtime-oauth': ('runtime-enforcement', 'experimental', 'companion', ['mission-authority-server', 'mission-authzen', 'mission-runtime', 'mission-substrate', 'oauth-mission', 'oauth-mission-containment', 'oauth-mission-cross-domain', 'oauth-mission-issuance-grant', 'oauth-mission-resource-access', 'oauth-mission-signals', 'oauth-mission-status', 'oauth-mission-status-list']),
    'mission-security-model': ('security-model', 'not_applicable', 'guide', ['mission-aauth', 'mission-architecture', 'mission-audit', 'mission-authority-server', 'mission-authzen', 'mission-discovery', 'mission-harness', 'mission-mandate', 'mission-metering', 'mission-orchestration', 'mission-runtime', 'mission-shaping', 'mission-substrate', 'oauth-mission', 'oauth-mission-approval', 'oauth-mission-approval-revision', 'oauth-mission-attenuation', 'oauth-mission-child-delegation', 'oauth-mission-consent-evidence', 'oauth-mission-containment', 'oauth-mission-cross-domain', 'oauth-mission-discharge', 'oauth-mission-expansion', 'oauth-mission-issuance-grant', 'oauth-mission-management', 'oauth-mission-progressive', 'oauth-mission-signals', 'oauth-mission-status', 'oauth-mission-transaction-authorization', 'oauth-mission-work-products']),
    'mission-shaping': ('approval-time', 'not_applicable', 'guide', ['mission-aauth', 'mission-architecture', 'mission-authority-server', 'mission-metering', 'mission-runtime', 'mission-substrate', 'oauth-mission', 'oauth-mission-approval', 'oauth-mission-approval-revision', 'oauth-mission-child-delegation', 'oauth-mission-consent-evidence', 'oauth-mission-progressive', 'oauth-mission-template']),
    'mission-substrate': ('bindings-substrate', 'candidate', 'core', ['mission-aauth', 'mission-architecture', 'mission-audit', 'mission-authority-server', 'mission-gnap', 'mission-mandate', 'mission-runtime', 'mission-security-model', 'mission-uma', 'oauth-mission', 'oauth-mission-status']),
    'mission-uma': ('bindings-substrate', 'sketch', 'adapter-binding', ['mission-aauth', 'mission-architecture', 'mission-audit', 'mission-authority-server', 'mission-authzen', 'mission-harness', 'mission-mandate', 'mission-metering', 'mission-runtime', 'mission-security-model', 'mission-shaping', 'mission-substrate', 'oauth-mission', 'oauth-mission-approval', 'oauth-mission-approval-revision', 'oauth-mission-attenuation', 'oauth-mission-child-delegation', 'oauth-mission-consent-evidence', 'oauth-mission-containment', 'oauth-mission-cross-domain', 'oauth-mission-expansion', 'oauth-mission-progressive', 'oauth-mission-signals', 'oauth-mission-status']),
    'oauth-mission': ('bindings-substrate', 'experimental', 'adapter-binding', ['mission-approval-governance', 'mission-architecture', 'mission-audit', 'mission-authority-server', 'mission-authzen', 'mission-metering', 'mission-runtime', 'mission-shaping', 'mission-substrate', 'oauth-mission-approval', 'oauth-mission-child-delegation', 'oauth-mission-consent-evidence', 'oauth-mission-containment', 'oauth-mission-continuation', 'oauth-mission-cross-domain', 'oauth-mission-expansion', 'oauth-mission-management', 'oauth-mission-progressive', 'oauth-mission-resource-access', 'oauth-mission-signals', 'oauth-mission-status', 'oauth-mission-template', 'oauth-mission-work-products']),
    'oauth-mission-approval': ('approval-time', 'experimental', 'companion', ['mission-approval-governance', 'mission-authority-server', 'mission-shaping', 'oauth-mission', 'oauth-mission-approval-revision', 'oauth-mission-consent-evidence', 'oauth-mission-expansion']),
    'oauth-mission-approval-revision': ('approval-time', 'experimental', 'companion', ['mission-approval-governance', 'mission-shaping', 'oauth-mission', 'oauth-mission-approval', 'oauth-mission-consent-evidence', 'oauth-mission-expansion']),
    'oauth-mission-attenuation': ('sub-agents', 'experimental', 'companion', ['mission-harness', 'mission-runtime', 'oauth-mission', 'oauth-mission-child-delegation', 'oauth-mission-containment', 'oauth-mission-cross-domain', 'oauth-mission-cross-org-delegation', 'oauth-mission-issuance-grant']),
    'oauth-mission-child-delegation': ('sub-agents', 'experimental', 'companion', ['mission-architecture', 'mission-authority-server', 'mission-harness', 'mission-metering', 'oauth-mission', 'oauth-mission-approval', 'oauth-mission-attenuation', 'oauth-mission-containment', 'oauth-mission-continuation', 'oauth-mission-discharge', 'oauth-mission-expansion', 'oauth-mission-issuance-grant', 'oauth-mission-signals', 'oauth-mission-status']),
    'oauth-mission-consent-evidence': ('approval-time', 'experimental', 'companion', ['mission-aauth', 'mission-approval-governance', 'mission-audit', 'mission-authority-server', 'mission-runtime', 'mission-security-model', 'mission-shaping', 'oauth-mission', 'oauth-mission-approval', 'oauth-mission-approval-revision', 'oauth-mission-discharge', 'oauth-mission-expansion', 'oauth-mission-template']),
    'oauth-mission-containment': ('lifecycle', 'experimental', 'companion', ['mission-audit', 'mission-authzen', 'mission-discovery', 'mission-harness', 'mission-runtime', 'mission-runtime-evidence', 'mission-substrate', 'oauth-mission', 'oauth-mission-attenuation', 'oauth-mission-child-delegation', 'oauth-mission-consent-evidence', 'oauth-mission-cross-domain', 'oauth-mission-discharge', 'oauth-mission-expansion', 'oauth-mission-management', 'oauth-mission-signals', 'oauth-mission-status', 'oauth-mission-status-list']),
    'oauth-mission-continuation': ('cross-domain-projection', 'experimental', 'companion', ['mission-aauth', 'mission-architecture', 'mission-authzen', 'mission-harness', 'mission-runtime', 'mission-uma', 'oauth-mission', 'oauth-mission-child-delegation', 'oauth-mission-cross-domain', 'oauth-mission-expansion']),
    'oauth-mission-cross-domain': ('cross-domain-projection', 'experimental', 'companion', ['mission-architecture', 'mission-mandate', 'mission-runtime', 'mission-runtime-evidence', 'mission-substrate', 'oauth-mission', 'oauth-mission-containment', 'oauth-mission-continuation', 'oauth-mission-cross-org-delegation', 'oauth-mission-resource-access', 'oauth-mission-signals', 'oauth-mission-status']),
    'oauth-mission-cross-org-delegation': ('cross-domain-projection', 'experimental', 'companion', ['mission-audit', 'mission-runtime', 'mission-runtime-evidence', 'mission-substrate', 'oauth-mission', 'oauth-mission-attenuation', 'oauth-mission-child-delegation', 'oauth-mission-cross-domain', 'oauth-mission-expansion', 'oauth-mission-status']),
    'oauth-mission-discharge': ('lifecycle', 'experimental', 'companion', ['mission-authzen', 'mission-runtime', 'oauth-mission', 'oauth-mission-child-delegation', 'oauth-mission-resource-access', 'oauth-mission-signals', 'oauth-mission-status']),
    'oauth-mission-expansion': ('lifecycle', 'experimental', 'companion', ['mission-authority-server', 'mission-authzen', 'mission-harness', 'mission-runtime', 'oauth-mission', 'oauth-mission-approval', 'oauth-mission-child-delegation', 'oauth-mission-containment', 'oauth-mission-continuation', 'oauth-mission-progressive', 'oauth-mission-signals', 'oauth-mission-status', 'oauth-mission-template']),
    'oauth-mission-issuance-grant': ('bindings-substrate', 'experimental', 'companion', ['mission-architecture', 'mission-authority-server', 'mission-mandate', 'mission-runtime', 'mission-substrate', 'oauth-mission', 'oauth-mission-containment', 'oauth-mission-cross-domain', 'oauth-mission-status']),
    'oauth-mission-management': ('lifecycle', 'experimental', 'companion', ['mission-architecture', 'mission-audit', 'mission-authority-server', 'mission-security-model', 'oauth-mission', 'oauth-mission-child-delegation', 'oauth-mission-expansion', 'oauth-mission-signals', 'oauth-mission-status']),
    'oauth-mission-progressive': ('lifecycle', 'experimental', 'companion', ['mission-aauth', 'mission-approval-governance', 'mission-architecture', 'mission-discovery', 'mission-metering', 'mission-runtime', 'mission-security-model', 'mission-shaping', 'oauth-mission', 'oauth-mission-child-delegation', 'oauth-mission-consent-evidence', 'oauth-mission-discharge', 'oauth-mission-expansion', 'oauth-mission-template']),
    'oauth-mission-resource-access': ('bindings-substrate', 'experimental', 'companion', ['oauth-mission', 'oauth-mission-cross-domain']),
    'oauth-mission-signals': ('lifecycle', 'experimental', 'companion', ['mission-aauth', 'mission-audit', 'mission-authority-server', 'mission-harness', 'oauth-mission', 'oauth-mission-child-delegation', 'oauth-mission-containment', 'oauth-mission-discharge', 'oauth-mission-expansion', 'oauth-mission-management', 'oauth-mission-status']),
    'oauth-mission-status': ('lifecycle', 'experimental', 'companion', ['mission-aauth', 'mission-authority-server', 'mission-authzen', 'mission-mandate', 'mission-runtime', 'oauth-mission', 'oauth-mission-child-delegation', 'oauth-mission-cross-domain', 'oauth-mission-discharge', 'oauth-mission-expansion', 'oauth-mission-management', 'oauth-mission-resource-access', 'oauth-mission-signals', 'oauth-mission-status-list']),
    'oauth-mission-status-list': ('lifecycle', 'experimental', 'companion', ['mission-runtime', 'oauth-mission', 'oauth-mission-status']),
    'oauth-mission-template': ('approval-time', 'experimental', 'companion', ['mission-approval-governance', 'mission-architecture', 'mission-metering', 'mission-runtime', 'mission-shaping', 'oauth-mission', 'oauth-mission-child-delegation', 'oauth-mission-consent-evidence', 'oauth-mission-containment', 'oauth-mission-continuation', 'oauth-mission-expansion', 'oauth-mission-progressive']),
    'oauth-mission-transaction-authorization': ('runtime-enforcement', 'experimental', 'companion', ['mission-aauth', 'mission-approval-governance', 'mission-audit', 'mission-authzen', 'mission-metering', 'mission-runtime', 'mission-runtime-evidence', 'mission-substrate', 'oauth-mission', 'oauth-mission-consent-evidence', 'oauth-mission-containment', 'oauth-mission-continuation', 'oauth-mission-cross-domain', 'oauth-mission-cross-org-delegation', 'oauth-mission-discharge', 'oauth-mission-resource-access', 'oauth-mission-signals', 'oauth-mission-status-list']),
    'oauth-mission-work-products': ('security-model', 'experimental', 'companion', ['mission-architecture', 'mission-audit', 'mission-discovery', 'mission-harness', 'mission-security-model', 'oauth-mission', 'oauth-mission-child-delegation', 'oauth-mission-continuation', 'oauth-mission-cross-domain', 'oauth-mission-resource-access']),
}

TAB_DEFAULT_TYPE = {
    "Published RFCs": "rfc",
    "Active IETF Drafts": "individual-draft",
    "Mission-Bound (Pre-pub)": "pre-publication-draft",
    "OpenID Foundation": "external-spec",
    "Other Standards & Govt": "external-spec",
    "Academic Papers": "academic-paper",
    "Industry & Implementations": "blog-post",
}

CATEGORY_RULES = [
    ("mission-bound", ("mission-bound", "mission_id", "mission authority", "draft-mcguinness-mission", "draft-mcguinness-oauth-mission")),
    ("payments", ("payment", "kyapay", "x402", "settlement", "refund", "spend", "purchase")),
    ("audit", ("audit", "receipt", "provenance", "evidence", "transparency", "accountability", "attestation")),
    ("discovery-transport", ("discovery", "discover", "well-known", "dns", "directory", "registry", "transport", "resolve")),
    ("identity", ("identity", "identifier", "credential", "workload", "spiffe", "wimse", "attest", "agent card")),
    ("delegation", ("delegation", "delegat", "on-behalf-of", "actor", "token exchange", "scope", "authoriz", "consent", "grant")),
]


def slugify(text, maxlen=60):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:maxlen].rstrip("-")


# Tabs whose rows ARE the spec they name. Commentary tabs are excluded: a blog post
# titled "RFC 9396: ... (CIAM Weekly)" is *about* RFC 9396, not RFC 9396 itself, and
# must not claim that node id.
SPEC_TABS = ("Published RFCs", "Active IETF Drafts", "Mission-Bound (Pre-pub)",
             "OpenID Foundation", "Other Standards & Govt")


def node_id_for(title, url, tab):
    """Stable id. Draft/RFC names win so the curated overlay keeps matching."""
    if tab in SPEC_TABS:
        m = re.search(r"(draft-[a-z0-9][a-z0-9-]*?)(?:-\d{2})?(?=\s|—|$|,|\))", title)
        if m:
            return m.group(1)
        m = re.search(r"RFC\s*(\d{4,5})", title, re.I) or re.search(r"rfc(\d{4,5})", url or "", re.I)
        if m:
            return f"rfc-{m.group(1)}"
        m = re.search(r"charter-ietf-([a-z0-9-]+)", title + " " + (url or ""))
        if m:
            return f"charter-{m.group(1)}"
    prefix = {"Academic Papers": "paper", "Industry & Implementations": "src"}.get(tab, "ext")
    return f"{prefix}-{slugify(title)}"


def type_for(node_id, tab, org, title):
    org_l = (org or "").lower()
    if node_id.startswith("rfc-"):
        return "rfc"
    if node_id.startswith("charter-"):
        return "wg-draft"
    if "pre-publication" in org_l:
        return "pre-publication-draft"
    if node_id.startswith("draft-ietf-"):
        return "wg-draft"
    if node_id.startswith("draft-"):
        return "individual-draft"
    if tab == "Academic Papers":
        return "academic-paper"
    if tab == "Industry & Implementations":
        if any(k in org_l for k in ("open-source", "implementation", "vendor spec")):
            return "external-impl"
        return "blog-post"
    return "external-spec"


def category_for(text, tab):
    if tab in ("Academic Papers", "Industry & Implementations"):
        low = text.lower()
        for cat, keys in CATEGORY_RULES[:2]:      # payments / mission still win for commentary
            if any(k in low for k in keys):
                return cat
        return "commentary"
    low = text.lower()
    for cat, keys in CATEGORY_RULES:
        if any(k in low for k in keys):
            return cat
    return "cross-cutting"


def extract_revision(comment):
    m = re.search(r"Revision (-\d+)", comment or "")
    return m.group(1) if m else None


# ============================================================
# 1. NODES — derived from the workbook
# ============================================================
wb = openpyxl.load_workbook(WORKBOOK)
rows = []
for tab in wb.sheetnames:
    if tab == "Index":
        continue
    for r in wb[tab].iter_rows(min_row=2, values_only=True):
        if not r or not r[1]:
            continue
        rows.append({"tab": tab, "title": str(r[1]), "summary": str(r[2] or ""),
                     "url": str(r[3] or ""), "org": str(r[4] or ""), "comment": str(r[5] or "")})

nodes, by_id, collisions = [], {}, 0
for r in rows:
    nid = node_id_for(r["title"], r["url"], r["tab"])
    if nid in by_id:                      # never silently merge two sources
        collisions += 1
        nid = f"{nid}--{slugify(r['title'], 24)}"
    blob = f"{r['title']} {r['summary']} {r['comment']}"
    n = {
        "id": nid,
        "type": type_for(nid, r["tab"], r["org"], r["title"]),
        "name": r["title"],
        "summary": r["summary"],
        "long_description": f"{r['summary']} {r['comment']}".strip(),
        "category": category_for(blob, r["tab"]),
        "tab": r["tab"],
        "standards_org": r["org"],
        "url": r["url"],
    }
    rev = extract_revision(r["comment"])
    if rev:
        n["revision"] = rev
    short = nid.replace("draft-mcguinness-", "").replace("draft-", "")
    if short in MISSION_FAMILY:
        grp, maturity, rung, _ = MISSION_FAMILY[short]
        n["category"] = "mission-bound"
        n["mission_group"] = grp
        n["maturity"] = maturity
        n["adoption_rung"] = rung
    n["origin"] = "workbook"
    nodes.append(n)
    by_id[nid] = n

# ---- curated overlay: hand-written analysis wins over derived text ----
CURATED_FIELDS = ("long_description", "short_name", "category", "tags",
                  "authors", "wg", "status", "year", "date")
# IMPORTANT: this script reads its own previous output, so it must never re-ingest
# its own derived work as if it were hand-curated. Everything is tagged with an
# `origin`; only origin == "curated" is inherited. Objects with no origin at all are
# from the pre-2.0 hand-maintained graph and count as curated (one-time migration).
curated_nodes, curated_edges = {}, []
if GRAPH_JSON.exists():
    prev = json.loads(GRAPH_JSON.read_text(encoding="utf-8"))
    curated_nodes = {n["id"]: n for n in prev.get("nodes", [])
                     if n.get("origin", "curated") == "curated"}
    curated_edges = [e for e in prev.get("edges", [])
                     if e.get("origin", "curated") == "curated"]

overlaid = 0
for nid, node in by_id.items():
    old = curated_nodes.get(nid)
    if not old:
        continue
    overlaid += 1
    for f in CURATED_FIELDS:
        if old.get(f):
            node[f] = old[f]
    node["origin"] = "curated"

# Curated nodes with no workbook row are kept as substrate: the graph legitimately
# contains foundational RFCs (7519, 7521, 7523, 9068, 9334...) and external specs
# that the bibliography references but does not track as its own sources. Dropping
# them would silently discard the curated edges that hang off them.
substrate = 0
for nid, old in curated_nodes.items():
    if nid in by_id:
        continue
    n = dict(old)
    n["in_workbook"] = False
    n.setdefault("category", "cross-cutting")
    n["origin"] = "curated"      # must stay curated so the next rebuild re-inherits it
    nodes.append(n)
    by_id[nid] = n
    substrate += 1

# ============================================================
# 2. EDGES
# ============================================================
edges, seen = [], set()


def add_edge(src, dst, rel, label="", origin="derived"):
    if src == dst or src not in by_id or dst not in by_id:
        return False
    key = (src, dst, rel)
    if key in seen:
        return False
    seen.add(key)
    e = {"source": src, "target": dst, "type": rel, "origin": origin}
    if label:
        e["label"] = label
    edges.append(e)
    return True


# -- 2a. curated edges from the previous graph --
kept_curated, dropped_curated = 0, []
for e in curated_edges:
    if add_edge(e["source"], e["target"], e["type"], e.get("label", ""), origin="curated"):
        kept_curated += 1
    elif e["source"] not in by_id or e["target"] not in by_id:
        dropped_curated.append((e["source"], e["target"], e["type"]))

# -- 2b. Mission-Bound family composition (exact, from the manifest) --
mission_edges = 0
for short, (_grp, _mat, _rung, deps) in MISSION_FAMILY.items():
    src = f"draft-mcguinness-{short}"
    for d in deps:
        if add_edge(src, f"draft-mcguinness-{d}", "composes", "Mission family dependency",
                    origin="mission-manifest"):
            mission_edges += 1

# -- 2c. auto-derived cross-references from the bibliography text --
draft_ids = sorted((i for i in by_id if i.startswith("draft-")), key=len, reverse=True)
rfc_ids = {i for i in by_id if i.startswith("rfc-")}
ref_edges = 0
for r in rows:
    src = node_id_for(r["title"], r["url"], r["tab"])
    if src not in by_id:
        continue
    text = f"{r['summary']} {r['comment']}"
    for did in draft_ids:
        if did != src and did in text:
            if add_edge(src, did, "references", "Named in corpus annotation"):
                ref_edges += 1
    for m in re.finditer(r"RFC\s*(\d{4,5})", text):
        rid = f"rfc-{m.group(1)}"
        if rid in rfc_ids and add_edge(src, rid, "references", "Cites RFC in annotation"):
            ref_edges += 1

# ============================================================
# 3. WRITE
# ============================================================
deg = Counter()
for e in edges:
    deg[e["source"]] += 1
    deg[e["target"]] += 1
for n in nodes:
    n["degree"] = deg.get(n["id"], 0)

graph = {"@meta": SCHEMA, "nodes": nodes, "edges": edges}
GRAPH_JSON.write_text(json.dumps(graph, indent=2, ensure_ascii=False), encoding="utf-8")

# splice into the HTML shell, preserving the inlined D3 bundle
if GRAPH_HTML.exists():
    html = GRAPH_HTML.read_text(encoding="utf-8")
    start_tag = '<script id="graph-data" type="application/json">'
    i = html.index(start_tag) + len(start_tag)
    j = html.index("</script>", i)
    html = html[:i] + "\n" + json.dumps(graph, indent=2, ensure_ascii=False) + "\n" + html[j:]
    GRAPH_HTML.write_text(html, encoding="utf-8")
    html_note = "spliced (D3 bundle untouched)"
else:
    html_note = "SKIPPED — html shell not found"

# ============================================================
# 4. REPORT
# ============================================================
print(f"Nodes: {len(nodes)}   Edges: {len(edges)}")
print(f"  {len(nodes)-substrate} from workbook + {substrate} curated substrate nodes (not bibliography entries)")
print(f"  curated overlay applied to {overlaid} nodes; id collisions disambiguated: {collisions}")
print(f"  edges: {kept_curated} curated kept, {mission_edges} mission-family composes, {ref_edges} auto-derived references")
if dropped_curated:
    print(f"  ! {len(dropped_curated)} curated edges dropped (endpoint no longer in corpus):")
    for s, t, rel in dropped_curated[:10]:
        print(f"      {s} -{rel}-> {t}")
print("\nBy type: ", dict(Counter(n["type"] for n in nodes)))
print("By category:", dict(Counter(n["category"] for n in nodes)))
print(f"\nagent_authz_graph.json written; agent_authz_graph.html {html_note}")

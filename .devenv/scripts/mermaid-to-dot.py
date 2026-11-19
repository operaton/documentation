#!/usr/bin/env python3
"""
Convert schema.mermaid (erDiagram) to schema.dot (Graphviz) for optimized SVG rendering.

Features:
  - subgraph cluster per domain prefix (ACT_GE_, ACT_RE_, ACT_RU_, ACT_HI_, ACT_ID_)
  - dotted cluster borders with domain color
  - splines=ortho for rectangular routing
  - HTML-table entity nodes with PK/FK markers and domain header color
"""

import re
import sys
from pathlib import Path

# ── domain config ──────────────────────────────────────────────────────────────
DOMAINS = {
    "GE": {"label": "General",    "header": "#4a6fa5", "fill": "#dbeeff", "border": "#4a6fa5"},
    "RE": {"label": "Repository", "header": "#2e8b57", "fill": "#dff0e8", "border": "#2e8b57"},
    "RU": {"label": "Runtime",    "header": "#8b6914", "fill": "#fff8e1", "border": "#b8860b"},
    "HI": {"label": "History",    "header": "#8b5e2e", "fill": "#fef2e0", "border": "#cd853f"},
    "ID": {"label": "Identity",   "header": "#6a42a0", "fill": "#f3e8ff", "border": "#7b5ea7"},
}

def domain_of(name: str) -> str | None:
    m = re.match(r"ACT_([A-Z]+)_", name)
    return m.group(1) if m else None


# ── parser ─────────────────────────────────────────────────────────────────────
def parse(text: str):
    entities: dict[str, list[tuple[str, str, str]]] = {}
    rels: list[tuple[str, str, str, str]] = []  # (src, card_left, card_right, dst, label)

    # entity blocks
    for m in re.finditer(r"^\s{4}(\w+)\s*\{([^}]+)\}", text, re.MULTILINE):
        name = m.group(1)
        cols: list[tuple[str, str, str]] = []
        for line in m.group(2).split("\n"):
            line = line.strip()
            if not line or line.startswith("%%"):
                continue
            parts = line.split(None, 2)
            if len(parts) < 2:
                continue
            col_type = parts[0]
            col_name = parts[1].rstrip(";")
            rest = parts[2] if len(parts) > 2 else ""
            marker = "PK" if "PK" in rest else ("FK" if "FK" in rest else "")
            cols.append((col_type, col_name, marker))
        entities[name] = cols

    # relationships  — e.g.  ACT_GE_BYTEARRAY }o--|| ACT_RE_DEPLOYMENT : "DEPLOYMENT_ID_"
    rel_re = re.compile(
        r"^\s{4}(\w+)\s+([|o}{]+)--([|o}{]+)\s+(\w+)\s+:\s+\"([^\"]+)\"",
        re.MULTILINE,
    )
    for m in rel_re.finditer(text):
        rels.append((m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)))

    return entities, rels


# ── Graphviz arrow mapping ─────────────────────────────────────────────────────
# Mermaid notation: `}o` = crow+odot (many, optional), `||` = tee+tee (one, mandatory)
def arrow_attrs(card: str) -> tuple[str, str]:
    """Return (arrowhead_style, style_fragment) for one side of a relationship."""
    if card in ("}|", "|{"):   # one-or-more
        return "crow", "tee"
    if card in ("}o", "o{"):   # zero-or-more
        return "crow", "odot"
    if card == "||":            # exactly one
        return "tee", "tee"
    if card in ("o|", "|o"):   # zero-or-one
        return "tee", "odot"
    return "normal", "normal"


def rel_attrs(card_src: str, card_dst: str) -> str:
    ah_head, _ = arrow_attrs(card_dst)   # arrowhead near dst
    ah_tail, _ = arrow_attrs(card_src)   # arrowtail near src
    return f'arrowhead="{ah_head}" arrowtail="{ah_tail}" dir=both'


# ── node HTML label ───────────────────────────────────────────────────────────
def node_label(name: str, cols: list[tuple[str, str, str]], dom: str) -> str:
    d = DOMAINS.get(dom, {"header": "#999999", "fill": "#f5f5f5"})
    rows = []
    for col_type, col_name, marker in cols:
        if marker == "PK":
            col_fmt = f'<B><U>{col_name}</U></B>'
            type_fmt = f'<FONT POINT-SIZE="9" COLOR="#444444">{col_type}</FONT>'
            badge = '<TD ALIGN="LEFT" BGCOLOR="#e8f0fe"><FONT POINT-SIZE="9" COLOR="#4a6fa5">PK</FONT></TD>'
        elif marker == "FK":
            col_fmt = f'<I>{col_name}</I>'
            type_fmt = f'<FONT POINT-SIZE="9" COLOR="#444444">{col_type}</FONT>'
            badge = '<TD ALIGN="LEFT" BGCOLOR="#fff8e1"><FONT POINT-SIZE="9" COLOR="#b8860b">FK</FONT></TD>'
        else:
            col_fmt = col_name
            type_fmt = f'<FONT POINT-SIZE="9" COLOR="#666666">{col_type}</FONT>'
            badge = '<TD ALIGN="LEFT"></TD>'
        rows.append(
            f'    <TR><TD ALIGN="LEFT" PORT="{col_name}">{col_fmt}</TD>'
            f'<TD ALIGN="LEFT">{type_fmt}</TD>{badge}</TR>'
        )
    rows_str = "\n".join(rows)
    return (
        f'  {name} [label=<\n'
        f'    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="3">\n'
        f'    <TR><TD COLSPAN="3" BGCOLOR="{d["header"]}" ALIGN="CENTER">'
        f'<FONT COLOR="white" POINT-SIZE="11"><B>{name}</B></FONT></TD></TR>\n'
        f'{rows_str}\n'
        f'    </TABLE>\n'
        f'  > shape=none margin=0]'
    )


# ── DOT generator ─────────────────────────────────────────────────────────────
def to_dot(entities: dict, rels: list) -> str:
    by_domain: dict[str, dict] = {}
    for name, cols in entities.items():
        d = domain_of(name)
        if d:
            by_domain.setdefault(d, {})[name] = cols

    out = [
        "digraph ER {",
        '  graph [',
        '    splines=ortho',
        '    rankdir=LR',
        '    nodesep=0.6',
        '    ranksep=3.0',
        '    compound=true',
        '    pad=0.8',
        '    fontname="Helvetica Neue,Helvetica,Arial,sans-serif"',
        '    fontsize=13',
        '  ]',
        '  node [shape=none fontname="Helvetica Neue,Helvetica,Arial,sans-serif" fontsize=10]',
        '  edge [',
        '    fontname="Helvetica Neue,Helvetica,Arial,sans-serif"',
        '    fontsize=9',
        '    color="#888888"',
        '    fontcolor="#555555"',
        '    penwidth=1.2',
        '  ]',
        "",
    ]

    for dom in ["GE", "RE", "RU", "HI", "ID"]:
        tables = by_domain.get(dom, {})
        if not tables:
            continue
        d = DOMAINS[dom]
        out += [
            f"  subgraph cluster_{dom} {{",
            f'    label="{d["label"]} (ACT_{dom}_)"',
            f'    style=dashed',
            f'    color="{d["border"]}"',
            f'    penwidth=2',
            f'    fontcolor="{d["header"]}"',
            f'    fontsize=14',
            f'    bgcolor="{d["fill"]}18"',  # 18 = ~10% alpha approximation in hex
            "",
        ]
        for name in sorted(tables.keys()):
            out.append(node_label(name, tables[name], dom))
        out += ["  }", ""]

    # edges — deduplicate by (src, dst, label)
    seen: set[tuple[str, str, str]] = set()
    out.append("  // Relationships")
    for src, c_src, c_dst, dst, label in rels:
        key = (src, dst, label)
        if key in seen:
            continue
        seen.add(key)
        if src not in entities or dst not in entities:
            continue
        rattrs = rel_attrs(c_src, c_dst)
        # self-referential: use different edge color
        extra = ' color="#cc4444" style=dashed' if src == dst else ""
        out.append(f'  {src} -> {dst} [xlabel="{label}" {rattrs}{extra}]')

    out.append("}")
    return "\n".join(out)


# ── main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <schema.mermaid> <schema.dot>", file=sys.stderr)
        sys.exit(1)

    src = Path(sys.argv[1]).read_text()
    entities, rels = parse(src)
    dot = to_dot(entities, rels)
    Path(sys.argv[2]).write_text(dot)
    print(f"Wrote {len(entities)} entities, {len(rels)} relationships → {sys.argv[2]}")

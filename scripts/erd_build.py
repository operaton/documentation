"""Build per-group mermaid ER sub-diagrams from parsed schema data."""


def extract_header(text):
    lines = text.splitlines()
    init_line = lines[0]
    classdef_lines = [l for l in lines if l.strip().startswith("classDef")]
    return init_line, classdef_lines


def build_subdiagram(tables, entities, rels, classes, init_line, classdef_lines):
    out = [init_line, "erDiagram"]
    out.extend("    " + l.strip() for l in classdef_lines)

    for t in tables:
        out.append(f"    {t} {{{entities[t]}\n    }}")

    for a, rel, b, col in rels:
        if a in tables and b in tables:
            out.append(f'    {a} {rel} {b} : "{col}"')

    for t in tables:
        if t in classes:
            out.append(f"    class {t} {classes[t]}")

    return "\n".join(out) + "\n"

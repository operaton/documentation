"""Parse schema.mermaid into entities, relationships, and class assignments."""
import re

ENTITY_RE = re.compile(r'^\s{4}(ACT_\w+)\s*\{(.*?)\n\s{4}\}', re.MULTILINE | re.DOTALL)
REL_RE = re.compile(
    r'^\s*(ACT_\w+)\s+([}|][o|]--[o|][|{])\s+(ACT_\w+)\s*:\s*"([^"]+)"',
    re.MULTILINE,
)
CLASS_RE = re.compile(r'^\s*class\s+(ACT_\w+)\s+(\w+)', re.MULTILINE)

TABLE_GROUPS = {
    "bpmn": [
        "ACT_GE_PROPERTY", "ACT_GE_BYTEARRAY", "ACT_GE_SCHEMA_LOG",
        "ACT_RE_DEPLOYMENT", "ACT_RE_PROCDEF", "ACT_RE_CAMFORMDEF",
        "ACT_RU_EXECUTION", "ACT_RU_JOB", "ACT_RU_JOBDEF", "ACT_RU_TASK",
        "ACT_RU_IDENTITYLINK", "ACT_RU_VARIABLE", "ACT_RU_EVENT_SUBSCR",
        "ACT_RU_INCIDENT", "ACT_RU_AUTHORIZATION", "ACT_RU_FILTER",
        "ACT_RU_METER_LOG", "ACT_RU_TASK_METER_LOG", "ACT_RU_EXT_TASK",
        "ACT_RU_BATCH",
    ],
    "dmn": ["ACT_RE_DECISION_DEF", "ACT_RE_DECISION_REQ_DEF"],
    "cmmn": ["ACT_RE_CASE_DEF", "ACT_RU_CASE_EXECUTION", "ACT_RU_CASE_SENTRY_PART"],
    "history": None,
    "identity": None,
}


def parse_schema(text):
    entities = {m.group(1): m.group(2) for m in ENTITY_RE.finditer(text)}
    rels = [
        (m.group(1), m.group(2), m.group(3), m.group(4))
        for m in REL_RE.finditer(text)
    ]
    classes = {m.group(1): m.group(2) for m in CLASS_RE.finditer(text)}
    return entities, rels, classes

"""Query intent classifier — zero latency, no API call.

Ported and extended from GBrain's intent.ts.
Adds Vietnamese patterns for AICOS use case.

Intent → context_kinds routing:
  working_state  → current_state, current_direction, handoff
  canonical      → canonical, policy, contract
  status         → status_item, open_items, open_questions
  task           → packet, task_state
  temporal       → handoff, status_item, task_state (full history)
  general        → all kinds (default)
"""
from __future__ import annotations

import re
from typing import Literal

QueryIntent = Literal["working_state", "canonical", "status", "task", "temporal", "general"]

# -----------------------------------------------------------------------
# Pattern lists — Vietnamese first, English second
# -----------------------------------------------------------------------

_WORKING_STATE = [
    # Vietnamese
    r"trạng thái", r"hiện tại", r"đang làm", r"đang xảy ra", r"hướng đi",
    r"định hướng", r"kế hoạch hiện", r"tình hình",
    # English
    r"\bcurrent[\s_-]state\b", r"\bcurrent[\s_-]direction\b",
    r"\bwhat.s happening\b", r"\bwhere are we\b", r"\bstatus\b",
    r"\bproject state\b",
]

_CANONICAL = [
    # Vietnamese
    r"quy tắc", r"quy định", r"chính sách", r"hợp đồng", r"nguyên tắc",
    r"tiêu chuẩn", r"chuẩn mực", r"policy", r"contract",
    # English
    r"\bpolic(y|ies)\b", r"\bcontract\b", r"\brule[s]?\b",
    r"\bcanonical\b", r"\bstandard[s]?\b", r"\bguideline[s]?\b",
]

_STATUS = [
    # Vietnamese
    r"open item", r"câu hỏi mở", r"vấn đề mở", r"nợ kỹ thuật",
    r"tech debt", r"chặn", r"blocked", r"đang bị",
    r"follow.?up", r"follow up", r"cần giải quyết", r"chưa xong",
    # English
    r"\bopen item[s]?\b", r"\bopen question[s]?\b", r"\btech debt\b",
    r"\bblock(er|ed)?\b", r"\bfollow.?up\b", r"\bunresolved\b",
    r"\bpending\b", r"\bstatus item[s]?\b",
]

_TASK = [
    # Vietnamese
    r"task", r"packet", r"nhiệm vụ", r"công việc cụ thể",
    r"đang thực hiện", r"sprint", r"workstream",
    # English
    r"\btask[\s_-]packet\b", r"\bpacket\b", r"\btask[\s_-]state\b",
    r"\bworkstream\b", r"\bassignment\b",
]

_TEMPORAL = [
    # Vietnamese
    r"lịch sử", r"gần đây", r"vừa xong", r"mới nhất", r"handoff",
    r"bàn giao", r"tiếp tục từ", r"lần trước", r"trước đó",
    r"continuity", r"continuation",
    # English
    r"\bhandoff\b", r"\brecent(ly)?\b", r"\blast\s+(session|update|change)\b",
    r"\bhistory\b", r"\btimeline\b", r"\blatest\b", r"\bwhat.s new\b",
]

# -----------------------------------------------------------------------
# Compile all patterns
# -----------------------------------------------------------------------

def _compile(patterns: list[str]):
    return re.compile("|".join(patterns), re.IGNORECASE | re.UNICODE)


_RE_WORKING  = _compile(_WORKING_STATE)
_RE_CANON    = _compile(_CANONICAL)
_RE_STATUS   = _compile(_STATUS)
_RE_TASK     = _compile(_TASK)
_RE_TEMPORAL = _compile(_TEMPORAL)

# -----------------------------------------------------------------------
# Public API
# -----------------------------------------------------------------------

_KIND_MAP: dict[QueryIntent, list[str]] = {
    "working_state": ["current_state", "current_direction", "handoff", "working"],
    "canonical":     ["canonical", "policy", "contract"],
    "status":        ["status_item", "open_items", "open_questions"],
    "task":          ["packet", "task_state", "workstream"],
    "temporal":      ["handoff", "status_item", "task_state", "current_state"],
    "general":       [],  # empty = search all kinds
}


def detect_intent(query: str) -> QueryIntent:
    """Classify query into an intent. Order matters: more specific first."""
    if _RE_TEMPORAL.search(query):  return "temporal"
    if _RE_WORKING.search(query):   return "working_state"
    if _RE_CANON.search(query):     return "canonical"
    if _RE_STATUS.search(query):    return "status"
    if _RE_TASK.search(query):      return "task"
    return "general"


def intent_to_kinds(intent: QueryIntent) -> list[str]:
    """Return suggested context_kind filter for this intent. Empty = no filter."""
    return _KIND_MAP.get(intent, [])


def suggest_kinds(query: str) -> list[str]:
    """One-call shortcut: query → suggested context_kinds list."""
    return intent_to_kinds(detect_intent(query))

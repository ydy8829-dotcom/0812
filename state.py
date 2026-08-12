from typing import Any, Literal
from typing_extensions import TypedDict

class AgentState(TypedDict, total=False):
    user_input: str
    mode: Literal["recommendation", "execution"]
    user_profile: dict[str, Any]
    context: dict[str, Any]
    primary_intent: str
    secondary_intent: str | None
    intent_confidence: float
    goal: str
    constraints: list[str]
    missing_information: list[str]
    information_sufficient: bool
    action_candidates: list[dict[str, Any]]
    prioritized_actions: list[dict[str, Any]]
    next_best_action: dict[str, Any]
    tool_requests: list[dict[str, Any]]
    decision_basis: str
    final_response: str
    error: str | None
    trace: list[dict[str, Any]]

from typing import Any, Literal
from pydantic import BaseModel, Field

IntentName = Literal["information_request", "decision_support", "planning", "problem_solving", "task_execution", "recommendation", "learning", "troubleshooting", "comparison", "scheduling", "brainstorming", "unknown"]

class IntentResult(BaseModel):
    primary_intent: IntentName
    secondary_intent: str | None = None
    confidence: float = Field(ge=0, le=1)
    evidence: str = ""

class ActionItem(BaseModel):
    action: str
    reason: str
    expected_outcome: str
    required_information: list[str] = []
    dependencies: list[str] = []
    impact: int = Field(ge=1, le=5, default=3)
    urgency: int = Field(ge=1, le=5, default=3)
    feasibility: int = Field(ge=1, le=5, default=3)
    goal_alignment: int = Field(ge=1, le=5, default=3)
    effort: int = Field(ge=1, le=5, default=3)
    priority: int = 0

class AgentResponse(BaseModel):
    summary: str
    decision_basis: str
    next_best_action: ActionItem | None = None
    action_plan: list[ActionItem] = []
    missing_information: list[str] = []
    requires_confirmation: bool = False

class ToolRequest(BaseModel):
    tool_name: str
    purpose: str
    arguments: dict[str, Any] = {}
    requires_confirmation: bool = True

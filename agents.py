from datetime import datetime
from schemas import IntentResult, ActionItem
from services.llm import structured_invoke

def trace(s, n):
    s.setdefault("trace", []).append({"node": n, "at": datetime.now().isoformat(timespec="seconds")})

def analyze_input(s):
    s["context"] = {**s.get("context", {}), "captured_at": datetime.now().isoformat(timespec="seconds")}; trace(s, "analyze_input"); return s

def classify_intent(s):
    text = s.get("user_input", "").lower()
    f = IntentResult(primary_intent="unknown", confidence=.42, evidence="More context is needed.")
    if any(x in text for x in ["interview", "prepare", "plan"]): f = IntentResult(primary_intent="planning", confidence=.91, evidence="The user asks for preparation steps.")
    elif any(x in text for x in ["compare", "difference", "choose"]): f = IntentResult(primary_intent="comparison", confidence=.88, evidence="The user asks to compare options.")
    elif any(x in text for x in ["error", "bug", "problem", "broken"]): f = IntentResult(primary_intent="troubleshooting", confidence=.86, evidence="The user asks for a diagnosis.")
    r = structured_invoke("Classify intent for: " + text, IntentResult, f)
    s.update(primary_intent=r.primary_intent, secondary_intent=r.secondary_intent, intent_confidence=r.confidence, decision_basis=r.evidence); trace(s, "classify_intent"); return s

def extract_context(s):
    t = s.get("user_input", "").lower(); s["context"] = {**s.get("context", {}), "domain_hint": "career" if "interview" in t else "general", "time_reference": "near-term" if any(x in t for x in ["next", "soon", "tomorrow"]) else None}; trace(s, "extract_context"); return s

def infer_goal(s):
    t = s.get("user_input", "").lower(); s["goal"] = "Show job fit and experience clearly in the upcoming interview." if "interview" in t else "Choose the best option using explicit decision criteria." if s.get("primary_intent") == "comparison" else "Turn the request into a concrete next step."; trace(s, "infer_goal"); return s

def identify_constraints(s):
    s["constraints"] = ["User confirmation is required before external changes."]; trace(s, "identify_constraints"); return s

def check_sufficiency(s):
    s["missing_information"] = []; s["information_sufficient"] = True; trace(s, "check_sufficiency"); return s

def generate_action_plan(s):
    if "interview" in s.get("user_input", "").lower():
        a = [ActionItem(action="Analyze the company and role JD", reason="Set the preparation scope.", expected_outcome="3-5 core competencies and likely questions.", impact=5, urgency=5, feasibility=5, goal_alignment=5, effort=2), ActionItem(action="Write three STAR experience stories", reason="Connect experience to the role.", expected_outcome="Three concise answer drafts.", impact=5, urgency=4, feasibility=4, goal_alignment=5, effort=3), ActionItem(action="Draft technical question answers", reason="Test technical understanding.", expected_outcome="A focused answer sheet.", impact=4, urgency=4, feasibility=4, goal_alignment=5, effort=3), ActionItem(action="Run a 20-minute mock interview", reason="Find delivery gaps.", expected_outcome="An improvement checklist.", impact=4, urgency=3, feasibility=3, goal_alignment=4, effort=4)]
    else: a = [ActionItem(action="Define the goal and completion condition", reason="Give the next action a clear direction.", expected_outcome="A measurable goal.", impact=5, urgency=4, feasibility=5, goal_alignment=5, effort=1)]
    s["action_candidates"] = [x.model_dump() for x in a]; trace(s, "generate_action_plan"); return s

def prioritize_actions(s):
    a = s.get("action_candidates", [])
    for x in a: x["score"] = round(x.get("impact", 3)*.25+x.get("urgency", 3)*.2+x.get("feasibility", 3)*.2+x.get("goal_alignment", 3)*.3-x.get("effort", 3)*.05, 2)
    a.sort(key=lambda x: x["score"], reverse=True)
    for i, x in enumerate(a, 1): x["priority"] = i
    s["prioritized_actions"] = a; s["next_best_action"] = a[0] if a else {}; trace(s, "prioritize_actions"); return s

def select_next_best_action(s):
    s["tool_requests"] = [{"tool_name": "execution_gateway", "purpose": s["next_best_action"]["action"], "requires_confirmation": True}] if s.get("mode") == "execution" and s.get("next_best_action") else []; trace(s, "select_next_best_action"); return s

def generate_final_response(s):
    lines = ["Intent: " + s.get("primary_intent", "unknown"), "Goal: " + s.get("goal", ""), "", "Recommended action plan:"]
    lines += [f"{x['priority']}. {x['action']} - {x['reason']}" for x in s.get("prioritized_actions", [])]
    s["final_response"] = "\n".join(lines); trace(s, "generate_final_response"); return s

def clarify(s):
    s["final_response"] = "Please share your goal, deadline, or current situation."; return s

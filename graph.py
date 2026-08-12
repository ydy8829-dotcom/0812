from langgraph.graph import StateGraph, END
from state import AgentState
from agents import analyze_input, classify_intent, extract_context, infer_goal, identify_constraints, check_sufficiency, generate_action_plan, prioritize_actions, select_next_best_action, generate_final_response, clarify

def route_sufficiency(state: AgentState):
    return "generate_action_plan" if state.get("information_sufficient", False) else "clarify"

def build_graph():
    b = StateGraph(AgentState)
    for name, fn in [("analyze_input", analyze_input), ("classify_intent", classify_intent), ("extract_context", extract_context), ("infer_goal", infer_goal), ("identify_constraints", identify_constraints), ("check_sufficiency", check_sufficiency), ("generate_action_plan", generate_action_plan), ("prioritize_actions", prioritize_actions), ("select_next_best_action", select_next_best_action), ("generate_final_response", generate_final_response), ("clarify", clarify)]: b.add_node(name, fn)
    b.set_entry_point("analyze_input")
    b.add_edge("analyze_input", "classify_intent")
    b.add_edge("classify_intent", "extract_context")
    b.add_edge("extract_context", "infer_goal")
    b.add_edge("infer_goal", "identify_constraints")
    b.add_edge("identify_constraints", "check_sufficiency")
    b.add_conditional_edges("check_sufficiency", route_sufficiency, {"generate_action_plan":"generate_action_plan", "clarify":"clarify"})
    b.add_edge("generate_action_plan", "prioritize_actions")
    b.add_edge("prioritize_actions", "select_next_best_action")
    b.add_edge("select_next_best_action", "generate_final_response")
    b.add_edge("generate_final_response", END)
    b.add_edge("clarify", END)
    return b.compile()

graph = build_graph()

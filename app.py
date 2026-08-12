import html
import streamlit as st
from run_graph import run

st.set_page_config(page_title="FlowPilot", page_icon="*", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;700;800&display=swap');
:root{--bg:#091115;--panel:#111c21;--line:#25333a;--muted:#89969e;--ink:#eaf0f2;--accent:#b7ef62;--cyan:#83d7ce}
.stApp{background:var(--bg);color:var(--ink);font-family:Manrope,sans-serif}.block-container{max-width:1400px;padding:2.5rem 4rem 4rem}[data-testid="stSidebar"]{background:#0c171c;border-right:1px solid var(--line)}h1,h2,h3{letter-spacing:-.04em}.brand,.eyebrow,.kicker,.score{font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:.12em}.brand{color:var(--accent);font-size:.8rem}.kicker{color:var(--cyan);font-size:.75rem;margin-bottom:.8rem}.hero{font-size:clamp(2.5rem,5vw,5.3rem);line-height:1;font-weight:800;max-width:780px;margin:0}.copy{color:var(--muted);max-width:610px;line-height:1.7;margin:1.4rem 0 2.4rem}.eyebrow{color:var(--muted);font-size:.68rem;margin-bottom:.45rem}.rule{border-top:1px solid var(--line);margin:2.4rem 0 1.5rem}.metric,.card{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:1.1rem 1.25rem}.metric{min-height:88px}.metric-value{font-size:1.5rem;font-weight:700}.muted{color:var(--muted);font-size:.8rem;line-height:1.55}.card{margin:.65rem 0}.selected{border-color:var(--accent)!important;box-shadow:0 0 0 1px #b7ef6233}.score{font-size:.72rem;color:var(--accent)}.action-title{font-weight:700;margin:.4rem 0}.pill{display:inline-block;border:1px solid #385047;border-radius:99px;padding:.28rem .6rem;color:var(--accent);font:500 .7rem 'DM Mono',monospace}div.stButton>button{border-radius:10px;border:1px solid var(--line);background:#17252a;color:var(--ink)}div.stButton>button[kind="primary"]{background:var(--accent);color:#0a120e;border:0;font-weight:800}
</style>
""", unsafe_allow_html=True)

if "result" not in st.session_state: st.session_state.result = None
with st.sidebar:
    st.markdown('<div class="brand">* FLOWPILOT / 01</div>', unsafe_allow_html=True)
    st.markdown("### Workspace")
    mode = st.radio("Mode", ["recommendation", "execution"], format_func=lambda x: "Recommendation" if x == "recommendation" else "Execution")
    st.caption("Execution mode asks for confirmation before external work.")
    st.markdown("<div class='rule'></div>", unsafe_allow_html=True)
    st.markdown("#### Pipeline")
    for label in ["Input analysis", "Intent classification", "Context and goal", "Action ranking", "Next best action"]: st.markdown(f"<div class='muted' style='padding:.45rem 0'>o &nbsp; {label}</div>", unsafe_allow_html=True)

st.markdown('<div class="kicker">INTENT -> ACTION INTELLIGENCE</div>', unsafe_allow_html=True)
st.markdown('<h1 class="hero">Turn thoughts into<br><span style="color:#b7ef62">next actions.</span></h1>', unsafe_allow_html=True)
st.markdown('<p class="copy">FlowPilot structures an ambiguous request into intent, goal, constraints, and the most useful next step.</p>', unsafe_allow_html=True)
prompt = st.text_area("Situation or goal", value="I have an interview at a semiconductor equipment company next month. What should I prepare?", height=125, placeholder="Example: I want to introduce RAG to our internal docs. Help me define the MVP.")
c1, c2 = st.columns([1, 5])
with c1: analyze = st.button("* Build plan", type="primary", use_container_width=True)
with c2: st.caption("No external action is taken automatically.")
if analyze:
    with st.spinner("Structuring your request..."): st.session_state.result = run(prompt, mode)

result = st.session_state.result
if result:
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
    confidence = result.get("intent_confidence", 0) * 100
    cols = st.columns(4)
    values = [result.get("primary_intent", "unknown"), f"{confidence:.0f}%", str(len(result.get("prioritized_actions", []))), mode.title()]
    for col, label, value in zip(cols, ["Detected intent", "Confidence", "Recommended actions", "Mode"], values):
        with col: st.markdown(f'<div class="metric"><div class="eyebrow">{label}</div><div class="metric-value">{html.escape(value)}</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
    left, right = st.columns([1.45, 1])
    with left:
        st.markdown('<div class="eyebrow">RECOMMENDATION MAP</div><h2>Action sequence</h2>', unsafe_allow_html=True)
        st.markdown(f'<p class="muted">Goal - {html.escape(result.get("goal", ""))}</p>', unsafe_allow_html=True)
        for a in result.get("prioritized_actions", []):
            selected = " selected" if a.get("priority") == 1 else ""
            deps = ", ".join(a.get("dependencies", [])) or "None"
            st.markdown(f'<div class="card{selected}"><div class="score">0{a.get("priority", "")} / SCORE {a.get("score", 0)}</div><div class="action-title">{html.escape(a.get("action", ""))}</div><div class="muted">{html.escape(a.get("reason", ""))}<br>Done means - {html.escape(a.get("expected_outcome", ""))}<br>Dependencies - {html.escape(deps)}</div></div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="eyebrow">DECISION BRIEF</div><h2>Why this plan</h2>', unsafe_allow_html=True)
        st.markdown(f'<div class="card"><span class="pill">{html.escape(result.get("primary_intent", "unknown"))}</span><p>{html.escape(result.get("decision_basis", ""))}</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="eyebrow" style="margin-top:2rem">NEXT BEST ACTION</div>', unsafe_allow_html=True)
        nxt = result.get("next_best_action", {})
        st.markdown(f'<div class="card selected"><div class="action-title">{html.escape(nxt.get("action", ""))}</div><div class="muted">{html.escape(nxt.get("expected_outcome", ""))}</div></div>', unsafe_allow_html=True)
        if mode == "execution": st.warning("Execution mode: confirmation is required before external work.")
        with st.expander("Show analysis trace"): st.json({"context": result.get("context"), "constraints": result.get("constraints"), "trace": result.get("trace", [])})
else:
    st.markdown('<div class="rule"></div><p class="muted">Enter a situation above and build a plan to see ranked actions.</p>', unsafe_allow_html=True)

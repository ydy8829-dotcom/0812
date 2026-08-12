from run_graph import run

def test_interview_plan():
    result = run("다음 달 반도체 장비회사 면접인데 뭘 준비해야 할지 모르겠어")
    assert result["primary_intent"] == "planning"
    assert result["next_best_action"]["action"] == "지원 회사와 직무 JD 분석"
    assert result["mode"] == "recommendation"

def test_mode_requires_confirmation():
    result = run("회사에 이메일 보내", mode="execution")
    assert result["tool_requests"][0]["requires_confirmation"] is True

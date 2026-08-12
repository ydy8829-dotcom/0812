# Intent-driven AI Action Recommendation Agent

자연어 입력을 `의도 → 상황 → 목표 → 제약 → 행동 계획 → 우선순위 → 다음 행동`으로 변환하는 LangGraph 기반 MVP scaffold입니다.

## 실행

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run_graph.py "다음 달 반도체 장비회사 면접인데 뭘 준비해야 할지 모르겠어"
streamlit run app.py
```

기본값은 `MOCK_LLM=true`이므로 API 키 없이도 구조를 확인할 수 있습니다. 실제 모델을 사용하려면 `.env`에서 `MOCK_LLM=false`, `LLM_PROVIDER=openai` 또는 `ollama`를 설정합니다.

## 그래프

```text
START
  ↓
analyze_input → classify_intent → extract_context → infer_goal
  ↓                                             ↓
identify_constraints → check_sufficiency ───────┘
                              ├─ 부족: clarify / safe response
                              └─ 충분: generate_plan → prioritize → select_next → response → END
```

실행 도구는 현재 mock interface만 제공하며, 외부 시스템 변경이 필요한 경우 `mode=recommendation`에서는 실행하지 않습니다.

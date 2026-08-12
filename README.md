# Intent-driven AI Action Recommendation Agent

## Furiosa NPU 연결

이 프로젝트는 FlowPilot UI/에이전트와 Furiosa-LLM의 OpenAI 호환 endpoint를 연결할 수 있습니다. Windows PC에서는 FlowPilot을 실행하고, Furiosa SDK와 NPU가 설치된 Linux NPU Pod에서는 모델 서버를 실행합니다.

### NPU Pod

```bash
furiosa-llm serve furiosa-ai/Llama-3.1-8B-Instruct --devices "npu:0" --port 8000
```

### Windows `.env`

```env
MOCK_LLM=false
LLM_PROVIDER=furiosa
FURIOSA_BASE_URL=http://<NPU_POD_HOST>:8000/v1
FURIOSA_API_KEY=EMPTY
FURIOSA_MODEL=EMPTY
```

FlowPilot 사이드바의 `Test Furiosa connection` 버튼을 눌러 `/version` endpoint 연결을 확인합니다. 연결이 안 되면 NPU Pod의 서버 실행 여부, host/port, 네트워크 접근을 확인합니다.

### 성능 측정

```bash
python benchmark.py --provider furiosa --base-url http://<NPU_POD_HOST>:8000/v1 --model EMPTY --runs 3
```

측정 결과는 latency와 API usage token을 출력합니다. Furiosa Apps의 chat-playground가 제공하는 TTFT, TPS, TPOT, 전력, 온도 지표는 NPU Pod에서 별도로 캡처해 최종 보고서에 추가합니다.

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

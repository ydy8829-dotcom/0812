# Intent-driven AI Action Recommendation Agent PRD

## 1. Product Overview

- Product name: Intent-driven AI Action Recommendation Agent
- Problem: 기존 챗봇은 질문에 답하지만 사용자의 실제 목표와 다음 행동을 구조화하지 못한다.
- Vision: 사용자의 자연어 상황을 실행 가능한 의사결정과 행동 계획으로 바꾸는 개인 업무·학습 에이전트.
- Target users: 업무·학습·프로젝트를 시작하거나 문제 해결 방향이 필요한 사용자.
- Value proposition: 의도, 목표, 제약, 정보 부족, 행동 우선순위, Next Best Action을 한 번에 제공한다.

## 2. MVP Scope

### In scope

자연어 입력, 범용 intent taxonomy, context/goal/constraint 추출, 정보 충분성 판단, 행동 후보 생성, 점수 기반 우선순위화, recommendation/execution mode 분리, Streamlit UI, mock LLM, OpenAI/Ollama abstraction.

### Future scope

Web Search, RAG/File Search, Calendar, Email, DB, 사내 API, 사용자 profile/memory, checkpoint 기반 대화 지속, Human-in-the-loop 실행 승인.

## 3. Key Scenarios

1. “다음 달 반도체 장비회사 면접인데 뭘 준비해야 할지 모르겠어.” → JD 분석부터 면접 준비 계획 제안.
2. “RAG 기반 사내 문서 챗봇을 만들고 싶은데 어디서 시작하지?” → 데이터 범위와 MVP 아키텍처부터 제안.
3. “회사에 이메일 보내.” → 수신자·본문·전송 시점을 정리하고 확인 전 실행하지 않음.
4. “이 두 기술 중 무엇을 선택할까?” → 비교 기준과 추가 정보, 의사결정 행동 제안.
5. “코드가 안 돼.” → 재현 조건·오류·최근 변경사항을 수집한 뒤 진단 순서 제안.

## 4. User Flow

`user_input → analyze_input → classify_intent → extract_context → infer_goal → identify_constraints → check_sufficiency → generate_action_plan → prioritize_actions → select_next_best_action → final_response`

정보가 부족하면 `clarify`로 분기한다. 외부 변경 작업은 execution mode에서도 확인 요청을 만든 뒤 별도 gateway에서 승인받는다.

## 5. Intent Taxonomy

핵심 taxonomy는 `information_request`, `decision_support`, `planning`, `problem_solving`, `task_execution`, `recommendation`, `learning`, `troubleshooting`, `comparison`, `scheduling`, `brainstorming`, `unknown`이다. `primary_intent`는 그래프 routing용, `secondary_intent`는 복합 요청 보조용이다. 새 agent/tool은 taxonomy를 추가하거나 기존 intent의 capability registry에 등록한다.

## 6. State Design

`AgentState`는 입력, mode, profile/context, intent, goal, constraints, missing_information, action candidates, prioritized actions, next_best_action, tool_requests, decision_basis, final_response, error, trace를 보유한다. 내부 Chain-of-Thought는 저장·출력하지 않고 짧은 근거만 기록한다.

## 7. Node Design

| Node | 책임 | 다음 |
|---|---|---|
| analyze_input | 입력 정규화·실행 mode 확인 | classify_intent |
| classify_intent | primary/secondary intent와 confidence | extract_context |
| extract_context | 기한·도메인·사용자 조건 추출 | infer_goal |
| infer_goal | 요청을 완료 가능한 목표로 변환 | identify_constraints |
| identify_constraints | 시간·권한·안전 제약 정리 | check_sufficiency |
| check_sufficiency | 필수 정보 충족 여부 | plan 또는 clarify |
| generate_action_plan | 행동 후보와 의존성 생성 | prioritize_actions |
| prioritize_actions | 점수와 dependency 기반 순위화 | select_next_best_action |
| select_next_best_action | 가장 실행 가능한 행동 선택·tool 요청 생성 | response |
| generate_final_response | 계획·근거·확인 필요 여부 출력 | END |

## 8. Prioritization

초기 점수는 `0.25 Impact + 0.20 Urgency + 0.20 Feasibility + 0.30 Goal Alignment - 0.05 Effort`이다. 모든 항목은 1~5점이며, dependency가 충족되지 않은 행동은 후순위로 내린다. 실제 운영에서는 사용자의 수락률과 완료율로 가중치를 보정한다.

## 9. Failure Handling and Safety

- 낮은 confidence/unknown: 목표·기한·대상을 묻는 clarification.
- Structured output 실패: schema validation 후 안전한 fallback과 오류 trace.
- 정보 부족: missing_information을 노출하고 추측으로 채우지 않음.
- Tool/API timeout: 재시도 횟수 제한, stale 결과 표시, 대체 행동 제안.
- hallucination: 검색·RAG 근거 필드와 confidence를 추가하고 사실 확인이 필요한 행동은 보류.
- 외부 변경: 기본 recommendation mode. execution mode도 `requires_confirmation=true`인 요청만 생성하며 승인 전 전송·삭제·결제를 수행하지 않음.

## 10. Observability and Evaluation

각 node trace에 node name, 입력/출력 key, latency, token usage, error, routing result를 기록하도록 확장한다. MVP 지표는 Intent Accuracy, Goal Extraction Accuracy, Action Relevance, Next Action Acceptance Rate, Action Completion Rate, Clarification Rate, Tool Confirmation Rate이다.

## 11. Existing Code Reuse / Refactoring

기존 `StateGraph`, `conditional_edges`, 시간·날씨 context node, `recommend_*` 분기, Streamlit 결과 출력은 재사용한다. 기존 `food/activity/unknown` 분기는 범용 intent taxonomy로 교체한다. 모든 agent가 `{**state, ...}`를 반환하는 패턴은 상태 충돌과 타입 불일치를 만들 수 있어 명시적 state update로 바꾼다. `json.loads(response.content)`는 Pydantic structured output으로 대체하고, API 호출은 tool adapter로 분리한다. 서울 고정 날씨, 첫 추천 항목만 장소 검색, print 기반 관찰성은 MVP 이후 제거·개선 대상이다.

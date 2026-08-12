# FlowPilot + Furiosa NPU 미니프로젝트 설계

## 프로젝트 결론

FlowPilot은 사용자의 자연어 상황을 의도, 목표, 제약조건, 우선순위 액션, 다음 행동으로 바꾸는 AI Action Recommendation 서비스다. LLM을 Furiosa NPU에서 실행하면 UI와 에이전트 로직은 유지한 채 추론 백엔드만 NPU로 교체할 수 있다.

## 전체 파이프라인

```text
사용자 브라우저
      |
      v
Streamlit Frontend
      |
      v
LangGraph Agent
      |
      +--> mock provider       개발/재현용
      +--> OpenAI API          외부 API baseline
      +--> Ollama              로컬 CPU/GPU baseline
      +--> Furiosa OpenAI API  NPU 실험/최종 lane
                                  |
                                  v
                         Furiosa-LLM Server
                                  |
                                  v
                             Furiosa NPU
```

## 모델·데이터

- 1차 모델: Furiosa가 제공하는 호환 instruct artifact 중 작은 모델로 기능을 먼저 검증한다.
- 비교 baseline: 동일 prompt와 decoding 설정으로 OpenAI-compatible local endpoint 또는 Ollama를 측정한다.
- 서비스 기능: intent classification, goal extraction, action planning, next-best-action recommendation.
- 데이터: 초기에는 사용자 입력과 합성 테스트 prompt만 사용한다. 실제 사내 문서는 승인된 자료만 별도 RAG 단계로 추가한다.

## Furiosa Pod 실습 흐름

Furiosa SDK/LLM이 설치된 Linux NPU Pod에서:

```bash
furiosa-llm serve furiosa-ai/Llama-3.1-8B-Instruct-FP8 --devices "npu:0"
```

기본 endpoint는 http://localhost:8000/v1이다. 다른 Pod에서 접근하면 FURIOSA_BASE_URL을 해당 Pod 주소로 바꾼다.

```bash
curl http://localhost:8000/v1/models
python benchmark.py --provider furiosa --base-url http://localhost:8000/v1 --model EMPTY --runs 3
```

Windows 개발 PC의 .env 예시:

```env
MOCK_LLM=false
LLM_PROVIDER=furiosa
FURIOSA_BASE_URL=http://<NPU_POD_HOST>:8000/v1
FURIOSA_API_KEY=EMPTY
FURIOSA_MODEL=EMPTY
```

## 성능 비교 지표

동일 prompt, model, max tokens, temperature, run 횟수를 고정한다.

| 지표 | 측정 방법 |
|---|---|
| 응답시간 | 요청 시작부터 전체 응답 수신까지 |
| 처리량 | total tokens / elapsed seconds |
| 입력·출력 토큰 | API response의 usage |
| 오류율 | HTTP/timeout 실패 비율 |
| 전력 | NPU Pod 모니터링 지표를 별도 기록 |

benchmark.py는 latency와 token usage를 자동 기록한다. 전력과 NPU utilization은 Pod의 Furiosa 모니터링 명령 또는 Prometheus metrics를 함께 캡처해야 한다.

## 영상 촬영 순서

1. 프로젝트와 .env에서 provider 확인
2. furiosa-llm serve로 NPU 모델 서버 실행
3. /v1/models 또는 /version health check
4. Streamlit UI에서 동일 prompt 실행
5. benchmark.py를 3~10회 실행
6. 결과 JSON과 /metrics를 저장
7. OpenAI/Ollama baseline과 표로 비교
8. 최종 UI와 추천 결과 녹화

## 현재 제한사항

Furiosa SDK는 Linux와 Furiosa 장치·드라이버가 필요한 환경이므로 Windows PC에서 직접 NPU 검증은 할 수 없다. 현재 코드는 NPU endpoint adapter와 재현 가능한 benchmark를 제공하고, 실제 모델 서버 실행은 NPU Pod에서 수행한다.

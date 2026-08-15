# ctf-skill

`ctf-skill`은 승인된 교육용 CTF를 AI 에이전트와 함께 풀 때 쓰는 진행 규칙입니다.

정답이나 공격 기법을 제공하지는 않습니다. 대신 에이전트가 다음과 같이 일하도록 만듭니다.

- 확인한 사실과 추측을 구분합니다.
- 같은 시도를 이름만 바꿔 반복하지 않습니다.
- 로컬에서 통과한 결과를 실제 정답으로 착각하지 않습니다.
- 막히거나 중단된 일을 성공이나 실패로 바꿔 적지 않습니다.
- 마지막에는 공식 채점 결과로 결론을 냅니다.

실제로 배포하는 파일은 `skills/ctf-solving/SKILL.md` 하나입니다.

## 왜 필요한가

에이전트가 CTF를 풀다 보면 흔히 이런 일이 생깁니다.

1. 처음 세운 추측이 확인 없이 사실처럼 굳습니다.
2. 진짜 대상 대신 직접 만든 테스트 코드에서 성공하고는 문제를 풀었다고 믿습니다.
3. 이미 효과가 없던 방법을 설정만 바꿔 다시 실행합니다.
4. 중요한 단서를 얻고도 실제 채점까지 확인하지 않습니다.
5. 중단, 환경 문제, 풀이 실패를 모두 같은 실패로 기록합니다.

이 스킬은 이런 진행상의 실수를 줄이는 데 집중합니다. 더 많은 기법을 알려 주는 도구가 아니라, **어떤 근거로 무엇을 확인했고 다음에 왜 그 행동을 하는지**를 기록하게 하는 도구입니다.

## 지원하는 문제 종류

문제 제목이 아니라 실제 파일과 실행 환경을 보고 다음 여섯 범주로 나눕니다.

- `crypto`: 암호 알고리즘이나 그 구현의 약한 부분을 다루는 문제
- `forensics`: 저장된 파일·패킷·메모리에서 흔적을 찾는 문제
- `misc`: 다른 다섯 범주에 들어가지 않는 문제
- `pwn`: 실행 중인 프로그램의 잘못된 동작을 이용하는 문제
- `reverse`: 프로그램 내부 동작을 거꾸로 분석하는 문제
- `web`: 웹 서비스의 동작과 요청 처리를 다루는 문제

## 먼저 알아 둘 용어

문서에는 꼭 필요한 기술 용어만 남겼습니다.

- **로컬 판정 수단(local oracle)**: 내 환경에서 시도가 맞는지 빠르게 확인하는 방법입니다.
- **실제 채점 창구(real acceptance surface)**: 대회 서버나 제출 화면처럼 최종 정답 여부를 결정하는 곳입니다.
- **대체물(surrogate)**: 진짜 대상 대신 쓰는 테스트 코드, 복제본, 에뮬레이터, 패치한 프로그램 등을 뜻합니다.
- **출처(provenance)**: 그 사실을 어디에서 확인했는지 나타내는 기록입니다.
- **가설**: 아직 사실인지 확인하지 않은 설명입니다.

가장 중요한 원칙은 간단합니다.

> 대체물에서 성공한 것은 실제 정답이 아니다.

## 어떻게 진행하는가

### 1. 시작 전에 대상부터 정한다

기법을 고르기 전에 다음 일곱 가지를 적습니다.

1. 정확히 무엇을 분석하는가
2. 어떤 파일이 필요한가
3. 무엇을 입력으로 바꿀 수 있는가
4. 실행 중 무엇을 관찰할 수 있는가
5. 로컬에서 맞고 틀림을 어떻게 확인하는가
6. 실제 정답은 어디에서 판정되는가
7. 시간과 실행 횟수를 어디까지 쓸 것인가

이 중 1·5·6번, 즉 분석 대상과 로컬 판정 수단, 실제 채점 창구를 모르면 큰 탐색을 시작하지 않습니다. 먼저 작은 확인 작업으로 빈칸을 채웁니다.

대상이나 채점 창구도 임의로 바꿀 수 없습니다. 원본 서비스에서 나온 직접 증거나 사용자·운영자가 준 새 정보가 있어야 합니다.

### 2. 채점 조건을 다 안다고 가정하지 않는다

채점 서버의 위치를 안다고 해서 서버가 확인하는 조건을 모두 아는 것은 아닙니다.

에이전트는 다음 내용을 계속 기록합니다.

- 지금까지 찾은 조건
- 마지막으로 확인한 판단 지점
- 아직 확인하지 못한 다음 판단
- 각 내용의 출처

확인 수준은 세 단계입니다.

- `unknown`: 아직 충분히 모릅니다.
- `frontier-complete`: 확인을 멈춘 지점을 명시했고, 거기까지는 검증했습니다.
- `authoritative-complete`: 실제 채점 경로를 처음부터 끝까지 실행했고, 도달 가능한 판단을 모두 설명할 수 있습니다.

마지막 단계가 되기 전에는 “다음에 확인할 것”을 적어도 하나 남깁니다. 그 확인 작업을 예산 안에서 할 수 있다면, 후보를 대량으로 훑기 전에 확인부터 합니다.

### 3. 대체물은 확인한 범위까지만 믿는다

대체물을 쓸 때는 다음 정보를 적어서 고정해 둡니다.

- 파일 내용
- 설정
- 도구와 실행 환경의 버전
- 원본과 같은 결과가 나온 입력과 지점
- 처음으로 달라진 지점

파일이나 설정, 도구, 실행 환경이 바뀌면 새 대체물로 취급합니다. 예전 확인 결과를 그대로 물려받지 않습니다.

원본과 비교하지 않은 범위에서 나온 결과로 후보를 버리거나, 가설을 닫거나, 진행 기록을 바꿀 수 없습니다. 이때는 “아직 확인하지 못한 차이”로만 남깁니다.

### 4. 첫 번째 후보를 곧바로 정답으로 정하지 않는다

한 조건을 만족하는 후보가 여러 개일 수 있습니다. “후보가 하나뿐인가”에 대한 판정은 세 가지입니다.

- `proven`: 후보가 하나뿐이라는 근거가 있습니다.
- `disproven`: 서로 다른 후보가 둘 이상 실제로 나왔습니다.
- `unknown`: 어느 쪽도 증명하지 못했습니다.

후보가 여러 개일 수 있다면 후보 묶음을 보존하고, 다음 조건으로 구분한 뒤 최종 후보를 고릅니다. 예산 안에서 확인할 수 있는 후보가 남아 있으면 일을 끝냈다고 선언하지 않습니다.

### 5. 가설은 적게, 실험은 한 번에 하나만 한다

동시에 다루는 가설은 최대 세 개입니다. 근거가 하나뿐이면 하나만 시작해도 됩니다. 숫자를 채우려고 근거 없는 가설을 만들지 않습니다.

각 가설에는 다음 내용이 필요합니다.

- 왜 가능하다고 보는가
- 한 번에 무엇만 바꿀 것인가
- 맞다면 무엇이 보여야 하는가
- 틀리다면 무엇이 보여야 하는가
- 언제 버릴 것인가

같은 파일을 다시 받거나, 인코딩·라이브러리·작업자 수만 바꾸는 것은 새 전략이 아닙니다. 같은 전략에서 두 번 연속으로 판단에 도움이 되는 정보가 나오지 않으면 다른 접근으로 바꾸거나 멈춥니다.

하위 작업(child)에게 나눠 준 일이 끝나면, 루트가 child마다 한 줄짜리 처리
결과를 남깁니다. `child_id`, 판단 근거로 삼은 증거, 영향을 받는 가설 계열,
`accepted`/`rejected`/`pending`, 그리고 실제로 바뀐 상태(없으면 `none`)입니다.
처리 결과가 없는 child 보고는 상태를 바꾸지 못하고, 근거가 부족한 상태 변경
요구는 `rejected`로 남기고 계열은 그대로 둡니다.

### 5-1. 외부 리뷰는 막혔을 때만, 준비까지만 한다

별도로 설치한 외부 리뷰 스킬은 다음 네 조건이 모두 맞을 때만 켭니다.

1. 같은 fingerprint에서 정보가 없는 라운드가 두 번 끝났다
2. 아직 시도할 만한 정당한 구분 실험이 남아 있지 않다
3. 표현을 실질적으로 바꿀 방법이 남아 있지 않다
4. 검증하지 않은 이전 리뷰 제안이 없다

어렵거나 느리다는 이유만으로는 켜지 않습니다. 자동 활성화는 로컬에서 패킷을
준비하는 데까지이며, 외부 전송은 사용자가 그 패킷을 명시적으로 승인해야
합니다. 리뷰 응답은 참고 자료일 뿐이라 루트가 직접 재현하고 실제 채점
창구로 확인하기 전에는 결과를 확정하지 못합니다.

### 6. 예산을 유리하게 바꾸지 않는다

첫 실행 전에 예산의 단위, 포함할 비용, 초기 한도를 정합니다. 이 값은 사용자가 정해 주거나, 상위 작업에서 내려오거나, 실제 외부 제약에서 옵니다.

시간이 오래 걸리는 로컬 계산을 예산에서 빼거나, 실행하지 않은 비용을 이미 사용한 것처럼 기록할 수 없습니다. 비용 추정이 여러 개라면 현재 확인된 값 가운데 가장 낮은 값을 기준으로 실행 가능 여부를 판단합니다.

### 7. 모순을 지우지 않는다

두 관찰이 함께 참일 수 없다면 모순입니다. 원본끼리든, 원본과 대체물 사이든, 대체물끼리든 어느 쪽에서 결과가 갈리면 모두 모순으로 봅니다.

“환경이 달라서 그럴 것”이라는 말은 설명 후보일 뿐입니다. 같은 조건에서 확인한 증거가 나오기 전까지 모순은 남겨 둡니다.

로컬에서는 통과했지만 실제 채점에서 거절되면 다음 순서로 처리합니다.

1. 로컬 모델의 확인 상태를 `unknown`으로 되돌립니다.
2. 그 모델을 더 다듬는 작업을 멈춥니다.
3. 대상과 채점 창구는 그대로 둡니다. 거절당했다고 더 쉬운 대상으로 갈아타지 않습니다.
4. 빠뜨린 조건, 파일·환경 차이, 입력 형식, 중간에 버렸던 후보가 있는지 확인합니다.

### 8. 마지막에는 실제 채점을 확인한다

깨끗한 상태에서 로컬 재현을 한 뒤 실제 채점 창구를 사용합니다. 로컬 성공만으로 `solved`라고 기록할 수 없습니다.

## 결과 기록 규칙

모든 시도는 “무엇을 얻었는가”와 “왜 멈췄는가”를 따로 기록합니다.

### 성과

- `solved`: 로컬 재현과 실제 채점 성공을 모두 확인했습니다.
- `failed-with-valid-oracle`: 로컬 판정 수단은 있었지만 정답을 얻지 못했습니다.
- `partial`: 쓸모 있는 사실은 확인했지만 정답은 아닙니다.
- `no-result`: 확인된 성과가 없습니다.

### 종료 이유

- `completed`: 해야 할 일을 마쳤습니다.
- `blocked`: 필요한 파일이나 서비스에 접근할 수 없습니다.
- `interrupted`: 외부에서 작업이 중단됐습니다.
- `budget-stop`: 정한 예산을 모두 썼습니다.

실행 가능한 확인 작업이 남아 있으면 `completed`를 쓸 수 없습니다. 종료 결과는 한 번 기록하면 그대로 둡니다. 이후 뒷정리 단계에서 오류가 나도 고쳐 쓰지 않습니다.

## 상태 기록 예시

아래 예시는 아직 실제 분석을 시작하지 않은 상태입니다.

```yaml
ctf_attempt:
  target:
    exact_target: "artifact-sha256:example"
    local_oracle: "example-local-check"
    real_acceptance_surface: "example-validator"
  acceptance_model:
    completeness: "unknown"
    next_discovery: "check whether another decision follows"
  active_hypotheses:
    - id: "hypothesis-1"
      evidence: "observed fact from local-session:example"
      next_test: "one bounded check"
  budget:
    unit: "actions"
    limit: 1
    used: 0
    remaining: 1
  result: null
  termination: null
  validator_response: null
```

전체 필드와 정확한 규칙은 `skills/ctf-solving/SKILL.md`에 있습니다.

## 설치

1. 저장소를 내려받습니다.
2. `skills/ctf-solving/SKILL.md`를 사용하는 에이전트의 스킬 디렉터리 아래 `ctf-solving/SKILL.md`로 복사합니다.

복사 대신 에이전트가 저장소 파일을 직접 읽도록 설정해도 됩니다.

스킬 디렉터리의 정확한 위치는 사용하는 에이전트 문서를 따르세요.

## 검증 결과

2026-08-15 개정판은 다음 검사를 통과했습니다.

- 정책 동작 시나리오 66건: `PASS: 66 model-control cases`
  - 필수 행동을 빠뜨리는 경우
  - 금지된 행동을 고르는 경우
  - 상태를 바꿔야 할 때 바꾸지 않는 경우
  - 정책 용어만 나열해 검사를 넘기려는 경우
  - 예측이 같은 가설을 계열 하나로 묶고, 다른 예측은 나누는 경우
  - 근거 없는 은퇴·재개방을 걸러 내는 경우
  - child 처리 결과를 빠뜨리거나 근거 없이 상태를 바꾸는 경우
  - 조건이 모자란데 외부 리뷰를 켜거나, 재현 없이 리뷰 응답을 확정하는 경우
  - prepare 전에 미래 evidence ID를 만들거나 child/evidence binding을 바꾸는 경우
  - 같은 semantic fingerprint를 반복하거나 재현된 candidate의 closure를 미루는 경우
- prompt schema v3가 case별 상태 키/JSON scalar type, candidate action 집합,
  caller가 선택한 provenance를 공개하되 답안 값은 공개하지 않는지 확인하는 구조화 테스트
- Ruff 코드 검사와 형식 검사
- basedpyright 타입 검사: 오류 0, 경고 0
- JSON 문법 검사와 `git diff --check`

검증 대상 파일의 SHA-256:

- 정책 (`skills/ctf-solving/SKILL.md`): `9b3210dd33ee706b31ece935fc95c66a31c23a8d4e6f64adb7b36098bea57c67`
- 검사 설명 (`tests/ctf-solving-model-controls.md`): `ce83abe9b73ed0afac78b8d1ec5226134337449c4fcb0c34d1c642663868a695`
- 실행기 (`tests/run_model_controls.py`): `fd49355653aa55167df6d544ea20043a295ab720bb97e781ba7b20a6041ba606`
- typed grader (`tests/model_control_harness.py`): `cb197a5ed9377e18f6881a9e3cef068a02fa8d194f31e9cfe801feedaf4cf968`
- 구조화 contract 테스트 (`tests/test_model_control_harness.py`): `4323198c69835f8038a64ab10aeb543b1733bbc7679857c22581e4820bb56343`
- 검사 시나리오 (`tests/model-control-cases.json`): `1a0030d6e1d35932c80ffa9f0938c52fb5a3cc528fbb3b512b52111c809b0907`
- 보관용 legacy 응답 기록 (`tests/fixtures/legacy/opus5-model-control-responses.v1.json`): `816c546101ff185ccdf270610b7caf4d1807e1ee4cc2f0f685c13b22379c85b9`
  - 검증되지 않은 schema v1 기록이며 현재 schema v2 response grader의 통과 증거로 사용하지 않습니다.

이 검증은 규칙에 맞는 판단과 상태 변경이 나오는지를 확인합니다. 실제 CTF 해결률이나 풀이 속도를 보장하지는 않습니다.

2026-08-08 실제 모델 qualification은 별도 결과입니다.
`openai-codex/gpt-5.6-sol`(thinking `medium`)을 Senpi 2026.8.7 +
OmO Native print surface에서 generic 52건과 derived product 8건에 각각 한
번만 실행했으며, strict schema-v2 parser/grader 결과는
**NON_QUALIFIED**였습니다. Synthetic 52/52 self-test와 위 파일 hash는
정책·검사기 구현의 재현성을 뜻할 뿐 실제 모델 준수나 base-model 향상을
뜻하지 않습니다. 사용자 취소로 treatment와 여섯 CTF domain 평가는
실행되지 않았고, 실측되지 않은 treatment는 `oh-my-ctf`에서 제거됐습니다.
정확한 session, artifact, parser/grader 수치는
`oh-my-ctf/docs/CTF_MODEL_EVALUATION_LEDGER.md`의 2026-08-09 closure
항목에 기록합니다.

## 저장소 책임과 OmCTF 동기화

이 저장소가 범용 CTF 풀이 정책과 model-control regression의 source of
truth입니다. 가설, 반증, 후보 보존, surrogate 범위, budget, 모순, 결과
판정처럼 OmCTF 없이도 의미가 있는 규칙은 여기에서 먼저 변경하고
검증합니다.

가설 계열 정의, child 처리 결과(root disposition), 외부 리뷰 활성화 조건도
이 저장소가 소유합니다. 외부 리뷰 패킷 구성과 실제 전송, Senpi/OmO의 skill
활성화, session lifecycle, tool 권한, terminal authority는 여기에서 정의하지
않습니다. 이 정책은 언제 준비를 허용하는지만 정하고, 전송 자체는 승인받은
리뷰 스킬이 수행합니다.

`oh-my-ctf`는 이 정책에서 자격을 갖춘(qualified) compact profile을
파생해 패키징합니다. 이 profile은 원문 복사본이 아니라 OmO Native에서
필요한 지시만 유지하고, Senpi TUI 활성화, session lifecycle, tool 권한,
evidence 저장, sandbox, terminal authority는 OmCTF runtime과 integration
test에 맡깁니다. `PROVENANCE.json`은 원본 정책과 case/grader, local
profile, package manifest의 각 hash를 따로 고정하고 `COVERAGE.json`은
각 model-control case의 profile/runtime 소유자를 기록합니다.

동기화 순서는 다음과 같습니다.

1. 이 저장소에서 범용 정책과 model-control case를 함께 수정합니다.
2. self-test와 policy-bound model 응답 평가를 통과시킵니다.
3. OmCTF compact profile에 영향을 주는 의미 변화만 profile에 반영하고,
   전체 case의 ownership/anchor를 다시 검증합니다.
4. OmCTF의 provenance와 build-pinned hash를 현재 파일별 hash로 갱신합니다.
5. OmCTF package, activation, evidence, release test를 실행합니다.

범용 규칙은 이 저장소에서 먼저 바꾸고, OmCTF 전용 규칙은 범용 skill에
복제하지 않습니다. profile, package manifest, model-control case 중 하나의
hash가 이후 바뀌면 OmCTF 계획의 Task 9에서 다시 동기화해야 합니다.

## 파일 구성

```text
ctf-skill/
├── README.md
├── skills/
│   └── ctf-solving/
│       └── SKILL.md
└── tests/
    ├── __init__.py
    ├── ctf-solving-model-controls.md
    ├── fixtures/
    │   └── legacy/
    │       └── opus5-model-control-responses.v1.json  # unverified schema v1 archive
    ├── model-control-cases.json
    ├── model_control_harness.py
    ├── run_model_controls.py
    └── test_model_control_harness.py
```

## 사용 범위

승인된 교육용 CTF에서만 사용합니다. 운영자가 정한 대상, 시간, 계정 범위를 지켜야 합니다.

이 스킬은 판단과 보고 방식을 통제합니다. 문제별 정답이나 기술 절차를 제공하지 않습니다. 최종 성공 여부는 공식 채점 결과로만 판단합니다.

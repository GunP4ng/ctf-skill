# ctf-skill

## 목적

`ctf-skill`은 승인된 교육용 CTF에서 의사결정을 증거 기반으로 통제합니다. 제품 스킬 파일은 `skills/ctf-solving/SKILL.md`이고, 통제 범위는 대상 계약, 가설, 위임, 재현, 수용입니다.

## 의사결정 통제가 필요한 이유

초기 추측이 검증 없이 사실로 굳거나, 로컬 결과를 실제 수용으로 착각하는 일을 막습니다. 같은 검증을 반복하는 것도 줄입니다. 그래서 주장마다 출처와 적용 범위를 남기고, 동시에 검증하는 가설 수를 제한합니다.

## 적용 범주

여섯 범주로 라우팅합니다.

- crypto
- forensics
- misc
- pwn
- reverse
- web

## 핵심 통제

### 기존 작업 흐름과의 경계

기존 작업 흐름이 오케스트레이션, 계획, 진행 상태, 지속 노트, 리뷰, 정리, 완료를 계속 소유합니다. CTF 정책은 `ctf_attempt`만 기록하고 이 소유 관계를 바꾸지 않습니다.

### 변경 개입 직렬화

변경 개입은 아티팩트, 환경/세션/행위자, 공유 validator/계정/서비스/자원 경계 집합이 겹치면 직렬화합니다. 서로 겹치지 않는 수동 읽기·리뷰·격리 복제본은 병렬로 진행할 수 있습니다.

### 일곱 필드 대상 계약

작업을 시작하기 전에 정확한 대상, 필수 아티팩트, 통제 가능한 입력, 관찰 가능한 중간 상태, 로컬 오라클, 실제 수용 표면, 예산 및 중단 조건의 일곱 필드를 고정합니다. 오라클이나 수용 표면을 증거로 도출할 수 있을 때는 이론을 넓히거나 `blocked`로 종료하기 전에 제한 발견 실험 하나를 선택합니다.

### 출처가 명시된 역량 원장

역량과 제약을 기록할 때 각 항목의 출처와 신뢰 범위를 함께 남깁니다. 확인되지 않은 추정은 확정된 사실과 분리합니다.

### 활성 가설, 예비 후보 및 제한 개입

조사 전에 출처가 있는 활성 가설군을 최대 세 개까지 둡니다. 증거가 세 개를 뒷받침하면 세 개를 쓰고, 그렇지 않으면 뒷받침되는 가설군과 그 사이에 남은 증거 공백을 기록합니다. 출처 없는 후보를 만들어 개수를 채우지 않습니다. 뒷받침된 가설군이 하나뿐이어도 시작할 수 있습니다. 각 활성 가설군에는 전제, 제한 개입 하나, 참/거짓 신호, 폐기 조건, 출처가 들어갑니다. 복합 가설은 하나의 예측을 갖는 하나의 슬롯으로 표현합니다. `tie, arbitrary pick`은 증거상 동등한 비승격 개입 후보에만 씁니다.

예비에는 출처가 있고 중복되지 않는 후보만 둡니다. 그 후보의 개입이 예산 안에 들어가고 판단이나 종료를 바꿀 수 있어야 합니다. 나머지는 개별 식별자와 전제 역할이 없는 `unfunded candidates` 미지수 하나로 묶습니다. 슬롯이 열리면 전제가 입증된 예비 하나를 승격합니다. 승격 순서는 종료를 바꿀 증거, 선언한 최악 비용당 판별력, 등록 순서를 따르고, 근거와 출처를 남깁니다.

불확정으로 끝났거나 감당 가능한 개입이 남지 않은 활성 후보는 예비로 내립니다. 같은 맥락의 직접 반증이 나오면 해당 후보를 폐기하고, 전제가 불가능해진 의존 후보도 함께 폐기합니다. 다시 여는 것은 전제가 입증된 후보에 한해 새 증거와 예산이 뒷받침할 때만 가능합니다. 감당 가능한 활성 제한 개입, validator 종료 작업, 예산이 배정된 예비 중 하나라도 남아 있을 때만 계속합니다.

다변수 결합 개입은 결합이 입증되었거나 각 구성 요소의 유효한 귀무 결과가 있고, 결합 예측을 미리 선언한 경우에만 제한 실험 한 번으로 허용합니다.

예산은 선언 단위·한도·사용량·잔여량만 기록합니다. 예산 대조는 예상 `budget-stop` 직전에만 합니다. `solved`, `interrupted`, `blocked` 뒤에는 재개를 위한 대조를 하지 않습니다. 개입 전에는 새로 준비할 필요 없이 이미 가능한 불변·무비용·무부작용 읽기를 선택적으로 최대 한 번 묶습니다.

### 모순 및 출처 확인

관찰 결과가 기존 주장과 충돌하면 양쪽 증거의 출처와 적용 조건부터 확인합니다. 모순을 감추거나 근거 없이 어느 한쪽을 채택하지 않습니다.

### 격리된 비중복 위임 및 독립 재현

위임에는 불변 격리 입력과 비중복 범위를 쓰고, 공유 상태는 바꾸지 않습니다. 독립 재현은 입력과 관찰 출처가 서로 독립일 때만 허용하고, 그 결과를 계약과 원장에 연결합니다.

활성 가설군은 동시 실행 작업이 아니라 후보 모델입니다. 독립 재현은 예산을 하나로 묶은 카드 한 장의 상태 갱신 한 번으로 처리합니다.

### 로컬 재현 후 실제 수용

결과를 깨끗한 로컬 상태에서 재현한 뒤 실제 대회 수용 여부를 확인합니다. 로컬 재현만으로 최종 성공을 선언하지 않습니다.

## 결과와 종료 상태

모든 작업은 `result` 하나와 `termination` 하나를 함께 기록합니다.

- 결과 축: `solved`, `failed-with-valid-oracle`, `partial`, `no-result`
- 종료 축: `completed`, `blocked`, `interrupted`, `budget-stop`

허용 조합은 `solved`+`completed`, `failed-with-valid-oracle`+`completed`, `failed-with-valid-oracle`+`budget-stop`이며, `partial`과 `no-result`는 모든 종료와 조합할 수 있습니다. 종료 사건 뒤 조합은 고정됩니다.

`solved`에는 깨끗한 로컬 메커니즘과 실제 validator 수용이, `failed-with-valid-oracle`에는 유효한 오라클과 제한된 거부 관찰, 선언한 예산·중단 조건이 필요합니다. `partial`에는 유용하게 입증된 사실과 실제 수용이 없었다는 사실을, `no-result`에는 유용한 사실을 입증하지 못한 정확한 이유를 남깁니다.

종료 축별 기록:

- `blocked`: 사용할 수 없는 경계, 필요한 증명, 해제 조건, validator 부재 이유
- `interrupted`: 외부 사건, 마지막으로 입증된 상태, validator `not-run` 이유
- `budget-stop`: 선언한 한도와 validator 상태
- `completed`: 종료 동작과 정리 결과

모든 종료 기록에는 결과, 종료, 아티팩트/환경 식별자(가능하면 해시), 종료 사건, validator 응답, 종료 처리(closure)가 들어갑니다.

## 증거 보존과 판단 상태 정규화

컨텍스트를 줄이기 전에 판단 증거를 지속 기록(receipt/reference)으로 옮깁니다. 옮기기 전에 유일한 필수 증거를 삭제하면 안 됩니다. 임시 디버깅 아티팩트는 영구 보존 대상이 아니고, 필요 없어지면 제거합니다. 판단 상태 정규화는 세션 축약이 아니라서 주변 지속 상태를 바꾸지 않고, 진행 중(in-flight) 개입의 식별자와 기록을 보존해 중복 변경을 막습니다. 세션 축약 뒤에는 적용할 제어와 지속 상태를 다시 읽습니다.

## 2026-07-29 개정 검증

아티팩트 `7b42c1bebde777ac552510fb33014569d66c85c1bafd12429681b6c3fae56544`에서 구조적 제약과 planning-only, in-flight, cleanup-interruption, evidence-sparse 시나리오가 통과했습니다. 해결률, 성능, 일반화를 뒷받침하는 증거는 아닙니다.

## 디렉터리 구조

```text
ctf-skill/
├── README.md
└── skills/
    └── ctf-solving/
        └── SKILL.md
```

배포 파일은 `README.md`와 제품 스킬 파일뿐입니다.

## 가져오기 및 설치 예시

저장소를 `<repository-url>`에서 `ctf-skill`로 clone한 뒤, `skills/ctf-solving/SKILL.md`를 `<agent-skill-directory>/ctf-solving/SKILL.md`로 복사하거나 에이전트가 그 경로를 직접 로드하도록 설정합니다. 정확한 배치 위치는 사용하는 에이전트의 문서를 따릅니다.

## 승인된 안전 사용 예시

다음 YAML은 운영 기법이 아니라 상태를 기록하는 예시입니다.

```yaml
ctf_attempt:
  target_contract:
    exact_target: "artifact-sha256:example"
    required_artifacts: ["local-session:example"]
    controllable_input: "example-controlled-input"
    observable_intermediate_state: "example-observable-state"
    local_oracle: "example-local-oracle"
    real_acceptance_surface: "example-validator"
    budget_and_stop_condition: "one bounded action or stop"
  artifact_environment_identity: "artifact-sha256:example / local-session:example"
  capabilities:
    - id: "read-1"
      provenance: "observed read from local-session:example"
      capability: "read-only"
  active_families:
    - id: "family-1"
      prerequisite: "evidence gap remains for the example target"
      bounded_intervention: "single bounded read"
      true_signal: "read confirms the target assumption"
      false_signal: "read contradicts the target assumption"
      retirement_condition: "target assumption becomes settled"
      evidence_provenance: "observed read from local-session:example"
  reserve_candidates: []
  retired_families: []
  unknowns:
    - "evidence gap: a second provenance-backed distinguishing observation that would support an additional active family has not been observed yet"
  optional_passive_observation_batch: null
  exactly_one_next_bounded_intervention:
    id: "family-1"
    prerequisite: "evidence gap remains for the example target"
    immutable_scoped_inputs:
      ["artifact-sha256:example", "local-session:example"]
    mutation: "single bounded read"
    true_signal: "read confirms the target assumption"
    false_signal: "read contradicts the target assumption"
    stateful_resource_boundary_set: ["local-session:example"]
  in_flight_bounded_intervention: null
  budget:
    unit: "actions"
    limit: 1
    used: 0
    remaining: 1
  compact_experiment_evidence_references: []
  result: null
  termination: null
  terminal_event: null
  validator_response: null
  closure: null
```

개입 전 상태로 유효한 예시입니다. 출처가 뒷받침된 가설군이 하나뿐이어도 되고, 없는 관찰을 만들어 넣지 않습니다. 다음 개입은 원자적으로 `in_flight_bounded_intervention`으로 옮기고, 종료 관련 필드 다섯 개는 아직 `null`입니다.

## 승인 범위와 제한

승인된 교육용 CTF에만 사용하고, 운영자가 정한 대상, 시간, 계정 범위를 지킵니다. 승인되지 않은 시스템이나 실제 서비스는 제외합니다.

정책은 판단과 보고만 통제하고, 과제별 정답이나 기술 절차는 제공하지 않습니다. 증거가 불완전하거나 검증할 수 없는 환경을 성공이나 실패로 과장하지 않고, 수용은 공식 판정으로 판단합니다. validator와 사용자 대면 확인 표면이 다르면 둘 다 확인합니다.

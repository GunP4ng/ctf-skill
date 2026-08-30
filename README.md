# ctf-skill

`ctf-skill`은 AI 에이전트가 **승인된 CTF 문제를 근거 중심으로 풀도록 돕는
행동 지침**입니다.

문제별 정답이나 exploit을 모아 둔 자료가 아닙니다. 모델이 조사, 실험,
검증, 종료를 올바른 순서로 수행하도록 안내하는 하나의 `SKILL.md`입니다.

실제로 에이전트가 읽는 파일은 다음입니다.

```text
skills/ctf-solving/SKILL.md
```

## 30초 요약

이 스킬은 CTF 풀이를 네 개의 질문으로 정리합니다.

```text
target -> action -> result -> finish
```

1. **Target** — 지금 조사하는 대상이 진짜 문제와 acceptance surface가 맞는가?
2. **Action** — 현재 판단을 바꿀 수 있는 가장 작은 실험은 무엇인가?
3. **Result** — 실제로 무엇이 증명됐고, 누구의 도움을 받았는가?
4. **Finish** — organizer acceptance와 cleanup까지 확인하고 끝냈는가?

읽기 전용 탐색은 자유롭게 할 수 있습니다. 하지만 대상을 바꾸거나, 외부
동작을 실행하거나, 결과를 확정할 때는 이 네 질문을 순서대로 확인합니다.

## 왜 GPT-5.6 Sol의 특성을 기준으로 만들었나

이 구조는 GPT-5.6 Sol을 사용한 실제 CTF 평가에서 반복해서 관찰한 행동을
바탕으로 작성했습니다. 모든 GPT-5.6 Sol 실행이 똑같다는 뜻은 아니며,
모델의 가중치를 변경하거나 성능 향상을 보장하는 것도 아닙니다.

### 관찰한 강점

GPT-5.6 Sol은 다음 작업을 비교적 잘 수행했습니다.

- 파일, binary, source, network response 같은 artifact 조사
- debugger, decompiler, solver, browser 등 여러 도구 사용
- 같은 문제를 수식, 상태 기계, dataflow처럼 다른 표현으로 바꾸기
- mechanism이나 candidate가 주어졌을 때 재현하고 설명하기
- 사용자나 child가 제공한 아이디어를 실제 실행으로 옮기기

### 반복해서 나타난 약점

반면 긴 자율 풀이에서는 다음 문제가 나타났습니다.

- 흥미로운 decoy 가설에 오래 머무름
- 결과가 같은 실험을 도구 이름이나 파라미터만 바꿔 반복함
- 여러 primitive를 찾고도 하나의 end-to-end mechanism으로 연결하지 못함
- child, 사용자, 외부 자료의 기여와 증거 수준을 혼합함
- local success를 실제 organizer acceptance처럼 강하게 해석함
- 정답을 찾고도 acceptance 또는 cleanup을 완료하지 못함
- 지나치게 강한 controller 제약에 막히면 문제 대신 wrapper 우회에 집중함

### 그래서 네 checkpoint를 사용한다

| 관찰된 문제 | 스킬의 대응 |
| --- | --- |
| decoy와 잘못된 target에 과투자 | `Target`에서 대상, 원본, oracle, acceptance surface를 먼저 고정 |
| 정보가 늘지 않는 반복 | `Action`에서 판단을 바꾸는 observable과 가장 싼 discriminator를 요구 |
| primitive는 있지만 mechanism이 없음 | `Result`에서 strongest evidence, candidate, next authority edge를 함께 정리 |
| 외부 도움을 독립 풀이로 오인 | 결과를 `independent` 또는 `assisted`로 명시 |
| local success를 실제 정답으로 오인 | organizer acceptance와 local replay를 분리 |
| 성공 후에도 끝내지 못함 | `Finish`에서 child, mutation, process, credential, 임시 파일 cleanup까지 확인 |

이 규칙은 모델의 생각을 대신하지 않습니다. 모델이 가진 추론 능력을 잘못된
대상, 반복 작업, 증거 혼합, 종료 실수에 낭비하지 않도록 돕습니다.

## 네 checkpoint를 쉽게 이해하기

### 1. Target

먼저 “무엇을 풀고 있는가?”를 고정합니다.

- 승인된 challenge와 범위
- 원본 artifact와 hash
- 조작할 수 있는 입력
- local oracle 또는 validator
- 실제 organizer acceptance surface
- remote endpoint와 실행 환경

예를 들어 local emulator가 성공했다고 해서 remote challenge가 해결된 것은
아닙니다. timeout, 추측, local rejection만으로 target identity를 바꾸지도
않습니다.

공식 write-up, expected flag, answer file 같은 자료는 모델이 자신의 candidate를
봉인하기 전까지 solver context에 넣지 않습니다. 나중에 비교하더라도 candidate
생성이 아니라 검증에만 사용합니다.

### 2. Action

다음에는 현재 판단을 바꿀 수 있는 **하나의 작은 실험**을 고릅니다.

좋은 action은 다음을 설명할 수 있습니다.

- 무엇을 실행하는가?
- 어떤 결과를 예상하는가?
- positive와 negative 결과가 각각 어떤 가설을 바꾸는가?
- 비용과 timeout은 얼마인가?
- 원본 출력은 어디에 보존하는가?
- process, container, submission 같은 stateful side effect가 생기는가?

큰 solver부터 만드는 대신 손으로 만든 모델의 예측 두세 개를 실제 target과
byte-for-byte로 비교하는 식입니다. 결과가 맞지 않으면 search를 확대하기 전에
모델을 고칩니다.

timeout이나 interruption은 실패 증명이 아닙니다. 실행 결과를 모르면
`unknown`으로 보존하고 postcondition을 확인한 뒤에만 재시도합니다.

### 3. Result

실험 뒤에는 관찰한 사실과 해석을 분리합니다.

- 가장 강한 evidence
- evidence가 실제로 증명하는 것
- 현재 candidate 또는 candidate set
- 아직 빠진 mechanism edge
- 다음 acceptance 또는 authority 단계

최종 결과 표현은 다음 네 가지입니다.

| 결과 | 의미 |
| --- | --- |
| `solved` | 실제 organizer acceptance가 있고, 가능한 경우 mechanism을 재현함 |
| `failed-with-valid-oracle` | 유효한 oracle이 남은 candidate를 거부함 |
| `partial` | target과 관련된 사실은 증명했지만 acceptance가 없음 |
| `no-result` | 유용한 target fact를 확보하지 못함 |

또한 결과를 `independent` 또는 `assisted`로 기록합니다. 사용자나 외부 agent가
mechanism, exploit chain, solver, candidate를 제공했다면 그 기여를 숨기지
않습니다.

### 4. Finish

마지막에는 결과와 실제 상태가 모두 일치하는지 확인합니다.

- organizer response가 기록됐는가?
- child가 완료, 취소 또는 disposition됐는가?
- mutation 결과가 정산됐는가?
- process와 container가 종료됐는가?
- credential과 임시 artifact가 정리됐는가?
- cleanup receipt가 남았는가?

알 수 없는 mutation 결과는 cleanup으로 간주하지 않습니다. 모델 내부의 시간이나
token 제한도 신뢰된 CTF 예산이 아니므로 `budget-stop`의 근거가 될 수 없습니다.

## Skill과 harness의 역할은 다르다

이 저장소는 **모델 행동 정책**만 제공합니다.

- 어떤 가설을 먼저 볼지
- 어떤 실험이 정보를 늘리는지
- 언제 representation을 바꿀지
- evidence와 acceptance를 어떻게 구분할지
- 결과와 기여를 어떻게 표현할지

session identity, mutation journal, evidence 저장, terminal authority, process cleanup
같은 결정적 강제는 `oh-my-ctf` harness가 담당합니다.

같은 reasoning policy를 skill과 runtime 양쪽에서 중복 강제하지 않는 것이
중요합니다. Skill은 올바른 행동을 설명하고, harness는 거짓 성공이나 중복
side effect처럼 절대 허용할 수 없는 경계만 막습니다.

## 지원 분야

문제 제목이 아니라 실제 artifact와 runtime behavior를 보고 분야를 정합니다.

- Crypto
- Forensics
- Pwn
- Reverse engineering
- Web
- Misc

각 분야의 최소 관찰 순서는 `SKILL.md`에 있습니다. Reverse engineering에서
Ghidra는 `analyzeHeadless` 또는 pyghidra headless로만 사용합니다.

## 설치

저장소를 내려받습니다.

```bash
git clone https://github.com/GunP4ng/ctf-skill.git
cd ctf-skill
git checkout --detach v0.7.1
```

사용하는 AI agent의 skill 디렉터리에 다음 파일을 등록합니다.

```text
skills/ctf-solving/SKILL.md
```

예를 들어 agent가 `ctf-solving/SKILL.md` 구조를 요구한다면 해당 위치로
복사하거나 저장소의 파일을 직접 읽도록 설정합니다. 정확한 등록 방법은
사용하는 agent의 skill 문서를 따르세요.

## 파일 구성

```text
ctf-skill/
├── README.md
├── CHANGELOG.md
├── skills/
│   └── ctf-solving/
│       └── SKILL.md
└── tests/
    └── test_checkpoint_contract.py
```

## 검증

```bash
uv run --with pytest pytest -q
```

이 테스트는 machine-consumed checkpoint contract와 핵심 정책 표현을
검사합니다.

실제 CTF 성능은 unit test만으로 판단하지 않습니다. 승인된 target에서 원본
evidence, local replay, organizer acceptance, attribution, cleanup을 함께
평가해야 합니다.

## 버전과 한계

현재 release는 `ctf-skill v0.7.1`입니다.

이 스킬은 다음을 하지 않습니다.

- 모델 가중치 변경
- 문제별 정답이나 exploit 제공
- 독립 solve 성능 향상 보장
- local success를 실제 acceptance로 승격
- 외부 도움을 숨긴 독립 풀이 주장

테스트 통과는 정책 구조와 문서가 일치한다는 뜻입니다. GPT-5.6 Sol의 CTF
성능이 인과적으로 향상됐다는 뜻은 아닙니다. 그 주장은 숨겨진 정답 경계를
유지한 실제 고정 cohort 평가로 별도 검증해야 합니다.

## 사용 범위

승인된 교육용 CTF에서만 사용하세요. 운영자가 정한 대상, 계정, 시간,
submission 범위를 지켜야 합니다.

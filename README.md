# ctf-skill

`ctf-skill`은 GPT-5.6 Sol이 승인된 CTF를 풀 때 **잘하는 분석은 살리고,
반복해서 나타나는 풀이 실패는 줄이기 위한 행동 지침**입니다.

문제별 정답이나 exploit 모음이 아닙니다. 모델이 실제로 읽는 파일은
다음 하나입니다.

```text
skills/ctf-solving/SKILL.md
```

## 왜 이 스킬이 필요한가

GPT-5.6 Sol은 CTF에서 강한 도구 사용자입니다. 하지만 도구를 잘 쓰는 것과
긴 풀이를 끝까지 올바르게 운영하는 것은 다른 문제입니다.

실제 CTF 평가에서 다음 특성이 반복해서 관찰됐습니다.

| 관찰된 특성 | 풀이에 주는 영향 |
| --- | --- |
| artifact, source, binary를 빠르게 조사함 | 초반 사실 수집이 빠름 |
| debugger, decompiler, solver, browser를 잘 사용함 | 적절한 도구가 정해지면 깊게 분석함 |
| 수식, 상태 기계, dataflow로 representation을 바꿀 수 있음 | 올바른 관점을 찾으면 문제를 크게 단순화함 |
| mechanism이나 candidate가 주어지면 replay를 잘함 | 해결 경로가 보인 뒤 검증과 설명이 강함 |
| 흥미로운 초기 가설이나 decoy에 오래 머무름 | 값비싼 분석이 실제 정답과 멀어질 수 있음 |
| 새 정보가 없는 실험을 이름만 바꿔 반복함 | 시간이 늘어도 frontier가 줄지 않음 |
| 여러 primitive를 찾고도 하나의 mechanism으로 연결하지 못함 | 부분 성과는 많지만 flag까지 가지 못함 |
| child, 사용자, 외부 자료의 기여를 혼합함 | evidence와 attribution이 부정확해짐 |
| local success를 실제 acceptance처럼 해석함 | 검증되지 않은 candidate를 solved로 오인함 |
| candidate 뒤 acceptance와 cleanup을 빠뜨림 | 정답을 찾고도 완결된 solve가 되지 않음 |

이 스킬은 모델의 지능이나 가중치를 바꾸지 않습니다. 대신 모델이 이미 가진
분석 능력을 **정확한 target, 정보가 늘어나는 action, 검증된 result,
완결된 finish**에 사용하도록 풀이 순서를 개선합니다.

## 어떻게 개선하는가

스킬은 전체 풀이를 네 checkpoint로 정리합니다.

```text
target -> action -> result -> finish
```

| Checkpoint | 줄이려는 실패 | 모델이 확인할 질문 |
| --- | --- | --- |
| **Target** | decoy, wrong target, hidden answer leakage | 지금 보는 artifact와 acceptance surface가 진짜 대상인가? |
| **Action** | no-information 반복, 과도한 search | 이 한 번의 실험이 어떤 판단을 바꾸는가? |
| **Result** | primitive/mechanism 단절, evidence 혼합 | 무엇이 증명됐고 다음 missing edge는 무엇인가? |
| **Finish** | false solved, acceptance·cleanup 누락 | 실제 응답과 모든 resource 상태가 결론과 일치하는가? |

### 개선 전과 후

예를 들어 binary challenge에서 crash를 하나 찾았다고 가정합니다.

**Checkpoint가 없을 때**

```text
crash 발견
-> 비슷한 fuzzing 반복
-> debugger에서 여러 address 수집
-> local shell 한 번 성공
-> solved라고 보고
```

**Checkpoint를 사용할 때**

```text
Target: exact binary, wrapper, remote acceptance를 고정
Action: crash가 RIP control인지 구분하는 최소 입력 실행
Result: primitive와 아직 빠진 exploit edge를 분리
Finish: fresh wrapper replay, organizer acceptance, process cleanup 확인
```

두 번째 흐름은 도구 사용을 줄이기 위한 것이 아닙니다. **도구 결과가 다음
결정을 실제로 바꾸도록 만드는 것**이 목적입니다.

## 1. Target: 올바른 문제에 집중한다

먼저 다음을 고정합니다.

- 승인된 challenge와 scope
- 원본 artifact와 hash
- 조작 가능한 입력
- local oracle 또는 validator
- remote endpoint
- 실제 organizer acceptance surface

공식 write-up, expected flag, answer file은 모델이 자기 candidate를 봉인하기
전까지 보여 주지 않습니다. 나중에 비교하더라도 candidate를 만드는 힌트가
아니라 독립 검증 자료로만 사용합니다.

이 단계는 강한 artifact 분석 능력이 decoy나 잘못된 target에 낭비되는 것을
막습니다.

## 2. Action: 정보가 늘어나는 실험을 고른다

다음 action은 한 문장으로 설명할 수 있어야 합니다.

```text
이 결과가 나오면 A를 유지하고, 저 결과가 나오면 A를 버린다.
```

좋은 action은 다음을 포함합니다.

- exact target과 command
- 예상 observable
- positive/negative 결과의 의미
- 비용과 timeout
- raw output 보존 위치
- process, container, submission 같은 side effect

도구 이름, prompt, parameter만 바꿨는데 같은 판단이 남는다면 새로운 실험이
아닙니다. Materially different observation이나 representation으로 바꿉니다.

이 단계는 GPT-5.6 Sol의 tool-use 강점을 유지하면서 no-information 반복을
줄입니다.

## 3. Result: primitive를 mechanism으로 연결한다

실험 뒤에는 다음을 함께 기록합니다.

- strongest evidence
- evidence가 실제로 증명하는 사실
- 현재 candidate 또는 lossless candidate set
- 확보한 primitive
- 아직 빠진 mechanism edge
- 다음 acceptance 또는 authority 단계

Child나 사용자가 제공한 mechanism, exploit, solver, candidate는 출처를
남깁니다. 핵심 외부 기여가 있었다면 결과는 `assisted`입니다.

Local emulator나 patched binary의 성공은 중요한 evidence지만 organizer
acceptance는 아닙니다.

최종 결과는 다음 중 하나만 사용합니다.

| 결과 | 의미 |
| --- | --- |
| `solved` | organizer acceptance가 있고 가능한 mechanism replay가 있음 |
| `failed-with-valid-oracle` | 유효한 oracle이 남은 candidate를 거부함 |
| `partial` | target 관련 사실은 증명했지만 acceptance가 없음 |
| `no-result` | 유용한 target fact를 확보하지 못함 |

이 단계는 흩어진 primitive를 end-to-end mechanism과 acceptance로 연결합니다.

## 4. Finish: 정답을 실제 완료로 만든다

종료 전에 확인합니다.

- exact target과 candidate가 acceptance receipt와 일치하는가?
- child가 완료, 취소 또는 disposition됐는가?
- mutation 결과가 정산됐는가?
- process와 container가 종료됐는가?
- credential과 임시 artifact가 정리됐는가?
- cleanup receipt가 남았는가?

Timeout이나 interruption 뒤 결과를 모르는 mutation은 성공이나 실패로
추측하지 않습니다. Postcondition을 확인하기 전에는 재실행하지 않습니다.

이 단계는 candidate를 찾은 뒤 acceptance와 cleanup을 빠뜨리는 실패를
줄입니다.

## Skill이 하는 일과 하지 않는 일

### 하는 일

- 모델이 확인할 reasoning 순서를 제공
- evidence와 inference를 분리
- 다음 action을 bounded discriminator로 압축
- local replay와 organizer acceptance를 구분
- independent/assisted attribution을 보존
- finish 조건에 cleanup을 포함

### 하지 않는 일

- 모델 가중치 변경
- 문제별 정답이나 exploit 제공
- 도구 실행을 deterministic하게 강제
- session, mutation, process를 직접 관리
- solve count 향상을 보장

Trusted activation, mutation journal, terminal authority, process cleanup처럼
반드시 강제돼야 하는 invariant는 `oh-my-ctf` harness가 담당합니다.

Reasoning policy는 skill에, fail-closed correctness는 harness에 두어 같은
행동 규칙을 두 곳에서 중복 강제하지 않습니다.

## 지원 분야

문제 제목이 아니라 실제 artifact와 runtime behavior를 보고 분야를 정합니다.

- Crypto
- Forensics
- Pwn
- Reverse engineering
- Web
- Misc

분야별 최소 관찰 순서는 `SKILL.md`에 있습니다. Reverse engineering에서
Ghidra는 `analyzeHeadless` 또는 pyghidra headless로만 사용합니다.

## 설치

```bash
git clone https://github.com/GunP4ng/ctf-skill.git
cd ctf-skill
git checkout --detach v0.7.2
```

사용하는 AI agent가 읽는 skill 경로에 다음 파일을 등록합니다.

```text
skills/ctf-solving/SKILL.md
```

정확한 등록 방법은 해당 agent의 skill 문서를 따르세요.

## 검증

```bash
uv run --with pytest pytest -q
```

이 테스트는 machine-consumed checkpoint contract와 핵심 정책 경계를
검사합니다.

실제 모델 개선은 unit test나 solve count 하나로 주장하지 않습니다. 승인된
challenge, hidden official-reference boundary, exact model과 thinking level,
원본 evidence, organizer acceptance, attribution, cleanup을 함께 기록한
평가가 필요합니다.

## 버전과 범위

현재 release는 `ctf-skill v0.7.2`입니다.

승인된 교육용 CTF에서만 사용하세요. 운영자가 정한 target, account, time,
submission 범위를 지켜야 합니다.

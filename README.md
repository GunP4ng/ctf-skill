# ctf-skill

`ctf-skill`은 승인된 교육용 CTF를 AI 에이전트와 함께 풀 때 사용하는 진행
정책입니다. 배포 파일과 모델 동작의 유일한 정책 원본은
`skills/ctf-solving/SKILL.md`입니다.

## GPT-5.6 Sol의 반복 특성을 기반으로 한 개선

주요 control은 `openai-codex/gpt-5.6-sol`을 medium/high thinking으로 실제
CTF에 반복 적용하며 관찰한 강점과 실패 양상에 대응해 보강했습니다.

반복해서 확인된 강점은 정확한 target 고정, 서로 다른 가설의 초기 전개,
국소적인 representation pivot, 그리고 authoritative acceptance가 없을 때
`solved`를 주장하지 않는 태도였습니다. 반면 기술적으로 의미 있는 단서를
찾고도 같은 semantic lane을 오래 반복하거나, root가 evidence와 child 결과를
정산하지 못한 채 review와 terminal closure까지 연결하지 못하는 경향도
지속적으로 나타났습니다.

| 반복적으로 나타난 모델 특성 | 관찰된 실패 양상 | `ctf-skill`의 개선 |
|---|---|---|
| 초기에 target과 acceptance 경계를 잘 고정하지만 긴 풀이 뒤에는 현재 authority edge를 잃기 쉽습니다. | local crash, decode, replay, primitive를 얻고도 proven capability, acceptance gap, 다음 검증 단계를 하나의 closure로 연결하지 못했습니다. | 매 decision-changing intervention 뒤 원래 target, local oracle, 실제 acceptance surface, candidate, strongest evidence, proven capability, next authority edge를 **Authority Closure Checkpoint**에 보존합니다. |
| 유망한 기술 lane을 깊게 파는 능력은 좋지만, 의미가 같은 실패를 도구·backend·prompt·parameter만 바꾸어 반복합니다. | solver `unknown`, timeout, child lane 교체가 새 정보처럼 취급되어 context와 실행 예산을 쓰고도 candidate, contradiction, bound, observable이 늘지 않았습니다. | modeled state, decomposition, unknown, observable predicate가 같은 결과를 하나의 no-information fingerprint로 묶습니다. 두 번 뒤에는 새 evidence, material representation pivot 또는 frontier audit 없이는 세 번째 equivalent intervention이나 terminal transition을 금지합니다. |
| 손으로 유도한 모델을 빠르게 자동화하지만, primitive semantics 검증보다 큰 search를 먼저 신뢰하는 경우가 있습니다. | 한 CCE `.NET` 사례에서는 opcode 의미를 잘못 모델링한 채 여섯 solver가 장시간 실행됐습니다. operator가 3분간 silent한 solver를 중단하고 접근을 바꾸게 한 뒤에야 모델을 다시 대조해 오류를 찾아 해결했습니다. | 큰 solver·full-state search 전에 target 예측 2~3개를 byte 단위로 differential-test합니다. 유용한 결과가 없는 solver는 기본 180초에 중단하고, compute 확장보다 **모델 의미론의 오인코딩**을 먼저 의심해 primitive behavior부터 재유도합니다. |
| 병렬 child로 탐색 폭을 넓히지만 root 통합은 상대적으로 약합니다. | 완료된 child를 다시 조회하거나, 실패한 child를 unresolved로 남기고, decision-changing claim을 root에서 재현·disposition하지 못했습니다. | 각 child를 exact evidence reference와 family에 결속해 root가 `accepted`, `rejected`, `pending`으로 disposition합니다. decision-changing 주장은 root 재현 전까지 advisory이며, 동일 no-progress wave는 하나로 합치고 취소 전 durable handoff를 남깁니다. |
| 유용한 decode나 구조를 찾으면 이를 progress로 표현하려는 경향이 있습니다. | target decision을 바꾸지 않는 배경 decode, 새 label, 구현 변경이 material pivot 또는 `partial`로 과대평가될 수 있었습니다. | representation progress는 source evidence, 재현 가능한 transform, observed output, 새로 보이는 property가 capability·prerequisite coverage·candidate·contradiction·bound·next decision 중 하나를 바꿀 때만 인정합니다. |
| controller 제한이나 자체 추정치를 풀이 예산처럼 해석해 종료 근거로 삼기도 합니다. | authoritative budget이 없는데도 `budget-stop` 또는 affordability 결론을 만들면서 아직 가능한 discriminator가 닫혔습니다. | budget은 user, organizer, authoritative target이 unit·limit·provenance를 선언한 경우에만 존재합니다. controller quota, elapsed time, evaluator cap, model estimate는 종료 authority가 될 수 없습니다. |
| review 필요성을 말로는 인식하지만 실제 전환과 후속 replay가 누락됩니다. | 반복 stall 뒤에도 equivalent local lane을 계속하거나 review를 제안만 하고 packet lifecycle, root replay, acceptance로 이어가지 못했습니다. | 같은 fingerprint의 no-information round가 두 번 끝나고, justified discriminator와 viable material pivot이 없으며, 이전 review proposal도 미검증 상태로 남아 있지 않을 때 모든 관련 child를 먼저 정산합니다. 그 뒤 다음 equivalent 시도보다 `ctf-review`를 우선하며, 응답은 advisory로 유지하고 root replay와 실제 acceptance를 다시 요구합니다. |
| unsupported solve를 피하는 규율은 비교적 강하지만, local success와 authoritative solve의 간극이 큽니다. | 실제 반복 평가에서는 유용한 partial evidence가 있어도 candidate, replay, authoritative acceptance, cleanup을 모두 갖춘 model-owned closure가 드물었습니다. | `partial`은 capability·prerequisite coverage·candidate·contradiction·bound·next decision을 바꾸는 target-relevant proven fact와 acceptance 부재를 요구합니다. `solved`는 authoritative acceptance와 가능한 경우 clean replayable mechanism을 요구하며, one-shot surface는 exact pinned invocation과 acceptance receipt를 보존합니다. root-owned verifier가 public format candidate를 만들고 두 번째 run이 재현하면 추가 탐색을 멈추고 replay, acceptance, cleanup, terminal proposal 순으로 closure를 완결합니다. |

이 개선은 **GPT-5.6 Sol 자체의 solve rate가 인과적으로 향상됐다는 주장**이
아닙니다. 고정 4-domain 평가에서는 localized hypothesis·representation
개선이 있었지만 accepted candidate는 0/4였습니다. 위 내용은 반복 관찰된
모델 특성을 policy control로 변환한 설계 근거이며, 실제 모델 개선은 별도의
명시적으로 승인된 controlled comparative evaluation과 authoritative
acceptance로만 판단합니다.

이 절은 현재 정책의 설계 근거와 동작 개요입니다. 정확한 판단 순서, 필드,
예외와 종료 조건은 항상 `skills/ctf-solving/SKILL.md`를 따릅니다.

## 직접 CTF 풀이로 평가

이 저장소는 미리 정한 응답을 비교하거나 점수화하는 평가 도구를 제공하지
않습니다. 평가는 승인된 실제 CTF 대상에서 직접 수행합니다.

1. 실제 문제 파일, 서비스, 계정 범위, 또는 대회 환경을 대상으로 풀이합니다.
2. 관찰한 원본 자료와 실행 결과를 보존합니다.
3. 로컬 재현 뒤 실제 제출 또는 공식 검증 창구의 결과를 확인합니다.
4. 확인된 산출물과 공식 결과를 바탕으로 풀이 과정을 평가합니다.

로컬 대체물의 성공은 실제 정답이 아닙니다. 풀이 중에는 organizer/reference
solutions, expected flags/results, and official solution material을 solver context
밖에 유지합니다. candidate sealing 뒤에만 authoritative validation을 수행합니다.
직접 풀이의 상세한 작업 규칙과 종료 조건은 `skills/ctf-solving/SKILL.md`를
따릅니다.

## 출처와 동기화

`ctf-skill`은 범용 CTF 풀이 정책의 source of truth이고, `oh-my-ctf`는
`skills/ctf-solving/SKILL.md`를 byte-identical로 import합니다. `oh-my-ctf`
runtime은 deterministic integration을 소유합니다. 각 producer release 뒤에는
새 SKILL bytes 기준으로 consumer bundle, provenance, package-manifest hashes를
refresh해야 합니다.

## 설치

1. 저장소를 내려받습니다.
2. `skills/ctf-solving/SKILL.md`를 사용하는 에이전트의 스킬 디렉터리 아래
   `ctf-solving/SKILL.md`로 복사합니다.

복사 대신 에이전트가 저장소의 파일을 직접 읽도록 설정해도 됩니다. 스킬
디렉터리의 정확한 위치는 사용하는 에이전트 문서를 따르세요.

## 파일 구성

```text
ctf-skill/
├── CHANGELOG.md
├── README.md
└── skills/
    └── ctf-solving/
        └── SKILL.md
```

## 사용 범위

승인된 교육용 CTF에서만 사용합니다. 운영자가 정한 대상, 시간, 계정 범위를
지켜야 합니다. 이 스킬은 문제별 정답이나 공격 절차를 제공하지 않습니다.

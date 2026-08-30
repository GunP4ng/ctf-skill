# ctf-skill

`ctf-skill`은 승인된 교육용 CTF를 푸는 AI agent를 위한 정책입니다. 실제로
agent가 읽는 파일은 `skills/ctf-solving/SKILL.md`입니다. 이 README는 정책의
의도와 설치 방법을 간단히 설명합니다.

## v0.7.0: 모델이 소유하는 네 점검 지점

v0.7.0은 장황한 실행 단계와 반복 횟수 규칙을 네 개의 순서 있는 점검 지점으로
바꿨습니다. `SKILL.md`의 machine-consumed frontmatter는 다음 계약을 제공합니다.

```text
target -> action -> result -> finish
```

모델은 각 점검 지점에서 근거와 다음 한 가지 제한된 동작을 직접 관리합니다.
읽기 전용 탐색은 유연하게 할 수 있지만, 외부 동작이나 최종 주장을 바꾸는 일은
이 순서를 따라야 합니다.

1. **Target** - 승인된 대상, 범위, 원본 자료, local oracle, 실제 organizer
   acceptance surface를 고정합니다. 공식 풀이, 예상 flag, 답 파일은 모델이 만든
   후보를 봉인하기 전까지 보여 주지 않습니다. CTF 예산은 사용자·운영자·권위 있는
   대상이 단위, 한도, 출처를 함께 선언한 경우에만 사용합니다.
2. **Action** - 판단을 바꿀 수 있는 가장 작은 동작 하나를 고르고 원본 출력과
   실제 결과를 보존합니다. mutation은 실행 전 in-flight로 기록하고 영구 영수증으로
   한 번만 정산합니다. 중단이나 timeout으로 결과를 모르면 재실행하지 않고 먼저
   그 상태를 확인합니다. 제출과 다른 external write는 정확한 대상과 범위에 대한
   명시적 사용자 또는 운영자 권한이 있어야 합니다.
3. **Result** - local emulator나 재현 결과와 organizer acceptance를 구분합니다.
   후보는 root가 두 번 독립적으로 재현한 뒤 봉인하고 실제 acceptance surface에서
   확인합니다. 결과는 `solved`, `failed-with-valid-oracle`, `partial`, `no-result`
   중 관찰한 근거가 뒷받침하는 하나만 사용하며, 외부 도움이나 사용자의 핵심 기여는
   `assisted`로 정확히 기록합니다.
4. **Finish** - child, mutation, process, container, credential, 임시 파일을 정리한
   영수증을 남긴 뒤에만 종료 상태를 고정합니다. 내부 시간이나 token 제한은
   `budget-stop`의 근거가 될 수 없습니다.

분야는 문제 제목이 아니라 관찰한 artifact와 runtime surface로 라우팅합니다.
Crypto, Forensics, Pwn, Reverse engineering, Web, Misc 각각의 최소 관찰 순서는
정책에 있습니다. Reverse engineering에서 Ghidra는 `analyzeHeadless` 또는
pyghidra headless로만 사용하며 GUI는 사용하지 않습니다.

## 실제 CTF 평가

이 정책은 미리 작성한 답변 문장을 비교하는 방식으로 평가하지 않습니다. 승인된
실제 CTF 대상에서 원본 관찰과 실행 결과를 보존하고, 가능한 경우 local replay 뒤
organizer acceptance surface를 확인합니다. local success는 실제 정답이 아닙니다.

## 설치

1. 저장소를 내려받습니다.

   ```bash
   git clone https://github.com/GunP4ng/ctf-skill.git
   cd ctf-skill
   ```

2. 사용하는 agent의 skill 디렉터리에
   `skills/ctf-solving/SKILL.md`를 `ctf-solving/SKILL.md`로 복사하거나, 해당
   파일을 직접 읽도록 설정합니다.

정확한 skill 경로와 활성화 방식은 사용하는 agent의 문서를 따르세요.

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

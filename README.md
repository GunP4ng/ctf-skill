# ctf-skill

`ctf-skill`은 승인된 교육용 CTF를 AI 에이전트와 함께 풀 때 사용하는 진행
정책입니다. 배포 파일과 모델 동작의 유일한 정책 원본은
`skills/ctf-solving/SKILL.md`입니다.

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
├── README.md
└── skills/
    └── ctf-solving/
        └── SKILL.md
```

## 사용 범위

승인된 교육용 CTF에서만 사용합니다. 운영자가 정한 대상, 시간, 계정 범위를
지켜야 합니다. 이 스킬은 문제별 정답이나 공격 절차를 제공하지 않습니다.

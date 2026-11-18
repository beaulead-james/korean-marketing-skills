# 루틴: 브랜드 건강 점검

**호출:** 로컬 브랜드 메모리 점검과 `_system/scripts/refresh_check.py` (비대화형, 질문 0).
**주기:** 매월 1일 08:00. 성과 리뷰가 읽기 전에 낡은 입력을 드러내요.

## 하는 일

건강 점검은 살펴보는 파일을 바꾸지 않고 로컬 브랜드 메모리를 감사해요. 매니페스트 무결성, 프로필 나이, TTL 헤더, 없는 에셋 경로, 조용한 캠페인을 봐요. 보고서는 영향 범위 순으로 주의를 정렬하고, 낡은 입력을 새로 고칠 스킬을 가리켜요. 건강한 브랜드는 불린 출력 대신 짧은 보고서를 받아요.

## /schedule 프롬프트

마케팅 워크스페이스에서 `/schedule`을 실행하고 붙여 넣어요.

```
Schedule: monthly, on the 1st at 08:00 (my timezone).

Task: 로컬, 비대화형 브랜드 건강 점검을 실행한다. 질문은 0. 활성 브랜드 디렉터리를 풀고, 없으면 ./brand/를 쓴다. brand.yaml, 나열된 프로필 파일, updated 날짜와 mtime, assets.md, learnings.md, 활성 캠페인 항목을 읽는다. 매니페스트 드리프트를 확인하고 프로필 파일을 FRESH, AGING, STALE, UNVERIFIED로 분류한다. <skills-pack-path>는 _system/scripts/refresh_check.py가 있는 디렉터리로 푼다. 존재하는 경로마다 실행한다. python3 <skills-pack-path>/_system/scripts/refresh_check.py ./brand/algo-cache.md <skills-pack-path>/skills/creative/references/MODEL_REGISTRY.md <skills-pack-path>/skills/*/references/*-facts.md. 없는 경로는 건너뛰고, 헤더가 없거나 파싱되지 않으면 UNVERIFIED로 보고하고, 신선도 출력을 새로 고침 없이 보고서에 복사한다. ./campaigns/brand-health/<YYYY-MM-DD>.md에 상태 표, 신선도 출력, 정리 신호, 영향 범위 순의 새로 고침 제안 1개에서 5개를 쓴다. ./brand/assets.md에 한 줄을 덧붙인다. 브랜드 메모리가 없으면 /start-here를 먼저 돌려야 한다고 적은 날짜 보고서를 쓰고 멈춘다. learnings.md를 쓰거나 감사한 파일을 수정하지 않는다. 제안 항목은 보고서 안에만 초안한다. 보고서만. 게시, 발송, 배포, 지출, 제3자 계정 변경은 하지 않는다.
```

## 모든 클라이언트 (대행사)

같은 프롬프트의 첫 줄을 이것으로 바꿔요. `./brands/ 아래 brand.yaml이 있는 각 클라이언트 디렉터리를 그 실행의 활성으로 두고 다음을 한다. 쓰기는 그 클라이언트의 폴더에만. 끝나면 클라이언트마다 롤업 한 줄.`
대상 클라이언트를 나열하려면 `route.py --all-brands --goal unsure`를 써요.

## 로컬 cron

```cron
0 8 1 * * cd /path/to/workspace && claude -p "Run local brand-memory checks and refresh_check.py on existing cache and fact paths, write the dated freshness report and an assets row, do not refresh or alter audited files, draft proposed learnings only, and never publish." --allowedTools "Read,Write,WebFetch,WebSearch"
```

## 클라우드 주의

클라우드 루틴은 저장소의 새 클론에서 돌아요. 그 저장소에 커밋된 스킬 (`.claude/skills/`)만 보고, 내 기계의 플러그인 설치는 보지 않아요. 클라우드로 돌리려면 스킬 폴더를 워크스페이스 저장소에 먼저 커밋하세요.

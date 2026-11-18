# 루틴: 월간 성과 리뷰

**호출:** `/performance-review` **MONTHLY** (비대화형, 질문 0).
**주기:** 매월 2일 08:00. 전월 데이터가 비교 전에 자리를 잡을 시간이에요.

## 하는 일

리뷰는 설정된 모든 읽기 전용 소스에서 직전 달력 월과 그 앞달을 모아요. 지금 병목을 찾고, 지난 보고서의 추천과 실제로 한 일을 비교하고, 다음 행동을 증거로 순위 매겨요. 부분 커버리지는 보이게 둬요. 이 루틴만 예정된 실행에서 증거 조건을 통과한 프라이어를 `learnings.md`에 덧붙일 수 있어요. 제품의 단일 작성자 규칙을 지켜요. 데이터 소스가 없으면, 없음을 결과로 다루지 않고 필요한 키나 내보내기의 이름을 말해요.

지역 사업이면 전화 대장, 예약, 스마트콜을 분모로 봐요. 네이버 검색광고, 플레이스, 메타, 구글의 전환 주장은 그 분모와 맞춰 보기 전에 성과로 치지 않아요. 네이버와 구글 검색을 한 시장처럼 섞지 마세요.

## /schedule 프롬프트

마케팅 워크스페이스에서 `/schedule`을 실행하고 붙여 넣어요.

```
Schedule: monthly, on the 2nd at 08:00 (my timezone).

Task: skills/performance-review/SKILL.md가 정의한 MONTHLY 모드로 /performance-review를 실행한다.
비대화형이다. 질문은 0이고 모드 기본값을 쓴다. 설정된 모든 읽기 전용 소스에서 직전 달력 월과 그 앞달을 읽고, 최신 ./campaigns/performance/ 보고서, assets.md, 관련 learnings.md, brand.yaml, 있으면 keyword-plan.md를 읽는다. 전화 대장, 예약, 스마트콜이 있으면 채널 주장의 분모로 쓴다. GET 또는 report-query 엔드포인트만 쓴다. 연결된 서비스를 바꾸지 않는다. ./campaigns/performance/<YYYY-MM>.md에 커버리지, 병목, 전월 대비 변화, 실행한 추천과 실행하지 않은 추천, 스킬로 연결되는 증거 기반 다음 행동 3개에서 5개를 쓴다. n=과 source:가 있는 항목만 ./brand/learnings.md에 덧붙이고, 데이터가 뒷받침하는 matched ad-matrix.json 결과와 assets.md 상태를 갱신한다. ./brand/assets.md에 보고서 한 줄을 덧붙인다. 설정된 소스가 없으면 필요한 키나 내보내기를 정확히 적은 날짜 보고서를 쓰고 멈춘다. 보고서, 증거가 있는 로컬 프라이어, 로컬 장부만. 게시, 발송, 배포, 지출, 제3자 계정 변경은 하지 않는다.
```

## 모든 클라이언트 (대행사)

같은 프롬프트의 첫 줄을 이것으로 바꿔요. `./brands/ 아래 brand.yaml이 있는 각 클라이언트 디렉터리를 그 실행의 활성으로 두고 다음을 한다. 쓰기는 그 클라이언트의 폴더에만. 끝나면 클라이언트마다 롤업 한 줄.`
대상 클라이언트를 나열하려면 `route.py --all-brands --goal convert`를 써요.

## 로컬 cron

```cron
0 8 2 * * cd /path/to/workspace && claude -p "Run /performance-review in MONTHLY mode using read-only sources, write the prior-month report, append only n=/source-qualified priors and matched local bookkeeping, add an assets row, and never publish or change a connected service." --allowedTools "Read,Write,WebFetch,WebSearch"
```

## 클라우드 주의

클라우드 루틴은 저장소의 새 클론에서 돌아요. 그 저장소에 커밋된 스킬 (`.claude/skills/`)만 보고, 내 기계의 플러그인 설치는 보지 않아요. 클라우드로 돌리려면 스킬 폴더를 워크스페이스 저장소에 먼저 커밋하세요.

# 루틴: 주간 콘텐츠 의식

**호출:** `/newsletter` **Edition**, 그리고 `/social-content` **CADENCE** (비대화형, 질문 0).
**주기:** 매주 금요일 06:00. 다음 발행 창 전에 사람이 검토할 초안이 준비돼요.

## 하는 일

이 루틴은 이번 주 실제 작업을 뉴스레터 초안과 네이티브 소셜 계획으로 바꿔요. 예정된 실행이 주제를 지어내게 하지 않고, 에셋 대장, 최근 learnings, 새 캠페인 파일에서 재료를 가져와요. 모든 산출물의 첫 줄은 `DRAFT. 사람 검토 필요`예요. 포맷이나 소셜 캐논이 없으면 그 절반만 설정 필요 스텁을 만들고, 다른 절반은 끝날 수 있어요.

한국 채널이 기본이에요. 뉴스레터를 카카오 채널이나 문자로 보낼 문안은 광고성이면 (광고), 보내는 이, 수신거부를 포함해요. 블로그 체험단 소재는 대가성 표시가 필요해요. 자동 발송과 자동 게시는 없어요.

## /schedule 프롬프트

마케팅 워크스페이스에서 `/schedule`을 실행하고 붙여 넣어요.

```
Schedule: every Friday at 06:00 (my timezone).

Task: 비대화형 콘텐츠 실행이다. 질문은 0. 모든 출력의 첫 줄에 “DRAFT. 사람 검토 필요”를 적는다. 최근 7일의 ./brand/assets.md, 관련 learnings.md, ./campaigns/의 새 파일, voice-profile.md, 있으면 뉴스레터 포맷과 소셜 캐논을 읽는다. /newsletter를 Edition 모드로 실행한다. 검증된 재료 중 가장 강한 것으로 ./campaigns/newsletters/<YYYY-MM-DD>-<topic-slug>.md를 쓰거나, 포맷이 없으면 <YYYY-MM-DD>-SETUP-NEEDED.md를 쓴다. /social-content를 CADENCE 모드로 실행한다. 서로 다른 증거 기반 초안 3개에서 5개를 ./campaigns/social/<YYYY>-W<ww>.md에 쓰거나, 캐논이 없으면 같은 SETUP-NEEDED 보고서를 쓴다. 약한 재료를 불리지 않는다. 파일마다 ./brand/assets.md에 한 줄을 덧붙인다. learnings.md는 쓰지 않는다. 가능한 항목은 해당 보고서에만 초안한다. 초안과 보고서만. 발송, 예약, 게시, 업로드, 배포는 하지 않는다. 광고성 문안에는 (광고), 보내는 이, 수신거부를 넣는다.
```

## 모든 클라이언트 (대행사)

같은 프롬프트의 첫 줄을 이것으로 바꿔요. `./brands/ 아래 brand.yaml이 있는 각 클라이언트 디렉터리를 그 실행의 활성으로 두고 다음을 한다. 쓰기는 그 클라이언트의 폴더에만. 끝나면 클라이언트마다 롤업 한 줄.`
대상 클라이언트를 나열하려면 `route.py --all-brands --goal authority`를 써요.

## 로컬 cron

```cron
0 6 * * 5 cd /path/to/workspace && claude -p "Run the non-interactive newsletter Edition and social-content CADENCE ritual from this week's real assets; write human-review drafts or setup-needed stubs, append each asset row, draft proposed learnings only, and never publish." --allowedTools "Read,Write,WebFetch,WebSearch"
```

## 클라우드 주의

클라우드 루틴은 저장소의 새 클론에서 돌아요. 그 저장소에 커밋된 스킬 (`.claude/skills/`)만 보고, 내 기계의 플러그인 설치는 보지 않아요. 클라우드로 돌리려면 스킬 폴더를 워크스페이스 저장소에 먼저 커밋하세요.

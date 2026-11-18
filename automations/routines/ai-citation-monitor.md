# 루틴: AI 인용 모니터

**호출:** `/ai-search` **MONITOR** (비대화형, 질문 0).
**주기:** 격주 화요일 07:00. 들쭉날쭉한 캡처 한 번에 반응하지 않고, 비교 간격을 일정하게 만들어요.

## 하는 일

모니터는 최신 감사 또는 모니터 보고서의 돈 되는 질문 기준선을 그대로 다시 돌려요. 질문마다 얻은 인용, 잃은 인용, 유지한 인용과 새로 인용된 도메인을 찾고, 캡처 공백을 그대로 말해요. 예정된 실행에서 질문 세트는 바뀌지 않아요. 기준선이 없으면 감사 필요 보고서를 쓰고 멈춰요.

한국에서 볼 표면은 네이버 Cue:, 네이버 AI 브리핑, ChatGPT, Perplexity, 그리고 그 사업이 구글을 볼 때의 Google AI Overview예요. 영어 웹의 인용 비중은 네이버로 옮기지 마세요. 인용되는 한국 출처는 공식 사이트, 블로그, 카페, 지식iN, 뉴스, 유튜브예요.

## /schedule 프롬프트

마케팅 워크스페이스에서 `/schedule`을 실행하고 붙여 넣어요.

```
Schedule: every two weeks, Tuesday at 07:00 (my timezone).

Task: skills/ai-search/SKILL.md가 정의한 MONITOR 모드로 /ai-search를 실행한다.
비대화형이다. 질문은 0. 가장 최근 ./campaigns/ai-search/audit-*.md 또는 monitor-*.md의 Monitor baseline을 읽고 같은 돈 되는 질문을 그대로 다시 돌린다. 질문 세트를 지어내거나 늘리지 않는다. 질문과 엔티티마다 인용 차이를 기록한다. GAINED, LOST, HELD, 새로 인용된 도메인, 커버리지 공백, Data: LIVE 라벨이 있는 증거. 네이버 Cue:와 네이버 AI 브리핑이 기준선에 있으면 포함한다. 영어권 인용 통계를 네이버 사실처럼 쓰지 않는다. ./campaigns/ai-search/monitor-<YYYY-MM-DD>.md에 발견, 제안 반응 최대 3개, 다음 실행을 위한 갱신된 Monitor baseline을 쓴다. ./brand/assets.md에 한 줄을 덧붙인다. 기준선이 없으면 /ai-search AUDIT를 먼저 돌려야 한다고 적은 짧은 날짜 보고서를 쓰고 멈춘다. learnings.md는 쓰지 않는다. 추적 가능한 원인 후보만 보고서의 “Proposed learnings” 아래에 초안한다. 보고서만. 게시, 포스팅, 발송, 배포, 제3자 계정 변경은 하지 않는다.
```

## 모든 클라이언트 (대행사)

같은 프롬프트의 첫 줄을 이것으로 바꿔요. `./brands/ 아래 brand.yaml이 있는 각 클라이언트 디렉터리를 그 실행의 활성으로 두고 다음을 한다. 쓰기는 그 클라이언트의 폴더에만. 끝나면 클라이언트마다 롤업 한 줄.`
대상 클라이언트를 나열하려면 `route.py --all-brands --goal authority`를 써요.

## 로컬 cron

```cron
0 7 * * 2 cd /path/to/workspace && [ $(( $(date +\%V) % 2 )) -eq 0 ] && claude -p "Run /ai-search in MONITOR mode using the existing money-query baseline verbatim; write the dated monitor report and refreshed baseline, append assets, draft proposed learnings only, and never publish." --allowedTools "Read,Write,WebFetch,WebSearch"
```

## 클라우드 주의

클라우드 루틴은 저장소의 새 클론에서 돌아요. 그 저장소에 커밋된 스킬 (`.claude/skills/`)만 보고, 내 기계의 플러그인 설치는 보지 않아요. 클라우드로 돌리려면 스킬 폴더를 워크스페이스 저장소에 먼저 커밋하세요.

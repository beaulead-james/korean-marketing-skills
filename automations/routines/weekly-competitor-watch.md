# 루틴: 주간 경쟁 감시

**호출:** `/competitive-intel` **WATCH** (비대화형, 질문 0).
**주기:** 매주 월요일 07:00. 주 시작의 차이가 팀이 의미 있는 변화에 대응할 시간을 줘요.

## 하는 일

이 루틴은 누가 중요한지 짐작하지 않고 `competitors.md`의 명단과 Watch 기준선을 다시 써요. 기록된 공개 표면을 다시 확인하고, 증거 링크와 데이터 라벨이 있는 차이만의 보고서를 만들어요. 움직임이 없는 것은 타당한 짧은 결과예요. 기준선이 없으면 지어낸 명단 대신 날짜 있는 설정 보고서를 만들어요.

한국 표면이 기본이에요. 네이버 스마트플레이스, 카카오맵, 블로그, 카페, 공개 사이트, 보이는 광고. 구글 지도는 그 사업이 구글도 볼 때의 보조예요. 경쟁 사장님에게 연락하거나 글을 남기지 마세요.

## /schedule 프롬프트

마케팅 워크스페이스에서 `/schedule`을 실행하고 붙여 넣어요.

```
Schedule: every Monday at 07:00 (my timezone).

Task: skills/competitive-intel/SKILL.md가 정의한 WATCH 모드로 /competitive-intel을 실행한다.
비대화형이다. 질문은 0이고 모드 기본값을 쓴다. 활성 브랜드의 competitors.md Watch baseline과, 있으면 positioning.md를 읽는다. 기록된 경쟁의 홈, 제안, 가격, 공개 콘텐츠, 보이는 캠페인 표면을 다시 확인한다. 네이버 플레이스와 카카오맵이 기준선에 있으면 포함한다. 관찰한 증거는 Data: LIVE로 표시하고, 닿지 않는 표면은 말한다. ./campaigns/competitor-watch/<YYYY-MM-DD>.md에 의미 있는 차이만, 그 증거, 각각이 왜 중요한지, 움직임 없음 커버리지, 제안 반응 최대 3개를 쓴다. Watch baseline을 새로 고치기 전에 이전 competitors.md를 .history에 버전하고 brand.yaml을 올린다. ./brand/assets.md에 한 줄을 덧붙인다. 쓸 수 있는 기준선이 없으면 대화형 해체가 필요하다고 설명하는 짧은 날짜 보고서를 쓰고 멈춘다. learnings.md는 쓰지 않는다. 가능한 항목은 보고서의 “Proposed learnings” 아래에 둔다. 보고서만. 게시, 연락, 포스팅, 발송, 배포, 제3자 계정 변경은 하지 않는다.
```

## 모든 클라이언트 (대행사)

같은 프롬프트의 첫 줄을 이것으로 바꿔요. `./brands/ 아래 brand.yaml이 있는 각 클라이언트 디렉터리를 그 실행의 활성으로 두고 다음을 한다. 쓰기는 그 클라이언트의 폴더에만. 끝나면 클라이언트마다 롤업 한 줄.`
대상 클라이언트를 나열하려면 `route.py --all-brands --goal authority`를 써요.

## 로컬 cron

```cron
0 7 * * 1 cd /path/to/workspace && claude -p "Run /competitive-intel in WATCH mode. Read the active brand Watch baseline, write the dated competitor delta report, refresh the versioned local baseline, append assets, draft proposed learnings only, and never publish." --allowedTools "Read,Write,WebFetch,WebSearch"
```

## 클라우드 주의

클라우드 루틴은 저장소의 새 클론에서 돌아요. 그 저장소에 커밋된 스킬 (`.claude/skills/`)만 보고, 내 기계의 플러그인 설치는 보지 않아요. 클라우드로 돌리려면 스킬 폴더를 워크스페이스 저장소에 먼저 커밋하세요.

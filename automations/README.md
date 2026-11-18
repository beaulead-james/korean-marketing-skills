# 자동화

스킬을 대신 돌리는 스케줄과 묶음입니다. 판단은 각 `SKILL.md`에 있고, 여기 파일은 그 스킬을 언제 어떤 순서로 부를지만 적습니다. 실행 결과는 항상 초안입니다. 게시, 발송, 광고 지출은 사람이 합니다.

## hooks

`hooks/hooks.json`은 Claude Code 플러그인이 불러옵니다.

- 쓰기가 활성 고객(`./brands/active`)이 아닌 다른 고객 폴더로 가면 막습니다.
- `./campaigns/`에 파일을 쓰면 활성 브랜드의 `assets.md`에 경로를 한 줄 덧붙입니다. 같은 경로는 다시 적지 않습니다.

## routines

`routines/`는 반복 점검입니다. 각 파일에 `/schedule`에 붙일 문장과, 그 문장이 부르는 스킬이 있습니다.

| 파일 | 하는 일 |
|---|---|
| `weekly-content-ritual.md` | 이번 주 실제 소재로 뉴스레터와 소셜 초안 |
| `weekly-competitor-watch.md` | 플레이스와 광고에서 경쟁 가게의 변화 |
| `monthly-performance-review.md` | 한 달 숫자로 유지, 중단, 테스트 |
| `ai-citation-monitor.md` | 네이버 Cue:, AI 브리핑, ChatGPT, Perplexity에 이름이 있는지 |
| `brand-health-check.md` | 브랜드 파일이 오래됐거나 비었는지 |

## workflows

`workflows/`는 한 번에 여러 스킬을 잇는 온디맨드 절차입니다.

| 파일 | 하는 일 |
|---|---|
| `full-funnel-build.md` | 각도, 리드 마그넷, 페이지, 알림톡·문자, 광고 브리프 |
| `campaign-fanout.md` | 정해진 캠페인 소재를 채널별 초안으로 나눔 |

둘 다 `./campaigns/<slug>/` 아래에만 쓰고, 라이브 반영은 하지 않습니다.

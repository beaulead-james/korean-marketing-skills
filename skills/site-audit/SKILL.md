---
name: site-audit
description: 구글과 AI 검색 로봇이 사이트를 만나는 방식으로 크롤하고, 사장님과 개발자가 오늘 손댈 수 있는 짧은 수정 목록을 쉬운 말로 돌려줍니다. 네이버 수집 로봇 Yeti는 이 스크립트가 보지 않으므로 서치어드바이저에서 따로 봅니다. 검색에서 막힌 페이지, noindex와 canonical 실수, robots.txt나 CDN에서 막힌 AI 로봇, 사이트맵, 깨진 링크, 중복·얇은 페이지, 구글의 무료 PageSpeed로 본 코어 웹 바이탈, 인용할 만한 본문 신호를 다룹니다. 기술 SEO 진단, 네이버·구글에 페이지가 안 나올 때, AI 로봇이 들어오는지, 고친 뒤 무엇이 바뀌었는지를 볼 때 쓰세요.
when_to_use: technical seo audit, site audit, crawl my site, check my robots.txt, is google indexing my pages, why aren't my pages indexed, are AI crawlers blocked, is GPTBot blocked, broken links on my site, core web vitals, page speed check, check my sitemap, noindex check, duplicate pages on my site, technical seo health check, re-audit my site, what changed since the last audit, 기술 SEO 크롤 진단, 네이버 서치어드바이저 수집 상태, 로봇txt가 검색을 막는지, 사이트맵과 노인덱스 충돌, 깨진 내부 링크, 코어 웹 바이탈 현장 데이터, 수정 후 재진단, naver search advisor crawl, yeti robot blocked check
argument-hint: "[사이트 주소] [quick | re-audit]"
metadata:
  boring:
    version: 1.0.0
    layer: execution
    reads: [brand-manifest, keyword-plan, stack]
    writes: [assets]
    optional-keys: [PAGESPEED_API_KEY, CRUX_API_KEY, FIRECRAWL_API_KEY]
    enhances_with:
      - toolset: web-scrape
        gains: "re-reads pages that build their text with JavaScript, so content checks run on what visitors see instead of an empty shell"
      - toolset: search-console
        gains: "confirms which pages Google actually indexed and why it skipped the rest"
---

# 사이트 진단

안 찾아지는 사이트에는 이유가 짧고, 75줄짜리 표는 그 이유를 숨깁니다. 이 스킬은 네이버, 구글, AI 검색 로봇이 사이트를 만나는 방식으로 정중하게 크롤하고, 찾아지는 데 가장 중요한 수정 5개에서 10개를, 크롤이 본 것과 함께 돌려줍니다. 끝난 상태는 사장님이나 개발자가 오늘 목록을 실행할 수 있고, 누구든 그 주장을 다시 확인할 수 있는 것입니다. 아래 점검과 순위는 바닥입니다. 앞에 있는 사업이 다른 순서를 요구하면 바꾸고, 이유를 한 줄로 적으세요.

## Context

`./brand/`, `./brands/`, `MARKETING.md` 중 하나라도 있을 때만 실행하세요. 없으면 불러올 것이 없습니다.

`python3 ${CLAUDE_SKILL_DIR}/../start-here/scripts/brand_context.py --for site-audit`

`${CLAUDE_SKILL_DIR}`는 이 스킬 폴더입니다. Claude Code 밖에서는 이 파일을 읽은 폴더를 쓰세요. 예시는 `.agents/skills/site-audit`입니다. 스크립트나 python3가 없으면 브랜드 폴더를 직접 읽으세요. `./brands/active`가 슬러그를 가리키면 `./brands/<slug>/`, 아니면 `./brand/`입니다. 이어서 `MARKETING.md`, `preferences.md`, `reads:`의 파일을 읽으세요. 아무것도 없으면 단독으로 진행하고 URL만 물어보세요.

`brand.yaml`의 사업 사실(서비스, 시·군·구, 업종)과 키워드 계획은 어느 페이지가 돈인지 알려 줍니다. 심각도를 판단하는 데 쓰세요. 없으면 메뉴와 URL 경로에서 돈 되는 페이지를 추론하세요. 서비스, 지역, 상품, 가격, 예약, 견적.

잠재 고객의 사이트를 보는 것이지 사용자의 사이트가 아니면, 그 건으로 브랜드 파일을 읽거나 쓰지 마세요. 보고서는 `./campaigns/`에만 두고 다른 것은 바꾸지 마세요.

URL이 없거나 자리표시자(example.com, yourdomain.com)뿐이면 한 줄로 URL을 물어보세요. 자리표시자는 크롤하지 마세요.

## 증거가 말하는 것

로봇, CDN, PageSpeed를 설명하기 전에 `references/crawler-facts.md`를 읽으세요. 머리글을 보고, 오래됐으면 새로고치세요. 낡지 않는 판단은 이것입니다.

- **수집되고 색인되는 것이 먼저입니다.** 돈 되는 페이지의 Disallow나 noindex 하나가 목록의 다른 모든 항목보다 큽니다. 실제 감사는 이런 것이 두세 개, 그리고 화장성 경고가 한 무더기인 경우가 많습니다.
- **한국 사이트의 기본 검색은 네이버입니다.** 구글은 같이 봅니다. 스크립트는 Googlebot과 목록에 있는 AI 로봇을 검사합니다. 네이버 수집 로봇 Yeti는 그 목록에 없습니다. robots.txt의 `User-agent: Yeti`와 네이버 서치어드바이저 수집·색인을 손으로 확인하세요. Googlebot이 열려 있다는 문장을 네이버도 수집한다는 뜻으로 쓰지 마세요.
- **일반 검색 순위는 AI 인용보다 앞에 있습니다.** 구글 AI 답변에서 인용되는 페이지의 상당수는 이미 순위에 있고, 다른 엔진은 자기 검색 색인에 기댑니다. 네이버 AI 브리핑과 Cue:도 수집된 페이지와 플레이스·블로그·뉴스 쪽에서 재료를 가져옵니다. AI 준비는 검색 로봇을 들이고, 본문을 HTML에 두고, 같은 기본을 맞추는 일에 가깝습니다. 기술 수정이 인용을 만든다고 약속하지 마세요.
- **선택 위생은 선택으로 남습니다.** llms.txt와 범용 구조화 데이터는 싸고 입증이 약합니다. "같이 하면 좋은 것"에 두고 맨 위에 두지 마세요. 스키마는 페이지 본문이 그 주장을 받칠 때만 자리가 있고, 사업을 한결같이 부르는 마크업 블록 하나가 여기저기 넣을 가치가 있습니다 (`references/schema-and-entity.md`).
- **근거가 있는 본문 신호**는 글에 대해 보고합니다. 통계, 인용문, 출처 (생성 답에 대한 통제 연구 하나가 이것들의 가시성 상승을 봤습니다. 영어권 생성 답의 결과입니다), 보이는 발행·수정일, 기명 저자, 답 캡슐 (질문형 제목 다음의 짧고 스스로 서며 링크가 적은 답). 신호이지 규칙이 아닙니다. 블로그 글의 날짜 빠짐은 상위 다섯 수정이 아닙니다.
- **심각도는 사업 영향입니다.** 경고가 건드린 페이지 수가 아닙니다. alt가 없는 이미지 300장보다, noindex인 서비스 페이지 한 장이 큽니다.

## 모드

| 사용자가 하는 말 | 모드 | 도는 것 |
|---|---|---|
| URL, "사이트 SEO 진단", "기술 SEO 감사" | **Full** (기본) | 최대 200페이지 (max-pages, 하드 캡 1,000), AI 로봇 점검, 홈과 핵심 템플릿 3개의 PageSpeed |
| "quick", "구글이 막힌 게 있나", "AI 로봇이 막혔나" | **Quick** | 홈과 약 20페이지, robots와 AI 로봇 접근, 홈 PageSpeed |
| "re-audit", "뭐가 바뀌었나", "고친 뒤 다시" | **Re-audit** | Full 또는 quick을 지난 발견 파일과 비교 |

좁은 질문 ("GPTBot이 막혔나")은 Quick과 몇 줄 답이고, 발견은 저장합니다. "사이트 봐 줘", "마케팅 진단"은 `start-here`가 가집니다. 이 스킬은 기술 절반입니다.

## 1단계. 실행 준비

크롤 전에 브랜드 파일이나 요청에서 세 가지를 정하세요. 추론할 수 없는 것만, 메시지 하나에 물어보세요.

1. **사이트와 돈 되는 페이지.** 홈 URL과 손님을 부르는 페이지 (서비스, 지역, 상품, 가격, 예약). 이것이 나중 심각도를 정합니다.
2. **AI에 보이고 싶은가.** 손님이 필요한 사업은 기본 예입니다. robots.txt가 AI 검색 로봇을 일부러 막으면 (콘텐츠를 지키는 매체 등) 문제라고 부르기 전에 한 번 물어보세요. 학습용 로봇을 막는 것은 사업의 선택입니다. 한 번 보고하고, 수정 항목으로 만들지 마세요. Yeti를 막는 것은 그 선택이 아닙니다. 네이버 검색 수집을 막는 것입니다.
3. **시간과 예의.** 200페이지 전체 크롤은 약 2분에서 6분, PageSpeed 호출이 1분에서 3분입니다. Quick은 약 1분입니다. 크롤러는 사용자 에이전트에 자기 이름을 밝히고, 자기 크롤에 대해 robots.txt를 지키고, 요청을 약 4개까지 동시에 두되 시작 사이에 간격을 두고, robots.txt가 crawl-delay를 주면 한 번에 하나씩으로 늦춥니다. CDN 확인은 AI 로봇 이름마다 홈 요청을 하나 보냅니다. 잠재 고객 사이트에도 가벼운 부하입니다.

**PageSpeed 키.** 구글 PageSpeed Insights API는 키 없이도 됩니다. 키 없는 할당량은 공유되고 자주 소진되며, 그러면 감사가 코어 웹 바이탈을 확인하지 못했다고 말합니다. 무료 키가 고칩니다. 구글 클라우드 콘솔에서 PageSpeed Insights API를 켜고 API 키를 만들어 `PAGESPEED_API_KEY`로 두세요. 같은 프로젝트에서 Chrome UX Report API를 켜면 그 키로 실제 방문 데이터도 가져옵니다 (`CRUX_API_KEY`로 따로 둬도 됩니다). 이것은 구글의 속도 측정입니다. 네이버가 같은 점수로 순위를 매긴다고 말하지 마세요. 손님의 휴대폰이 기다리는지는 그 자체로 중요합니다.

## 2단계. 크롤 실행

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/crawl_audit.py <url>                  # full
python3 ${CLAUDE_SKILL_DIR}/scripts/crawl_audit.py <url> --mode quick     # quick
python3 ${CLAUDE_SKILL_DIR}/scripts/crawl_audit.py <url> --compare auto   # re-audit against the last run for this site
```

스크립트(파이썬 3 표준 라이브러리, 설치 없음)는 robots.txt와 그것이 가리키는 모든 사이트맵을 읽고, 홈을 가져오고, 같은 사이트 링크를 너비 우선으로 돌면서 사이트맵 URL 표본을 섞고, 크롤하지 않은 내부 링크 대상을 확인하고, 홈이 브라우저와 각 AI 로봇에게 어떻게 답하는지 비교하고, 없는 URL로 소프트 404를 엿보고, llms.txt와 ai.txt를 찾고, PageSpeed를 돌립니다. `findings.json`과 `pages.jsonl`을 `./campaigns/site-audit-<domain>-<YYYY-MM-DD>/`에 씁니다. 같은 날 두 번째 실행은 `-2`가 붙어 이전 실행을 덮지 않습니다. 요약을 출력합니다. 유용한 플래그는 max-pages, no-psi, no-bot-check, psi-templates, max-minutes이고, 나머지는 도움말에 있습니다.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/crawl_audit.py --help
```

python3가 없으면 손으로 표본 감사를 하세요. robots.txt, 사이트맵, 홈, 돈 되는 페이지 5장에서 10장을 WebFetch나 curl로 가져와 같은 점검을 하고, 출처와 가정에 N페이지 표본이라고 적으세요. Yeti 그룹은 이 손 확인에 포함하세요.

**자바스크립트로 본문을 만드는 사이트.** 대부분 페이지의 HTML에 글이 거의 없으면 크롤은 `js_rendered_content`를 보고, 그 페이지를 얇다고 부르지 않은 채 본문 점검에서 뺍니다. 보고서에 그렇게 말하세요. 구글은 자바스크립트를 그리되 HTML보다 늦습니다. AI 로봇은 받은 HTML만 읽을 수 있습니다. /ai-search의 검색 사실은 서버가 보낸 본문을 챗GPT의 조건으로 둡니다. 네이버 수집도 빈 껍데기에서는 할 말이 없습니다. 손님이 보는 것을 감사하려면 렌더된 HTML로 다시 돌리세요. Firecrawl은 이 용도의 선택 도구입니다 (무료 구간, TOOLS.md). `FIRECRAWL_API_KEY`가 있으면 render 플래그에 firecrawl을 주세요 (최대 25페이지, Firecrawl 크레딧에서 차감). Firecrawl MCP면 각 페이지를 `rawHtml`로 긁어 JSON 줄(`{"url": ..., "html": ...}`)로 저장하고 rendered 플래그에 그 파일을 넘기세요.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/crawl_audit.py <url> --render firecrawl
python3 ${CLAUDE_SKILL_DIR}/scripts/crawl_audit.py <url> --rendered <file>
``` 둘 다 없으면 건너뛴 점검을 나열하고 거기서 멈추세요. 유료 도구가 없어도 HTML이 있는 사이트의 기술 진단은 끝납니다.

## 3단계. 발견 읽기

`findings.json`에는 `findings` (각각 `id`, `severity`, `count`, `key_pages_affected`, `examples`, `urls`, `observation`, `fix`, `effort`, `confidence`), `checked_and_fine`, `not_checked`, `site` 블록 (robots, 로봇별 AI 정책, CDN 비교, 사이트맵, AI 파일, 호스트 변형, 소프트 404, 본문 신호 요약), `cwv`가 있습니다. 각 발견의 의미, 올리거나 내릴 때, 사각, 플랫폼별 수정은 `references/checks.md`에 있습니다.

상위 목록에 넣기 전에.

- **예시 하나를 직접 보세요.** 예시 URL을 가져와 증명하는 줄을 찾으세요. meta 태그, Disallow 규칙, 404. 스크립트 휴리스틱에는 사각이 있고, 틀린 항목 하나를 사장님이 잡으면 나머지를 믿지 않습니다. 확인한 것을 `notes.md`에 적으세요.
- **"확인 못 함"과 "괜찮음"을 나누세요.** `not_checked`는 출처와 가정의 미지로 갑니다. `checked_and_fine`만 괜찮다고 부를 수 있습니다. Yeti와 서치어드바이저는 스크립트가 안 보면 미지입니다. 괜찮음이 아닙니다.
- **범위를 지키세요.** `crawl.truncated`가 참이면 개수는 "크롤한 페이지 중 적어도 N"이고, 고아 페이지는 약한 증거입니다.
- **CDN 확인은 대역 요청입니다.** 이 기계에서 로봇 이름을 보냅니다. 업체 IP 대역이 아닙니다. 거절은 CDN이나 방화벽이 그 이름을 막는다는 강한 증거이고, 수정은 CDN 봇 설정이나 서버 로그에서 확인됩니다. 그대로 말하세요.
- **현장이 실험실을 이깁니다.** PageSpeed의 실제 방문 데이터(크롬 UX 리포트, 28일)는 트래픽이 충분한 페이지만 있습니다. 실험실 데이터뿐이면 "시뮬레이션된 휴대폰 로딩"이라고 쓰고 "손님들이 기다린다"고 쓰지 마세요.

## 4단계. 수정 순위

사업이 찾아지는 데 각 수정이 얼마나 도움이 되는지, 그다음 노력으로 순위를 매기세요. 기본 순서입니다. 이유를 밝히면 바꿀 수 있습니다.

1. **구글이나 네이버를 사이트 또는 돈 되는 페이지 밖에 두는 것.** 홈이 죽거나 HTTPS 실패, robots.txt 오류나 `/` Disallow, 돈 되는 페이지의 noindex (거의 모든 페이지 noindex는 보통 설정 하나. 워드프레스 "검색 엔진이 이 사이트를 색인하지 못하도록" 같은 것), 돈 되는 페이지가 다른 페이지나 다른 도메인으로 canonical. Yeti의 `/` Disallow는 네이버 쪽에서 같은 급입니다.
2. **보이고 싶은데 AI 검색 로봇이 막힌 것.** 검색·비서 로봇 (OAI-SearchBot, Claude-SearchBot, PerplexityBot, ChatGPT-User, Claude-User, Perplexity-User). robots.txt 또는 CDN.
3. **돈 되는 페이지로 가는 깨진 길.** 메뉴나 홈의 깨진 링크, 리다이렉트 루프, 서버 오류, noindex·깨짐·차단 URL을 실은 사이트맵.
4. **검색이 못 보거나 못 가르는 본문.** 자바스크립트로만 만들어진 글, 구 이름만 바꾼 거의 복사 페이지, 얇은 돈 페이지. 지역명만 바꾼 묶음은 네이버 저품질(유사 문서) 위험입니다. 고치거나 합치라고 말하고, 양산 페이지의 설계는 /programmatic-seo와 /service-area-pages로 보내세요.
5. **돈 되는 페이지에서 실제 손님이 기다림.** 현장 코어 웹 바이탈이 나쁨. 실험실만의 느림은 더 아래입니다.
6. **돈 되는 페이지의 기본.** 없는 제목, H1 없음, 모바일 뷰포트 없음.
7. **나머지** (설명 길이, alt, 공유 태그, HSTS, URL 모양, llms.txt, 범용 스키마, 옛 글의 본문 신호)는 "같이 하면 좋은 것"이나 괜찮음 한 줄로.

아슬한 판단.

- **페이지 가치로 가중하세요.** 서비스 페이지 한 장이 태그 보관함 쉰 장보다 위입니다. 색인을 푸는 10분 수정이 재설계보다 앞입니다.
- **원인이 하나면 합치세요.** noindex이면서 사이트맵에도 있는 페이지는 항목 하나입니다. 메뉴 하나에서 나온 깨진 링크 스무 개는 수정 하나입니다.
- **5개에서 10개를 고르세요.** 건강한 사이트는 세 개일 수 있습니다. 그렇다고 말하고 멈추세요. 목록을 채우면 중요한 항목이 숨습니다.
- **진짜 문제가 순위면** 기술 수정이 AI 인용이나 트래픽을 만들지 않습니다. 그렇다고 말하고 `/keyword-research`나 `/local-seo-plan`으로 보내세요.

하드 규칙. 관찰 없이 고장이라고 부르지 말 것. "확인 못 함"을 괜찮음으로 내놓지 말 것. 트래픽, 매출, 순위 영향을 지어내지 말 것. AI 준비 수정으로 인용을 약속하지 말 것.

## 5단계. 보고서

사장님에게 쉬운 말로 쓰세요. 보고서에 스크립트 경로, 과정으로서의 도구 이름, 점검 id, 심각도 라벨을 넣지 마세요. 그것은 `notes.md`에 남습니다. 길이. 계획 예산(약 1,200에서 2,500단어)은 천장이고, 대부분 감사는 600에서 1,200이면 됩니다. **먼저 고칠 것**이 1번을 전부 담고, 번호 목록이 나머지를 순서대로 담아 두 번 말하지 않습니다. 각 항목은 무엇이 잘못됐는지, 이 사업에 왜 중요한지, 해당 페이지(개수와 예시 두세 개), 수정, 대략의 노력을 말합니다.

예시 업체 한빛설비 (대구, 설비). 예시 사이트이며 숫자는 예시입니다.

```markdown
## SITE AUDIT: hanbit.example (예시)
2026-11-18 · 184페이지 크롤, 네이버·구글과 AI 답변에서 찾아지기 위한 진단

**먼저 고칠 것:** 보일러 페이지가 검색에 색인되지 말라고 되어 있습니다. /boiler/ 아래 6페이지가 모두 `noindex`이고 (예. /boiler/교체/), 그중 4개가 사이트맵에 있습니다. 가장 많이 광고하는 서비스라, 이것을 바꾸기 전에는 순위에 오르거나 인용되지 않습니다. 수정. SEO 플러그인에서 그 페이지의 "검색에서 숨기기"를 끄고, 구글 서치 콘솔과 네이버 서치어드바이저에서 다시 수집을 요청하세요. 약 15분.

**그다음, 이 순서로:**

1. **챗GPT와 퍼플렉시티의 검색 로봇이 막혀 있습니다.** robots.txt에 `User-agent: OAI-SearchBot` / `Disallow: /`가 있고 PerplexityBot도 같습니다. 그들의 답에 출처로 실릴 수 없습니다. 페이지. 사이트 전체. 수정. 그 두 그룹을 지우세요. 학습에 넣고 싶지 않으면 GPTBot 차단은 두세요. 5분. Yeti 그룹은 이 실행의 스크립트가 검사하지 않았습니다. 서치어드바이저에서 확인이 필요합니다.
2. **메뉴의 "온라인 예약"이 깨져 있습니다.** /book-now/를 가리키고 404를 돌려 줍니다. 184페이지 모두. 수정. 메뉴를 /schedule/로. 5분.
3. **구 페이지 12장이 거의 복사입니다.** /설비-수성구/와 /설비-달서구/는 구 이름만 다릅니다 (12페이지, 예. /설비-중구/). 수정. 그 구에서 한 일, 현장 디테일, 사진을 넣거나 출장 범위 페이지 하나로 합치세요. 페이지당 약 한 시간. 이름만 바꾼 묶음은 네이버 저품질 위험입니다.
4. **휴대폰에서 홈이 느립니다.** 휴대폰 실제 방문자는 대표 이미지를 약 4.6초 뒤에 봅니다 (구글의 좋음 기준은 2.5초). 수정. 히어로 사진을 압축·리사이즈하고, 채팅 위젯을 페이지보다 먼저 불러오지 마세요. 개발자 반나절. 이 4.6초는 예시 숫자입니다.

**같이 하면 좋은 것:** canonical이 없는 40페이지에 자기 자신을 가리키는 canonical, 시공 사진 alt, 홈에 사업 마크업 (상호, 전화, 주소).

**확인했고 괜찮음:** HTTPS와 리다이렉트, 구글용 robots.txt, 사이트맵 형식, 서버 오류 없음, 제목이 있고 서로 다름, 모든 페이지의 모바일 뷰포트.

**출처와 가정:**
- 2026-11-18에 약 210개 URL 중 184개를 크롤했습니다 (200페이지에서 멈춤). 내부 링크 확인 150개. 홈은 PageSpeed 실제 방문 데이터, 서비스 페이지 두 장은 실험실 데이터.
- CDN 확인은 이 기계에서 로봇 이름을 보낸 것이고 그들 네트워크가 아닙니다. 차단은 보이지 않았습니다.
- 확인 안 함. 구글이 실제로 색인한 페이지 (서치 콘솔 접근 필요), 네이버 서치어드바이저의 수집 현황, robots.txt의 Yeti.
```

재진단은 **<날짜> 이후 바뀐 것**으로 여세요 (해결, 새로움, 그대로. 발견 파일의 `changes`). 그다음 현재 수정 목록. 각 실행은 자기 페이지 한도 안에서 크롤하므로, 한쪽에서만 보인 페이지는 다른 실행의 표본 밖이었을 수 있습니다. 새로 생기거나 사라졌다고 부르지 말고 그렇게 말하세요.

## 산출

보고서 `site-audit.md`를 실행 폴더 `./campaigns/site-audit-<domain>-<YYYY-MM-DD>/`에, 스크립트의 `findings.json`, `pages.jsonl` 옆에 쓰세요. `notes.md`는 작업 기록입니다. 손으로 확인한 예시, 합치거나 뺀 발견과 이유, 코어 웹 바이탈 원숫자, 개발자에게 넘길 것. 브랜드 폴더가 있으면 `./brand/assets.md`에 한 줄 (잠재 고객 건은 절대 아님). 그다음 채팅 요약. 머리글, 수정 목록, **저장한 파일**, **다음**.

## 사용자가 결과물을 고치면

고친 내용을 반영한 뒤 남기세요. `./brand/gold/<이 스킬>/`에 골드 사례 하나, `./brand/checks.md`에 예/아니오 점검 1개에서 3개, 한 줄로 확인. 넘기기 전에 컨텍스트가 불러온 점검을 조용히 답하고, 아니오는 모두 고치세요. 방법은 `${CLAUDE_SKILL_DIR}/../start-here/references/taste-loop.md`입니다.

## 다음

- `/ai-search`. 로봇이 사이트에 닿을 수 있게 된 뒤, 챗GPT·퍼플렉시티·구글 AI·네이버 브리핑이 실제로 이 업체를 부르고 인용하는지 (약 20분)
- `/keyword-research`. 페이지는 멀쩡한데 순위가 없으면, 무엇으로 찾아져야 하는지 (약 15분)
- `/local-seo-plan`. 지역 사업이 어떤 서비스·구 페이지를 만들거나 합치거나 버릴지 (약 30분)
- `/first-screen-check`. 돈 되는 페이지를 손님이 휴대폰에서 보는 방식 (약 10분)

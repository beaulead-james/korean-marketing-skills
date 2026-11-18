# 로봇, CDN, PageSpeed 사실 (상하기 쉬움. 아래를 믿기 전에 머리글을 확인)

last-verified: 2026-11-18 · ttl-days: 90 · refresh: 맨 아래 출처를 다시 읽고 (OpenAI, Anthropic, Perplexity 로봇 문서, 구글 일반 크롤러와 robots.txt 명세, 클라우드플레어 AI 로봇 정책, PageSpeed와 CrUX), 네이버 서치어드바이저에서 Yeti와 수집 안내를 확인하세요. 바뀐 행을 고치고, 업체가 추가한 로봇 이름을 더하고, 스크립트의 `AI_BOTS`와 어긋나면 그 차이를 이 파일에 적으세요. 스크립트는 이 스킬이 고치지 않습니다.
changes: 2026-11-18 한국 사이트용 설명. Yeti는 스크립트 목록에 없으므로 손 확인이라고 명시. 구글 robots 숫자와 코어 웹 바이탈 기준은 구글 문서의 규칙으로 남김. 이전 2026-11-16은 업체 페이지를 그날 읽은 첫 버전.

로봇이 무엇을 하는지, CDN이 기본으로 무엇을 막는지, PageSpeed가 재고 못 재는지를 설명하기 전에 읽으세요. 오늘이 last-verified + ttl-days를 넘으면 먼저 새로고치고 한 줄로 알리세요. `로봇 사실을 새로고쳤습니다 (캐시가 N일 지남).`

## 한국 사이트에서 먼저 볼 로봇

- **Yeti**는 네이버 수집 로봇입니다. `User-agent: Yeti`가 `/`를 Disallow하면 네이버 검색 수집이 막힙니다. AI 브리핑과 Cue:의 재료에서도 빠질 수 있습니다. 공식 안내는 네이버 서치어드바이저입니다. https://searchadvisor.naver.com
- 이 스킬의 `scripts/crawl_audit.py` `AI_BOTS` 목록에는 Yeti가 없습니다. 스크립트가 "Googlebot 허용"이라고 해도 네이버 수집을 확인한 것이 아닙니다. robots.txt에서 Yeti 그룹을 직접 읽고, 서치어드바이저의 수집·색인 현황을 따로 보세요.
- 아래 표의 구글 robots 해석(500KiB, 5xx일 때 12시간 등)은 **구글 문서의 규칙**입니다. 네이버가 같은 숫자로 동작한다고 적지 마세요.

## AI와 검색 로봇

| robots.txt 토큰 | 업체 | 하는 일 | robots.txt를 지키나 | 막으면 잃는 것 |
|---|---|---|---|---|
| Googlebot | Google | 검색. AI Overview와 AI Mode 포함 | 예 | 구글 검색 |
| Google-Extended | Google | 제어 토큰만 (자기 사용자 에이전트 없음). Gemini 학습과 Gemini 앱·Vertex AI의 그라운딩 | 예 | Gemini 학습과 그라운딩. 구글은 구글 검색의 포함이나 순위에 영향 없다고 함 |
| Bingbot | Microsoft | 빙과 코파일럿 검색 | 예 | 빙과 코파일럿 답 |
| OAI-SearchBot | OpenAI | 챗GPT 검색 | 예 (반영에 약 24시간) | 챗GPT 검색 답의 출처로 안 나옴. OpenAI는 탐색 링크로는 남을 수 있다고 함 |
| ChatGPT-User | OpenAI | 사람이 챗GPT나 커스텀 GPT에 물을 때 페이지를 가져옴 | OpenAI는 이 사용자 시작 방문에 robots.txt가 적용되지 않을 수 있다고 함 | 묻는 사람을 위해 페이지를 못 염 |
| GPTBot | OpenAI | 학습 | 예 | 학습만. OpenAI는 설정이 서로 독립이라고 함 |
| OAI-AdsBot | OpenAI | 챗GPT 광고로 제출된 랜딩 확인 | 제출된 페이지만 방문 | 감사 목록에 없음. 광고주에게만 해당 |
| Claude-SearchBot | Anthropic | Claude 검색 결과를 위해 색인 | 예 | Anthropic은 막으면 Claude 검색의 가시성과 정확도가 줄 수 있다고 함 |
| Claude-User | Anthropic | 사람이 Claude에 물을 때 페이지를 가져옴 | 예 | 묻는 사람을 위해 페이지를 못 가져옴 |
| ClaudeBot | Anthropic | 학습 | 예 (Crawl-delay도 읽음) | 학습만. Claude-SearchBot이나 Claude-User를 멈추지 않음 |
| PerplexityBot | Perplexity | 퍼플렉시티 검색에 사이트를 올리고 링크. 학습에 안 씀 | 예 (최대 24시간) | 퍼플렉시티 답에 못 올라옴 |
| Perplexity-User | Perplexity | 사람의 질문을 위해 페이지를 가져옴 | 퍼플렉시티는 대체로 robots.txt를 무시한다고 함 | 가장자리 차단만 멈춤 |
| Applebot-Extended | Apple | 학습용 제어 토큰 | 이번엔 다시 안 읽음 | 학습만 |
| CCBot | Common Crawl | 많은 모델이 학습하는 공개 크롤 데이터 | 이번엔 다시 안 읽음 | 학습 데이터 |
| meta-externalagent | Meta | 학습 | 이번엔 다시 안 읽음 | 학습만 |
| Bytespider | ByteDance | 학습 | 이번엔 다시 안 읽음 | 학습만 |
| Amazonbot | Amazon | Alexa 답과 모델 작업 | 이번엔 다시 안 읽음 | 아마존 비서 |

Googlebot, Bingbot, OpenAI 행과 Anthropic, Perplexity 행은 아래 업체 페이지에서 옵니다. Applebot-Extended, CCBot, meta-externalagent, Bytespider, Amazonbot과 스크립트의 더 작은 학습 로봇(cohere-ai, AI2Bot, Timpibot, FacebookBot)은 이번에 다시 읽지 않았습니다. 행동을 말하기 전에 업체 페이지를 읽으세요.

찾아지고 싶은 사업의 의미. 검색 로봇과 사용자 가져오기 로봇은 허용하세요. 학습 로봇은 별도 선택이고, 그 선택이 AI 검색에서 사이트를 빼지는 않습니다. Yeti는 학습 로봇이 아닙니다. 네이버 검색 수집입니다. 업체는 공개 IP 대역으로 로봇을 확인합니다 (OpenAI와 Perplexity는 JSON 목록을 냄). 사용자 에이전트만 믿는 방화벽은 속일 수 있고, IP를 확인하는 규칙은 이름만 빌린 대역 요청을 거절합니다.

## 구글이 robots.txt를 읽는 법

구글 robots.txt 명세 (2026-10-23 업데이트)에서. 네이버 규칙이 아닙니다.

- **상태 코드.** 2xx면 규칙을 씁니다. 3xx면 구글이 최소 다섯 번 따라간 뒤 404로 봅니다. 429를 뺀 4xx는 robots.txt가 없는 것처럼 보아 크롤 제한이 없습니다. 5xx(시간 초과, DNS, 연결 오류도 서버 오류로 침)면 처음 12시간은 사이트 크롤을 멈추고, 다음 30일은 마지막 좋은 사본을 쓰며(캐시가 없으면 제한 없음으로 가정), 30일 뒤에는 사이트가 그 외에는 살아 있으면 robots.txt가 없는 것처럼 행동하고, 살아 있지 않으면 크롤을 멈춥니다. 503은 자주 재시도합니다.
- **크기.** 500KiB. 한도를 넘는 내용은 무시됩니다.
- **필드.** user-agent, allow, disallow, sitemap. Crawl-delay는 구글이 지원하지 않습니다 (ClaudeBot을 포함한 다른 로봇은 읽습니다). 모르는 줄은 무시되고, user-agent 줄 사이의 sitemap 줄은 그룹을 나누지 않습니다.
- **그룹.** 크롤러는 자기 제품 토큰을 가장 구체적으로 부르는 그룹을 대소문자 무시로 따릅니다. 같은 토큰의 여러 그룹은 합쳐집니다. 이름 있는 그룹과 `*` 그룹은 합쳐지지 않으므로, 어디선가 이름이 불린 봇은 `*` 규칙을 통째로 무시합니다.
- **규칙 우선.** 가장 긴 경로가 이기고, 동점이면 덜 제한적인 쪽(allow)이 이깁니다. `*`는 아무 문자, `$`는 끝. 경로 없는 규칙은 무시되므로 뒤에 아무것도 없는 `Disallow:`는 모두 허용입니다.
- 구글은 대체로 robots.txt를 최대 24시간 캐시합니다.

구글의 robots.txt 소개와 noindex 페이지에서. robots.txt에서 금지된 URL도 다른 페이지가 링크하면 색인될 수 있고, noindex는 robots.txt가 페이지를 막지 않을 때만 작동합니다. 페이지를 가져오지 못한 크롤러는 태그를 못 보기 때문입니다. 결과에서 빼려면 Disallow가 아니라 noindex를 쓰세요.

## CDN과 AI 로봇

- **클라우드플레어** (AI Crawler and Agent access policies, 2026-11-02 업데이트). 행동별(Search, Agent, Training)로 Block, 광고 있는 페이지만 Block, Allow, Disallow(학습만, robots.txt에 기록). 새 도메인은 세 행동 모두 기본 Allow. 학습을 막으면 학습과 검색을 같이 하는 로봇도 막힙니다. 옛 존에는 이전 "Block AI bots"이나 관리형 robots.txt가 남아, `# BEGIN Cloudflare Managed content`로 표시된 블록이 학습 로봇(GPTBot, ClaudeBot, Google-Extended, CCBot 등)을 금지하고 `Content-signal: search=yes, ai-train=no` 줄을 더할 수 있습니다. Bot Fight Mode도 로봇에 챌린지를 걸 수 있습니다. 감사는 관리형 블록과 content-signal 줄을 기록합니다.
- 다른 CDN과 방화벽(Akamai, Fastly, Vercel, Sucuri, Wordfence 등)은 자기 봇 규칙이 있고, 이 파일은 그들의 기본값을 주장하지 않습니다. 서버 헤더가 가리키는 CDN의 이름을 말하고, 봇 설정이 어디 있는지 사장님에게 알려 주세요. 한국 호스팅의 웹방화벽도 같은 방식으로, 기본값을 짐작하지 말고 헤더와 설정 화면을 보세요.

## PageSpeed Insights와 코어 웹 바이탈

구글의 측정입니다. 네이버가 같은 점수로 순위를 매긴다고 말하지 마세요. 손님의 휴대폰이 기다리는지는 그 자체로 중요합니다.

- **API.** `https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=...&strategy=mobile`. 키가 없어도 됩니다. 구글은 자주, 자동으로 물을 때 키를 권합니다. 키 없는 호출은 할당량을 공유하고 "Quota exceeded ... Queries per day"로 자주 실패합니다. 구글 클라우드 콘솔의 무료 키가 고칩니다.
- **이 API에서 현장 데이터가 빠질 예정.** 구글 시작 문서는 PageSpeed Insights API에 크롬 UX 리포트(실제 방문)를 넣는 것을 멈출 계획이고 CrUX API를 쓰라고 합니다. 스크립트는 있는 동안 PageSpeed에서 현장 데이터를 읽고, 키가 있으면 CrUX API로 넘어갑니다.
- **CrUX API.** `POST https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=...` 본문 `{"url": ..., "formFactor": "PHONE"}` 또는 `{"origin": ...}`. 크롬 UX 리포트 API가 켜진 구글 클라우드 키. 무료, 프로젝트당 분당 150쿼리. 404는 그 페이지나 오리진의 트래픽이 부족하다는 뜻입니다.
- 현장 데이터는 최근 28일의 75백분위이고, 크롬 트래픽이 충분한 페이지와 오리진에만 있습니다. 실험실 데이터는 시뮬레이션 로딩 한 번입니다.
- **기준** (구글). 좋음은 LCP 2.5초 안, INP 200ms 미만, CLS 0.1 미만. 나쁨은 LCP 4초 초과, INP 500ms 초과, CLS 0.25 초과.
- **무게.** 구글은 코어 웹 바이탈을 순위 시스템이 쓰고, 좋은 점수가 상위 순위를 보장하지 않으며, "페이지 경험이 나빠도 가장 관련 있는 내용을 보여 주려 한다"고 합니다. 속도는 순위 레버로서보다 손님을 잃을 때 중요합니다.

## 구조화 데이터와 AI 파일

이 라이브러리의 AI 검색 사실에서 (`ai-search/references/aeo-facts.md`, 2026-11-18에 확인). 거기서 다시 보세요.

- FAQ 리치 결과는 2026년 5월 7일 모든 사이트에서 제거되었습니다. FAQ 마크업의 남은 가치는 깨끗한 질문·답 구조입니다. HowTo 리치 결과는 2023년에 끝났습니다.
- 구글의 AI 기능 안내는 특별 마크업이 필요 없고 llms.txt도 구글 검색에 필요 없다고 합니다. llms.txt를 보상한다고 확인된 엔진은 없습니다.
- 짝지은 대조에서 스키마만으로 인용 상승은 없었습니다. 영어권 시험입니다.

## 출처 (2026-11-16에 읽고, 2026-11-18에 한국 쪽을 더함)

- OpenAI 로봇. https://developers.openai.com/api/docs/bots
- Anthropic 로봇. https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler
- Perplexity 로봇. https://docs.perplexity.ai/docs/resources/perplexity-crawlers
- 구글 일반 크롤러 (Googlebot, Google-Extended). https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers
- 구글 robots.txt 명세. https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec
- 클라우드플레어 AI 로봇 정책. https://developers.cloudflare.com/bots/additional-configurations/block-ai-bots/
- 클라우드플레어 관리형 robots.txt. https://developers.cloudflare.com/bots/additional-configurations/managed-robots-txt/
- PageSpeed Insights API. https://developers.google.com/speed/docs/insights/v5/get-started
- CrUX API. https://developer.chrome.com/docs/crux/api
- robots 소개와 noindex. https://developers.google.com/search/docs/crawling-indexing/robots/intro 와 https://developers.google.com/search/docs/crawling-indexing/block-indexing
- 코어 웹 바이탈과 페이지 경험. https://developers.google.com/search/docs/appearance/core-web-vitals 와 https://developers.google.com/search/docs/appearance/page-experience
- 네이버 서치어드바이저. https://searchadvisor.naver.com

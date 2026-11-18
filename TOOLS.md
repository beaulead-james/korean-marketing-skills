# 도구 가이드: 선택 도구가 여는 것

키 0개로 모든 것이 동작해요. 모든 스킬은 에이전트 자신의 웹 검색·가져오기와 사용자가 준 파일 (내보내기, 통화 기록, CSV, 스크린샷)로 일을 끝내요. 도구는 리서치를 깊게 하고, 스킬이 행동하게 해요 (시퀀스 초안 푸시, 이미지 생성, 광고 계정 읽기). 키는 워크스페이스 루트 `.env`, 또는 한 클라이언트면 `./brands/<client>/.env`. 어떤 스킬도 값을 보여 주지 않아요.

## 우리가 쓰는 것

이것들 없이도 모든 스킬이 동작해요. 더 하고 싶을 때 이 스택을 써요. 일마다 하나. 스킬은 도움이 되는 단계에서 선택, 비용, 무료 방법을 말해요.

| 일 | 우리가 쓰는 것 | 비용 | 키 | 쓰는 스킬 |
|---|---|---|---|---|
| 에이전트용 웹 검색 | Exa | 무료 티어, 그다음 쓴 만큼 | `EXA_API_KEY` | 리서치 스킬, `ai-search`, `competitive-intel` |
| 페이지 읽기, 크롤, 추출 | Firecrawl | 무료 티어, 그다음 요금제 | `FIRECRAWL_API_KEY` | 리서치 스킬, `first-screen-check`, `site-audit` |
| 검색량, 검색 결과, 키워드 | 무료 기본은 네이버. DataForSEO는 구글 검색량의 선택 유료 | 쓴 만큼 | `DATAFORSEO_LOGIN`, `DATAFORSEO_PASSWORD` | `keyword-research`, `local-seo-plan`, `programmatic-seo` |
| 이미지와 GIF | GPT Image (OpenAI) | 이미지당 | `OPENAI_API_KEY` 또는 `REPLICATE_API_TOKEN` | `creative` |
| 영상 | Seedance (ByteDance)를 Higgsfield 또는 Replicate로 | 클립당 | `HF_API_KEY_ID` + `HF_API_KEY_SECRET`, 또는 `REPLICATE_API_TOKEN` | `creative` |
| 프레젠터·UGC형 광고 영상, 빠른 정적 광고 | Higgsfield Marketing Studio (CLI: `npm i -g @higgsfield/cli`, 그다음 `higgsfield auth login`) | 크레딧 요금제 | Higgsfield 로그인 | `creative` |
| 보이스와 보이스오버 | ElevenLabs | 무료 티어, 그다음 요금제 | `ELEVENLABS_API_KEY` | `creative` |
| 메타 광고 | Meta 공식 Ads MCP와 Ads CLI, 또는 Marketing API | 광고 계정이 있으면 무료 | `META_ACCESS_TOKEN` | `meta-ads`, `paid-ads` |
| 구글 광고 | Google Ads API | 무료 | `GOOGLE_ADS_*` (아래 광고) | `google-ads-tracking`, `paid-ads` |
| 네이버 검색광고·플레이스 광고 | 광고주 센터, 플레이스 관리자. 사람이 보고서를 내보냄 | 무료 | 없음. 계정에 로그인해서 내보내기 | `paid-ads`, `google-business-profile`, `performance-review` |
| 소셜 게시와 예약 | Zernio (API와 MCP, 약 18개 플랫폼) | 요금제 | `ZERNIO_API_KEY` | `social-content`, `content-atomizer`, `google-business-profile` |
| 많은 데이터 API, 키 하나 | treg | 호출당 | `TREG_TOKEN` | 계정 여러 개 없이 SERP, 소셜, 리드, 광고 데이터가 필요한 스킬 |
| 서치 콘솔 | Google | 무료 | 서비스 계정 / 본인 로그인 | `local-seo-plan`, `performance-review`, `keyword-research`, `site-audit` |
| 지역 업체 찾기 | 네이버 검색, 스마트플레이스, 카카오맵을 사람이 보고 적기 | 무료 | 없음 | `find-local-clients`, `pitch-the-fix`, `first-screen-check` |

무료가 먼저예요. 스킬이 유료 도구를 말하면 그 앞에 무료 방법을 주고, 도구가 보태는 것을 말해요. 이 팩은 유료 제안으로 보내지 않아요. 어떤 스킬도 유료 도구를 필요로 하지 않아요.

**파트너.** 일부 도구가 언급을 후원할 수 있어요. 파트너는 우리가 이미 쓰거나 어차피 말할 도구이고, 나오는 곳마다 ◆로 표시하며, 무료 경로나 더 나은 선택을 대체하지 않아요. 아직 파트너는 없어요.

아래는 스킬이 확인하는 순서의 툴셋이에요. 각각 무엇을 여는지, 없으면 무슨 일이 나는지, 어느 스킬이 쓰는지, 대략의 비용, 어디서 받는지. 달러 가격과 플랫폼 목록은 각 절이 다른 날짜를 말하지 않으면 2026-09-02에 확인했어요. 확인한 페이지는 맨 끝에 있어요. 2026-11-18에 한국 채널 기본값 (네이버, 카카오, 문자)을 앞에 두었고, 달러 가격을 원화로 환산하지는 않았어요. 견적 전에 판매자 페이지를 보세요.

지금 무엇이 살아 있는지 보려면 `/start-here`에 "뭘 추가하지"라고 하거나 `python3 <스킬 폴더>/start-here/scripts/capability.py --markdown`을 실행해요. 현재 목표에 가장 쓸모 있는 빠진 키 하나를 말하는 문장 하나, 한 번. 그다음 스킬은 기본에서 계속해요.

## 웹 스크랩 (`web-scrape`): Firecrawl (`FIRECRAWL_API_KEY`)

- 열리는 것: 모든 리서치 스킬의 전체 페이지, JS 렌더 읽기 (온보딩, 감사, 경쟁 해체, 키워드 검색 결과).
- 없으면: 에이전트의 WebFetch가 페이지를 요약으로 읽어요. 결과는 그렇게 표시돼요.
- 쓰는 스킬: /start-here, /brand-voice, /positioning-angles, /audience-research, /competitive-intel, /keyword-research, /seo-content, /ai-search, /landing-page, /programmatic-seo, /google-business-profile, /local-seo-plan, /service-area-pages, /reviews, /first-screen-check, /find-local-clients, /pitch-the-fix, /long-form-article, /site-audit
- 비용: 카드 없이 월 1,000크레딧 무료 티어. Hobby는 연 결제 기준 월 $16부터 5,000크레딧. 충전은 $5 단위. 온보딩 한 번은 페이지 읽기 몇백 회. [1]
- 받는 곳: firecrawl.dev 가입, https://www.firecrawl.dev/app/api-keys

## 웹 검색 (`web-search`): 내장

- 열리는 것: 라이브 검색 결과 (오늘 무엇이 올라오는지, 자동완성, 최근 플랫폼 변경). 한국 기본 읽기는 네이버 통합검색, 플레이스, 블로그, 카페, 지식iN이에요.
- 없으면: Claude Code, Codex, Cursor는 웹을 검색해요. 웹 검색이 없는 에이전트는 모델 지식으로 떨어지고 그렇게 말해요.
- 쓰는 스킬: /keyword-research, /seo-content, /competitive-intel, /ai-search, /positioning-angles, /lead-magnet, /google-business-profile, /local-seo-plan, /reviews, /find-local-clients, /long-form-article
- 비용: 없음. 에이전트에 포함.
- 받는 곳: 할 일 없음.

## 소셜 데이터 (`social-data`): ScrapeCreators (`SCRAPECREATORS_API_KEY`)

- 열리는 것: 오디언스 리서치, 경쟁 정찰, 소셜 캐논에 쓸 실제 게시, 댓글, 프로필, 자막, 광고 라이브러리. 로그아웃 공개 페이지가 보여 주는 것 대신.
- 없으면: WebFetch가 닿는 공개 페이지를 읽어요. 표본은 더 작고 그렇게 표시돼요. 인스타그램, 페이스북, 링크드인, X, 스레드의 로그인 벽은 기본에서 가져오지 마세요.
- 쓰는 스킬: /audience-research, /competitive-intel, /social-content, /content-atomizer
- 2026-09-02에 https://docs.scrapecreators.com 에서 확인한 플랫폼: Reddit, X, Instagram, TikTok, YouTube, LinkedIn, Threads, Facebook, Bluesky, Pinterest, Telegram, 그리고 Facebook, TikTok, Google, LinkedIn 광고 라이브러리. 스킬은 그 문서에 있는 엔드포인트만 호출해요. 네이버 블로그·카페는 이 키의 기본이 아니에요. 공개 페이지를 직접 읽어요.
- 비용: 만료되지 않는 종량 크레딧. 카드 없이 100크레딧. 25,000크레딧이 $47부터 (요청 1,000회에 약 $1.88). 대부분 엔드포인트는 요청당 1크레딧. 캐시된 결과는 무료. [2]
- 받는 곳: scrapecreators.com 가입. 키는 대시보드에 있어요.

## 크리에이티브 (`creative`): Replicate (`REPLICATE_API_TOKEN`)

- 열리는 것: 이미지·영상 생성과, 보여 주기 전에 브랜드 키트에 맞춰 점수를 매기는 비전 QA.
- 없으면: /creative가 아무 이미지나 영상 도구에 붙여 넣을 프롬프트를 써요. 대신 생성해 주지는 않아요.
- 쓰는 스킬: /creative, /paid-ads, /landing-page, /meta-ads
- 비용: 쓴 만큼, 모델별. 출력당 또는 영상 초당 (2026-11-13 기준 기본 1K 이미지 약 $0.07, 제작 영상 초당 약 $0.18에서 $0.40. 크리에이티브 스킬의 모델 레지스트리가 가격을 가져요). 일부 모델은 무료 체험 다음 결제. [3]
- 받는 곳: https://replicate.com/account/api-tokens

## 메시지와 이메일 (`esp`): 카카오·문자가 기본, Kit·beehiiv는 선택

- 기본: 카카오 알림톡 (정보성, 템플릿 검수), 친구톡 (광고성, 채널 친구), 문자 SMS/LMS, 그다음 이메일. 초안은 `./campaigns/<name>/`의 파일이고, 카카오비즈니스, 문자 대행사, 스티비, 메일리에 사람이 붙여 넣어요. 이 팩이 그 API를 대신 호출하지는 않아요.
- 키가 열면: 시퀀스와 뉴스레터 에디션을 리스트에 초안으로 푸시 (Kit: `KIT_API_KEY`. beehiiv: `BEEHIIV_API_KEY` + `BEEHIIV_PUBLICATION_ID`). /newsletter가 그 리스트의 클릭을 읽어요. Loops, Resend, Mailchimp, HubSpot 키 (`LOOPS_API_KEY`, `RESEND_API_KEY`, `MAILCHIMP_API_KEY`, `HUBSPOT_ACCESS_TOKEN`)는 감지되어 그 플랫폼 형식으로 맞추고 가져올 파일을 건네요.
- 없으면: 모든 메시지가 `./campaigns/<name>/emails/` 파일로 써져요. 제목 변형과 시점 포함. 사람이 붙여 넣어요.
- 쓰는 스킬: /email-sequences, /newsletter, /lead-magnet
- 비용: Kit는 구독자 10,000명까지 무료, 유료는 월 $33부터. 요금 페이지는 API를 유료 플랜에 두지만, Kit 도움말은 V4 키가 플랜으로 막히지 않는다고 해서 무료 플랜을 먼저 시도해요. beehiiv 무료 Launch (구독자 2,500명까지)에 API가 포함되고, Scale은 월 $43부터. [4][5] 원화 견적으로 바꾸지 마세요. 카카오·문자 요금은 각 대행사 화면을 확인해요.
- 받는 곳: Kit는 Settings, Developer, V4 Keys (https://app.kit.com/account_settings/developer_settings). beehiiv는 Settings, Workspace, API (https://app.beehiiv.com/settings/workspace/api. Owner 또는 Admin, 인증된 계정). Publication ID는 같은 페이지.

사용자를 대신해 발송하지 않아요. 푸시는 초안을 만들고, 스킬이 먼저 물어요. 광고성 정보에는 (광고), 보내는 이, 수신거부, 야간 21:00~08:00 별도 동의가 필요해요. 조문 번호는 단정하지 마세요.

## 분석 (`analytics`): GA4 서비스 계정 또는 PostHog, 읽기 전용

- 열리는 것: /performance-review가 붙여 넣은 내보내기를 기다리지 않고 실제 트래픽과 전환을 읽고, 배운 것을 `./brand/learnings.md`에 써서 다른 스킬이 써요. 지역 사업의 분모는 여전히 전화 대장, 예약, 스마트콜이에요. GA4가 그 분모를 대체하지 않아요.
- 없으면: CSV나 대시보드 스크린샷을 붙여 넣어요. 리뷰는 그것으로 돌아요.
- 쓰는 스킬: /performance-review, /keyword-research, /ads-incrementality-check
- 비용: GA4 API는 Google 계정으로 무료. PostHog는 월 이벤트 100만까지 무료, 그다음 종량. 카드를 넣지 않으면 무료 한도에서 멈춰서 청구가 갑자기 생기지 않아요. [6]
- 받는 곳: GA4는 Google Cloud에서 서비스 계정을 만들고 JSON 키를 받아 `GOOGLE_APPLICATION_CREDENTIALS`에 경로를 두고, 그 이메일을 GA4 속성의 Viewer로 추가 (`GA4_PROPERTY_ID`). PostHog는 https://us.posthog.com/settings/user-api-keys 에서 `POSTHOG_API_KEY` (+ `POSTHOG_PROJECT_ID`).

## 서치 콘솔 (`search-console`): Google 서비스 계정

- 열리는 것: 실제 쿼리, 노출, 클릭률이 키워드 리서치, 콘텐츠 새로 고침, 월간 리뷰에 들어가요. 네이버가 기본인 사이트는 네이버 서치어드바이저 내보내기가 같은 역할이에요. 둘을 한 검색시장처럼 섞지 마세요.
- 없으면: 키워드 작업은 라이브 검색 확인과 모델 지식 추정을 쓰고, 그렇게 표시해요.
- 쓰는 스킬: /performance-review, /seo-content, /keyword-research, /local-seo-plan, /service-area-pages, /site-audit
- 비용: Google 계정으로 무료.
- 받는 곳: GA4와 같은 서비스 계정 (`GOOGLE_APPLICATION_CREDENTIALS`). 그 이메일을 Search Console 속성의 사용자로 추가하고 `GSC_SITE_URL`을 설정해요. 네이버 서치어드바이저는 searchadvisor.naver.com에서 사람이 내보내요.

## Core Web Vitals: Google PageSpeed Insights (`PAGESPEED_API_KEY`, 선택 `CRUX_API_KEY`)

- 열리는 것: /site-audit가 홈과 핵심 템플릿의 폰 속도를 재요. Google에 실사용자 데이터가 있으면 그것을 써요.
- 없으면: 키 없는 PageSpeed 할당량은 공유되고 자주 소진돼서, 감사가 Core Web Vitals를 확인하지 못했다고 보고해요.
- 쓰는 스킬: /site-audit
- 비용: 무료. 2026-11-16 확인.
- 받는 곳: Google Cloud 콘솔에서 PageSpeed Insights API를 켜고 (실사용자 데이터는 Chrome UX Report API), Credentials에서 API 키를 만들어요.

## 광고 (`ads`): 메타 (`META_ACCESS_TOKEN`), 구글 광고 (`GOOGLE_ADS_DEVELOPER_TOKEN`), 네이버는 내보내기

- 열리는 것: /paid-ads가 실제 캠페인, 광고 세트, 소재 성과를 읽어 중단·확대·반복을 판단해요. /google-ads-tracking이 전환 설정을 읽어요. /meta-ads가 캠페인을 일시정지로 만들고 픽셀과 Conversions API를 확인해요. /ads-incrementality-check가 중단 테스트용 지출과 전환을 가져와요. /performance-review가 진단에 지출을 넣어요.
- 네이버 검색광고, 플레이스 광고, 브랜드검색은 광고주 센터와 플레이스 통계를 사람이 내보내는 것이 무료 경로예요. 이 팩이 네이버 광고 계정에 쓰지 않아요. 당근 비즈프로필은 지역 보조예요.
- 없으면: 광고 관리자나 구글 광고 화면의 내보내기·스크린샷, 전화 시스템의 통화 기록이나 CSV를 붙여 넣어요. 광고 매트릭스, 추적 감사, 중단 테스트, 정책 점검은 그래도 돌아요.
- 쓰는 스킬: /paid-ads, /google-ads-tracking, /ads-incrementality-check, /meta-ads, /performance-review
- 비용: 두 API 모두 무료. 광고비는 따로예요. Google Ads는 관리자 계정의 개발자 토큰이 필요하고 basic access는 짧은 심사 뒤예요. Meta는 Marketing API가 있는 앱과 광고 계정의 토큰이 필요해요.
- 받는 곳: Meta는 developers.facebook.com에서 앱을 만들고 Marketing API에서 액세스 토큰. Google Ads는 관리자 계정, 도구, API 센터, 개발자 토큰. 읽기에는 OAuth와 계정 id도 필요해요. `GOOGLE_ADS_CLIENT_ID`, `GOOGLE_ADS_CLIENT_SECRET`, `GOOGLE_ADS_REFRESH_TOKEN`, `GOOGLE_ADS_LOGIN_CUSTOMER_ID` (관리자 계정), `GOOGLE_ADS_CUSTOMER_ID` (광고 계정). Google Cloud와 Google Ads에서.

여기서 돈을 쓰지 않아요. 스킬은 읽어요. 변경은 광고 플랫폼에서 사용자가 승인해요. 플레이스홀더 계정 id는 `act_123`, `AW-123456789`처럼 가짜로 보여야 해요. 실제처럼 보이는 숫자는 쓰지 마세요.

## 소셜 API (`social-api`): X (`X_BEARER_TOKEN`)

- 열리는 것: /social-content가 자신의 과거 글을 채점해서, 패턴 라이브러리가 그 오디언스가 실제로 반응한 것을 배워요.
- 없으면: 붙여 넣은 상위 글이나 가져올 수 있는 공개 프로필로 일해요. 한국 채널 (블로그, 인스타, 스레드, 유튜브 쇼츠)은 공개 페이지와 사용자가 붙여 넣은 성과가 기본이에요.
- 쓰는 스킬: /social-content, /performance-review
- 비용: X API는 무료 티어 없는 종량. 게시 읽기 $0.005, 게시 작성 $0.015 (링크가 있으면 $0.20). 크레딧은 선불. 혼자 쓰는 계정은 대부분 한 달에 몇 달러. [7]
- 받는 곳: https://console.x.com 에서 프로젝트와 앱을 만들고 bearer token.

## 예약 (`scheduling`): Zernio (`ZERNIO_API_KEY`), Buffer (`BUFFER_ACCESS_TOKEN`) 또는 Hootsuite (`HOOTSUITE_API_KEY`)

- 열리는 것: 쪼갠 글과 소셜 초안이 복사 붙여 넣기 대신 예약 대기열로 가요.
- 없으면: 모든 글이 `./campaigns/`의 플랫폼별 파일로 써져요. 사람이 스케줄러에 붙여 넣어요.
- 쓰는 스킬: /content-atomizer, /social-content
- 비용: Buffer 무료는 채널 3개, 채널당 예약 10개, API 키 포함 (월 3,000요청). Essentials는 채널당 월 $5부터. Hootsuite Standard는 연 결제 월 $99부터, 14일 체험. [8][9]
- 우리의 선택: Zernio. API와 MCP 하나, 약 18개 플랫폼 (zernio.com). 채널이 몇 개면 Buffer가 무료 선택.
- 받는 곳: Buffer는 https://publish.buffer.com/settings/api. Hootsuite는 hootsuite.com 개발자 포털에서 앱 생성.

예약은 여기서 라이브 계정을 건드리는 유일한 행동이에요. 스킬은 항상 글을 보여 주고, 대기열에 넣기 전에 물어요. 자동 게시는 없어요.

## 앱 여러 개를 연결 하나: Composio (`COMPOSIO_API_KEY`)

- 열리는 것: 여러 앱의 로그인을 계정 하나가 가져요. Composio가 OAuth를 맡고 Claude Code에 MCP로 앱을 열어서, 플랫폼마다 키를 모으지 않아요. 2026-09-02 툴킷 디렉터리에서 확인 (앱 1,000개 이상, 그날 툴킷 1,452개): Kit, beehiiv, Mailchimp, HubSpot (이메일). Google Analytics, PostHog (분석). Google Search Console. Meta Ads, Google Ads. Buffer (예약). X (social-api. Composio는 2026년 2월부터 자체 X 자격 증명을 주지 않아서, 자신의 X 개발자 앱을 가져오고 X 종량 요금은 그대로). 안 보임: Hootsuite. 카카오 비즈메시지와 네이버 검색광고는 이 연결의 기본이 아니에요.
- 없으면: 아무것도 바뀌지 않아요. 위 툴셋은 각자 네이티브 키나 기본에서 동작해요.
- 쓰는 스킬: 위 절에서 네이티브 키가 없는 툴셋의 스킬. /email-sequences, /newsletter, /performance-review, /keyword-research, /seo-content, /paid-ads, /social-content, /content-atomizer.
- 비용: 카드 없이 월 도구 호출 100,000, 연결 계정 무제한 무료 티어. Pro는 월 $29부터. 상한이 있어서 청구가 갑자기 생기지 않아요. 뒤의 앱은 자기 요금을 유지해요. [10]
- 받는 곳: 가장 단순한 길은 `claude mcp add --transport http composio https://connect.composio.dev/mcp` 다음 열리는 로그인. 그 경로에는 키가 필요 없어요 (명령 형태는 Composio의 Claude Code 페이지, URL은 Claude 설정 페이지). 키 경로는 https://dashboard.composio.dev 에서 `COMPOSIO_API_KEY`를 만들어 `.env`에 둬요.
- 자리: 키 다섯 개를 관리하고 싶지 않으면 Composio를 한 번 연결해요. 스킬은 네이티브 키가 없는 위 툴셋의 제공자로 봐요. 둘 다 있으면 네이티브 키가 이겨요.

## 네이버 스마트플레이스와 구글 비즈니스 프로필

폴더 id는 `google-business-profile`로 남아요. 일은 네이버 플레이스예요.

- 열리는 것: /google-business-profile과 /reviews가 공개 검색이 보여 주는 것 대신, 사람이 연 플레이스 관리자 (업종, 서비스, 사진, 소식, 리뷰와 답글, 예약, 스마트콜)에서 일해요. 구글 프로필은 외국인이나 구글 검색이 필요할 때의 보조예요.
- 없으면: 스킬이 로그인 없이 열리는 검색 결과와 리뷰 화면을 읽고, 못 본 사실을 말해요.
- 쓰는 스킬: /google-business-profile, /reviews, /local-seo-plan, /performance-review
- 비용: 무료. `.env` 키 없음. 사용자 (또는 클라이언트)가 관리자에서 내보내거나 붙여 넣고, 통계 스크린샷을 공유해요.
- 받는 곳: 네이버 스마트플레이스 관리, 플레이스 소유자 또는 관리자 로그인. 구글은 business.google.com, 소유자 또는 관리자.

## 통화 기록과 리드 내보내기: 이미 가진 파일, 무료

- 열리는 것: /speed-to-lead가 놓친 전화와 회신 시간을 세고, /ads-incrementality-check가 중단 테스트의 분모로 전화 대장을 써요. 플레이스 통화 클릭과 스마트콜은 플랫폼 주장이에요. 분모가 아니에요.
- 없으면: 스킬이 일주일 치를 손으로 묻고, 결과를 작은 표본이라고 표시해요.
- 쓰는 스킬: /speed-to-lead, /ads-incrementality-check, /performance-review
- 비용: 무료. CSV를 내보내는 전화 시스템이나 CRM (날짜, 시각, 발신, 받음 또는 놓침, 통화 시간).

## 검색량: 네이버가 무료, DataForSEO는 선택 유료

- 무료 경로: 네이버 자동완성, 연관검색어, 네이버 데이터랩, 네이버 검색광고 키워드도구 (광고주 센터에서 검색량 구간을 무료로). `scripts/suggest.py`는 구글 자동완성 도우미예요. 한국어 구글 제안은 `--lang ko`. 이 스크립트가 네이버를 조회한다고 말하지 마세요. 서치 콘솔이 연결되면 구글 쿼리를 보태요. 검색량 없이 주제를 순위 매기고, 추정 검색량에는 `~`와 확인 표시를 해요. 키워드도구 값은 구간이지 정확한 월간 검색수가 아니에요.
- DataForSEO가 여는 것: /keyword-research와 /local-seo-plan의 구글 월간 검색량. 네이버 구간을 대체하지 않아요.
- 비용 (2026-11-13 확인): 구독 없이 쓴 만큼. 만료되지 않는 최소 충전 $50, 가입 시 체험 크레딧 $1. [11]
- 받는 곳: app.dataforseo.com 등록, 대시보드의 API 로그인과 비밀번호.

## 지역 업체를 찾고 제안하기: 무료 수기 확인

- 기본: /find-local-clients, /first-screen-check, /pitch-the-fix가 무료 데이터로 같은 일을 해요. 누구나 보는 평점, 리뷰 수, 사이트, 사장님 답글. 네이버 검색, 스마트플레이스, 카카오맵을 사람이 보고 적어요. 구글 지도 스크레이퍼는 쓰지 마세요.
- 선택: `places_search.py`는 구글 플레이스 도우미예요. 기본이 아니에요. 무료 경로가 같은 답을 손으로 얻어요.
- 쓰는 스킬: /find-local-clients, /pitch-the-fix, /first-screen-check
- 비용: 없음.
- 예의: 상호와 이름으로 시작, 밤 연락 금지, 짧은 정중한 제안, 과장된 성과 약속 금지, 먼저 고칠 문제 하나.

## 위에 절이 없는 우리의 선택

- **Exa** (`EXA_API_KEY`): 에이전트용 의미 웹 검색. 키워드 검색이 놓치는 페이지를 찾고 깨끗한 텍스트를 돌려줘요. exa.ai.
- **GPT Image** (`OPENAI_API_KEY`): OpenAI 이미지 모델. 직접 또는 Replicate. platform.openai.com. 최신 모델 이름과 가격은 크리에이티브 스킬의 레지스트리를 봐요.
- **Higgsfield** (`HF_API_KEY_ID`, `HF_API_KEY_SECRET`): 이미지·영상 모델 여러 개를 API 하나. Seedance 포함. 쓴 만큼. higgsfield.ai.
- **ElevenLabs** (`ELEVENLABS_API_KEY`): 영상 광고와 토킹 헤드의 보이스오버와 보이스 클로닝. elevenlabs.io.
- **Meta 공식 Ads MCP와 Ads CLI**: 에이전트가 Meta 자신의 커넥터로 광고를 읽고 관리. Meta Business Suite, 설정, 연동, Ads MCP. developers.facebook.com (Ads AI Connectors).
- **Zernio** (`ZERNIO_API_KEY`): API와 MCP 하나로 약 18개 플랫폼에 게시·예약. Google Business Profile, Facebook, Instagram, LinkedIn, X 포함. zernio.com.
- **treg** (`TREG_TOKEN`): 토큰 하나, MCP 하나로 데이터 엔드포인트 (SEO, 소셜, 리드, 광고, 스크랩)에 호출당 과금. 계정 다섯 개를 열고 싶지 않을 때. treg.to.

## 일부러 넣지 않은 것

AI 가시성 측정 서비스 (어느 AI가 얼마나 인용하는지)는 이 팩에 없어요. 로컬에서 돌리는 스킬이 아니라 호스팅 구독에 속해요. /ai-search는 답을 라이브로 확인하고, 점유율 숫자는 모델 지식 추정이라고 표시해요. 순위 추적기도 같은 이유로 빠졌어요. 검색량 API는 스킬이 무료 경로 다음에 선택으로 말할 수 있는 유일한 유료 검색 데이터 도구예요.

영어권 인용 통계 (레딧 비중, AI Overview CTR, 미국 맵팩)는 한국 사실이 아니에요. 네이버 Cue:, 네이버 AI 브리핑, 블로그, 카페, 지식iN, 뉴스, 유튜브를 따로 봐요.

## 가격이 온 곳 (다른 날짜가 없으면 2026-09-02 확인)

1. Firecrawl: https://www.firecrawl.dev/pricing
2. ScrapeCreators: https://scrapecreators.com/ (홈의 가격). 문서 https://docs.scrapecreators.com
3. Replicate: https://replicate.com/pricing 와 https://replicate.com/docs/topics/billing
4. Kit: https://kit.com/pricing 와 https://help.kit.com/en/articles/9902901-kit-api-overview
5. beehiiv: https://www.beehiiv.com/pricing 와 https://www.beehiiv.com/support/article/13091918395799-how-to-access-your-publication-id-or-api-keys
6. PostHog: https://posthog.com/pricing
7. X API: https://docs.x.com/x-api/getting-started/pricing
8. Buffer: https://buffer.com/pricing 와 https://developers.buffer.com/
9. Hootsuite: https://www.hootsuite.com/plans
10. Composio: https://composio.dev/pricing. 툴킷 디렉터리 https://composio.dev/toolkits. Claude Code 설정 https://composio.dev/toolkits/composio/framework/claude-code 와 https://composio.dev/claude

11. DataForSEO (2026-11-13 확인): https://dataforseo.com/pricing

가격은 바뀌어요. 여기 숫자가 이상하면 판매자 페이지가 이겨요. 달러 금액을 원화 견적으로 쓰지 마세요.

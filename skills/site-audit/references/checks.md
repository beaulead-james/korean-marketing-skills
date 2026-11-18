# 점검. 각 발견의 의미와 고치는 법

3단계에서, 어떤 발견을 상위 목록에 넣을지 정하기 전에 읽으세요. 각 항목은 `findings.json`에 나오는 발견 id, 기본 심각도, 크롤러가 실제로 본 것, 올리거나 내릴 때, 알려진 사각, 수정을 줍니다. id와 심각도는 작업 어휘입니다. 고객 보고서에는 나오지 않습니다.

심각도. critical (구글·네이버나 손님이 사이트 또는 돈 되는 페이지에 닿지 못함), high (중요한 페이지의 가시성을 깎음), medium (실재하지만 범위가 있음), low (편할 때 할 가치), info (사실이나 선택이지 문제가 아님). 돈 되는 페이지가 걸리면 여러 점검이 한 단계 올라갑니다. 발견의 `key_pages_affected`가 몇 장인지 말합니다.

스크립트는 Googlebot 기준으로 아래 id를 만듭니다. Yeti는 이 id에 없습니다. Yeti의 `/` 금지는 네이버 쪽에서 critical로 손으로 올리세요.

## 수집과 색인

- **homepage_unreachable** (critical). 홈이 크롤러에게 HTML로 2xx를 주지 않았습니다. 보고 전에 브라우저에서 여세요. 거기서는 되면 서버나 CDN이 모르는 크롤러를 거절하는 것이고, 다른 발견입니다 (어느 쪽인지 말하세요). 호스팅, 방화벽, 도메인을 먼저 고치세요. 열리기 전에는 다른 것이 중요하지 않습니다.
- **tls_error** (critical). 인증서 확인이 실패했습니다. 브라우저도 경고 페이지를 보여 손님이 떠납니다. 갱신하거나 다시 설치하세요. www와 맨 도메인 둘 다.
- **not_https** (critical). 최종 홈 주소가 http입니다. 호스트나 CDN에서 HTTPS를 켜고 모든 http URL을 한 번에 넘기세요.
- **host_variants** (high. 변형이 한 번이 넘게 건너뛰면 low). http, https, www, 맨 도메인 중 일부가 대표 주소로 끝나지 않습니다. 스스로 답하는 변형은 복제 사이트입니다. 변형마다 301 하나.
- **robots_unreachable** (critical). robots.txt가 5xx, 429, 또는 무응답. 구글은 robots.txt가 오류인 동안 크롤을 멈춥니다 (자세한 것은 `crawler-facts.md`, 구글 규칙). 깨끗한 404는 괜찮고 오류는 아닙니다. 네이버가 같은 시간 규칙을 쓴다고 말하지 마세요. 파일이 죽으면 서치어드바이저에서 수집이 멈췄는지를 확인하라고 하세요.
- **robots_is_html** (medium). /robots.txt가 웹 페이지를 돌려줍니다. 보통 CMS의 포괄 처리. 구글은 규칙을 못 찾아 아무것도 안 막히지만, 아무것도 선언되지 않습니다.
- **robots_missing** (low). robots.txt 없음. 크롤러는 모두 허용으로 봅니다. 비용은 사이트맵을 선언하지 않는 것뿐입니다. 상위 목록에 넣지 마세요.
- **robots_too_large** (medium). 500KiB 초과. 구글은 나머지를 무시합니다. 구글 한도입니다.
- **robots_blocks_google** (critical). Googlebot이 `/`를 가져오지 못합니다. 보통 스테이징 규칙(`Disallow: /`)이 실서버에 나간 것입니다. 관찰이 규칙을 인용합니다. Yeti에게 같은 규칙이 있으면 네이버 critical로 따로 적으세요.
- **robots_blocks_pages** (high, 돈 되는 페이지면 critical). Googlebot이, 적어도 두 페이지에서 링크되거나 사이트맵에 있거나 핵심인 페이지에서 막힙니다. 관리자, 장바구니, 계정, 검색 경로는 일부러 뺍니다. 차단은 크롤을 멈추지 색인을 멈추지 않습니다. 막힌 URL은 설명 없이 결과에 남을 수 있습니다.
- **robots_blocks_resources** (medium). 사이트의 CSS나 자바스크립트가 Googlebot에게 막힙니다 (종종 /wp-includes/의 옛 워드프레스 규칙). 구글이 레이아웃 없이 페이지를 그립니다.
- **noindex_key_pages** (critical). 돈 되는 페이지, 또는 거의 모든 페이지가 meta robots, googlebot 메타, X-Robots-Tag에 noindex를 가집니다. 거의 모든 페이지가 noindex면 스위치 하나를 찾으세요. 워드프레스 설정, 읽기, "검색 엔진이 이 사이트를 색인하지 못하도록". 호스트의 스테이징 설정. 글 유형의 SEO 플러그인 기본값. Wix, Squarespace, Webflow는 페이지 SEO 설정에 검색에서 숨기기가 있습니다. 그다음 구글 서치 콘솔과 네이버 서치어드바이저에서 대표 페이지 수집을 요청하세요.
- **noindex_pages** (medium). 그 외 noindex 페이지. 의도인 경우가 많습니다 (감사 페이지, 끝난 행사). 나열하고 사장님이 확인하게 하세요. 이유 없이 높게 두지 마세요.
- **soft_404** (medium). 만든 URL이 200과 페이지로 답했습니다. 구글은 이것을 소프트 404로 부르고 진짜 얇은 페이지도 같이 볼 수 있습니다. 서버는 모르는 URL에 404를 주되 친절한 페이지는 보여 주세요.
- **js_rendered_content** (대부분이거나 홈이면 high, 아니면 medium). HTML에 단어가 50개 미만이고 스크립트를 불러오거나, 빈 `#root`나 `#__next` 같은 앱 뿌리가 있는 페이지. 본문 점검은 이 페이지를 건너뜁니다. 본문에 대해 말하기 전에 렌더된 HTML로 다시 돌리세요. 수정은 서버 렌더나 사전 렌더입니다. 프레임워크 문서가 설정을 부릅니다. 빈 HTML은 네이버 수집에도 할 말이 없습니다.
- **meta_refresh** (medium). meta refresh 리다이렉트. 301로 바꾸세요.

## 사이트맵

스크립트는 읽은 사이트맵(색인과 gzip 포함)을 파싱하므로, 이 발견은 URL이 존재하는지가 아니라 파일의 실제 내용에 있습니다.

- **sitemap_missing** (medium). robots.txt에 없고 /sitemap.xml이나 /sitemap_index.xml에도 없음. 내부 링크가 좋은 작은 사이트는 그래도 찾아지므로, 상위 셋에 들어가는 일은 드뭅니다. 대부분 CMS와 SEO 플러그인이 하나를 만듭니다. 구글 서치 콘솔과 네이버 서치어드바이저에 제출하고 robots.txt에 적으세요.
- **sitemap_unparseable** (high). 적힌 사이트맵이 열리지만 사이트맵이 아닙니다 (HTML, 깨진 XML, DOCTYPE). 구글이 쓸 수 없습니다. 네이버도 같은 파일을 못 읽으면 수집 요청이 비게 됩니다.
- **sitemap_errors** (low). 파싱은 되는데 문제. 다른 호스트 URL, https 사이트의 http, 미래 lastmod, URL 없는 항목.
- **sitemap_not_in_robots** (low). 한 줄 수정.
- **noindex_in_sitemap** (high, 돈 되는 페이지면 critical). 사이트맵은 "색인하라"고 하고 페이지는 "하지 말라"고 합니다. 페이지마다 어느 쪽이 맞는지 정하세요. 개수는 이번 실행이 가져온 사이트맵 URL입니다. 큰 사이트맵은 표본입니다.
- **sitemap_non_200** (리다이렉트면 medium, 오류면 high). 사이트맵이 리다이렉트, 404, 오류 URL을 실었습니다. 최종 URL만 적으세요.
- **sitemap_blocked_by_robots** (high). Googlebot에게 robots.txt가 막는 URL이 실려 있습니다.
- **sitemap_canonicalized** (medium). 적힌 URL의 canonical이 다른 페이지를 부릅니다.
- **indexable_not_in_sitemap** (low). 링크로 찾은 색인 가능 페이지가 사이트맵에 없음. 크롤과 사이트맵을 둘 다 끝까지 읽었을 때만 보고됩니다.

## Canonical

- **canonical_conflict** (high). 한 페이지에 서로 다른 canonical 둘 (태그 둘, 또는 태그와 Link 헤더가 불일치). 보통 플러그인 둘, 또는 테마와 플러그인.
- **canonical_to_bad_target** (high, 돈 되는 페이지면 critical). canonical이 리다이렉트, 오류, noindex URL을 가리킵니다.
- **canonical_off_site** (high. 홈이면 critical). canonical이 다른 도메인을 부릅니다. 콘텐츠를 일부러 신디케이션한 것이 아니면 스테이징 호스트, 옛 도메인, 다른 사이트에서 복사한 템플릿을 보세요.
- **canonical_elsewhere** (medium, 돈 되는 페이지면 high). 페이지가 이 사이트의 다른 페이지를 canonical로 불러, 구글에게 다른 쪽을 색인하라고 합니다. 파라미터 URL이 깨끗한 버전을 가리키는 것은 예상되어 빠져 있습니다.
- **canonical_missing** (low). canonical 없음. 구글이 하나를 고릅니다. 위생이지 수정이 아닙니다.
- **canonical_relative** (info). 동작하지만 절대 URL이 더 안전합니다.

## 링크와 상태 코드

- **broken_internal_links** (high. 메뉴, 홈, 또는 사이트의 절반에 있으면 critical). 대상이 4xx나 5xx인 내부 링크. 크롤에서, 또는 크롤하지 않은 많이 링크된 대상의 추가 확인에서. 발견은 각 대상에 몇 페이지가 링크하는지 나열합니다. 메뉴 링크를 한 번 고치면 사이트 전체가 고쳐집니다.
- **server_errors** (high). 5xx로 답한 URL. 보고 전에 브라우저에서 하나 여세요. 크롤 중의 일시 장애일 수 있습니다.
- **redirect_loop** (high). 끝나지 않습니다.
- **redirect_chains** (medium). 두 번 이상 건너뜀. 옛 URL을 최종 페이지로 바로 보내세요.
- **internal_links_to_redirects** (low). 리다이렉트되는 URL로의 링크. http, 빠진 슬래시, 옛 경로. 메뉴와 푸터부터.
- **orphan_pages** (medium. 크롤이 한도에서 멈추면 low). 사이트맵에는 있는데 크롤한 페이지가 링크하지 않음. 잘린 크롤에서는 약한 증거입니다. 그렇다고 말하세요.
- **deep_pages** (low). 홈에서 세 클릭이 넘음.
- 크롤러를 거절한 페이지(401, 403, 429)나 답이 없는 페이지는 `not_checked`에 있고, 깨진 것이 아닙니다. 사람과 구글에게는 열릴 수 있습니다.

## 페이지 위

- **title_missing** (high, 돈 되는 페이지면 상승). 색인 가능 페이지에 title 없음.
- **title_duplicate** (medium). 여러 페이지가 제목을 공유. 보통 템플릿 기본값. 구 이름만 다른 제목 묶음은 네이버 유사 문서의 신호일 수 있습니다. 본문도 보면 /service-area-pages로 보내세요.
- **title_length** (low). 60자 초과 또는 30자 미만. 화장. 구글은 많은 제목을 다시 씁니다. 상위 다섯 수정이 아닙니다.
- **description_missing**, **description_duplicate** (low). 스니펫을 만들고 순위를 만들지 않습니다.
- **h1_missing** (medium). 글이 있는 페이지에 H1 없음.
- **h1_multiple**, **heading_structure** (info). 대부분 사이트에서 괜찮음.
- **viewport_missing** (high, 돈 되는 페이지면 상승). 모바일 뷰포트 메타가 없어 휴대폰이 축소된 데스크톱을 그립니다.
- **lang_missing** (info). 한국어 사이트는 `lang="ko"`가 맞습니다. 없다고 상위 수정으로 올리지 마세요.
- **images_missing_alt**, **images_missing_dimensions** (low). **images_legacy_formats** (info). 추적 픽셀과 noscript 대체는 무시됩니다.
- **anchor_text** (low). 글자 없는 내부 링크나 "여기" 클릭.
- **social_tags_missing** (low). og:title이나 og:image가 없는 핵심 페이지는 공유될 때 빈 미리보기입니다. 카카오톡 미리보기도 같은 태그에 기대는 경우가 많습니다.
- **url_hygiene** (info). 대문자, 밑줄, 매우 긴 URL. 이것만으로 작동하는 URL의 이름을 바꾸지 마세요.

## 본문

- **thin_content** (medium. 홈이거나 서비스·지역 페이지가 세 장 이상 얇으면 high). 색인 가능 페이지의 본문(메뉴와 푸터 제외)이 300단어 미만. 연락 페이지는 빠집니다. 단어 수는 대리입니다. 얇다고 부르기 전에 예시 하나를 읽으세요. 250단어에 가격 구간과 예약 양식이 있는 서비스 페이지는 일을 할 수 있습니다. 한국어는 단어 수가 영어와 다르므로, 숫자만으로 저품질이라고 단정하지 마세요.
- **duplicate_content** (medium. 돈 되는 페이지면 high). 색인 가능 페이지 둘 이상의 본문이 같음.
- **near_duplicate_content** (medium). 본문 지문이 거의 같은 페이지 쌍. 고전은 구 이름만 바꾼 페이지입니다. 다시 쓰기는 `/service-area-pages`로. 네이버 유사 문서·저품질 위험이라고 보고서에 쉬운 말로 적으세요.
- **content_no_dates**, **content_stale**, **content_no_author**, **content_no_answer_capsules**, **content_thin_evidence** (low). 300단어 이상 글에 대해 보고됩니다. `site.content_signals`가 크롤한 글 전체의 요약입니다. 보이는 날짜 비율, 중앙 나이, 저자 비율, 100단어당 통계, 인용문, 외부 출처, 질문형 제목과 짧은 답. /seo-content 새로고침의 브리프에 쓰고, 사이트의 사업이 콘텐츠인 경우가 아니면 상위 목록 항목으로 쓰지 마세요.

## AI 로봇 접근

`site.ai_crawlers`가 각 로봇의 robots.txt 상태(허용, 일부, 차단), 그룹이 이름을 부르는지 `*`를 따르는지, 결정 규칙을 가집니다. `site.edge_check`가 CDN 비교를 가집니다. 각 로봇이 하는 일은 `crawler-facts.md`입니다. Yeti는 이 블록에 없습니다.

- **ai_search_blocked** (완전 차단이면 high, 일부면 medium). OAI-SearchBot, Claude-SearchBot, PerplexityBot이 robots.txt에서 막힘. 사업이 AI에 보이고 싶은지 확인한 뒤 그 그룹을 지우세요.
- **ai_user_fetch_blocked** (medium). ChatGPT-User, Claude-User, Perplexity-User가 막힘. 이 중 일부는 robots.txt를 무시할 수 있어 (사실 파일), 규칙보다 가장자리 차단이 더 중요할 수 있습니다.
- **search_engine_blocked** (high). Bingbot이 막혀 코파일럿 답도 줄어듭니다.
- **ai_blocked_at_edge** (high). 홈이 브라우저에는 200이고, 검색·비서 로봇 이름을 붙인 요청은 거절 (403, 429, 503, 챌린지, 거의 빈 페이지). 확신은 "대역 요청"입니다. 서버 힌트가 CDN을 보이면 거기서 볼 설정의 이름을 말하세요.
- **ai_training_blocked**, **ai_training_blocked_at_edge** (info). GPTBot, ClaudeBot, Google-Extended, CCBot 등 학습 로봇을 거부. 선택입니다. 한 번 언급해 사장님이 알게 하고, AI 검색에는 영향 없다고 말하세요. Yeti를 이 항목에 넣지 마세요.
- **llms_txt_missing** (info). 선택 위생.

## 구조화 데이터와 사업 개체

마크업을 권하기 전에 `schema-and-entity.md`를 읽으세요.

- **schema_parse_errors** (medium). 유효한 JSON이 아닌 JSON-LD는 모든 엔진이 무시합니다. 흔한 원인. 스크립트 태그 하나에 객체 둘을 붙임, 끝 쉼표, 안 닫힌 스크립트.
- **schema_problems** (low). @context나 기본 속성이 빠짐.
- **faq_markup_not_visible** (medium). 질문이 페이지 HTML 텍스트에 없는 FAQ 마크업. 자바스크립트가 더한 질문은 놓칠 수 있습니다. 보고 전에 렌더된 페이지를 확인하세요.
- **schema_dead_types** (info). HowTo 마크업.
- **org_schema_missing** (low). 홈이 Organization이나 LocalBusiness 마크업으로 사업을 부르지 않음.
- **entity_inconsistent** (low. 지역 사업에서 전화번호가 다르면 medium). 페이지마다 상호나 전화번호가 여럿. 콜트래킹 번호는 의도일 수 있습니다. 실수라고 부르기 전에 물어보세요.
- **sameas_missing**, **self_serving_reviews**, **no_structured_data** (info).

## 속도

- **slow_server** (medium). 감사를 돌린 곳에서 잰 서버 응답이, 페이지의 적어도 5분의 1에서 1.8초 초과. 장소 하나, 순간 하나. 그렇다고 말하세요.
- **cwv_poor** (medium. 홈이나 돈 되는 페이지면 high). 실제 방문 데이터의 75백분위가 구글의 나쁨 구간에 있는 LCP, INP, CLS. `cwv.pages[].opportunities`의 PageSpeed 기회가 가장 큰 레버를 부릅니다. 구글 기준입니다.
- **cwv_needs_improvement** (low). 중간 구간.
- **lab_slow** (low). 현장 데이터 없음. 시뮬레이션된 휴대폰 로딩이 느림. 실험실 데이터만으로 "손님이 기다린다"고 쓰지 마세요.

## 보안과 다국어

- **mixed_content** (스크립트, 스타일, 프레임이 http로 오면 high. 브라우저는 막습니다. 이미지와 미디어는 low).
- **hsts_missing** (low).
- **hreflang_issues** (medium). x-default 없음, 자기 자신을 안 적음, 언어 버전이 되링크하지 않음. hreflang을 쓰는 사이트에서만. 한국어만인 사이트에 억지로 넣지 마세요.

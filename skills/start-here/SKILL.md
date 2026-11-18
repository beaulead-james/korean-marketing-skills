---
name: start-here
description: 사이트와 고객이 남긴 말에서 사업을 약 3분 만에 읽고, 다른 스킬이 쓰는 브랜드 파일을 만든 뒤, 막연한 마케팅 요청을 맞는 스킬이나 워크플로로 보냅니다. 네이버 플레이스 중심의 지역 업체, 대행사 고객사 온보딩, 사이트 리뷰, 제안서 초안, 깊은 기초 조사도 여기서 고릅니다. 처음 실행할 때, 뭐부터 할지 모를 때, 새 고객사를 받을 때 쓰세요.
when_to_use: start here, get started, where do I start, what should I do next, set up my brand, set up my business, set up my marketing, onboard my business, help me with marketing, what's the plan, go deep, deep foundation, review my site, audit my site, what should I fix first, what should I add, which API keys, new client, onboard a client, switch client, agency status, status across clients, proposal for this prospect, remember that, show my checks, drop that check, 마케팅 어디서부터 하지, 브랜드 폴더 처음 만들기, 뭐부터 손대야 하는지, 신규 고객사 폴더 열기, 대행사 전체 현황, 이 가게 제안서 초안, 이 규칙 기억해 둬, 저장된 점검 항목 보여줘, 저장된 점검 항목 삭제, 심층으로 다시 조사, naver place 세팅은 뭐부터, kakao 채널은 뭐부터, alimtalk 도입은 뭐부터, powerlink 시작은 뭐부터
argument-hint: "[상호 | url | deep | audit | stack | 'new client <url>' | 'prospect <url>' | --brand <slug> | 마케팅 요청]"
metadata:
  boring:
    version: 1.0.0
    layer: foundation
    reads: [brand-manifest, learnings, assets]
    writes: [stack, brand-manifest, preferences, voice-profile, positioning, audience, voc, competitors]
    optional-keys: [FIRECRAWL_API_KEY, SCRAPECREATORS_API_KEY]
    enhances_with:
      - toolset: web-scrape
        gains: "the first run and audits read full pages instead of summaries"
      - toolset: social-data
        gains: "the deep foundation reads real posts and comments"
---

# 시작점

방금 들어온 마케팅 담당처럼 사업을 읽고 바로 일을 시작하세요. `brand.yaml`을 한 번 읽고, 질문은 한두 개가 한도이며, 가장 짧은 길로 맞는 스킬이나 워크플로에 보냅니다. 소프트웨어, 쇼핑몰, 크리에이터, 대행사, 지역 서비스업 모두 받습니다. 지역 업체는 네이버 스마트플레이스가 먼저이고, 카카오맵이 다음입니다. 구글 비즈니스 프로필은 외국인 손님이나 구글 검색도 원할 때의 덧붙임입니다. 말은 평문으로 통하고, 플래그는 지름길일 뿐 필수가 아닙니다. 이 파일은 바닥입니다. 상황이 더 나은 길을 가리키면 그 길을 가고, 이유를 한 줄로 말하세요.

고객 데이터는 워크스페이스의 브랜드 폴더에만 둡니다. 숫자는 출처가 있는 것만 씁니다. 없는 숫자는 지어 넣지 말고, 그림이 필요하면 예시라고 적습니다. 자동 발송과 자동 게시는 하지 않습니다. 광고 문안을 내보내기 전에는 표시광고법의 거짓·과장·기만·부당 비교, 그리고 정보통신망법상 광고성 정보 표시를 확인하라고 한 줄 경고합니다. 조문 번호는 단정하지 않습니다. 의료, 대부, 금융, 건강기능식품은 업종 심의와 금칙이 있으니 문안을 내보내기 전에 확인하라고만 경고합니다.

## 한국에서 먼저 보는 곳

유료 도구 전에 무료로 보는 순서입니다. 발견은 네이버 스마트플레이스, 그다음 카카오맵, 지도의 업종 검색, 플레이스 광고, 리뷰, 예약, 스마트콜입니다. 당근 비즈프로필은 동네 업종에 붙입니다. 글은 네이버 블로그, 카페, 지식iN, 인스타그램, 스레드, 유튜브 쇼츠입니다. 블로그 체험단은 대가성(광고·협찬·추천) 표시가 있어야 합니다. 키워드는 네이버 자동완성, 연관검색어, 네이버 데이터랩, 검색광고 키워드도구(광고주 센터에서 검색량 구간을 무료로 봄)가 본류입니다. 광고는 파워링크, 플레이스 광고, 브랜드검색, 메타(인스타·페이스북), 계정이 있을 때만 구글입니다. 메시지는 카카오 채널, 알림톡(정보성, 템플릿 검수), 친구톡(광고성, 채널 친구), 문자, 그다음 이메일입니다. 광고성 정보는 시작에 (광고), 보내는 이 명칭과 연락처, 수신거부, 밤 21시에서 08시는 별도 동의입니다. 모은 번호와 메일은 개인정보보호법 범위입니다. AI 답변은 네이버 Cue:, 네이버 AI 브리핑, ChatGPT, Perplexity, Google AI Overview입니다. 영어 웹의 인용 비율은 한국으로 옮기지 않습니다. 가격은 원이고, 혜택을 먼저 말하며, 첫 화면에는 하는 일·지역·약속·전화·카카오·예약이 있습니다. 한 업종은 한 상권입니다. `suggest.py`는 구글 자동완성 도우미입니다. 구글을 볼 때 언어를 한국어로 넘깁니다. 이 스크립트가 네이버를 조회한다고 말하지 않습니다.

```
python3 ${CLAUDE_SKILL_DIR}/../keyword-research/scripts/suggest.py --lang ko "대구 보일러"
```

## 맥락

`./brand/`, `./brands/`, `MARKETING.md` 중 하나라도 있을 때만 실행합니다. 없으면 불러올 것이 없습니다.

`python3 ${CLAUDE_SKILL_DIR}/scripts/brand_context.py --for start-here`

`${CLAUDE_SKILL_DIR}`는 이 스킬 폴더입니다. Claude Code 밖에서는 이 파일을 읽은 폴더를 씁니다. 예시는 `.agents/skills/start-here`입니다. 스크립트나 python3가 없으면 `./brands/active`가 가리키는 `./brands/<slug>/`를, 없으면 `./brand/`를 읽고 `brand.yaml`부터 봅니다. 둘 다 없으면 첫 실행입니다.

이 스킬 `scripts/`의 `brand_context.py`, `capability.py`, `route.py`는 다른 스킬이 `${CLAUDE_SKILL_DIR}/../start-here/scripts/...`로 부르는 공통 런타임입니다. `npx skills add`가 스킬 폴더만 복사하므로 여기에 둡니다.

## 모드 판별

먼저 맞는 것 하나만 탑니다.

1. **빠른 모드.** 산출물 하나를 콕 집습니다. "인스타 캡션 하나", "제목 5개", "이 리뷰에 답글". 조사도, 현황 보고도, 기초 조사 제안도 없이 그 스킬로 바로 갑니다. 빠른 모드는 이 파일의 다른 규칙보다 앞섭니다.
2. **이름 있는 모드.** 아래 표의 한 줄과 맞으면 그 절로 갑니다.
3. **조언.** "마케팅 계획을 어떻게 짜죠?"처럼 계획을 묻는 질문입니다. 요청과 브랜드 파일만으로 이 답변 안에서 답하고, 맞는 워크플로나 첫 실행을 한 줄로 제안합니다. 질문에는 조사를 돌리지 않습니다.
4. **대행사 모드.** `./brands/`가 있거나, 고객사를 지목하거나, brand 슬러그 인자가 있을 때. 대행사 모드를 보세요.
5. **첫 실행.** `./brand/`도 `./brands/`도 없습니다. 라이트 읽기를 합니다.
6. **재방문.** `./brand/`가 있습니다. `brand.yaml`을 한 번 읽습니다. 파일 목록, 신선도, 사업 사실, 캠페인. 재방문을 보세요.

| 하는 말 | 가는 곳 |
|---|---|
| 상호, URL, "사업 세팅", set up my business | 첫 실행, 라이트 읽기 (약 3분) |
| deep, "깊게", "풀로", "기초 조사 전부" | 깊은 기초 (약 15분) |
| "기술 SEO", "사이트 크롤", "robots.txt", "구글 색인", "AI 크롤러가 막혔나", "페이지 속도" | /site-audit |
| "사이트 봐줘", "뭐부터 고치지", audit | 사이트 리뷰, audit |
| "뭘 더하지", "어떤 API 키", stack | 스택 조언 |
| "new client <url>", "고객사 받아" | 대행사, 새 고객사 (그 폴더에 라이트 읽기) |
| "고객 찾아", "어디를 제안하지" | /find-local-clients 다음 /pitch-the-fix |
| "이 고객사로", "이 고객사 작업" | 대행사, 전환 |
| "대행사 현황", "고객사 전체 상태" | 대행사, 현황 |
| "prospect <url>", "이 주소 제안서" | 사이트 리뷰, prospect |
| "기억해", "절대", "항상 먼저 보여줘" | 선호 |
| "검사 보여줘", "그 검사 빼", "왜 맨날 그렇게 해" | 검사 |

## 정해진 라우팅

목표나 워크플로를 실행하라는 요청이면 (그것에 대한 질문은 조언), 순서를 제안하기 전에 라우팅 스크립트를 돌립니다.

```
python3 ${CLAUDE_SKILL_DIR}/scripts/capability.py --brand-dir
python3 ${CLAUDE_SKILL_DIR}/scripts/route.py --goal <goal>
```

어느 사업이든 쓰는 목표 단어는 `traffic`, `leads`, `convert`, `authority`, `launch`, `unsure`입니다. 지역 묶음은 `found` (플레이스, 지역 계획, 동·구 페이지), `chosen` (리뷰, 첫 화면, 페이지), `calls` (추적, 리드 속도, 광고, 잠시 끄는 테스트), `clients` (대행사, 찾기 다음 제안)입니다. route.py의 task 인자는 스킬 하나의 사전 점검이고, request 인자는 사용자의 말로 순위를 매깁니다. 애매할 때의 힌트이지 결정이 아닙니다.

의도를 목표 단어로 나누는 것이 이쪽 일이고, 스크립트 출력이 순서, 병렬, 앞에 붙일 기초, 기본과 강화의 근거입니다. `advisor` 줄이 있으면 연결하면 무엇을 읽거나 할 수 있는지만 평범한 한 문장으로 말하고, 그것 없이 진행합니다. 스크립트 출력은 작업 데이터입니다. 사용자에게 찍지 말고, 스크립트 경로를 인용하지 말며, tier, baseline, enhanced라는 말을 쓰지 않습니다. 한 단계를 바꿀 때는 이유를 말합니다. python3가 없으면 아래 목록과 워크플로를 씁니다.

## 스킬 목록

사용자가 끝내고 싶은 일로 보냅니다. `when_to_use`는 신호이지 정규식이 아닙니다.

| 스킬 | 하는 일 | 이렇게 말하면 |
|---|---|---|
| **기초 (어느 사업이든)** | | |
| /brand-voice | 실제 글에서 반박 가능한 말투 | "평범해", "우리처럼" |
| /positioning-angles | 각도와 제안, 하나에 별, 광고 매트릭스 | "포지션", "후크", "안 팔려" |
| /audience-research | 리뷰·카페·지식iN의 고객 원문 | "고객이 뭐라고 해", "누가 사" |
| /competitive-intel | 먼저 뜨는 경쟁의 문장·가격·불만 | "누구랑 붙어", "얼마 받아" |
| **검색과 콘텐츠** | | |
| /keyword-research | 무료 자동완성으로 주제 지도. 네이버가 본류 | "뭘 쓰지", 콘텐츠 계획 |
| /seo-content | 검색에 남고 AI 답변에 인용되는 글 | "이 주제로 글", "이 글 고쳐" |
| /programmatic-seo | 템플릿 하나와 실제 데이터로 많은 페이지 | "연동·지역·경쟁마다 페이지" |
| /ai-search | Cue:, AI 브리핑, ChatGPT, Perplexity에 이름이 있는지 | "챗지피티에 있어", "왜 AI는 쟤를 추천해" |
| /long-form-article | 숫자와 출처가 있는 긴 가이드 | "긴 가이드", "플레이북" |
| **페이지와 문안** | | |
| /direct-response-copy | 제목, 제안, 페이지와 채점 고리 | "카피", "판매 페이지", "팔리게" |
| /landing-page | 제안 하나의 페이지를 만들어 내보냄. 살아있는 페이지 해체 | "랜딩", "이 페이지 안 돼" |
| /lead-magnet | 연락처와 바꾸는 체크리스트·계산기·가이드 | "명단", "뭘 공짜로 주지" |
| **광고와 소재** | | |
| /paid-ads | 파워링크, 메타, 구글. 구조, 예산, 테스트 | "광고 돌려", "광고 문안" |
| /meta-ads | 메타 API, 캠페인, 추적이 실제로 도는지 | "페이스북 광고", "픽셀" |
| /google-ads-tracking | 전화와 문의가 전환으로 집계되게 | "광고가 전화를 안 세" |
| /ads-incrementality-check | 전화 기록이나 매출과 맞춘 일시정지 테스트 | "광고가 일하는 거야", "PMax가 가로채" |
| /creative | AI로 광고 이미지와 짧은 영상, 채점 | "광고 이미지", "쇼츠", "썸네일" |
| **메시지, 소셜, 측정** | | |
| /email-sequences | 환영, 육성, 출시, 견적 후속, 리뷰 부탁. 카카오·문자가 메일보다 앞 | "환영 메시지", "후속", "도달" |
| /newsletter | 브랜드 말투의 호. 형식과 전략 | "뉴스레터", "이번 호" |
| /social-content | 잘된 글에서 나온 인스타·스레드·블로그 원글 | "글 하나", "뭘 올리지" |
| /content-atomizer | 끝난 하나에서 플랫폼 2곳이나 3곳의 네이티브 글 | "이거 쪼개", "포스트로" |
| /performance-review | 실제 숫자를 넣고, learnings.md에 사전, 다음 행동을 냄 | "어때", "이 내보내기", 월간 |
| **지역 업체 묶음** | | |
| /google-business-profile | 폴더 이름은 그대로. 하는 일은 네이버 플레이스를 상위와 비교하고 한 달 글을 씀 | "플레이스에 안 떠", "스마트플레이스" |
| /local-seo-plan | 어떤 서비스와 동·구에 페이지를 둘지 | "네이버에 안 떠", "지역 SEO" |
| /service-area-pages | 동 이름만 바꾼 복붙이 아닌 지역 페이지 | "동마다 페이지" |
| /reviews | 영수증 리뷰 속도, 사장님 답글, 일 끝난 뒤 부탁. 가짜 리뷰는 안 함 | "리뷰가 적어", "악플 답글" |
| /first-screen-check | 폰에서 첫 화면의 전화, 하는 일, 지역, 약속 | "사이트에서 전화가 안 와" |
| /speed-to-lead | 놓친 전화, 늦은 답, 문자·카카오 회신 | "전화를 놓쳐", "리드가 식어" |
| **대행사 길** | | |
| /find-local-clients | 업종과 상권, 손님을 가장 많이 놓치는 곳부터 | "고객 찾아", "누구한테 제안해" |
| /pitch-the-fix | 대표를 찾고, 고장난 것 하나에 대한 짧은 제안 | "제안 써", "이 사장님께" |

갈림길입니다.

- 있는 글을 나누면 /content-atomizer, 원글은 /social-content, 이름이 붙는 긴 글은 /long-form-article, 검색용 글은 /seo-content.
- 지역 업체의 "전화가 더": 집계가 불명확하면 /google-ads-tracking이 먼저. 광고를 몇 달 했는데 사장님이 의심하면 /ads-incrementality-check. 전화는 오는데 놓치면 /speed-to-lead. 사이트에서 아무도 안 하면 /first-screen-check.
- "네이버에 안 떠": 플레이스 상위는 /google-business-profile, 일반 검색은 /local-seo-plan 다음 /service-area-pages. 페이지마다 큰 데이터면 /programmatic-seo, 실제로 일하는 동마다 한 페이지면 /service-area-pages.
- "리뷰": 받고 답하면 /reviews, 고객 말을 캐면 /audience-research.
- "글이랑 그걸 나눈 메시지"처럼 겹친 요청은 워크플로지, 첫 스킬로 보내는 것이 아닙니다.

깨끗하게 안 맞으면 가리는 질문을 하나 하고 보냅니다.

## 첫 실행, 라이트 읽기 (기본, 약 3분)

브랜드 폴더가 없습니다. 요청에 없으면 하나만 묻습니다.

> **상호를 말하거나 URL을 주세요.** 지역 업체는 시·구까지. 사이트와 고객이 한 말을 읽고 브랜드 파일을 쓴 다음, 먼저 할 일 하나를 말합니다. 약 3분. 에이전트가 물으면 웹 검색과 웹 가져오기를 허용해 주세요.

내 사업인지 고객사인지 모르면 같은 질문에 "사장님 건가요, 고객사인가요?"를 붙입니다. `preferences.md`에 `role: owner | agency | builder`를 남깁니다. "우리 가게"는 owner, "고객사"나 "new client"는 agency, 템플릿이나 데모는 builder. agency면 새 고객사 길로 갑니다.

예산은 약 3분, 웹 호출은 검색과 가져오기 합쳐 최대 8번, 서브에이전트는 없습니다. 리뷰 페이지 하나가 가져오기 한 번이고, 페이지를 넘기지 않습니다. 로그인 벽(인스타, 페이스북, 링크드인 글, x.com, 스레드, 카카오 단톡)은 가져오지 않습니다. 첫 검색이 거절되면 사용자가 말한 것만으로 파일을 쓰고 `Data: MODEL KNOWLEDGE`라고 달며, voc.md는 만들지 않고 그 사실을 말합니다.

1. **뼈대.** `./brand/`에 `brand.yaml`(name, slug, url), 빈 `assets.md`, `learnings.md`를 만듭니다. 워크스페이스 루트의 `README.md`, `MARKETING.md`, `docs/`, `content/`, 사이트 소스를 보고 있는 것은 `Data: LOCAL DOCS`로 남깁니다. 아직 안 낸 계획은 의도이지 사실이 아닙니다.
2. **찾기 (검색 1).** 상호, 지역 업체는 지역까지. 사이트, 별점, 리뷰가 어디 있는지. 네이버 플레이스가 먼저, 카카오맵이 다음입니다.
3. **사이트 (가져오기 2번이나 3번).** 홈, 대표 서비스, 필요할 때만 하나 더(가격, 지역 업체는 연락처나 지역 페이지). 무엇을 파는지, 누구에게, 첫 화면의 약속과 증거, 제안, 지역 업체는 전화·영업시간·시·구·동.
4. **고객의 말 (가져오기 1번이나 2번).** 지역은 검색 결과에 보인 네이버 별점과 리뷰 수를 그대로 말하고, 로그인 없이 열리는 리뷰 한 페이지. 소프트웨어는 블로그·카페 후기, 앱이면 스토어. 쇼핑몰과 크리에이터는 상품 후기, 후기 페이지, 공개 글. 원문 5줄에서 10줄과 URL. 칭찬, 불만, 문제를 부르는 말. 영어권에만 파는 제품만 G2나 Capterra를 봅니다.
5. **먼저 뜨는 곳 (검색 1).** 지역은 `<업종> <시·구>`, 네이버 플레이스나 상위 결과 3곳에서 5곳과 보일 때의 별점. 그 외는 문제 검색이나 `<카테고리> 대안` 3곳에서 5곳. 라이트 읽기에서는 그 사이트를 가져오지 않습니다.
6. **핵심 파일.** 각각 짧게, 머리에 `Depth: lite`와 데이터 라벨.
   - `brand.yaml`의 `brand:` 블록에 `category`, `depth: lite`, `services`, 지역이면 `phone`, `city`, `service_area`, `rating`(본 그대로, 출처와 날짜). 모든 스킬이 brand_context.py로 이 블록을 봅니다. `files:` 항목도 넣습니다.
   - `voice-profile.md`. 말하는 방식, 고객 말, 피할 말. 10줄에서 20줄.
   - `audience.md`. 누가, 어떤 일로, 무엇이 검색이나 전화를 일으키는지.
   - `voc.md`. URL이 있는 원문만. 읽은 것이 없으면 파일을 만들지 않습니다.
   - `positioning.md`. 지금 약속, 고객이 가장 칭찬하는 것, 그 간격, 시험할 각도 하나에 별.
   - `competitors.md`. 먼저 뜨는 이름, 한 줄씩.
   - `stack.md`. 도구 감지에서.
7. **보고.** 25줄 안, 출력 계약대로. 사업을 한 줄, 중요한 사실 세 가지, 먼저 할 일 하나와 그 스킬, 출처와 가정(무엇을 언제 읽었고 무엇을 못 읽었는지, 최대 3줄), 그다음 이렇게 말합니다.

> 한 줄로 두 가지만 주세요. 틀린 것, 그리고 지금 가장 중요한 것(더 찾기 / 리드 / 전환 / 출시, 지역이면 발견 / 선택 / 전화, 대행사는 고객사). **깊게**라고 하면 언제든 풀 기초입니다. 조사 에이전트 넷, 약 15분.

고친 말은 바로 파일에 넣고, 계속 지킬 규칙은 `preferences.md`에도 넣습니다. 목표 단어는 `stack.md` 1행에 route.py 단어로 적습니다.

**먼저 할 일**은 체크리스트가 아니라 판단입니다. 사업과 증거를 잽니다.

- 지역이고, 상위 3곳보다 리뷰가 적거나 오래됐거나, 답글이 없으면 /reviews.
- `<업종> <시·구>` 네이버 상위에 없으면 /google-business-profile.
- 첫 화면에 하는 일, 누구, 지역, 다음 행동이 없으면 지역은 /first-screen-check, 그 외는 /landing-page 해체.
- 검색광고를 하는데 전환이 뭔지 모르면 /google-ads-tracking.
- 붐비는 판에서 약속이 흐리면 /positioning-angles.
- 검색에 기대는데 글이 적으면 /keyword-research. AI 답변을 물으면 /ai-search.
- 명단이나 리드는 있는데 후속이 없으면 /email-sequences 또는 /speed-to-lead.

**URL 대신 한 문장**이면 같은 단계인데, 읽을 것은 업종의 경쟁 사이트와 그 리뷰이고 말투는 추출이 아니라 만듭니다. 한 번 말하고 파일에 라벨을 답니다.

## 깊은 기초 (요청할 때만, 약 15분)

"깊게" 또는 풀 조사를 말하면 `references/deep-foundation.md`를 따릅니다. /brand-voice, /positioning-angles, /audience-research, /competitive-intel을 병렬로 돌려 라이트 파일을 올리고(이전 파일은 `.history/`로), 브랜드 기초 보고와 교정 한 번을 합니다. `brand.yaml`에 `depth: deep`. 출시, 리브랜드, 큰 광고비가 기초에 매달릴 때만 제안하고, 묻지 않았으면 돌리지 않습니다.

## 재방문

`brand.yaml` 한 번으로 파일, 신선도, 사업 사실, 캠페인을 봅니다. 브랜드 폴더를 통째로 긁거나 프로필을 다시 읽지 않습니다. 대화에 필요할 때만 그 파일을 엽니다.

**특정 요청**이면 보냅니다. 산출물 하나면 빠른 모드. 무엇을 읽었는지 알리지 않습니다. 오래됐거나 라이트인 기초는, 조언을 바꿀 때만 파일과 고치는 스킬을 한 줄로 말합니다.

**막연하거나 "다음에 뭐 하지"**이면 `brand.yaml`에서 3줄에서 6줄(깊이, 신선도, 진행 캠페인, 마지막 활동, 30일이 넘은 것)을 말하고, 홈을 딱 한 번 가져옵니다. `./campaigns/audit/`에 이전 감사가 있으면 차이를 봅니다. 권고는 하나나 둘, 각각 스킬과 정직한 시간.

- "예시입니다. 네이버 별점 4.4에 리뷰 38건, 상위 3곳은 4.8에 200건대. /reviews가 일 끝날 때마다 부탁을 붙입니다 (약 15분)."
- "올린 글이 넷인데 나눈 적이 없습니다. /content-atomizer가 각각을 일주일 글로 바꿉니다 (글당 약 10분)."
- "경쟁 파일이 70일 됐고 포지션 문안을 쓰려 합니다. /competitive-intel을 먼저 고치거나 (약 10분) 오래된 읽기로 간다고 말하세요."

오래됐거나 라이트인 기초는 막는 의식이 아니라, 담당 스킬(또는 "깊게")을 한 줄로 알립니다.

## 대행사 모드

`./brands/`는 고객사마다 폴더 하나와 `active` 포인터입니다. 순서는 brand_context.py가 구현합니다. brand 슬러그 인자, 그다음 `./brands/active`, 그다음 `./brand/`.

**어느 고객사인지.** 요청이 지목하지 않으면 포인터를 보고, 없거나 다른 고객사 냄새면 한 번 묻습니다. "어느 고객사인지요. 한빛설비, 북산일정, 아니면 새로 받을 곳인가요?" 전환은 `./brands/active`에 슬러그 하나를 쓰는 것이고, 한 줄로 확인합니다. 한빛설비(대구, 설비)와 북산일정(다지점 일정 소프트웨어)은 예시 상호입니다.

**새 고객사 URL**이면 도메인에서 슬러그를 뽑아 `./brands/<slug>/`를 만들고, 포인터를 맞춘 뒤 그 폴더에 라이트 읽기를 합니다. 약 3분, 킥오프 통화에서 라이브로 하기 좋습니다. "깊게"는 같은 폴더에 깊은 기초를 돌립니다.

**고객 찾기**는 /find-local-clients(업종과 상권, 손님을 가장 많이 놓치는 곳) 다음 상위 이름에 /pitch-the-fix. 영업 목록의 기본은 네이버 검색, 플레이스, 지도를 손으로 확인하는 것입니다. `places_search.py`는 선택인 구글 장소 도움이지 기본이 아닙니다. 후보는 `./campaigns/prospects-{업종}-{지역}/`에 두고 `brands/` 아래에는 두지 않습니다. 계약하면 `new client <url>`이고, 후보에서 본 것이 라이트 읽기의 씨앗입니다. 제안은 상호와 이름으로 시작하고, 밤에는 연락하지 않으며, 긴 영어식 콜드메일 대신 짧은 정중한 메일이나 문자로, 고칠 문제 하나만, 성과를 과장하지 않습니다.

**고객사 전체 현황**은 각 `./brands/*/brand.yaml`을 고객사당 한 번 읽고, `files:`가 놓친 디스크의 프로필을 적어 표 하나로 냅니다.

| 고객사 | 기초 | 진행 캠페인 | 마지막 활동 | 표시 |
|---|---|---|---|---|
| 한빛설비 (예시) | deep | 봄-점검 | YYYY-MM-DD | 없음 |
| 북산일정 (예시) | lite | 없음 | YYYY-MM-DD | 41일 묵음 |

그다음 대행사 판단입니다. 받는 돈에 비해 가장 덜 돌본 고객사와, 그걸 고치는 스킬 하나.

**고객사별 키**는 `./brands/<slug>/.env`가 워크스페이스 `.env`를 덮고, 값은 보여 주지 않습니다. "모든 고객사에 루틴"은 route.py에 all-brands와 goal을 주면 폴더마다 격리된 계획을 냅니다. 한 번에 한 고객사. 두 고객사 에이전트를 동시에 띄우지 않습니다.

**격리는 강제됩니다** (Claude Code 플러그인 훅). 활성이 아닌 고객사 폴더에 쓰는 것은 Write, Edit, 셸 리다이렉트 모두 막힙니다. "wrong client: active is <Y>". 막을 피하려고 활성 고객사를 바꾸지 않습니다. 전환은 사용자가 말할 때만. 훅이 없는 다른 에이전트도 같은 규칙을 지킵니다. 세션당 고객사 하나, 쓰기는 활성 폴더만.

## 사이트 리뷰, audit과 prospect

엔진은 하나, 부르는 쪽은 둘. 절차는 `references/site-review.md`입니다. /landing-page TEARDOWN, 지역이면 /first-screen-check, /ai-search AUDIT를 돈 되는 쿼리 약 10개로 압축, /competitive-intel TEARDOWN을 엮고, 목표에 대한 영향 곱하기 쉬움으로 틈을 줄 세웁니다. 틈마다 고치는 스킬과 정직한 예상 시간. 숫자는 라이브 출처, 로컬 문서, 또는 표시된 추정. 증거는 작업 노트에 있고, 보고의 짧은 출처와 가정이 무엇이 무엇인지 말합니다. 영어 웹의 인용 비율은 네이버 사실이 아닙니다.

**Audit** ("사이트 봐줘", "뭐부터 고치지"). 브랜드 URL에 엔진을 돌리고 `./campaigns/audit/audit-<YYYY-MM-DD>.md`를 씁니다. 채팅에는 상위 3가지와 각각의 스킬, 예상 시간만. 브랜드 폴더가 없으면 URL을 한 번 묻고, 단독으로 돌린 뒤 끝에 라이트 읽기를 제안합니다. 약 15분에서 25분.

**Prospect** ("prospect <url>", "이 주소 제안서"). `./brand/`와 `./brands/`는 읽지 않습니다. `./campaigns/prospects-<slug>/`를 만들고, prospect 모드로 돌린 뒤 `references/proposal-template.md`로 `proposal.md`를 씁니다. 가격도, 지어낸 트래픽이나 매출도 없습니다. 질문은 최대 하나("처음에 뭘 팔까요?")이거나, 추론하고 그렇다고 말합니다. 지역 사장님 콜드 제안은 /pitch-the-fix가 더 가볍습니다. 약 20분에서 30분.

## 스택 조언, "뭘 더하지"

키 없이도 기본은 다 돕니다. 이 모드는 어떤 키가 가장 도움이 되는지 순서대로 말하고 멈춥니다.

- 읽기. capability.py에 brand-dir와 markdown을 주면 매니페스트만 나오고 키 값은 절대 안 나옵니다. `stack.md` 1행 목표로 route.py의 goal을 돌리고(없으면 `unsure`), 있으면 라이브러리 루트의 `TOOLS.md`(설치된 스킬의 일부가 아님)에서 비용과 가입을 봅니다.
- 하기. 그 목표의 advisor 순서로 없는 도구 묶음을 먼저, 나머지는 뒤에, 한 줄씩. 무엇을 여는지, 키는 어디서, 무료인지 유료인지. 없는 것이 둘 이상이고 Composio가 없으면 연결 하나로 모을 수 있다고 한 번 말합니다.
- 쓰기. `./brand/stack.md`(갱신, 목표 줄은 유지)와 `brand.yaml` 항목.
- 돌려 말하기. 순위, 그리고 "이것 없이도 다 돕니다." 보통 라우팅에서 advisor는 세션당 한 문장입니다.

## 선호, "기억해"

"기억해", "절대", "항상 먼저 보여줘", "이 말은 쓰지 마"는 `./brand/preferences.md`(대행사는 활성 고객사 폴더)에 덧붙이고, 새것이면 `brand.yaml`에도 넣은 뒤 한 줄로 확인합니다. "preferences.md에 적어 뒀습니다. 모든 스킬이 읽습니다." 사용자에게 파일을 쓰라고 하지 않고, 전부 다시 읽어 주지 않습니다. 워크스페이스 루트 `MARKETING.md`는 상시 브리프입니다. 첫 실행 뒤에 한 번만 제안합니다. "이 내용으로 MARKETING.md를 쓸까요? 그러면 모든 스킬이 목표와 한계에서 시작합니다." 고치는 것은 사용자이고, 요구하지 않습니다.

## 검사, 고친 글이 가르친 것

모든 스킬은 사용자가 결과물을 고치면 골드 케이스와 예/아니오 검사를 남깁니다 (`references/taste-loop.md`). "검사 보여줘"는 `./brand/checks.md`를 스킬별로, 골드 케이스 수와 함께 보여 줍니다. "그 검사 빼"는 `./brand/.history/`로 옮깁니다. "왜 맨날 X를 해"는 그 검사, 골드, 선호, 학습을 찾아 한 줄로 이름을 댑니다. 묻지 않았으면 파일 전체를 읽지 않습니다.

## 도구 감지

첫 실행, "스택 새로고침", "뭐가 연결됐지", 그리고 스택 조언 안에서 돌리고 `stack.md`에 씁니다.

1. **MCP와 커넥터 먼저.** Firecrawl(조사), Replicate나 이미지·영상 MCP(/creative), 브라우저(살아있는 페이지), Zapier나 Composio(메일 도구, CRM, 전화 도구). 보이는 도구 목록의 이름으로만 파악합니다. 감지하려고 커넥터를 부르지 않고, 온보딩이나 조사 중에 부르지 않습니다. 데이터 경계는 워크스페이스와 공개 웹만.
2. **그다음 `.env` 키.** 각 스킬 `optional-keys`. 예를 들어 `REPLICATE_API_TOKEN`, `KIT_API_KEY`, `BEEHIIV_API_KEY`, `META_ACCESS_TOKEN`, `GOOGLE_ADS_DEVELOPER_TOKEN`, `GOOGLE_APPLICATION_CREDENTIALS`(GA4, Search Console), `POSTHOG_API_KEY`, `BUFFER_ACCESS_TOKEN`, `X_BEARER_TOKEN`, `FIRECRAWL_API_KEY`, `SCRAPECREATORS_API_KEY`, `COMPOSIO_API_KEY`.

빈 자리는 오류가 아니라 아직 되는 일로 말합니다. "메일 도구 키가 없습니다. /email-sequences는 시퀀스 전체를 쓰고 직접 붙여 넣습니다. Kit나 Beehiiv 키를 더하면 밀어 넣습니다. 국내 기본은 카카오 채널과 문자입니다." `ANTHROPIC_API_KEY`는 확인하지 않습니다.

## 워크플로

기본 사슬이지 경전은 아닙니다. 이미 있는 산출물이 다른 순서를 가리키면 빼고 이유를 말합니다. `(parallel: …)`는 동시에 띄우고, 벽시계는 가장 느린 갈래입니다. 3단계 이상은 먼저 계획(단계, 산출, 총시간)과 세 선택(전부 / 1단계만 / 고르기)을 냅니다. 두 단계는 한 줄 메모와 함께 진행합니다. 단계 사이에는 파일을 확인하고, 다음 스킬의 `reads:`와 직전 핵심 산출만 넘깁니다.

| 워크플로 (route.py 목표) | 사슬 | 시간 |
|---|---|---|
| 지역에서 발견 (`found`) | /google-business-profile → /local-seo-plan → /service-area-pages | 약 45분에서 60분 |
| 선택받게 (`chosen`) | (parallel: /reviews + /first-screen-check) → /landing-page | 약 30분에서 40분 |
| 전화가 울리게 (`calls`) | (parallel: /google-ads-tracking + /speed-to-lead) → /paid-ads → 몇 주 뒤 /ads-incrementality-check | 약 40분, 그다음 테스트 |
| 고객사 따기 (`clients`) | /find-local-clients → /pitch-the-fix | 약 20분에서 30분 |
| 리드 (`leads`) | /lead-magnet → (parallel: /landing-page + /email-sequences 환영) → /content-atomizer | 약 20분에서 30분 |
| 출시 (`launch`) | /positioning-angles (신선하면 생략) → (parallel: /landing-page + /creative) → (parallel: /email-sequences + /content-atomizer + /paid-ads) | 약 20분에서 30분 |
| 콘텐츠 엔진 (`traffic`) | /keyword-research → /seo-content → (parallel: /content-atomizer + /newsletter) | 약 25분에서 35분 |
| 전환 수리 (`convert`) | /positioning-angles → /direct-response-copy → /email-sequences | 약 25분 |
| 권위 (`authority`) | /brand-voice → (parallel: /social-content + /newsletter) → /content-atomizer | 약 25분 |

뉴스레터 시작, AI 인용, 월간 리뷰, 프로그래매틱 SEO와 메모는 `references/workflows.md`에 있습니다.

**마케팅이 안 된다** ("성과 없음", "사람은 오는데 안 삼", "전화가 멈춤"). 만들기 전에 진단합니다. `brand.yaml`, `assets.md`, `learnings.md`, 캠페인 브리프를 읽고 끊긴 곳을 찾습니다. 발견이 안 됨(검색, 플레이스, 글), 발견은 되는데 행동이 없음(페이지, 제안, 첫 화면, 리뷰), 리드는 오는데 안 닫힘(후속, 속도, 문안), 팔리는데 얇음(포지션, 가격). 그 지점을 고치는 스킬 하나로 보냅니다. 실제 숫자가 있으면 /performance-review가 먼저입니다.

## 자동화

루틴 조리법은 라이브러리 `automations/`에 있습니다. Claude Code 플러그인, 예약된 클라우드 에이전트, 저장된 워크플로 스크립트. 필요할 때가 되면 한 줄만 제안하고, 제안 벽을 세우지 않습니다. 첫 /competitive-intel 뒤에는 주간 경쟁 감시, /ai-search 감사 뒤에는 인용 모니터, 첫 /performance-review 뒤에는 월간 리뷰, /social-content 설정 뒤에는 주간 콘텐츠 의식.

## 라우팅 원칙

1. 이쪽이 정하고 사용자가 확인합니다. 스킬 목록을 펼쳐 고르라고 하지 않습니다.
2. 일 시작 전 질문은 최대 둘. 첫 실행은 최대 하나.
3. 빠른 모드는 절대입니다. 산출물 하나짜리는 나머지를 건너뜁니다.
4. 독립인 스킬은 병렬입니다. 기본을 직렬로 두는 것은 버그입니다.
5. 겹친 요청은 워크플로지, 첫 스킬로 보내는 것이 아닙니다.
6. 있는 것을 다시 만들기 전에 `brand.yaml`을 봅니다. 새로 만들기보다 고칩니다.
7. 기초가 없어도 막지 않습니다. 3분 라이트 읽기를 제안하거나 기본으로 진행하고, 선택을 존중합니다. 조용히 평범한 결과만 내지 않습니다.
8. 권고는 구체적입니다. 프로젝트 상태, 스킬 이름, 정직한 시간. "글을 좀 쓰면 좋겠습니다"는 금지입니다.
9. 보낸 스킬이 끝나면 파일을 확인하고, `assets.md`에 행이 들어갔는지 보고, 프로필이 바뀌었으면 `brand.yaml`을 고칩니다.
10. 무엇이 라우팅을 빚었는지 늘어놓지 않습니다. 오래됐거나 얇은 맥락은 조언을 바꿀 때만, 파일과 고치는 스킬을 한 줄로.

## 선택적 맥락

태스크 에이전트 브리프(사용자에게 보이지 않음)는 스킬 경로, 할 일, 직전 핵심 산출, 브랜드 맥락 한 줄입니다. 파일 덤프나 `reads:` 밖의 브랜드 파일은 넣지 않습니다. 방법은 `${CLAUDE_SKILL_DIR}/references/brand-memory.md`입니다.

## 출력

출력 계약(`${CLAUDE_SKILL_DIR}/references/output-format.md`)을 따릅니다. 머리, 내용, 정확한 경로의 **Files saved**, 스킬 2개에서 4개와 시간의 **What's next**. 마크다운만, 상자 그림은 없습니다. 보고, 감사, 제안서에는 일만 담습니다. 스크립트 경로, 과정으로서의 도구·스킬 이름, 점수표, 줄마다 다는 데이터 태그, 라우팅 출력은 작업 노트에 둡니다. 감사는 계획 예산(약 1,200단어에서 2,500단어)을 씁니다.

start-here가 쓰는 것은 `brand.yaml`, `stack.md`, `preferences.md`, 라이트 버전의 `voice-profile.md`, `positioning.md`, `audience.md`, `voc.md`, `competitors.md`, 선택인 `MARKETING.md`, `./campaigns/audit/`의 감사, `./campaigns/prospects-*/`의 제안서입니다. 깊은 기초와 이후 갱신은 기초 스킬 넷의 일입니다. 첫 실행은 보고와 먼저 할 일 하나로 끝나고, 재방문은 메뉴가 아니라 보낸 행동으로 끝납니다.

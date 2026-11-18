---
name: meta-ads
description: 메타(페이스북·인스타그램) 광고를 마케팅 API로 끝까지 만들고 검증합니다. 비즈니스 관리자 권한, 주택·신용·채용을 포함한 특수 광고 카테고리, 거절을 피하는 일시정지 생성, 브라우저에서만 되는 단계, 크롭에 안전한 소재, 픽셀과 전환 API가 실서버에서 찍히는지를 다룹니다. 문안은 표시광고법의 거짓·과장·기만·부당 비교를 경고한 뒤에 내보냅니다. API 접근, 코드로 캠페인 생성과 디버그, 채용·대출·부동산 광고, 픽셀이 정말 동작하는지 확인할 때 씁니다.
when_to_use: set up the meta ads api, launch facebook ads from code, create a meta campaign, meta ads permission error, system user token, is my facebook pixel working, conversions api setup, meta test events, special ad category, hiring ad on facebook, facebook ad image got cropped, instant form lead ads, meta ads preflight, 메타 픽셀이 실서버에서 안 찍혀, 전환 API 테스트 이벤트, 인스타 광고를 일시정지로 생성, 채용 광고 특수 카테고리, 주택 광고 타겟 제한, meta pixel test events korea, instagram ads paused launch
argument-hint: "[캠페인 설정 경로] | preflight | launch | verify-tracking"
metadata:
  boring:
    version: 1.0.0
    layer: distribution
    reads: [positioning#chosen-angle, creative-kit, learnings]
    writes: []
    optional-keys: [META_ACCESS_TOKEN, META_AD_ACCOUNT_ID, META_PIXEL_ID, META_PAGE_ID, META_APP_ID, META_GRAPH_VERSION]
    enhances_with:
      - toolset: ads
        gains: "preflight and campaign creation run against the real ad account; without a token the skill still writes the config, the launch checklist and the tracking audit"
---

# 메타 광고

여기는 집행 층이에요. `/paid-ads`가 무엇을 말하고 무엇을 시험할지 정하면, 이 스킬이 마케팅 API로 라이브까지 가져가요. 권한 막다른 길, 400 오류, 계측이 깨졌는데 추적이 깨진 줄 아는 오독을 피해요. 끝났다는 것은 캠페인이 일시정지로 존재하고, 게재 위치마다 미리보기를 봤고, 배포된 사이트에서 전환 이벤트가 테스트 이벤트에 처리됨으로 보이고, 서버 경로가 자기 응답으로 증명됐고, 사람이 켰다는 뜻이에요. 방법은 바닥이에요. 눈앞 계정이 더 나은 길을 부르면 그 길을 가고 이유를 한 줄로 적어요.

문안을 내보내기 전에 표시광고법을 한 번 경고해요. 거짓·과장, 기만, 부당 비교는 넣지 않아요. 의료, 대부, 금융, 건강기능식품은 업종 심의가 있으니 확인하라고만 해요. 조문 번호는 단정하지 않아요. 이 점검은 법률 자문이 아니에요.

하드 룰.

1. **전부 일시정지로 만들어요.** 캠페인을 켜는 것은 돈을 쓰는 일이고, 검토가 아무리 꼼꼼해도 매번 사람의 결정이에요.
2. **비밀번호, 2단계 인증 코드, 결제 수단을 다루지 않아요.** 약관 동의와 비즈니스 인증도 대신하지 않아요. 사람이 로그인하고, 에이전트는 그 세션에서 일해요.
3. **만료 없는 `ads_management` 토큰은 돈을 쓸 수 있어요.** 환경 변수에만. 인쇄하지 않고 커밋하지 않아요. 대화, 로그, 스크린샷에 나오면 폐기해요.
4. **예산은 계정 통화의 최소 단위예요.** 보내기 전에 범위를 확인해요. 달러 계정은 오프셋 100이라 3000이 30.00달러예요. 원화 계정은 오프셋 1이라 30000이 3만 원이에요. 원화에 100을 곱하면 100배 과다 지출이에요. 계정 통화부터 읽어요.

## 맥락

`./brand/`, `./brands/` 또는 `MARKETING.md`가 있을 때만 실행해요.
`python3 ${CLAUDE_SKILL_DIR}/../start-here/scripts/brand_context.py --for meta-ads`
(`${CLAUDE_SKILL_DIR}`는 이 스킬 폴더예요. Claude Code 밖에서는 이 파일을 읽은 폴더, 예를 들어 `.agents/skills/meta-ads`. 스크립트나 python3이 없으면 브랜드 폴더를 직접 읽어요. `./brands/active`가 가리키면 `./brands/<slug>/`, 아니면 `./brand/`. 이어서 `MARKETING.md`, `preferences.md`, `reads:`의 파일. 없으면 단독으로 진행하고 이것만 물어요. 무엇을 광고하는지, 고객이 어디서 전환하는지, 하루 예산(원), 채용·주택·금융 상품 광고인지.)

**먼저 `references/meta-facts.md`를 읽어요.** 마케팅 API 버전은 일정대로 만료해요. v24.0은 2026-11-10에 만료됐어요. 헤더가 오래됐으면 스크립트를 돌리기 전에 갱신해요.

| 일 | 읽을 곳 |
|---|---|
| API 접근 자체 | 2절, 이어서 `references/setup.md` |
| 무엇으로 최적화할지 | 3절 |
| 채용, 주택, 금융 상품 광고 | 4절, 이어서 `references/creative.md` |
| 코드로 캠페인 생성 | 5절, 이어서 `references/publishing.md` |
| API가 못 하는 단계 | 6절, 이어서 `references/browser.md` |
| 픽셀, 전환 API, "추적되니?" | 1절과 7절, 이어서 `references/tracking.md` |
| 이미지 만들기 | 8절, 이어서 `references/creative.md` |

## 1. 검증 함정. 시험 결과를 믿기 전에

한 집행에서 거짓 음성 셋이 나왔어요. 각각 진짜 버그처럼 보였고, 각각 시스템이 아니라 계측이었어요.

| 함정 | 무슨 일이었나 | 대신 쓸 것 |
|---|---|---|
| localhost에서 시험 | 픽셀과 예약 임베드가 localhost에서는 통과. 프로덕션의 Content-Security-Policy가 둘을 막았고, localhost는 그 헤더를 안 보냄 | **배포된** URL에서 확인. localhost 통과는 프로덕션 헤더에 대해 아무것도 증명하지 않아요 |
| `performance.getEntriesByType('resource')` | 요청이 안 보여 "Lead가 안 찍힌다"고 결론. 이벤트 ID가 있으면 픽셀은 `navigator.sendBeacon`을 쓰고, 비콘은 리소스 타이밍에 안 나와요 | 메타 **테스트 이벤트**. 메타 자신의 계측이라 논쟁을 끝내요 |
| 테스트 이벤트에 서버 행이 없음 | 전환 API가 깨졌다고 결론. 서버가 `test_event_code`를 보낼 때만 서버 이벤트가 보여요 | 서버가 자기 전송 결과를 돌려주게 (7절) |

없는 증거를 없음의 증거로 읽은 패턴이에요. 계측이 측정 대상을 볼 수 없었어요. 깨졌다고 결론 내기 전에, 계측이 무엇을 볼 수 있는지 물어요. 한 번에 하나만 바꿔요. "분리 시험"이 변수 둘을 같이 빼면 엉뚱한 쪽에 죄가 가요.

## 2. 권한 사슬 (대부분 여기서 멈춤)

**에이전트가 계정을 읽고 관리하게 하는 것.** 메타 공식 Ads MCP와 Ads CLI. 광고 계정에 메타 자신의 커넥터를 줘요. 광고 계정이 있으면 추가 요금이 없어요. 메타 비즈니스 설정, 연동, Ads MCP에서 켜요. 문서는 developers.facebook.com의 Ads AI Connectors. 이 스킬의 스크립트는 마케팅 API 경로로 남고, 아래는 그 경로예요. 커넥터가 없어도 그 스크립트와 6절의 브라우저 단계가 같은 일을 해요. 어느 쪽이든 하드 룰은 같아요. 일시정지로 만들고, 사람이 켜요.

API로 광고를 만들려면 **별도의 권한 넷**이 필요해요. 하나라도 빠지면 다른 권한의 이름을 말하지 않는 오류가 나요.

1. **메타 앱.** 사업자에 있는 앱을 재사용해요. 두 번째 앱은 심사와 게시가 한 번 더예요.
2. **시스템 사용자가 앱 역할을 가짐.** 비즈니스 설정, 앱, 해당 앱, 사람 추가, 시스템 사용자, 앱 개발. 이게 없으면 토큰 생성에 "사용 가능한 권한 없음"만 나오고 어떤 권한이 빠졌는지 힌트가 없어요. 사람들이 건너뛰는 단계예요.
3. **시스템 사용자가 자산을 가짐.** 시스템 사용자, 해당 사용자, 자산 할당. 광고 계정은 **캠페인 관리**(재무·사용자 권한이 아님). 페이지는 **광고**. 픽셀 또는 데이터 세트는 **이벤트 데이터 세트 사용**.
4. **토큰.** 시스템 사용자, 토큰 생성, 해당 앱, 만료 **없음**, `ads_management`. 시스템 사용자 토큰은 사업자 소유라 직원이 바뀌어도 남아요. 개인 토큰은 비밀번호가 바뀌면 죽어요. 기한이 있는 토큰은 조용히 만료되고, 며칠 뒤 "왜 지출이 멈췄지"로 발견돼요.

나머지는 다른 것이 다 된 뒤, 광고 생성 순간에야 드러나요.

- **인스타그램이 광고 계정에 연결됨.** Advantage+ 게재 위치는 인스타그램을 포함해요. 인스타에 낼 생각이 없어도 "Ad account has no access to this Instagram account"로 생성이 실패해요.
- **앱이 개발이 아니라 라이브.** 개발 모드는 소재 생성만 막아요. 다른 호출은 성공해서, 긴 스크립트의 마지막에 실패해요. 게시에 개인정보 처리방침 URL과 카테고리가 필요해요.

다른 일보다 먼저 프리플라이트. 위를 모두 확인하고 아무것도 쓰지 않아요.

```
META_ACCESS_TOKEN=... META_AD_ACCOUNT_ID=act_123 META_PIXEL_ID=... \
  node ${CLAUDE_SKILL_DIR}/scripts/preflight.mjs
```

`act_123`은 가짜 자리표시예요. 실제 계정 번호를 파일에 적지 않아요.

## 3. 캠페인보다 먼저 전환을 고르기

광고 세트가 무엇에 최적화하는지가 메타가 찾는 사람을 정해요. 먼저 정해요.

**물량으로 최적화하고, 진실로 측정해요.** 광고 세트는 학습을 벗어나려면 한 주에 최적화 이벤트 약 50건을 원해요. 진짜 결과가 그보다 드물면, 자주 일어나는 앞 단계 이벤트에 입찰하고 진짜 결과는 보고로 봐요. 약 50건은 메타 학습의 이야기예요. 네이버 품질지수가 아니에요.

**의미하는 순간에 이벤트를 찍어요.** 예약 달력이 그려질 때 `Schedule`을 찍으면 "달력을 본 사람"이에요. 그쪽으로 최적화하면 메타는 들어왔다가 나가는 사람을 찾아요. 예약 도구의 성공 콜백에 찍고, 그리기는 아예 안 쓰거나 별도 맞춤 이벤트로 둬요.

**예시 A. 지역 서비스 리드 광고.** 한빛설비(대구, 설비, 지어낸 상호). 보일러 교체, 반경 15km, 하루 3만 원(원화 계정, 오프셋 1). 리드가 오는 길 셋.

| 경로 | 트레이드오프 | 최적화 |
|---|---|---|
| 메타 안의 즉시 양식 | 리드가 싸고 의도가 낮음. "높은 의도" 양식은 검토 단계가 있어 일부를 걸러요 | 리드. CRM이 전환 API로 결과를 돌려주면 전환 리드 |
| 웹사이트 폼 | 적고 따뜻함. 픽셀과 전환 API가 되어야 함 (7절) | 제출이 확인된 `Lead` |
| 전화 | 가장 따뜻함. 메타는 탭을 보지 통화 내용은 못 봐요 | 메타 숫자가 아니라 전화 기록, 스마트콜, 카카오 문의로 측정 |

지역 서비스 기본은 웹사이트 폼, 또는 CRM에 동기화된 높은 의도 즉시 양식이고, 사람이 몇 분 안에 다시 걸어요 (`/speed-to-lead`). 두 시간 동안 아무도 안 거는 폼 리드는 값을 두 번 낸 리드예요.

**예시 B. 온라인 상점.** 광고 세트가 한 주에 구매 약 50건을 기록하면 `Purchase`로 최적화. 그 아래는 `InitiateCheckout` 또는 `AddToCart`로 최적화하고 판단은 상점 주문으로. `value`와 `currency`를 보내요. 원화 계정이면 `KRW`. 2만 원 주문과 20만 원 주문을 가치 입찰이 구분하게.

## 4. 특수 광고 카테고리

캠페인 생성 때 `special_ad_categories`는 항상 가요. 해당 없으면 `[]` 또는 `NONE`.

값은 `HOUSING`(주택), `EMPLOYMENT`(채용), `FINANCIAL_PRODUCTS_SERVICES`(신용·금융상품. 2025-01-14부터 옛 `CREDIT`를 대체), `ISSUES_ELECTIONS_POLITICS`(사회 이슈·선거·정치)예요. 세부 날짜와 국가 범위는 `references/meta-facts.md`예요.

미국·캐나다·유럽 일부 오디언스에 주택·채용·금융 상품 광고가 닿으면 연령은 대체로 18~65+, 성별은 전체, 우편번호 타겟과 제외와 유사 타겟이 빠지고, 위치 반경은 미국·캐나다는 최소 15마일(약 25km), 유럽은 최소 15km로 넓어져요. 카테고리는 만든 뒤에 쉽게 바꾸지 못해요. 잘못 선언하면 지우고 다시 만들어요.

**한국만 대상이고 미국·캐나다·유럽에 안 닿으면** 같은 업종 광고라도 제한을 받을지 선택할 수 있어요. `NONE` 또는 빈 배열로 빠져나오거나, 카테고리를 선언해 제한에 들어갈 수 있어요. 필드는 어느 쪽이든 보내요. 2026-05-21자 개발자 문서의 문장이에요. 오늘 그 페이지를 다시 열지는 않았고, 실행 전에 meta-facts의 갱신 지시를 봐요.

채용 광고는 사실인 급여 주장에도 거절되는 경우가 있어요. 문안을 고칠 수 있는 곳마다 막고, 실패는 크게 알려요. 원화 계정용 가드 예.

```js
const MONEY = /월급|연봉|시급|순수익|월\s?\d+\s?만|\d+\s?억/;
```

달러 계정은 예시 설정의 `\$\s?\d|\b\d+\s?(k|dollars|usd)\b|\bper hour\b|/hr\b`를 유지해요. 예시 JSON은 아직 미국 배관 샘플이에요. 복사한 뒤 상호, 좌표, 링크, 예산 단위를 한빛설비와 원화로 바꿔요. 스크립트 원본은 고치지 않아요.

프리랜서(사업소득) 채용에 "지금 채용 중"만 크게 쓰면 근로 계약을 찾는 사람이 클릭하고 자격에서 떨어져요. 고용 형태를 문안에 적어요.

"할부 가능"을 스치듯 넣은 서비스 광고는 회색이에요. 도움말의 현재 정의를 읽어요. 애매하면 할부는 랜딩에만 두고 광고에서는 빼요. 대출 금리와 한도를 단정하는 문안은 표시광고법과 업종 심의 경고를 같이 붙여요.

**타겟이 잠긴 캠페인에서는 소재가 타겟이에요.** 관심사 타겟이 없으면, 맞는 사람이 자신을 알아보는 것은 광고뿐이에요. 오디언스를 이미지에 말로 넣어요. `대구 설비 기사`. 그 줄이 피드 크롭에서 살아남는지 봐요(8절). 피드에서 사라지면 남은 타겟이 없어져요. 한국만 대상이고 카테고리를 선언하지 않았다면 이 제약은 적용되지 않아요. 그래도 첫 줄이 누구의 광고인지 말해야 해요.

## 5. 캠페인 생성. 거절이 나오는 순서

각각 생성을 멈추는 실제 400이에요. 앞에서 넣어요.

```js
// 캠페인
{ objective: 'OUTCOME_LEADS', status: 'PAUSED', special_ad_categories: [],
  buying_type: 'AUCTION', is_adset_budget_sharing_enabled: false }  // 예산이 광고 세트에 있으면 필수

// 광고 세트. 원화 계정 예시. 대구 중심, 반경 15km, 하루 3만 원
{ daily_budget: 30000,                       // 오프셋 1. 3만 원. 달러 계정이면 3000이 30달러
  billing_event: 'IMPRESSIONS',
  bid_strategy: 'LOWEST_COST_WITHOUT_CAP',  // 필수. 이력이 없는 픽셀에 상한은 전달을 막아요
  optimization_goal: 'OFFSITE_CONVERSIONS',
  promoted_object: { pixel_id, custom_event_type: 'LEAD' },
  targeting: { geo_locations: { custom_locations: [{ latitude: 35.8714, longitude: 128.6014,
    radius: 15, distance_unit: 'kilometer' }] }, age_min: 18, age_max: 65, genders: [1, 2] } }
```

좌표는 대구 도심의 공개된 대략 위치예요. 고객 주소가 아니에요.

| 오류 | 원인 |
|---|---|
| `must specify True or False in is_adset_budget_sharing_enabled` | 예산이 광고 세트에 있는데 플래그가 없음 |
| `Bid amount or bid constraints required` | `bid_strategy`가 없음 |
| `daily budget must be greater than $0` | 예산이 `null`로 도착 (아래) |
| `Ad account has no access to this Instagram account` | 인스타그램이 광고 계정에 연결 안 됨 |
| `created by an app that is in development mode` | 앱이 게시 안 됨 |
| `standard_enhancements has been deprecated` | 필드를 빼고 화면에서 설정 (6절) |

**null 예산은 호출자 버그였어요.** `argv[argv.indexOf('--flag') + 1]`은 플래그가 없으면 `indexOf`가 -1이라 `argv[0]`을 돌려요. `Number('--apply')`는 `NaN`이고 `JSON.stringify`가 `null`로 만들며, 메타는 예산 0으로 보고해요. 플래그가 있는지 확인하고, 보내기 전에 값이 정수이고 기대 범위인지 봐요. 원화면 3만 원이 30000인지, 실수로 3000000이 아닌지.

**고아를 치워요.** 실패한 실행은 캠페인이나 광고 세트를 남겨요. 다시 시도하기 전에 지우지 않으면 중복이 쌓이고 전달이 나뉘어요.

캠페인 스크립트는 JSON 설정으로 이 일을 해요. 기본은 드라이런 (`--replace-ads`도 `--apply`가 있기 전에는 드라이런).

```
cp ${CLAUDE_SKILL_DIR}/scripts/campaign.example.json ./campaigns/<name>/meta-campaign.json
node ${CLAUDE_SKILL_DIR}/scripts/campaign.mjs --config ./campaigns/<name>/meta-campaign.json          # 확인, 쓰기 없음
node ${CLAUDE_SKILL_DIR}/scripts/campaign.mjs --config ./campaigns/<name>/meta-campaign.json --apply  # 일시정지로 생성
```

채운 설정은 버전 관리에 넣지 않아요. 계정 ID가 들어가요. 예시 파일의 상호와 달러 주석을 원화 계정에 그대로 두지 않아요.

## 6. 브라우저만 할 수 있는 것

API가 없는 필수 단계. 시스템 사용자와 권한 만들기, 앱 게시, 인스타그램 연결, **Advantage+ 크리에이티브 보정 끄기**, **게재 위치별 광고 미리보기**, 테스트 이벤트, 자동 이벤트 감지 끄기, 결제 수단 추가.

둘은 하중을 받는데 자주 건너뛰어요. Advantage+ 크리에이티브 보정은 이미지를 자동으로 자르고 글자를 올려요. API 필드는 폐기됐고 대체 필드는 움직여요. 광고 관리자에서 끄고, 소재의 `degrees_of_freedom_spec`을 읽어 확인해요 (`advantage_plus_creative: OPT_OUT`). 광고 미리보기는 게재 위치를 실제로 그려요. 전체 크기에서는 살고 피드에서 죽는 소재를 잡는 방법이에요. `references/browser.md`에 딥 링크와 에이전트가 이 UI를 다루는 법이 있어요.

## 7. 증명된 전환 추적

**경로 둘, 이벤트 ID 하나.** 브라우저 픽셀과 서버 전환 API가 같은 `event_id`와 `event_name`을 보내요. 메타는 하나를 남겨요. 광고 차단기는 방문자 상당수의 브라우저 경로를 버려요. 영어권 "약 3분의 1" 같은 비율을 한국 숫자로 쓰지 않아요. 서버 경로가 그 공백을 메우는 이유는 같아요. 선택이 아니에요. 브라우저는 서버가 알 수 없는 것을 전달해요. 이벤트 ID, 페이지 URL, 자사 쿠키 `_fbp`와 `_fbc`. 다른 호스트의 서버는 그 쿠키를 못 봐요.

**서버가 자기 결과를 보고하게.** 전환 API 호출이 폼 제출을 실패시키면 안 돼요. 그래서 몇 달간 조용히 썩을 수 있어요. 응답에 결과를 넣어요 (`meta_capi: "sent:1"` 또는 `"failed:<이유>"`). `curl` 한 번이 서버 경로만 증명해요.

**픽셀 설정에서 자동 이벤트 감지를 꺼요.** 평범한 폼 사용을 `Subscribe` 같은 이벤트로 만들어 최적화를 오염시켜요. 자동 고급 매칭은 다른 설정이고 매칭을 돕어요. 개인정보 처리방침이 막지 않으면 켜 둬요. 이메일·전화 해시는 전환 매칭 목적의 고지가 필요해요.

**Content-Security-Policy가 조용히 전부 죽일 수 있어요.** `script-src`는 `connect.facebook.net`을 허용. `connect-src`는 `www.facebook.com`과 `connect.facebook.net`. `frame-src`는 `www.facebook.com`. 라이브러리가 막히면 `fbq`는 인라인 스텁으로 남아 이벤트를 쌓기만 하고 영원히 안 보내요. 배포된 사이트 콘솔에 `scripts/verify-tracking.js`를 붙여요. `fbq.callMethod`가 함수면 진짜 라이브러리가 로드된 거예요. `fbq.loaded`와 `fbq.version`은 스텁이 설정하므로 아무것도 증명하지 않아요.

## 8. 소재. 크롭 안전 영역

1080x1920 애셋은 피드에서 잘려요. 레터박스가 아니에요. 4대5는 위아래 약 285px, 1대1은 위아래 약 420px이 빠져요. 위나 아래 420px 근처는, 노출이 가장 많은 자리에서 사라져요. **중요한 요소는 전부 y 420에서 1500 안에** 한 블록으로 쌓아요. 식별, 메시지, 행동 요청이 어떤 크롭에도 남게. 전체 크기 렌더를 믿지 말고 크롭을 시뮬레이션하고, 광고 관리자 미리보기를 봐요. `references/creative.md`에 크롭 스크립트, 디자인처럼 보이지 않게 하는 법, 자막 상자 자동 맞춤이 있어요.

## 9. 집행 뒤

- **결과 읽기.** 전환은 인사이트 응답의 `actions` 배열에 `offsite_conversion.fct.lead` 같은 이름으로 있어요. 최상위 필드가 아니에요.
- **귀속은 원인이 아니에요.** 메타는 기여 기간 안의 클릭이나 조회에 맞출 수 있는 것을 세요. 어차피 전환할 사람 포함. 메타 숫자로 늘리기 전에 전화 기록, 스마트콜, 카카오 문의, 주문과 비교해요 (`/ads-incrementality-check`).
- **소재 반복.** 소재는 수정이 안 돼요. 광고를 지우고 다시 만들어요 (스크립트의 `--replace-ads <adset_id> --apply`. `--apply` 없이는 지울 목록만). 광고를 지우면 광고 세트의 학습은 남고, 광고 세트를 지우면 리셋돼요.
- 셀별 끄기·늘리기·고치기는 `/paid-ads` 결과 읽기예요.

## 집행 체크리스트

조용히 따라요. 론치 파일에는 아직 열린 것만 적어요.

- [ ] 프리플라이트 통과. 토큰, 범위, 광고 계정 활성, 결제 수단, 페이지, 픽셀이 최근에 찍힘, 인스타그램 연결, 앱 라이브
- [ ] 특수 광고 카테고리 결정. 한국만이면 선언할지 `NONE`인지. 생성 뒤에 바꾸기 어려움
- [ ] 문안이 카테고리 내용 규칙과 표시광고법 경고를 통과. 가드 통과
- [ ] 소재의 핵심이 y 420에서 1500 안. 크롭 시뮬레이션
- [ ] 일시정지로 생성. 게재 위치별 미리보기. Advantage+ 크리에이티브 보정 꺼짐
- [ ] 배포 사이트에서 `fbq.callMethod`가 함수
- [ ] 전환 이벤트가 테스트 이벤트에서 **처리됨**
- [ ] 서버 경로가 자기 응답으로 `sent:N` 확인
- [ ] 시험 리드를 CRM 또는 데이터베이스에서 삭제
- [ ] 사람이 캠페인을 켰고, 로그에 누구와 언제가 있음
- [ ] 토큰이 대화, 로그, 스크린샷에 나왔으면 교체

## 산출

`./campaigns/<name>/meta-launch.md`.

1. `## META LAUNCH: <campaign>`와 한 줄. 날짜와 이 집행이 무엇을 위한 것인지.
2. **무엇이 있나.** 전부 일시정지. 캠페인, 광고 세트, 광고 이름, 예산(원 또는 계정 통화), 카테고리, 최적화 이벤트, 게재 위치.
3. **열린 항목.** 순서대로, 담당과, 누가 언제 켰는지.
4. **증명.** 몇 줄. 게재 위치별 미리보기, 테스트 이벤트 상태, 서버 자신의 전송 결과, 배포 URL의 CSP 확인.
5. **출처와 가정.** 짧은 노트. 무엇을 라이브로 봤고 무엇이 설정뿐인지. 토큰이 없으면 한 줄(아무것도 안 만들어짐. 설정과 체크리스트). 픽셀 ID나 도메인이 자리표시면 빠졌다고 한 줄. 그 값으로 확인을 돌리지 않아요.

프리플라이트 출력, 객체 ID, 요청 세부는 `./campaigns/<name>/notes.md`에만. 저장하고 붙이지 않아요. 론치 파일에 스크립트 경로와 명령은 없어요.

`./brand/assets.md`에 한 줄.

**다음에**

- `/paid-ads`. 문안, 시험 매트릭스, 결과가 오면 끄기·늘리기 (약 20분)
- `/creative`. 크롭 안전 띠 안의 광고 이미지와 짧은 영상 (약 20분)
- `/ads-incrementality-check`. 메타 자신의 숫자로 늘리기 전 (계획 약 20분)
- `/speed-to-lead`. 폼 리드가 지출 값어치를 하려면 몇 분 안의 콜백 (약 20분)

## 사용자가 결과물을 고치면

고친 내용을 적용하고 남기세요. `./brand/gold/<this skill>/`에 골드 사례 하나, `./brand/checks.md`에 예/아니오 점검 1~3개, 확인은 한 줄. 넘기기 전에 맥락 블록이 불러온 점검을 조용히 답하고 아니오는 고쳐요. 방법은 `${CLAUDE_SKILL_DIR}/../start-here/references/taste-loop.md`예요.

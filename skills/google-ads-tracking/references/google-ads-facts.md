# 구글 광고 추적에 쓰는 사실 (잘 상해요)

last-verified: 2026-11-18 · ttl-days: 90 · refresh: support.google.com/google-ads/answer/6095882 (광고 통화 측정)의 통화 추적 라벨과 단계, answer/10995103과 /11461796의 목표·주요·보조, answer/9013908과 /3246303의 지역 액션, answer/10993988의 추적 상태, developers.google.com/google-ads/api/reference/rpc/latest 의 현재 API 버전, 열거형 숫자는 github.com/googleapis/googleapis 의 google/ads/googleads/<version>/enums/. 아래 라벨과 숫자를 고치고 last-verified를 올려요.

매 실행 처음에 읽어요. SKILL.md가 방법이고, 이 파일이 바뀌는 이름과 숫자예요. 한국어 UI 이름은 같은 화면의 대응이고, 글자가 다르면 화면을 따라요. 이 스킬은 구글 광고예요. 네이버 메뉴로 바꾸지 않아요.

## 화면 이름과 경로 (2026-11-13 확인, 오늘은 원문 재확인 안 함)

- 전환 액션은 **Goals, Conversions, Summary**. 한국어 화면은 목표, 전환, 요약.
- 새 통화 액션. **전환 액션 만들기, 전화 통화에서 발생한 전환, 저장 후 계속, 카테고리 "전화 리드", 전환 액션 추가.** 그다음 하나.
  - **Calls from ads (광고에서 발생한 통화).** 통화 애셋과 위치 애셋의 전화. 통화 보고가 켜지면 구글이 이 이름의 기본 액션을 만들고 전환에 포함해요.
  - **Calls from website visits (웹사이트 방문에서 발생한 통화).** 둘 중 하나. **"사이트에 표시된 번호로 전화"** (구글 착신 번호가 페이지 번호를 대체) 또는 **"사이트 번호를 클릭해 전화"** (전화 링크 탭).
  - **업로드 통화.** 전화 리드 카테고리에서는 제공되지 않아요. 다른 카테고리에서, 다른 곳에서 추적한 통화를 가져올 때.
- 광고 통화의 요건. 인증된 번호가 있는 통화 애셋 또는 위치 애셋, 계정 설정의 **통화 보고**, 지원 국가의 사업자.
- **AI 자격 통화 리드.** 통화 녹음이 켜지면 구글 AI가 녹음으로 리드 품질을 판단해요. 녹음은 양 당사자가 미국 또는 캐나다에 있는 통화로 제한되고 Call Ads 추가 약관의 적용을 받아요. 녹음이 없으면 설정한 최소 통화 시간으로 돌아가고, 통화 보고가 없으면 광고 상호작용 데이터로 돌아가요. 한국 번호 통화를 이 녹음 기능이 분석한다고 말하지 않아요.
- **비즈니스 프로필 통화.** 구글 광고 계정이 비즈니스 프로필에 연결되고, 프로필의 통화 기록이 켜지고, 통화 보고가 켜지면, 광고 상호작용에 귀속할 수 있는 프로필 통화가 **Calls from ads**에 들어와요.
- **주요와 보조.** 주요 액션은 입찰에 쓰이고, 캠페인이 그 목표로 최적화할 때 전환 열에 나와요. 보조 액션은 전환에서 빠지고 관찰용 **모든 전환**에 나와요.
- **계정 기본 목표**가 캠페인의 입찰 대상이에요. 캠페인이 자기 목표로 설정된 경우는 제외.
- **추적 상태 열.** "최근 전환 없음"은 보통 최근 7~14일에 광고 클릭이 전환으로 이어지지 않았다는 뜻이에요. 항상 태그 오류는 아니에요. "비활성", "주의 필요", "미확인"은 보통 태그가 없거나 잘못됐거나, 전환 ID·라벨이 틀리거나, 향상된 전환 문제예요. 태그 변경 뒤 24~48시간을 기다려요.
- **Tag Assistant.** tagassistant.google.com. 라이브 도메인을 연결하고, 고객처럼 행동하고, 어떤 태그와 이벤트가 어디로 가는지 읽어요.
- 예산 읽기 열. **검색 노출 점유율**, **검색 손실 노출 점유율(순위)**, **검색 손실 노출 점유율(예산)**.

## 지역 액션 (숫자를 부풀리는 인정)

- 위치 애셋이 활성이면 구글 광고가 **지역 액션** 전환을 자동으로 만들어요. **길찾기**는 퍼포먼스 맥스와 검색에서 입찰 가능하고, **통화 클릭**은 퍼포먼스 맥스에서 입찰 가능해요. 주요이고 캠페인 목표에 포함될 때만 입찰해요.
- 지역 액션은 고객이 광고와 상호작용한 뒤 그 행동을 할 때 집계돼요. **나중 오가닉 결과에서 그 업체를 탭한 것도 포함**되고, 클릭 기여 기간(기본 30일) 안이에요.
- API에서는 전환 출처 **GOOGLE_HOSTED**, 유형 **GOOGLE_HOSTED** ("광고와 상호작용한 뒤 구글 제품에서 발생한 지역 액션"). 계정은 "Business profile - Call" 같은 이름을 쓰는 경우가 많아요.

## API 사실 (2026-11-13 확인, 오늘은 프로토 재확인 안 함)

- 참조 페이지의 API 버전은 **v26**이었어요. URL에 최신 버전을 써요 (`https://googleads.googleapis.com/v26/...`). 버전 오류가 나면 여기서 다시 확인해요.
- **BiddingStrategyType** (v26 프로토). UNSPECIFIED 0, UNKNOWN 1, ENHANCED_CPC 2, MANUAL_CPC 3, MANUAL_CPM 4, PAGE_ONE_PROMOTED 5, TARGET_CPA 6, TARGET_OUTRANK_SHARE 7, TARGET_ROAS 8, **TARGET_SPEND 9 (화면 이름 클릭수 최대화)**, **MAXIMIZE_CONVERSIONS 10**, MAXIMIZE_CONVERSION_VALUE 11, PERCENT_CPC 12, MANUAL_CPV 13, TARGET_CPM 14, TARGET_IMPRESSION_SHARE 15, COMMISSION 16, INVALID 17, MANUAL_CPA 18, FIXED_CPM 19, TARGET_CPV 20, TARGET_CPC 21, FIXED_SHARE_OF_VOICE 22. 숫자는 원시를 해독하려고 적었어요. 손으로 지도를 만들라고 적은 것이 아니에요. 라이브러리의 열거형 이름을 써요.
- **ConversionOrigin.** WEBSITE 2, GOOGLE_HOSTED 3, APP 4, CALL_FROM_ADS 5, STORE 6, YOUTUBE_HOSTED 7, LOCAL_SERVICES_ADS 8.
- 지역 계정에서 만나는 **ConversionActionType.** AD_CALL 2 (광고 통화 애셋), CLICK_TO_CALL 3 (모바일 사이트 번호 탭), UPLOAD_CALLS 6, UPLOAD_CLICKS 7, WEBPAGE 8, WEBSITE_CALL 9 (사이트의 동적 번호로 전화), GOOGLE_HOSTED 28 (지역 액션), STORE_VISITS 36, WEBPAGE_CODELESS 37, LOCAL_SERVICES_ADS 51.
- **CustomerConversionGoal** 리소스 이름. `customers/{customer_id}/customerConversionGoals/{category}~{origin}`. 카테고리와 출처는 열거형 이름 (`PHONE_CALL_LEAD~WEBSITE`). `biddable`은 목표 자체에 설정돼요.

## 중지 시험 밖의 측정

- 구글은 자체 증분 실험(Conversion Lift) 최소 금액을 2025년에 **5,000달러**로 내렸어요. 베이지안 방법. 작은 지역 계정은 전화 기록에 대한 무료 중지 시험(`/ads-incrementality-check`)이 같은 질문에 답해요. 한국에서 그 분모는 전화 기록, 네이버 스마트콜, 카카오 문의이고, 구글 비즈니스 프로필 통화 클릭은 구글 캠페인을 시험할 때 같이 넣어요. 5,000달러는 구글 상품의 최소액이지 한국 계정에 권하는 예산이 아니에요.

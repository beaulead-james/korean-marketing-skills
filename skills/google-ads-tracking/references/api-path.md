# 구글 광고 API 경로 (선택)

개발자 토큰이 있고, 감사를 API로 읽거나 고침을 스크립트로 할 때 읽어요. SKILL.md의 화면 경로가 같은 답을 손으로 내요. API 버전과 열거형 숫자는 `google-ads-facts.md`에 있어요. 먼저 그 헤더를 봐요.

## 준비

구글 광고 관리자 계정의 개발자 토큰(기본 액세스는 짧은 심사 뒤), 그 계정을 볼 수 있는 사용자의 OAuth, 고객 ID(숫자 10자리, 하이픈 없음)가 필요해요. 계정이 관리자 아래면 관리자 ID를 `login-customer-id`로 보내요. 모든 호출에 `Authorization: Bearer <token>`과 `developer-token: <token>`이 가요. `.env`에만 두고 출력하지 않아요.

클라이언트 라이브러리 관례의 변수 이름이에요. `GOOGLE_ADS_DEVELOPER_TOKEN`, `GOOGLE_ADS_CLIENT_ID`, `GOOGLE_ADS_CLIENT_SECRET`, `GOOGLE_ADS_REFRESH_TOKEN`, `GOOGLE_ADS_CUSTOMER_ID`, 관리자 아래면 `GOOGLE_ADS_LOGIN_CUSTOMER_ID`. 공유 기능 점검이 보는 것은 개발자 토큰뿐이고, 나머지는 API 경로가 돌 때 `.env`에서 읽어요. 갱신 토큰을 `https://oauth2.googleapis.com/token`에서 `grant_type=refresh_token`으로 바꿔 짧은 액세스 토큰을 받아요. OAuth가 없으면 SKILL.md의 화면 경로를 써요.

## 감사를 만드는 쿼리 넷

`POST https://googleads.googleapis.com/<version>/customers/<id>/googleAds:search`에 `{"query": "..."}`. REST는 열거형 필드를 이름으로 돌려요 (`"TARGET_SPEND"`). 그게 원하는 값이에요. 어떤 클라이언트 라이브러리는 숫자를 돌려요. 라이브러리의 열거형 도우미로 바꾸고, 손으로 쓴 지도는 쓰지 않아요.

**1. 전환 액션과 설정**

```sql
SELECT conversion_action.id, conversion_action.name, conversion_action.type,
  conversion_action.category, conversion_action.origin, conversion_action.status,
  conversion_action.primary_for_goal, conversion_action.include_in_conversions_metric,
  conversion_action.counting_type, conversion_action.click_through_lookback_window_days
FROM conversion_action
WHERE conversion_action.status != 'REMOVED'
```

**2. 액션이 실제로 기록한 것** (GAQL에 LAST_90_DAYS 리터럴은 없어요. 날짜를 써요)

```sql
SELECT segments.conversion_action_name, metrics.conversions, metrics.all_conversions
FROM customer
WHERE segments.date BETWEEN '2026-08-15' AND '2026-11-12'
```

날짜는 감사 기간으로 바꿔요. 위 구간은 형식 예시예요.

**3. 어떤 목표가 입찰하는지. 계정과 캠페인**

```sql
SELECT customer_conversion_goal.category, customer_conversion_goal.origin,
  customer_conversion_goal.biddable
FROM customer_conversion_goal
```

```sql
SELECT campaign.name, conversion_goal_campaign_config.goal_config_level
FROM conversion_goal_campaign_config
```

**4. 입찰 전략, 예산, 노출을 놓친 이유**

```sql
SELECT campaign.name, campaign.status, campaign.bidding_strategy_type,
  campaign_budget.amount_micros, metrics.cost_micros, metrics.clicks, metrics.conversions,
  metrics.search_impression_share, metrics.search_budget_lost_impression_share,
  metrics.search_rank_lost_impression_share
FROM campaign
WHERE campaign.status = 'ENABLED' AND segments.date DURING LAST_30_DAYS
```

`amount_micros`와 `cost_micros`는 계정 통화의 100만분의 1이에요. 40000000은 그 통화의 40.00이에요. 원화 계정의 하루 예산 4만 원은 40000000000이에요. 달러 계정의 40달러를 원화 40원으로 읽지 않아요.

## 입찰 함정과 고침

`customer_conversion_goal.biddable`은 각 액션의 `primary_for_goal`에서 **유도되지 않아요.** 실제로 본 것.

- 목표 안의 유일한 액션에 `primary_for_goal=false`를 줘도 그 목표는 입찰 가능으로 남았어요.
- `primary_for_goal=false`로 새 액션을 만들어도 그 목표가 입찰 가능해졌어요.

목표 자체를 `customerConversionGoals:mutate`로 고쳐요.

```json
POST https://googleads.googleapis.com/<version>/customers/<id>/customerConversionGoals:mutate
{
  "operations": [{
    "updateMask": "biddable",
    "update": {
      "resourceName": "customers/<id>/customerConversionGoals/PURCHASE~CALL_FROM_ADS",
      "biddable": false
    }
  }]
}
```

리소스 이름은 **열거형 이름**이에요. `PURCHASE~CALL_FROM_ADS`. 같은 쌍의 숫자 형태는 요청 오류예요. 그다음 쿼리 3을 다시 돌려 결과를 확인해요. 쓰기 성공 응답만으로 목표가 바뀌었다고 보고하지 않아요.

## 웹사이트 리드 액션 만들기

한 수리에서 쓴, 리드 액션에 중요한 필드예요.

```
name: "Web: Phone Tap"
type: WEBPAGE
category: PHONE_CALL_LEAD
status: ENABLED
counting_type: ONE_PER_CLICK
click_through_lookback_window_days: 30
value_settings: { default_value: 0, always_use_default_value: true }
primary_for_goal: true
```

폼 액션은 같고 `category: SUBMIT_LEAD_FORM`. 폼을 거의 안 쓰면 `primary_for_goal: false`로 두고, 위의 목표 입찰 여부를 확인해요. 만든 뒤에 `conversion_action.tag_snippets`를 다시 읽어 사이트가 쓸 전환 라벨을 받아요. 라벨은 액션이 생기기 전에 알 수 없어요. 라벨은 비밀은 아니지만 계정을 식별해요. 실제 라벨은 공개되는 곳에 두지 않아요.

## 쓰기 규율

- 스크립트 기본은 드라이런이에요. 계획된 변경(객체, 필드, 이전, 이후)을 인쇄해요. 쓰기는 명시 플래그와, 그 변경에 대한 사용자의 예스가 필요해요.
- 진단 중에는 한 번에 하나. 둘을 같이 바꾸면 결과를 읽을 수 없어요.
- 목표와 입찰 변경은 그것을 쓰는 모든 캠페인의 학습을 다시 시작해요. 일시정지 캠페인도 재개하면 그래요. 보고서에 적어요.
- 전환 액션 삭제는 되돌릴 수 없어요. 자리표시는 숨겨요.

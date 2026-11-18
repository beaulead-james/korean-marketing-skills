# 코드로 캠페인 게시

기본 URL `https://graph.facebook.com/v26.0` (버전은 만료돼요. `meta-facts.md`를 봐요)
인증 `Authorization: Bearer $META_ACCESS_TOKEN`

## 객체 계층

```
캠페인          목표, 특수 광고 카테고리, 구매 유형
  └─ 광고 세트   예산, 일정, 타겟, 최적화, 입찰 전략
       └─ 광고   광고 세트와 소재를 짝지음
            └─ 광고 소재    이미지·영상 + 문안 + 링크 + CTA, 페이지에 묶임
```

예산은 **캠페인(CBO) 또는 각 광고 세트 중 하나**에만 있어요. 둘 다는 아니에요.
광고 세트에 예산이 있으면 캠페인에 `is_adset_budget_sharing_enabled`가 필요해요.

## 최소 요청 도우미

```js
const GRAPH = `https://graph.facebook.com/${process.env.META_GRAPH_VERSION || 'v26.0'}`;

async function graph(path, { method = 'GET', body } = {}) {
  const init = { method, headers: { Authorization: `Bearer ${process.env.META_ACCESS_TOKEN}` } };
  if (body) {
    init.headers['Content-Type'] = 'application/json';
    init.body = JSON.stringify(body);
  }
  const res = await fetch(`${GRAPH}/${path}`, init);
  const json = await res.json().catch(() => ({}));
  if (!res.ok) {
    const e = json.error || {};
    // error_user_msg가 사람이 읽는 쪽이고, 종종 유일한 쓸모예요
    throw new Error(`${res.status} ${e.message || JSON.stringify(json).slice(0, 300)}`
      + (e.error_user_msg ? ` | ${e.error_user_msg}` : ''));
  }
  return json;
}
```

메타 오류는 `message`(개발자용)와 가끔 `error_user_msg`(화면이 보여줄 말)를 가져요. 둘 다 남기세요. 원인을 자주 다르게 말해요.

## 캠페인

```js
await graph(`${AD_ACCOUNT}/campaigns`, { method: 'POST', body: {
  name: '한빛설비 | 대구 | 리드 | 2026-11',
  objective: 'OUTCOME_LEADS',
  status: 'PAUSED',
  special_ad_categories: [],
  buying_type: 'AUCTION',
  is_adset_budget_sharing_enabled: false,
}});
```

이름은 예시예요. 한빛설비는 지어낸 상호예요. 목표(ODAX. 옛 `LINK_CLICKS` 시대 이름은 없음).
`OUTCOME_LEADS`, `OUTCOME_SALES`, `OUTCOME_TRAFFIC`, `OUTCOME_AWARENESS`,
`OUTCOME_ENGAGEMENT`, `OUTCOME_APP_PROMOTION`.

`special_ad_categories`는 **생성 뒤에 바꾸기 어려워요.** 틀리면 캠페인을 지우고 다시 시작해요. 채용, 주택, 금융 상품, 사회 이슈·선거·정치는 각자 카테고리와 제한이 있어요. 한국만 대상이면 빈 배열로 빠질 수 있어요. 범위는 `meta-facts.md`예요.

## 광고 세트

```js
await graph(`${AD_ACCOUNT}/adsets`, { method: 'POST', body: {
  name: '대구 15km | 넓게',
  campaign_id,
  status: 'PAUSED',
  daily_budget: 30000,                       // 원화 오프셋 1. 3만 원
  billing_event: 'IMPRESSIONS',
  bid_strategy: 'LOWEST_COST_WITHOUT_CAP',
  optimization_goal: 'OFFSITE_CONVERSIONS',
  promoted_object: { pixel_id: PIXEL_ID, custom_event_type: 'LEAD' },
  targeting: {
    geo_locations: {
      custom_locations: [{ latitude: 35.8714, longitude: 128.6014, radius: 15, distance_unit: 'kilometer' }],
    },
    age_min: 18, age_max: 65, genders: [1, 2],
    targeting_automation: { advantage_audience: 1 },
  },
}});
```

좌표는 대구 도심의 공개된 대략 위치예요.

**예산은 계정 통화의 최소 단위예요.** 원화는 오프셋 1이라 `30000`이 3만 원이에요. 달러는 오프셋 100이라 `3000`이 30.00달러예요. 원화에 달러식 100배를 보내면 100배 과다 지출이고, 이 API에서 가장 비싼 실수예요. 보내기 전에 `currency`를 읽어요.

**`bid_strategy`는 명시해야 해요.** 예산은 있는데 전략이 없는 광고 세트를 메타가 거절해요. `LOWEST_COST_WITHOUT_CAP`이 새 픽셀의 기본으로 맞아요. 전환 이력이 없는 픽셀의 입찰 상한은 배우기 전에 전달을 조여요.

**지역 타겟**은 `custom_locations`(위도·경도·반경) 또는 이름 있는 `cities` / `regions` / `countries`예요. 반경 상한은 쓰기 전에 확인해요. 특수 광고 카테고리를 선언하고 미국·캐나다 오디언스에 닿으면 최소 15마일이에요. 여러 점 주변의 근접 타겟으로 도 전체를 사지 않고 생활권을 덮어요. 한국은 시·군·구 단위로 점을 찍어요.

자주 쓰는 최적화 목표. `OFFSITE_CONVERSIONS` (`promoted_object` 필요), `LEAD_GENERATION`(즉시 양식), `LANDING_PAGE_VIEWS`, `LINK_CLICKS`, `REACH`, `THRUPLAY`.

## 이미지 올리기

이미지는 멀티파트예요. JSON 도우미는 파일을 못 실어요.

```js
const form = new FormData();
form.append('filename', new Blob([readFileSync(file)]), basename(file));
const res = await fetch(`${GRAPH}/${AD_ACCOUNT}/adimages`, {
  method: 'POST',
  headers: { Authorization: `Bearer ${TOKEN}` },
  body: form,
});
const json = await res.json();
const hash = Object.values(json.images)[0].hash;
```

응답은 망가진 파일 이름을 키로 써요. 키를 찾지 말고 값을 읽어요.

## 광고 소재

```js
await graph(`${AD_ACCOUNT}/adcreatives`, { method: 'POST', body: {
  name: 'variant-a',
  object_story_spec: {
    page_id: PAGE_ID,
    link_data: {
      image_hash: hash,
      link: 'https://example.com/daegu?utm_source=facebook&utm_medium=paid&utm_campaign=hanbit-2026-11&utm_content=MA-H2-A-v1',
      message: PRIMARY_TEXT,     // 이미지 위 본문
      name: HEADLINE,            // 이미지 아래 굵은 줄
      description: DESCRIPTION,  // 제목 아래 작은 줄
      call_to_action: { type: 'LEARN_MORE' },
    },
  },
}});
```

`example.com`은 자리표시예요. 소재는 **불변**이에요. 문안이나 이미지를 바꾸면 새 소재와 새 광고를 만들어요. 수정은 없어요.

CTA 유형에 `LEARN_MORE`, `APPLY_NOW`, `CONTACT_US`, `GET_QUOTE`, `SIGN_UP`, `SHOP_NOW`, `CALL_NOW`가 있어요. 목표에 따라 막히는 것이 있어요. 한국어 버튼 이름은 광고 관리자 목록을 따라요.

`utm_content`에 변형 이름을 넣어, 광고 관리자만이 아니라 자기 분석에서 성과가 돌아가게 해요.

## 광고

```js
await graph(`${AD_ACCOUNT}/ads`, { method: 'POST', body: {
  name: 'variant-a',
  adset_id,
  creative: { creative_id },
  status: 'PAUSED',
}});
```

## 소재 교체

소재가 불변이므로, 반복은 광고를 지우고 다시 만드는 일이에요.

```js
const existing = await graph(`${adsetId}/ads?fields=id,name&limit=50`);
for (const ad of existing.data) await graph(ad.id, { method: 'DELETE' });
// 그다음 위의 방식으로 새 소재와 광고를 만들어요
```

*광고*를 지우면 광고 세트의 학습은 남아요. 광고 세트를 지우면 리셋돼요.

## 결과 읽기

```js
await graph(`${campaignId}/insights?fields=spend,impressions,clicks,actions,cost_per_action_type`
          + `&date_preset=last_7d&level=ad`);
```

`actions`는 `{ action_type, value }`의 배열이에요. 전환은 `offsite_conversion.fct.lead` 같은 이름으로 그 안에 있어요. 최상위 필드가 아니에요. `spend`는 계정 통화의 소수 문자열이에요. 원화 계정이면 원으로 읽어요.

**귀속된 전환은 일으킨 전환이 아니에요.** 메타는 기여 기간 안의 노출이나 클릭에 맞출 수 있는 것을 보고해요. 어차피 전환할 사람 포함. 실제 예산이 있으면 홀드아웃이나, 총량의 전후를 매체 숫자와 비교해요. 전화 업종은 전화 기록, 스마트콜, 카카오 문의예요.

## 에이전트 안전 규칙

- **항상 일시정지로 만들어요.** 켜기는 사람이 확인하는 별도 단계예요.
- **먼저 드라이런.** 쓰기가 없는 `--check`가 객체가 생기기 전에 권한과 설정 문제를 잡아요.
- **보내기 전에 예산 범위를 확인해요.** 기대 구간의 정수인지. `NaN`이나 통화 단위가 틀린 값은 던져야 해요.
- **실패한 실행의 고아를 치운 뒤** 다시 시도해요.
- **토큰을 커밋하지 않아요.** 환경 변수만.

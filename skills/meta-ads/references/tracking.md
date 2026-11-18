# 전환 추적, 그리고 동작 증명

"픽셀이 깨졌다"는 조사의 대부분은 픽셀이 아니라 *픽셀을 재는 방법*이 깨진 경우예요. 바르게 설치하고, 묻는 것을 볼 수 있는 계측으로 확인해요.

## 구조. 경로 둘, 이벤트 ID 하나

```
브라우저  ──fbq('track','Lead',{...},{eventID: X})──►  메타
서버      ──POST /[PIXEL_ID]/events  event_id: X   ──►  메타
                                                       └─ 중복 제거되어 전환 하나
```

서버 경로가 있는 이유는 광고 차단기와 추적 방지가 브라우저 경로를 버리기 때문이에요. 영어권에서 말하던 "약 3분의 1"은 한국 숫자가 아니에요. 둘을 보내고 중복을 제거하면, 두 번 세지 않고 놓친 전환을 되찾아요.

**중복 제거는 양쪽의 `event_id`와 `event_name`이 같고, 48시간 안이어야 해요.** 메타는 먼저 받은 것을 남기고 중복을 버려요. ID는 브라우저에서 한 번 만들어 서버로 넘기세요.

## 브라우저

```html
<script>
!function(f,b,e,v,n,t,s){/* 메타 기본 스니펫 */}(...);
fbq('init', 'PIXEL_ID');
fbq('track', 'PageView');
</script>
```

전환 순간에.

```js
const evId = crypto.randomUUID();

fbq('track', 'Lead', { content_name: 'contact-form' }, { eventID: evId });

await fetch('/api/lead', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    ...formData,
    meta: {
      event_id: evId,
      event_source_url: window.location.href,
      fbp: cookie('_fbp'),
      fbc: cookie('_fbc'),
    },
  }),
});
```

**`_fbp`와 `_fbc`는 브라우저에서 읽어 전달해야 해요.** 자기 도메인의 자사 쿠키예요. 다른 곳에서 도는 서버(다른 호스트의 서버리스, 다른 서브도메인, 제3자 백엔드)는 그 쿠키를 받지 못하고, 없으면 서버 이벤트의 매칭이 크게 줄어요. `_fbc`는 방문자가 `fbclid` 매개변수로 들어왔을 때만 있어요.

## 서버 (전환 API)

```js
const res = await fetch(`https://graph.facebook.com/v26.0/${PIXEL_ID}/events`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    access_token: CAPI_TOKEN,
    data: [{
      event_name: 'Lead',
      event_time: Math.floor(Date.now() / 1000),
      event_id: meta.event_id,             // 중복 제거 키
      event_source_url: meta.event_source_url,
      action_source: 'website',
      user_data: {
        em: [sha256(email.trim().toLowerCase())],
        ph: [sha256(phoneE164)],
        client_ip_address: ip,
        client_user_agent: userAgent,
        fbp: meta.fbp,
        fbc: meta.fbc,
      },
    }],
  }),
});
```

**`em`과 `ph`는 SHA-256으로 해시해요. 소문자, 앞뒤 공백 제거.** 전화는 `+` 없는 E.164. 한국 휴대전화 예시는 `821012345678` 형태예요. 실제 고객 번호는 넣지 않아요. `fbp`, `fbc`, `client_ip_address`, `client_user_agent`는 원문으로 보내요. 해시하면 매칭이 깨져요.

`user_data` 필드가 많을수록 매칭 품질이 좋아요. 메타는 이벤트 소스마다 점수를 매겨요. 약 5.0 아래면 서버 경로의 기여가 적어요. 5.0은 메타 매칭 품질 점수예요. 한국 전환율 통계가 아니에요.

이메일과 전화를 전환 매칭에 쓰면 개인정보보호법상 목적 고지와 처리 근거가 필요해요. 조문 번호는 단정하지 않아요. 해시해도 개인정보 처리예요.

## 서버가 자기 결과를 보고하게

CAPI 호출이 사용자의 행동을 실패시키면 안 돼요. 기여 이벤트 하나를 잃으려고 폼 제출을 실패시킬 이유는 없어요. 그 올바른 설계는 몇 달간 조용히 썩을 수도 있어요. 그래서 결과를 돌려요.

```js
const capi = await sendCapi(payload).catch(e => ({ ok: false, error: e.message }));

return json({
  success: true,
  id: record.id,
  meta_capi: capi.ok ? `sent:${capi.events_received}` : `failed:${capi.error}`,
});
```

`curl` 한 번이 브라우저와 광고 차단기 없이 서버 경로 전체를 증명해요. 논쟁을 끝내는 확인이에요.

## 확인. 각 계측이 실제로 보는 것

| 계측 | 보는 것 | 못 보는 것 |
|---|---|---|
| 메타 **테스트 이벤트** | 브라우저 이벤트는 실시간. 서버 이벤트는 **`test_event_code`가 있을 때만** | 그 코드 없는 서버 이벤트 |
| 이벤트 관리자 **개요** | 양과 매칭 품질, 약 20분 지연 | 방금 일어난 일 |
| 브라우저 개발자 도구 **네트워크** | facebook.com으로 가는 XHR/fetch | **`sendBeacon`**. eventID가 있으면 fbevents가 이걸 써요 |
| `performance.getEntriesByType('resource')` | 리소스 타이밍에 잡힌 요청 | **`sendBeacon`**. 같은 맹점 |
| 서버 응답의 `meta_capi` | 서버가 보내고 받은 것 그대로 | 브라우저 쪽 전부 |
| 메타 **픽셀 헬퍼** 확장 | 픽셀 존재, 이벤트 발생, 매개변수 경고 | 서버 이벤트 |

**이 표의 오른쪽 칸에서 거짓 음성 셋이 나왔어요.** 이벤트가 안 찍힌다고 결론 내기 전에, 계측이 찍혔다면 볼 수 있었는지 확인해요.

## 라이브러리가 실제로 로드됐는지

```js
typeof window.fbq.callMethod === 'function'   // true면 진짜 fbevents.js
window.fbq.queue.length                        // 0보다 크고 자라면 아직 스텁
```

`fbq.loaded`와 `fbq.version`은 **인라인 스텁**이 설정해요. `fbevents.js`가 막혀도 참이에요. 아무것도 증명하지 않아요.

## CSP

이 출처를 빼먹은 Content-Security-Policy는 눈에 보이는 오류 없이 픽셀을 죽여요. `fbq`는 스텁으로 남고, 이벤트를 쌓고, 영원히 안 보내요.

```
script-src   https://connect.facebook.net
connect-src  https://www.facebook.com  https://connect.facebook.net
frame-src    https://www.facebook.com
```

**배포된 사이트에서 확인해요.** localhost는 보통 CSP를 아예 안 보내서, localhost 시험은 통과하고 프로덕션은 몇 주째 조용히 깨져 있을 수 있어요.

## 최적화할 이벤트 고르기

**의미하는 순간에 찍어요.** 예약 달력이 *그려질 때* 찍는 `Schedule`은 "달력을 본 사람"이에요. 그쪽으로 최적화하면 메타는 들어왔다가 나가는 사람을 찾아요. 진짜 이벤트는 임베드의 성공 콜백을 쓰고, 그리기는 별도 맞춤 이벤트로 둬요.

**물량으로 최적화하고, 진실로 측정해요.** 메타는 광고 세트당 한 주 약 50전환이 있어야 학습을 벗어나요. 그 아래는 전달이 들쭉날쭉하고 CPA는 소음이에요. 진짜 결과가 주 50보다 드물면, 물량이 더 많은 앞 단계(`Purchase`가 아니라 `Lead`)에 입찰하고 진짜 결과는 보고로 남겨요. 약 50은 메타 학습 숫자예요.

전환에 **모형 값**(`value`와 `currency`)을 넣는 것을 검토해요. 가치 입찰이 같은 폼 제출을 전부 같게 보지 않고, 자격 있는 리드와 그냥 누른 사람을 나누게. 통화는 계정에 맞게. 한국 사업자는 `KRW`와 원 금액.

## 자동 이벤트 감지

메타는 버튼 클릭과 폼 동작을 스스로 감지해 이벤트로 만들 수 있어요 (`Subscribe`와 `Contact`가 흔해요). 그 지어낸 이벤트가 보고에 나타나고 최적화에 채택될 수 있어요. 꺼요. 이벤트 관리자, 픽셀, 설정, 자동 감지 이벤트 토글. 이름과 위치는 이벤트 관리자 버전마다 움직여요.

자동 고급 매칭은 다른 설정이에요. 이메일·전화 같은 폼 필드를 해시해 매칭을 돕어요. 사이트의 개인정보 처리방침이 막지 않으면 켜 둬요.

## 정리

시험 전환은 프로덕션 데이터 세트와 데이터베이스에 들어가요. 시험 기록은 나중에 지워요. 메타 쪽에 남은 시험 이벤트는 지울 수 없어요. 기여 기간이 지나며 낡아요.

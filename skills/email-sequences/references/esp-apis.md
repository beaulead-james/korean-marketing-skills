# ESP API 메모: Kit v4, Beehiiv v2, Resend (그 외는 감지만)

last-verified: 2026-11-18 · ttl-days: 90 · refresh: `developers.kit.com/llms.txt`, `developers.beehiiv.com/llms.txt`, `resend.com/docs/llms.txt`, `loops.so/docs/llms.txt` 를 다시 받아 아래 경로와 페이로드를 고친다. 스티비·메일리·카카오 비즈메시지·문자 대행사는 이 파일의 푸시 대상이 아니다. 각 콘솔 현재 안내를 본다.
changes: 2026-09-02. Resend Automations가 생겨 "시퀀스 엔진 없음"을 뺐고, Audience는 Contacts·Segments·Topics가 되었다. Loops는 캠페인·워크플로 생성을 API로 연다. Kit v3는 레거시이며 폐기 예고는 없고, `per_page` 최대 1000, 비활성 시퀀스에 이메일로 등록하면 422, 통계 보관은 2026-10-15부터. HubSpot 마케팅 이메일 v1은 종료, v3 발행은 엔터프라이즈. Beehiiv 포스트 생성은 여전히 베타·엔터프라이즈. 2026-11-18 각색에서는 끝점을 바꾸지 않았고, 한국 도구는 파일 인계라고만 밝혔다.

시퀀스를 ESP에 넣거나 캠페인 통계를 당길 때만 읽어요 (SKILL.md 1단계, 5단계). 만드는 호출은 모두 게이트가 있어요. 정확한 페이로드를 보여 주고 "네, 초안 만들어 주세요" 전에 POST하지 않아요. 예약이나 실발송은 두 번째 확인이 있어도 이 스킬이 하지 않아요.

한국어 리스트의 기본 도구는 스티비, 메일리, 카카오 비즈메시지, 문자 대행사예요. 그 API를 이 파일이 구현한다고 말하지 않아요. 문안 파일로 넘기고, 콘솔에서 사람이 검토해요. 아래는 키가 이미 있는 Kit, Beehiiv, Resend예요.

## Kit (예전 ConvertKit. 브랜드는 2024년 10월부터 Kit. 산출물에서 ConvertKit이라고 부르지 않아요)

- Base `https://api.kit.com`. 헤더 `X-Kit-Api-Key: $KIT_API_KEY` (설정 → Developer의 v4 키). 레거시 `CONVERTKIT_API_KEY`는 대개 v3. Kit은 v3를 레거시로 부르며(동작, 제거 예고 없음) 문서는 v4만. v4 키를 받게 해요.
- 페이지. 커서 (`after`=end_cursor, `before`=start_cursor). `per_page` 기본 500, 최대 1000.

**Kit은 API로 시퀀스 전체를 만들 수 있어요.** 껍데기, 그다음 통마다 한 번.

```bash
curl -X POST https://api.kit.com/v4/sequences \
  -H "X-Kit-Api-Key: $KIT_API_KEY" -H "Content-Type: application/json" \
  -d '{"name":"<sequence name>","send_hour":9,"time_zone":"Asia/Seoul","active":false}'
```

다른 필드. email_address, email_template_id, send_days, repeat, hold, exclude_subscriber_sources.

```bash
curl -X POST https://api.kit.com/v4/sequences/{sequence_id}/emails \
  -H "X-Kit-Api-Key: $KIT_API_KEY" -H "Content-Type: application/json" \
  -d '{"subject":"<subject A>","preview_text":"<preview>","content":"<html>",
       "delay_value":2,"delay_unit":"days","position":1,"published":false}'
```

- `delay_value` / `delay_unit`(`days` 또는 `hours`)은 이전 통 기준(첫 통은 진입). 첫 통만 즉시(`delay_value: 0`).
- `position`은 0부터. `published: false`가 초안.
- **푸시.** `active: false`와 `published: false`로만 만들고 Kit URL을 건네요. 사용자가 켜요. `active: true`를 직접 넣지 않아요.
- 단발(출시). `POST /v4/broadcasts`. 문서가 subject, preview_text, content, description, public, published_at, subscriber_filter 일곱을 필수로 표시. **`send_at: null`이 초안.** ISO8601 `send_at`은 예약이라 넣지 않아요.
- 등록. `POST /v4/sequences/{sequence_id}/subscribers/{subscriber_id}` (빈 본문) 또는 `.../subscribers`에 `{"email_address": ...}`. 구독자는 이미 있어야 해요(`POST /v4/subscribers`, upsert). 시퀀스가 활성이어야 하고, 초안에서 이메일 등록은 422 "Sequence is inactive". 등록은 사용자가 켠 **뒤**이지 푸시의 일부가 아니에요.

**통계.**

- `GET /v4/broadcasts`로 id. `GET /v4/broadcasts/{id}/stats`에 recipients, emails_opened, open_rate, total_clicks, click_rate, unsubscribes, unsubscribe_rate. 묶음은 `GET /v4/broadcasts/stats?broadcast_ids[]=...`.
- 제목 패턴은 `click_rate`. `open_rate`는 부풀은 잡음.
- 2026-10-15부터 API 통계는 최근 5년만.

## Beehiiv

- Base `https://api.beehiiv.com/v2`. `Authorization: Bearer $BEEHIIV_API_KEY`.
- 첫 호출 `GET /v2/publications`에서 `pub_...` id.

**API로 되는 것과 안 되는 것.**

- **자동화와 그 메일은 UI에서 만들어요. API가 아니에요.** API는 자동화 목록(`GET .../automations`), 자동화의 메일 목록, 구독자 등록은 되고, 플로나 본문은 못 만들어요. 시퀀스 푸시는 통별 파일을 붙여 넣게 하고, 등록만 API.
- 등록. `POST /v2/publications/{pubId}/automations/{automationId}/journeys`에 `{"email": "..."}` 또는 `{"subscription_id": "sub_..."}`. 자동화에 **"Add by API"** 트리거가 활성이어야 해요. 편집 화면에서 사용자가 켜요. 신규는 `POST /v2/publications/{pubId}/subscriptions`에 email과 `automation_ids`. `utm_source` 등도 받아요.
- 단발은 포스트로 만들 수 있어요. `POST /v2/publications/{pubId}/posts`. `title` 필수, `body_content`(HTML) 또는 `blocks`, `email_subject_line`, `email_preview_text`, `status`. 기본이 confirmed라 **항상 `"draft"`**. `scheduled_at`은 넣지 않아요. `recipients`로 등급·세그먼트. 생성은 2026-09 재확인 기준으로 베타이고 **엔터프라이즈**. 404나 403이면 플랜에 없는 것. 파일로 돌아가요. 생성은 비동기라 바로 GET이 202일 수 있어요.

**통계.**

- `GET /v2/publications/{pubId}/posts?expand=stats&limit=<100 이하>&order_by=publish_date&direction=desc`
- 포스트 `stats.email`에 recipients, delivered, unique_opens, open_rate, unique_clicks, verified_clicks(봇을 거른 값, 이쪽을 우선), click_rate, unsubscribes, spam_reports. `spam_reports / delivered`를 0.10% 선과 견주는 것은 지메일 쪽 건강 점검이에요. 넘는 포스트가 있으면 표시.

## Resend

- Base `https://api.resend.com`. `Authorization: Bearer $RESEND_API_KEY`.
- **Automations.** 이벤트 트리거 플로(예: `user.created` 다음 delay, condition, wait-for-event, send_email). send_email은 저장된 Template. 시퀀스는 메일 사이 delay가 있는 automation 하나. 세그먼트가 아니라 이벤트마다라, 앱이 이벤트를 내보내야 해요. 대시보드 또는 `POST /automations` `{name, steps[], connections[], status}`. `status` 기본이 `"disabled"`. 그대로 두고 사용자가 켜요. 템플릿 id가 먼저 있어야 해요.
- 단발 Broadcast. `POST /broadcasts`. `segment_id` 필수, `from`(`"이름 <addr@domain>"`), `subject`, `html` 또는 `text`, `name`, `reply_to`, 선택 `topic_id`. 기본은 초안. `send: true`는 발송이라 넣지 않아요. `scheduled_at`도 `send: true`가 필요해서 넣지 않아요. 나중 발송은 사용자가 `POST /broadcasts/{id}/send`.
- 세그먼트 `GET /segments`. Audience는 전역 Contacts, Segments, Topics로 바뀌었어요. 연락처 끝점에 `audience_id`가 필요 없어요.
- 수신거부. Broadcast와 Automation 본문에 `{{{RESEND_UNSUBSCRIBE_URL}}}`. 거래용 `POST /emails`로 마케팅을 넣지 않아요. 그 끝점은 `List-Unsubscribe`를 직접 넣어야 해요.

## 감지만 (여기서 푸시 배선을 하지 않아요)

- **Loops** (`LOOPS_API_KEY`, base `https://app.loops.so/api`, Bearer). API가 캠페인(`POST /v1/campaigns`, Draft와 빈 `emailMessageId`)과 워크플로(`POST /v1/workflows`, 빈 트리거와 종료 노드)를 만들 수 있어요. 노드는 workflow-nodes. 일부 팀은 "workflow creation is unavailable". 여기선 파일 인계와 연락처·이벤트만. API로 짓고 싶으면 `loops.so/docs/llms.txt`를 다시 받아요.
- **Mailchimp** (`MAILCHIMP_API_KEY`, 키 접미사 `-usX`가 서버, base `https://<usX>.api.mailchimp.com/3.0`). Customer Journey는 UI. API는 단계 트리거만(`POST /customer-journeys/journeys/{id}/steps/{step_id}/actions/trigger`). 캠페인 생성은 가능. 통계는 `/campaigns`와 `/reports`. 기억으로 journey 페이로드를 만들지 않아요.
- **HubSpot** (`HUBSPOT_ACCESS_TOKEN`, 비공개 앱 토큰). Marketing Emails v3 (`/marketing/v3/emails`)는 GA, v1은 종료. 발행·발송은 Marketing Hub Enterprise 또는 거래 애드온. 워크플로는 엔터프라이즈 형태. 기본은 파일. 사용자가 청하면 현재 문서를 다시 받아요.

## 통계를 learnings로

시퀀스를 통계로 받쳤으면 `./brand/learnings.md`에 표준 형식. 예.

`- [2026-11-18] [email-sequences] 구체 숫자 제목이 질문 제목보다 클릭이 높음 (n=12 sends, source: beehiiv-api)`

발송 n이 4 미만이면 대화에만 말하고 사전 지식으로 남기지 않아요. 배율은 실제 계산일 때만. 예시 배율을 사실처럼 쓰지 않아요.

카카오·문자·스티비 화면을 사용자가 붙여 넣으면 `source:`에 `stibee-csv`, `kakao-export`처럼 적어요. 없는 API를 호출한 것처럼 쓰지 않아요.

---
name: performance-review
description: 붙여 넣은 CSV, 대시보드 스크린샷, 읽기 전용 API(서치어드바이저, GSC, GA4, PostHog, Beehiiv, Kit, 검색광고)를 정직한 진단과 learnings.md 프라이어, 스킬로 잇는 다음 행동 3~5개로 바꿔요. 발행 뒤 숫자가 있을 때와 월간 루틴에 쓰세요. 채널이 주장하는 성과를 그 사업의 카운트(지역은 전화 대장, 온라인은 신규 주문)와 맞춰 본 뒤에만 채널 공을 줘요.
when_to_use: how did it perform, review my numbers, analyze these results, here's my GSC export, read this dashboard screenshot, what's working, did the campaign work, performance review, monthly review, what should I do next based on results, which variant won, close the loop, did the ads actually bring calls, compare my ads to the phone log, which channel deserves the credit, 이번 달 성과 리뷰, 서치어드바이저 내보내기 분석, 파워링크 성과 리뷰, 전화 대장과 광고 비교, 어떤 채널이 전화를 가져왔나, 월간 성과 리뷰, naver search advisor export, powerlink performance review, place stats versus calls
argument-hint: "[붙여 넣은 데이터 / CSV 경로 / 스크린샷 경로] 또는 monthly"
metadata:
  boring:
    version: 1.0.0
    layer: growth
    reads: [assets, learnings, brand-manifest, keyword-plan#cluster-priorities]
    writes: [learnings]
    optional-keys: [GOOGLE_APPLICATION_CREDENTIALS, GSC_SITE_URL, GA4_PROPERTY_ID, POSTHOG_API_KEY, POSTHOG_PROJECT_ID, BEEHIIV_API_KEY, BEEHIIV_PUBLICATION_ID, KIT_API_KEY]
---

# 성과 리뷰

생성 스킬은 베팅을 해요. ★ Quick Pick, 우선순위 1 클러스터, 추천 A/B. 이 스킬은 그 베팅을 실제 숫자와 맞추고, 버틴 것을 `./brand/learnings.md`에 프라이어로 써서 모든 생성 스킬이 다음에 읽고 적용하게 하고, 다음에 고칠 병목 하나를 이름 지어요. 완료는 회의적인 사람이 서명할 진단, 해석 없이 생성 스킬이 적용할 프라이어, 기대 효과로 순위 매긴 다음 행동 3~5개예요. 차트 벽이 아니에요. 아래 파이프라인은 바닥이에요. 눈앞 데이터에 더 나은 판단이 이기면, 한 줄로 말해요. 아래 하드 규칙 둘은 기본값이 아니에요.

1. **읽기 전용.** API는 GET과 보고서 쿼리만. 이 스킬은 연결된 플랫폼의 캠페인, 연락처, 속성, 설정을 수정하지 않아요.
2. **Learnings는 데이터에서.** 모든 항목에 `n=`과 `source:`가 있어요. 표본과 출처가 없는 발견은 보고서의 언급이지 프라이어가 아니에요.

지어낸 숫자 없음. 예시 숫자는 예시. 고객 실명, 전화번호, 광고 계정, 전환 라벨은 브랜드 폴더 밖과 라이브러리에 쓰지 마세요. 이 팩은 유료 제안으로 보내지 않아요.

## 맥락

Only if `./brand/`, `./brands/` or `MARKETING.md` exists (nothing to load otherwise), run:
`python3 ${CLAUDE_SKILL_DIR}/../start-here/scripts/brand_context.py --for performance-review`
(`${CLAUDE_SKILL_DIR}`는 이 스킬 폴더예요. Claude Code 밖에서는 이 파일을 읽은 폴더, 예를 들면 `.agents/skills/performance-review`를 써요. 스크립트나 python3가 없으면 브랜드 폴더를 직접 읽어요. `./brands/active`가 슬러그를 가리키면 `./brands/<slug>/`, 아니면 `./brand/`. 그다음 `MARKETING.md`, `preferences.md`, `reads:`의 파일 (`assets.md`, `learnings.md`, `brand.yaml`, `keyword-plan.md#cluster-priorities`). 아무것도 없으면 단독으로 진행해요. 붙여 넣은 데이터는 그래도 리뷰할 수 있고, 엔티티 매칭은 데이터 자신이 이름 짓는 것까지로 떨어져요.)

`.env` (그리고 `brand.yaml`이 가리키는 캠페인 디렉터리)에서 위 선택 키를 확인해요. 1단계에서 어떤 라이브 수집이 가능한지 정해요. 네이버 서치어드바이저, 검색광고, 플레이스 통계는 키가 아니라 사람이 내보낸 파일이에요.

## 모드

| 트리거 | 모드 |
|---|---|
| 기본. 붙여 넣은 데이터, 파일 경로, 스크린샷, "숫자 봐 줘" | **REVIEW** (1~4단계) |
| "monthly", 또는 예정·비대화 실행 | **MONTHLY** (질문 0) |

퀵 모드: 눈앞 데이터에 대한 좁은 질문 ("어느 제목이 이겼어?", "제일 좋은 페이지는?")은 답과 중요한 주의 하나 (보통 표본 크기). 전체 파이프라인 없음. 보고서 파일은 요청이 있을 때만. 답이 3단계 기준을 넘으면 learnings 항목은 여전히 써요.

---

## 1단계: 수집

도착한 형태 그대로 받아요. 세 intake가 같은 정규 모양으로 모여요.

### 1a. 붙여 넣은 내보내기와 CSV

사용자가 부르는 이름이 아니라 열로 출처를 알아봐요.

| 열이 이렇게 보이면 | 출처 |
|---|---|
| 검색어/페이지, 클릭, 노출, CTR, 순위 | 네이버 서치어드바이저 또는 Google Search Console. 헤더 언어로 구분하고 섞지 마세요 |
| 소스/매체/캠페인, 세션, 주요 이벤트 / 전환 | GA4 |
| 광고 이름 / 광고 세트, 지출, 결과, CPM, CTR | 메타 광고 |
| 캠페인, 키워드, 노출, 클릭, 비용, 전환 | 네이버 검색광고 (파워링크, 브랜드검색) |
| 조회, 통화, 길찾기, 예약, 스마트콜 | 네이버 플레이스 통계 |
| 날짜/시각, 방향, 상태 또는 결과, 통화 시간, 발신/착신 | 전화 시스템 통화 기록 |
| 날짜, 주문 또는 고객 id, 금액, 신규 또는 재방문 | 스토어·결제 주문 (온라인 분모) |
| 캠페인 이름, 노출, 클릭, 지출, 리드 | 링크드인 광고 |
| 제목, 수신/도달, 오픈, 클릭, 수신거부 | Beehiiv, Kit, 스티비, 메일리 캠페인 보고서 |

엑셀 재저장, 로캘 소수점, "1.2천" 약어처럼 섞이거나 망가진 내보내기는 정리하고, 무엇을 가정했는지 한 줄. 해석할 수 없는 열은 추측해서 분석에 넣지 마세요. 네이버 키워드도구의 검색량은 구간이에요. 정확한 월간 검색수처럼 쓰지 마세요.

### 1b. 스크린샷

이미지를 읽어요. 읽을 수 있는 지표를 모두 정규 모양으로 옮기세요. 규칙: 전사하고, 보간하지 마세요 (일부가 가려진 숫자는 추정이 아니라 `UNVERIFIED`). 보이는 기간을 적고, 안 보이면 REVIEW에서는 묻고 MONTHLY에서는 기간을 `unknown`으로. 스크린샷은 가장 낮은 충실도예요. 출처와 가정 노트에 평범한 말로 한 번 말해요.

### 1c. 라이브 API 수집 (키가 있는 곳만, 읽기 전용)

키가 있는 소스만 가져오고, 나머지는 조용히 건너뛰고 커버리지를 출처와 가정 노트에 한 번 말해요. 기본 창: 최근 28일과 그 앞 28일 (MONTHLY는 달력 월). 질문이 다른 기간이면 넓히거나 좁혀요.

**GSC:** 쿼리와 페이지에 Google Search Console을 써요. Google 계정으로 무료이고, 실제 쿼리·노출·클릭률을 더해요. API 수집이 없으면 내보내기 (1a)를 붙여 넣으면 리뷰는 그것으로 돌아요. 수집에는 `GOOGLE_APPLICATION_CREDENTIALS` (Search Console 속성에 사용자로 추가된 서비스 계정, 또는 본인 로그인)와 `GSC_SITE_URL`이 필요해요. 토큰은 Search Console 읽기 범위를 가져야 해요. `gcloud auth application-default login --scopes=https://www.googleapis.com/auth/webmasters.readonly,https://www.googleapis.com/auth/cloud-platform`으로 application-default 자격 증명을 두고, `gcloud auth application-default print-access-token` (또는 google-auth)으로 토큰을 받아요. 헤더 `x-goog-user-project: <your-project-id>`와 URL 인코딩한 사이트 (예: `sc-domain%3Aexample.com`, 또는 인코딩한 URL 접두)를 보내요.

```
POST https://searchconsole.googleapis.com/webmasters/v3/sites/{url-encoded GSC_SITE_URL}/searchAnalytics/query
{"startDate":"<d1>","endDate":"<d2>","dimensions":["page","query"],"rowLimit":5000}
```

네이버 서치어드바이저는 이 엔드포인트가 아니에요. searchadvisor.naver.com 내보내기를 1a로 받아요.

**GA4:** `GA4_PROPERTY_ID`와 같은 Google 자격 증명 (Analytics 읽기 범위).

```
POST https://analyticsdata.googleapis.com/v1beta/properties/{GA4_PROPERTY_ID}:runReport
{"dateRanges":[{"startDate":"<d1>","endDate":"<d2>"}],
 "dimensions":[{"name":"sessionSource"},{"name":"sessionCampaignName"},{"name":"landingPagePlusQueryString"}],
 "metrics":[{"name":"sessions"},{"name":"keyEvents"},{"name":"totalUsers"}]}
```

AI 리퍼러로 거른 두 번째 보고서를 돌려요 (패턴 목록은 `references/metrics-judgment.md`). AI 유입은 자기 채널로 분석해요. 네이버 Cue:와 AI 브리핑 유입은 GA4 리퍼러로 안 잡히는 경우가 많아요. 없다고 단정하지 말고, 잡힌 것만 바닥으로 말해요.

**PostHog:** `POSTHOG_API_KEY` (개인 키, 읽기 범위)와 `POSTHOG_PROJECT_ID`. HogQL은 읽기 쿼리예요.

```
POST https://us.posthog.com/api/projects/{POSTHOG_PROJECT_ID}/query
{"query":{"kind":"HogQLQuery","query":"select properties.utm_campaign, count() from events where event = '<conversion event>' and timestamp > now() - interval 28 day group by 1"}}
```

**Beehiiv:** `BEEHIIV_API_KEY`와 `BEEHIIV_PUBLICATION_ID`.

```
GET https://api.beehiiv.com/v2/publications/{BEEHIIV_PUBLICATION_ID}/posts?expand[]=stats&limit=20
```

**Kit:** `KIT_API_KEY` (헤더 `X-Kit-Api-Key`).

```
GET https://api.kit.com/v4/broadcasts          → 최근 발송
GET https://api.kit.com/v4/broadcasts/{id}/stats → 수신자, 클릭, 수신거부
```

위 호출은 보고서를 읽어요. POST 둘은 Google의 쿼리 엔드포인트이고 여전히 읽기예요. 이 스킬은 원격 객체를 만들거나, 고치거나, 지우지 않아요. 네이버 검색광고와 플레이스에는 쓰지 않아요.

### 1d. 정규화

모든 것이 한 모양으로 모여요. 엔티티 × 지표 × 기간마다 한 행. 작업 데이터예요. `./campaigns/performance/<YYYY-MM-DD>-notes.md`에 저장하고, 붙여 넣지 마세요.

```
| source | period | entity | entity_match | metric | value | flag |
| gsc | YYYY-MM-DD..MM-DD | /blog/proposal-templates | campaigns/content/proposal-templates.md · cluster: proposals (P1) | clicks | 412 | |
| meta-csv | YYYY-MM-DD..MM-DD | MA-H3-B-9x16-v1 | spring-launch/ad-matrix.json · cell MA-H3-B | cpa | 18400 | 72h-lag |
| naver-ads | YYYY-MM-DD..MM-DD | 파워링크/온수기 | spring-launch/ads.md | clicks | 71 | |
```

위 숫자 412, 18400, 71은 표 형식 예시예요. 실제 행은 가져온 값만.

### 1e. 이 시스템이 만든 것과 엔티티 맞추기

다른 스킬이 이름 규칙을 강제하는 이유예요. 매칭은 기계적이고, 이 순서예요.

1. **UTM 캠페인** → `./campaigns/<utm_campaign>/` (생성 스킬이 `utm_campaign`을 캠페인 슬러그로 둬요).
2. **광고 매트릭스 셀 id:** 광고·에셋 이름 안의 `MA-H{1-4}-{A-C}` → `./campaigns/<name>/ad-matrix.json`의 셀.
3. **URL 경로** → `./campaigns/content/<slug>.md`, 그다음 `keyword-plan#cluster-priorities`의 소유 클러스터.
4. **이메일 제목** → `./campaigns/<sequence>/emails/*.md`의 변형 목록.
5. **느슨한 후퇴** → 이름·날짜 근접으로 `assets.md` 대장.

안 맞는 행은 `UNMATCHED`로 분석에 남겨요. 억지로 맞추지 마세요. 미매칭이 대략 3분의 1을 넘으면 이름 규칙이 흐트러진 거예요. 그 자체를 발견으로, 평범한 말로 ("일부 광고는 계획으로 거슬러 못 가서, 2라운드 광고 이름은 매트릭스에서 지으세요").

### 1f. 분모: 그 사업의 기록

광고 플랫폼, GA4, 이메일 도구는 자기가 귀속할 수 있는 것을 보고해요. 고객이 실제로 몇이나 왔는지는 어느 것도 보고하지 않아요. 진단 전에, 같은 기간에 플랫폼이 통제하지 않는 카운트 하나를 구해요.

- **전화로 리드가 오는 사업 (대부분의 지역 서비스):** 전화 시스템의 통화 기록. 하루 인바운드, 대표 번호에서 30초 이상 받은 통화, 고유 발신. 옆에 네이버 플레이스 통화·스마트콜·길찾기. `/speed-to-lead`와 `/ads-incrementality-check`가 CSV에서 이것을 계산하는 스크립트를 가져요.
- **온라인 사업:** 스토어, 결제, CRM의 신규 고객 주문이나 가입. 재방문과 나눠요.
- **CRM이 있는 리드젠:** 생성된 리드와 성사된 거래, 소스 필드별.

정리 규칙은 `references/metrics-judgment.md`의 "분모"를 불러요. 플랫폼 전환은 이 카운트를 대신하지 않고, 이 카운트와 맞춰 읽어요.

기간 규율: 같은 창만 비교해요. 소스가 창을 다르게 말하면 (30일 서치어드바이저 옆에 7일 광고 보고서) 따로 분석하고 그렇다고 말해요. 섞지 마세요. 네이버 검색과 구글 검색은 다른 시장이에요.

---

## 2단계: 진단

**이 단계 전에 `references/metrics-judgment.md`를 불러요.** 작은 표본 예시, 퍼널 산수, 지표가 거짓말하는 표, 채널별 짧은 지표 목록, AI 유입 탐지 패턴이 있어요. 네 동작.

### 2a. 예측 대 실제

생성 스킬이 한 ★ Quick Pick, 우선순위, 추천 A/B는 반증 가능한 예측이에요. 맞춘 산출물에서 모아요 (별 표시된 광고 매트릭스 셀, 키워드 계획 클러스터 우선순위, 이메일 파일의 추천 제목 테스트, 채점된 카피 변형). 각각을 **확인됨** / **반박됨** / **검증 불가** (데이터가 닿지 않음)로 판단해요. 반박된 예측이 리뷰에서 가장 값진 행이에요. 다음 생성 실행을 바꾸는 프라이어가 돼요. 검증 불가는 판결이 아니라 배포 문제예요. 트래픽이 안 간 것과 이유를 한 줄.

### 2b. 작은 표본의 정직한 통계

대부분의 고객은 기간당 n이 1,000 아래예요. 규율 (예시는 레퍼런스).

- **방향이지, 소수점이 아니에요.** "대략 2배", "거의 같음". 두 자릿수에 "+23.7%"를 붙이지 마세요.
- **2배 차이는 신호**예요. 크지 않은 n에서도. **클릭 80에 15% 차이는 잡음**, 사건 한두 개 차이예요.
- **더 드문 사건의 개수**를 비교해요. 전환율 차이가 전환 8 대 6에 서 있으면 차이가 아니에요.
- **유의성 연극을 하지 마세요.** 작은 표본에 p값이나 "95% 확신"을 입히지 마세요. 정직한 판결은 분명한 승, 기울어짐, 아직 모름과 알려면 필요한 n.
- **일관이 크기를 대신해요.** 독립된 발송·게시·주 4~5번에 같은 방향이면, 각각이 작아도 증거예요.
- "이 n에서는 차이를 못 본다"는 완전하고 쓸모 있는 판결이에요. 사과 없이 쓰세요.

### 2c. 지표 문해

숫자로 추론하기 전에 숫자를 고쳐요. 레퍼런스 quirk 표가 각각을 다뤄요. 이메일 오픈은 MPP로 부풀어요 (클릭·답장·수신거부로 판단). GA4 전환은 모델링되고 약 48~72시간에 자리 잡아요. 광고 플랫폼은 지출 뒤 약 72시간 전환을 채워요 (셀을 일찍 부르지 마세요). GSC 순위는 노출 가중 평균이지 등수가 아니에요. B2B 이메일 클릭에는 스캐너 봇이 있어요. 네이버 검색광고·플레이스 전환 지연은 그 도움말에 적힌 시간을 확인하고, 모르면 최근 2~3일은 판정에서 빼요. AI 유입 (chatgpt.com, perplexity.ai 등)은 자기 채널로 분리해요. 전환이 다르고, 뜻이 달라요. 인용되고 있다는 뜻이에요. 영어권 AI Overview CTR은 네이버 사실이 아니에요.

### 2d. 병목 하나

기간의 실제 카운트로 퍼널을 걸어요. **세션 → 리드 → 판매** (또는 브랜드의 같은 단계). 각 단계 전환을 계산하고, 레퍼런스의 도달 가능 구간과 비교하고, 도달 가능 대비 가장 새는 단계를 이름 지어요. 가장 작은 숫자가 아니라 가장 나쁜 비율.

- 세션에서 새면 **트래픽 문제**. 키워드, SEO, 광고, 배포 스킬.
- 세션에서 리드로 새면 **전환 문제**. 랜딩, 리드 마그넷, 제안 페이지 카피.
- 리드는 괜찮은데 리드에서 판매가 깨지면 **제안 문제**. 포지셔닝, 가격, 시퀀스·영업 경로.
- **전화 사업:** 리드에서 판매 샘을 제안 문제라고 부르기 전에, 통화 기록에서 놓친 전화와 회신 시간을 읽어요. 벨만 울리거나 몇 시간 뒤 회신하는 전화는 모든 보고서에서 약한 리드처럼 보여요. `/speed-to-lead`.

### 2e. 공을 주기 전에 증분

채널이 보고한 전환은 귀속 주장이에요. 진단이 어느 채널에 리드나 판매의 공을 주기 전에 셋.

1. **분모 대비 그럴듯함.** 유료 검색이 한 달에 통화 60을 주장하는데 전화 대장이 모든 출처 합쳐 받은 통화 70이면, 주장은 사업 거의 전체예요. 다른 채널이 무엇을 했는지 물어요. 숫자는 읽는 법의 예시예요.
2. **어떤 종류의 전환인가.** 플레이스·구글 비즈니스 프로필의 전화, 길찾기, 브랜드 검색, 리타게팅, 조회 후 전환은 어차피 오던 사람을 세는 경우가 많아요. 의도가 있는 검색, 깨끗한 추적, 새 오디언스는 그중 더 적게 세요.
3. **데이터 안의 자연 실험.** 캠페인 중단, 예산 삭감, 카드 실패, 정책 정지. 그 전과 도중에 분모를 읽어요.

한 지역 사업 계정에서 구글은 Performance Max에 계정 전환 대부분을 돌렸지만, 중단은 전화 대장 측정 넷을 움직이지 않았어요. 그 사업의 정확한 숫자는 여기 없어요. 온라인 예시: 브랜드 검색과 리타게팅이 매출의 상당 부분을 주장해도, 브랜드 중단 2주 동안 신규 주문이 평평하면 공이 아니에요.

지출이 의미 있고 자연 실험이 없으면, 첫 추천은 측정이에요. 예산 변경 전에 `/ads-incrementality-check`. 채널이 learnings에 "통한다"로 들어가려면, 카운트가 분모 대비 그럴듯하고, 깨끗한 추적으로 새 의도를 잡거나 중단·리프트 테스트가 보여 줘야 해요.

퍼널당 병목 하나. 진단의 헤드라인. 문제 다섯을 동등하게 순위 매기면 아무것도 바꾸지 않는 리뷰예요. 고치면 하류 전체에 곱해지는 단계를 고르는 것이 규율이에요. 다른 관찰은 2차 발견으로, 명시적으로 아래 둬요.

---

## 3단계: 학습

데이터가 증명한 것을 `./brand/learnings.md`에 써요 (append-only. 먼저 읽고, 맞는 섹션 맨 아래. `## What Works`, `## What Doesn't Work`, `## Audience Insights`). 형식은 `${CLAUDE_SKILL_DIR}/../start-here/references/brand-memory.md`.

```markdown
- [YYYY-MM-DD] [email-sequences] subject-pattern=question outperformed curiosity 2.3x (n=4 sends, source: kit-api)
- [YYYY-MM-DD] [paid-ads] hook=contrarian beat proof ~2.1x on CPA, video only (n=214 clicks, source: meta-csv spring-launch)
- [YYYY-MM-DD] [seo-content] comparison-format pages earn AI referrals; how-to pages don't (n=6 pages, source: ga4-api)
```

배율은 형식 예시예요. 실제 항목은 이번 데이터의 숫자만.

**문장 규칙:** 프라이어는 생성 스킬이 그대로 적용할 지시예요. "이 리스트에서는 질문형 제목이 호기심형 제목을 이긴다"는 제목을 쓰는 생성 스킬에게 무엇을 할지 말해요. "이번 달 이메일 참여가 좋았다"는 프라이어가 아니에요. 보고서에서 죽어요.

**항목을 쓰는 기준** (아래면 발견은 보고서의 관찰로 남아요).

- 더 드문 지표에서 팔당 사건 약 20 이상에 효과 약 2배 이상, 또는
- 독립 인스턴스 (발송, 게시, 주) 3회 이상 같은 방향, 또는
- 반박된 예측. 방향만이어도 항상 기록하고 `(directional)`을 표시.

모델 지식이나 애매한 발송 한 번으로 프라이어를 쓰지 마세요. 플랫폼 전환만으로 "채널 X가 통한다"를 쓰지 마세요 (2e). 빈 리뷰는 항목 0개를 쓰고 한 줄로 말해요.

다른 스킬이 맞춘 캠페인 `notes.md`의 "Draft learnings" 아래에 남긴 초안은 후보예요. 이 기준을 넘을 때만 `learnings.md`에 들어가요. 항목 자체는 `learnings.md`에 있고, 보고서는 붙여 넣지 않아요. 저장한 파일이 개수를 보여요.

**압축.** 이 스킬이 돌려요. learnings.md가 약 50항목을 넘으면, 반복 확인된 durable 발견을 맨 위 `## PRIORS`로 승격 (한 줄, 확인 날짜). 거의 중복은 가장 강한 항목으로 병합 (n이 크고 최근). 낡거나 대체된 항목은 `./brand/.history/learnings.<YYYY-MM-DD>.md`로 옮겨요. 지우지 마세요. `learnings.md`의 저장한 파일 줄에 압축을 적어요.

**승자는 골드 케이스가 돼요.** 한 에셋이 같은 기준으로 형제들을 분명히 이기면 (제목, 광고, 페이지 변형) `${CLAUDE_SKILL_DIR}/../start-here/references/taste-loop.md`대로 `./brand/gold/<만든 스킬>/<YYYY-MM-DD>-<slug>.md`에 골드 케이스를 저장해요. "나간 것"은 승자, "이유"는 결과와 n. 인용 대신. 그 스킬의 다음 실행이 기준으로 읽어요. 패턴 자체는 위처럼 `learnings.md`로. `checks.md`로 가지 않아요. 점검은 사용자 수정에서, 프라이어는 데이터에서.

**검토한 산출물의 장부** (캠페인 파일, 브랜드 메모리 아님): 각 광고 셀의 숫자를 `ad-matrix.json`의 `results` 블록에 써요 (지출, 노출, 클릭, 전환, 노트. 스키마 `${CLAUDE_SKILL_DIR}/../start-here/references/schemas/ad-matrix.schema.json`). 데이터가 증명하는 `assets.md` 상태를 뒤집어요 (트래픽이 있으면 `draft`에서 `live`, 죽인 것은 `live`에서 `retired`).

---

## 4단계: 추천

다음 행동 3~5개. **기대 효과 = 샘의 크기 × 데이터 확신 × 고침의 값쌈**. 확신하는 중간 승이, 클릭 30개에서 읽은 큰 승을 이겨요. 각 행동은 증거와 구체적인 스킬 호출을 이름 지어요. 사용자가 생각 없이 실행할 수 있으면 추천은 끝난 거예요.

- "노출이 있는 순위 8~15 쿼리 12개가 페이지 3장에 매핑됨. 그 3장을 `/seo-content`로 새로 고침 (타격 거리. SEO에서 가장 싼 클릭)."
- "증거 훅 영상이 다른 광고보다 CPA에서 약 2.1배. `/paid-ads` 2라운드에서 그 훅을 새 소재로 늘리기 전에 피로를 확인."
- "리드 마그넷 페이지가 사이트 전체 대비 낮음. 트래픽 문제가 아니라 마그넷과 제안의 불일치. 드러난 VoC 반대와 함께 `/lead-magnet`."
- "AI 유입은 세션 비중은 작은데 전환은 자연 검색보다 나음. `/ai-search`로 어떤 질문이 인용하는지 찾고 발자국을 넓히기. 영어 Overview 통계로 네이버를 설명하지 않기."
- "Performance Max가 전환 대부분을 받았지만, 지난달 예산을 줄였을 때 하루 받은 전화는 안 움직였어요. 갱신 전에 `/ads-incrementality-check`로 4주 중단을 계획."

(위 비율과 카운트는 예시예요.)

1번 추천은 2d 병목을 다뤄야 해요. 나머지는 같은 데이터의 기회예요. 데이터가 아직 받치지 못하는 것은 측정 추천이 돼요 ("변형 B는 판정할 만큼 발송되지 않았으니, 무엇을 바꾸기 전에 테스트를 다시").

---

## 모드: MONTHLY (루틴 안전, 비대화)

배포된 월간 리뷰 루틴이 호출해요. **질문은 절대 0.** 모든 결정에 기본값이 있어요.

1. **수집:** 키가 있는 모든 소스 (1c), 직전 달력 월과 그 앞달. 키가 전혀 없고 내보내기도 없으면 `./campaigns/performance/<YYYY-MM>.md`에 다음에 설정할 키나 붙여 넣을 내보내기를 정확히 적은 짧은 보고서를 쓰고 멈춰요. 부분 커버리지는 괜찮아요. 말해요. 네이버 내보내기가 있으면 그것이 소스예요.
2. **진단:** 1d~2e 그대로. 추가로 `./campaigns/performance/`에 지난달 보고서가 있으면 diff. 지표 변화, 지난달 추천, `assets.md`가 실행됐음을 보여 주는지 (실행 대 무시 자체가 보고. 잔소리는 없음).
3. **학습:** 3단계 그대로. 기준을 넘는 항목만. 압축 점검 포함.
4. **쓰기** `./campaigns/performance/<YYYY-MM>.md`:

```markdown
## PERFORMANCE REVIEW: <Month YYYY>
<날짜> · 월간 읽기, <전월> 대비

### 병목
<한 단락: 단계, 산수, 분류>

### 추천 행동
<순위. 각각 증거와 /skill 호출>

### 채널 노트
<데이터가 있는 채널마다, 중요한 지표 2~3개, 지난달 대비 방향. 네이버와 구글은 따로>

### 예측 대 실제
<반박이 먼저, 그다음 확인, 한 줄씩. 검증 불가는 한 줄>

### 출처와 가정
<최대 10줄. 무엇을 가져왔고 키·내보내기 부족으로 무엇을 건너뛰었는지 평범한 말.
데이터 품질, 확인할 것, 읽기를 바꾼 학습이 있으면 그것만>
```

5. 보고서에 `assets.md` 행 하나. 얇은 달은 짧은 보고서. 불리지 마세요.

---

## 출력

REVIEW 모드는 네 섹션 계약 (`${CLAUDE_SKILL_DIR}/../start-here/references/output-format.md`). 헤더 (`## PERFORMANCE REVIEW: <범위>`와 날짜·용도 한 줄). 내용 (병목 먼저, 추천 행동, 채널 노트, 예측 대 실제, 모든 소스를 평범한 말로 이름 짓는 출처와 가정 노트. 예: "서치어드바이저 내보내기, 메타 내보내기, 스크린샷 하나. 스크린샷이 가장 낮은 충실도"). **저장한 파일**. **다음**. 파일 길이 약 1,200에서 2,500단어, 얇은 달은 더 짧게. 채팅은 병목, 행동, 노트. 전체 표는 파일. 정규 행, 스크립트 경로, 수집 명령은 어느 쪽에도 없어요.

| 모드 | 쓰는 것 |
|---|---|
| REVIEW | `./campaigns/performance/<YYYY-MM-DD>-review.md`, `learnings.md` (덧붙임), 맞춘 곳의 `ad-matrix.json` results와 `assets.md` 상태 |
| MONTHLY | `./campaigns/performance/<YYYY-MM>.md`, `learnings.md` (덧붙임), 같은 장부, `assets.md` 보고서 행 |

## 사용자가 결과물을 고치면

수정을 적용하고 남기세요. `./brand/gold/<이 스킬>/`에 골드 케이스, `./brand/checks.md`에 예/아니오 점검 1~3개, 한 줄 확인. 넘기기 전에 불러온 점검에 조용히 답하고 아니오를 고치세요. 방법: `${CLAUDE_SKILL_DIR}/../start-here/references/taste-loop.md`.

## 다음

여기 라우팅은 동적이에요. 4단계 추천이 라우팅이에요. 아무것도 지배하지 않을 때의 기본 (`automations/routines/monthly-performance-review.md`의 월간 리뷰 루틴을 더하면 MONTHLY가 사용자 없이 돌아요. 약 5분).

- 1번 추천의 스킬을 실행. 증거를 같이 가져가요 (약 15~30분)
- `/positioning-angles`: 진단이 제안 문제면, 고침은 카피가 아니라 각도 (약 15분)
- `/ads-incrementality-check`: 한 채널이 결과 대부분을 주장하고 자연 실험이 없으면, 전화 대장이나 주문 시스템 대비 중단 테스트 (계획 약 20분)
- `/competitive-intel` 감시: 내부 원인 없이 성과가 떨어지면 판이 움직였는지 (약 10분)

판매 클로징 문장은 붙이지 마세요. 채팅에도, 저장된 보고서에도, MONTHLY에도. 이 팩은 유료 제안으로 보내지 않아요.

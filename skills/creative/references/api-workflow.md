# API 작업 흐름. 크리에이티브 엔진

```
last-verified: 2026-11-18 · ttl-days: 180 · refresh: replicate.com/docs 에서 HTTP API 변경을 확인합니다
changes: 2026-11-18. 설명을 한국어로 바꿈. 호출 방법과 한도는 2026-09-02 확인분을 유지. 상태 목록에 canceled/aborted. 공개 한도 생성 분당 600, 그 외 분당 3,000, 문서화된 동시성 상한 없음(파도 크기는 운영 관행). API 보존 1시간, 만료된 output은 null. Prefer wait 동기 단축. 404는 공급자 종료일 수 있음(Sora 2 API는 2026-09-24 종료).
```

Replicate 호출, 파일 관례, 캠페인 매니페스트, 비전 QA 방법, 핸드오프 계약의 한 벌. 모든 모드가 여기를 가리킵니다. 모델 ID와 페이로드는 `references/MODEL_REGISTRY.md`에만 있습니다.

세션의 첫 생성 전에 엽니다. 실패하기 전에는 다시 필요 없습니다.

---

## 1. 비동기 호출

Replicate 생성은 모두 비동기입니다. 예측을 만들고, 폴링하고, 내려받습니다.

### 만들기

```bash
curl -s -X POST "https://api.replicate.com/v1/models/{owner}/{model}/predictions" \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"input": { ...MODEL_REGISTRY.md 의 페이로드... }}'
```

모델 경로는 **URL**에 있습니다. 본문에는 `{"input": {...}}`만. `model`, `model_owner`, `version` 키를 넣지 않습니다. 응답(HTTP 201)에 `"id"`와 `"urls": {"get": ...}`가 있습니다.

### 폴링

```bash
curl -s "https://api.replicate.com/v1/predictions/{id}" \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN"
```

이미지는 5초, 영상은 10초마다. `status`는 `starting`에서 `processing`, 그다음 `succeeded` 또는 `failed` 또는 `canceled`(시작된 뒤 중단) 또는 `aborted`(시작 전 중단). `succeeded`면 `output`(URL 또는 URL 배열)을 읽습니다. `failed`면 `error`. `canceled`와 `aborted`는 `failed`처럼. 받을 파일 없음.

**이미지 동기 단축.** 생성 호출에 `Prefer: wait`(또는 `Prefer: wait=N`, N은 최대 60초)를 넣으면 Replicate가 요청을 붙잡습니다. 시간 안에 끝나면 응답에 이미 `output`이 있습니다. 아니면 `starting` 또는 `processing`인 예측이 오고 위처럼 폴링합니다. 이미지 한 장(15~40초)에는 가치가 있습니다. 영상에는 없습니다.

벽시계 감. 이미지 15~40초, 초안 영상 약 20~40초, 프로덕션 영상 1~3분, 프리미엄 영상 3~10분. 독립 생성은 병렬로. 묶음은 합이 아니라 가장 느린 구성원만큼 걸립니다.

### 다운로드. 1시간 안, 예외 없음

API로 만든 예측은 완료 **한 시간** 뒤에 입력, 출력 파일, 로그를 지웁니다. 웹 UI에서 만든 예측은 무기한 보관됩니다. API가 엄격한 경우입니다. 그 뒤 파일 URL은 404이고 예측의 `output`은 `null`입니다. 성공 즉시 캠페인 경로로 받습니다. 사용자에게 보여 주기 전에. 내려받지 않은 "좋은 결과"는 다시 만들 비용입니다.

```bash
curl -s -o "{local_path}" "{output_url}"
```

### 오류

| HTTP / 상태 | 뜻 | 행동 |
|--------------|---------|--------|
| 401 | 토큰 없음 또는 틀림 | `REPLICATE_API_TOKEN` 확인. 프롬프트 전용 모드를 제안 |
| 404 | 모델 ID 틀림, 이름 변경, 공급자 종료 (Sora 2와 Sora 2 Pro는 2026-09-24 종료. 목록에서 내린 모델도 API 메타데이터는 200일 수 있음) | `scripts/verify_models.sh`. MODEL_REGISTRY.md의 명단과 역할 지도를 고칩니다 |
| 422 | 매개변수 틀림 | MODEL_REGISTRY.md의 가족별 이름 표. 가족마다 이름이 다릅니다 |
| 429 | 속도 제한 | 60초 대기. 파도를 줄입니다 |
| `failed`, 흐린 오류 | 콘텐츠 필터 또는 일시 오류 | 걸린 표현을 바꾸고 한 번 재시도. 그다음 replicate.com/predictions 로그 |
| `succeeded`인데 `output: null` | 조용한 실패, 또는 완료 1시간 뒤에 다시 읽음 | 한 시간 안이면 실패로 보고 한 번 재시도. 이후면 만료. 다시 생성 |

### 속도 제한과 묶음

Replicate 공개 한도는 예측 생성 **분당 600**, 다른 엔드포인트 **분당 3,000**. 넘으면 `429`. 계정당 동시성 상한은 문서에 없습니다. 파도 크기는 플랫폼 규칙이 아니라 운영 관행입니다. **5~8개 파도**로 묶고 다음 파도 전에 기다립니다. 중간 실패를 싸게 재개하고, 공급자 용량 오류(`failed`로 나오고 `429`가 아님)를 가둡니다. 소재 20개 이상이면 먼저 매니페스트(4절)를 써서 중간 실패가 재개되게 합니다.

---

## 2. 비전 QA 방법

(QA *정책*은 SKILL.md다. 전부 채점하고, 7 미만은 최대 두 번 다시 만들고, 최선과 비판을 보여 줍니다. 여기는 방법입니다.)

**이미지.** 받은 뒤 로컬 파일을 `Read`합니다. 루브릭. creative-kit.md 제약, VISUAL_INTELLIGENCE.md 4부의 슬롭 방지, 요청 스펙(매체 비율, 글 공간, 초점).

**영상.** 프레임 셋. 첫 프레임(썸네일·후크), 중간, 끝 무렵.

```bash
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 clip.mp4)
MID=$(awk -v d="$DUR" 'BEGIN{printf "%.2f", d/2}')
ffmpeg -y -i clip.mp4 -frames:v 1 f1.png 2>/dev/null
ffmpeg -y -ss "$MID" -i clip.mp4 -frames:v 1 f2.png 2>/dev/null
ffmpeg -y -sseof -0.2 -i clip.mp4 -frames:v 1 f3.png 2>/dev/null
```

(`-ss`를 `-i` 앞에 두면 중간으로 이동. `-sseof -0.2`는 끝 0.2초 전.) 각 프레임을 `Read`. ffmpeg가 없으면 예측의 썸네일 URL이 있을 때 그것을 `Read`하고 노트에 한 줄. "썸네일만 봤습니다. 프레임 전체는 ffmpeg가 필요합니다."

**채점.** 정수 1~10과, 실패한 차원마다 이유 한 줄. 매니페스트에만. 점수는 정직하다. 의식용이 아니고 클라이언트에게 안 보여 줍니다. 결함 이름이 있는 6이 안 본 8보다 낫다.

**여러 모델.** 후보마다 QA한 뒤 **미리 순위**를 매겨 이유를 말합니다. 점수와 모델 이름은 없습니다. "A. 제품은 가장 정확한데 조명이 평평합니다. B. 움직임이 가장 좋고 3초에 라벨이 약간 휨. 이쪽을 권합니다." URL 셋을 던지고 "어떤 것인가요"라고 묻지 않습니다.

---

## 3. 파일 관례

파일이 먼저입니다. 채팅에 요약하기 전에 모든 소재를 받아 저장하고, `./brand/assets.md`에 한 줄을 붙입니다.

### 디렉터리

```
creative-output/
├── explorations/<project>/          direction-1.png … direction-5.png
├── product-photos/<product>/        hero/ detail/ lifestyle/ ecommerce/ flat-lay/ edits/
├── videos/<product>/                drafts/ production/ premium/ sequence/ approved/
├── social-graphics/<campaign>/      instagram/ blog/ shorts/ threads/ youtube/
├── talking-heads/<campaign>/        presenter-pack/ generation/ audio/ lip-sync/ approved/
├── ad-creative/<campaign>/          매트릭스 셀 ID로 이름 (ad-creative 모드)
└── exports/<campaign>/              최종과 manifest.yaml
```

캠페인 디렉터리가 있으면 `./campaigns/<name>/creative/`에 두어도 됩니다. 캠페인을 따릅니다. 트리를 둘로 만들지 않습니다.

### 이름

```
[type]-[descriptor]-[ratio]-v[N].[ext]          일반
hero-walnut-desk-16x9-v2.png
reveal-orbit-kling-9x16-v1.mp4                  영상. 모델 짧은 이름
MA-H2-B-9x16-v1.mp4                             광고. 항상 매트릭스 셀 ID
```

반복은 `vN`을 올립니다. 이전 버전을 덮어쓰지 않습니다. 예시 브랜드가 필요하면 한빛설비 또는 북산일정. 고객 실명 파일을 저장소에 넣지 않습니다.

### 기록

소재마다 `./brand/assets.md`에 한 줄.

`- [2026-11-18] [creative] creative-output/videos/hanbit/production/reveal-orbit-kling-16x9-v2.mp4: 프로덕션 공개, kling, 약 $1.12`

달러는 레지스트리 가격입니다. 원화로 바꾸어 단정하지 않습니다.

---

## 4. 캠페인 매니페스트 (실패 후 재개)

소재 3개 이상이면 생성 전에 매니페스트를 쓰고 소재마다 갱신합니다. 실패한 묶음을 처음부터가 아니라 재개하게 합니다.

`creative-output/exports/<campaign>/manifest.yaml`

```yaml
campaign: spring-launch
created: 2026-11-18
brand_kit: ./brand/creative-kit.md
style_lock: ./creative-output/explorations/spring-launch/style-lock.md   # 잠갔으면
assets:
  - id: hero-still
    file: product-photos/hanbit/hero/hero-floating-16x9-v1.png
    role: image-default            # 역할. MODEL_REGISTRY.md 에서 푼다
    model: google/nano-banana-2    # 실제로 돈 것
    prompt: "…프롬프트 전문…"
    seed: 41782                    # 모델이 시드를 지원하면
    ratio: "16:9"
    cost: 0.067
    qa_score: 8
    status: done                   # pending | generating | done | failed
  - id: MA-H2-B-9x16
    file: ad-creative/spring-launch/MA-H2-B-9x16-v1.mp4
    role: video-production
    status: pending
totals:
  spent: 0.07
  budget: 10.00
```

**재개.** 다시 들어오면 매니페스트를 읽고 `done`은 건너뛰고 `failed`는 한 번 재시도하고 `pending`을 생성합니다. 매니페스트의 프롬프트와 시드가 다시 만든 소재를 형제와 맞게 합니다.

---

## 5. 핸드오프

### 브리프를 받을 때 (/positioning-angles, /direct-response-copy, /paid-ads …)

```yaml
creative_brief:
  subject: 만들 것
  audience: 누구를 위한지
  message: 핵심 한 줄
  platform: 어디에 나가는지
  style_notes: 시각 방향, 있으면
  ad_matrix: ./campaigns/<name>/ad-matrix.json   # 광고면 ad-creative 모드
```

### 넘길 때 (/content-atomizer, /paid-ads, /email-sequences …)

```yaml
creative_delivery:
  campaign: spring-launch
  manifest: creative-output/exports/spring-launch/manifest.yaml
  assets:
    - path: creative-output/videos/hanbit/approved/reveal-final-16x9.mp4
      type: video
      duration: 5s
      ratio: "16:9"
      qa_score: 8
  brand_kit: ./brand/creative-kit.md
  style_locked: true
```

매니페스트가 정본입니다. 전달 블록은 포인터와 승인된 부분집합입니다. 부른 스킬에게 갑니다. 클라이언트가 보는 글에 넣지 않습니다.

---

## 6. 토큰 없을 때 (프롬프트 전용)

`REPLICATE_API_TOKEN`이 없으면 멈추지 않습니다. 한 번 말하고, 같은 흐름(브랜드 키트, 모드 판단, 프롬프트)을 돌린 뒤 소재마다 복사할 블록을 줍니다. 클라이언트가 돌릴 추천이므로 여기서 모델 이름을 적어도 됩니다. 정확한 프롬프트, 역할과 그 역할의 현재 모델(MODEL_REGISTRY.md), 비율·길이·설정, 참조 이미지 지시. 프롬프트를 캠페인 디렉터리에 저장해 나중에 토큰이 생기면 그대로 실행되게 합니다. 프로덕트는 프롬프트와 방향입니다. API 호출은 마지막 단계입니다.

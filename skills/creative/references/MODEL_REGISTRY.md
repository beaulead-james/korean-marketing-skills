# 모델 레지스트리

```
registry_version: 3.4.0
last-verified: 2026-11-13
ttl-days: 60
refresh: scripts/verify_models.sh를 실행합니다. Replicate API로 모든 모델 ID를 다시 확인하고 ./brand/creative-stack.md를 다시 씁니다. 종료가 가까운 모델은 replicate.com/{owner}/{model}을 엽니다. 목록에서 빠진 모델도 API 검사를 통과할 수 있습니다.
changes: 2026-11-16 GPT Image 역할은 GPT Image 2.6으로 옮겼습니다. `openai/gpt-image-2.6-flare`는 빠른 초안, `openai/gpt-image-2.6-sunburst`는 최종과 일관된 수정. 두 ID 모두 200이었고, 입력 스키마는 API에서, 가격은 모델 페이지에서 2026-11-16에 읽었습니다. 이전 GPT Image ID는 명단에서 빠졌습니다. 2.6은 투명 배경을 다시 지원하고 움직이는 GIF와 SVG 출력을 더합니다. 2026-11-13 verify_models.sh는 Sora 2와 Sora 2 Pro를 뺀 뒤 25 pass / 0 fail이었습니다. 페이지는 2026-09-24 API 종료 이후 404인데 GET /v1/models는 200일 수 있어, 스크립트 통과만으로 판매 중이라고 보지 않습니다. 스키마와 가격을 다시 읽었습니다. Seedance 2.0은 비디오 입력이 없으면 더 쌉니다. video-ugc와 히어로 트리오는 종료 이후 경로로 연결됩니다. 새 ID 목록을 갱신했습니다. 2026-11-18 본문은 한국어로 옮겼고 모델 ID, 가격, 스키마, registry_version은 바꾸지 않았습니다.
```

**페이로드, 파라미터, 가격이 있는 제품 안의 유일한 파일입니다.** SKILL.md와 모든 모드는 역할로 라우팅합니다 ("초안 단계", "제작 영상 모델", "글자 렌더 이미지 모델"). 호출 때 역할을 여기서 풉니다. 허락된 예외 하나. `references/model-routing.md`는 라우팅 표에서 역할 옆에 모델 이름을 적습니다. 판단에 이름이 필요합니다. 그 밖에 페이로드와 가격이 나타나면 버그입니다. 그 파일을 이 레지스트리로 되돌립니다.

오늘이 last-verified + ttl-days를 넘으면, 돈을 쓰기 전에 refresh를 실행하고, 깨끗이 통과한 뒤 `last-verified`를 고칩니다. 세션 중에 호출이 404나 422면 `replicate.com/{owner}/{model}/api`에서 현재 스키마를 보고, 이 파일을 고친 뒤 재시도합니다.

**모델별 검증 상태 (`Status` 열).**

- `schema-verified`. ID가 200을 반환했고, 입력 스키마를 2026-11-13에 Replicate API에서 읽었습니다. 여기 적은 파라미터 표면이 그 스키마와 맞습니다. Replicate README는 군데군데 스키마보다 늦습니다. 모델 절에 적었습니다. 호출을 검증하는 것은 스키마입니다.
- `sunset`. 제공처가 종료일을 발표했습니다. 새 작업을 시작하지 않습니다. 역할 맵이 종료 이후 경로를 말합니다. 2026-11-13 명단에는 없습니다.

호출 방법(비동기 생성, 폴링, 1시간 안 다운로드, 오류, 파일 이름, 캠페인 매니페스트)은 `references/api-workflow.md`. 아래 페이로드 블록은 요청 **본문**만 보여 줍니다. 모델 ID는 URL에 있습니다.

가격은 Replicate 페이지의 달러입니다. 원화로 환산하지 않습니다.

---

## 기계가 읽는 명단

`scripts/verify_models.sh`가 이 블록을 파싱합니다. 한 줄에 모델 ID 하나. 아래 절과 동기화합니다. 모델을 더하면 여기와 그 절에 모두 넣습니다.

```models
google/nano-banana-2
google/nano-banana-pro
openai/gpt-image-2.6-flare
openai/gpt-image-2.6-sunburst
black-forest-labs/flux-2-max
black-forest-labs/flux-2-pro
black-forest-labs/flux-2-flex
bytedance/seedream-4.5
recraft-ai/recraft-v4
recraft-ai/recraft-v4-svg
ideogram-ai/ideogram-v3-turbo
wan-video/wan-2.5-i2v-fast
wan-video/wan-2.5-t2v-fast
wan-video/wan-2.7-i2v
kwaivgi/kling-v3-video
kwaivgi/kling-v3-omni-video
bytedance/seedance-2.0
bytedance/seedance-1-pro
runwayml/gen-4.5
google/veo-3.1
google/veo-3.1-fast
sync/lipsync-2-pro
pixverse/lipsync
bytedance/omni-human
kwaivgi/kling-lip-sync
```

`openai/sora-2`와 `openai/sora-2-pro`는 2026-11-13에 명단에서 빠졌습니다. OpenAI가 Sora 2 API를 2026-09-24에 종료했고, 두 replicate.com 페이지는 404입니다.

---

## 역할 맵

모드가 역할을 요청하면 이 표가 모델로 답합니다. 여기서 모델을 바꾸면 모든 모드가 따라갑니다.

### 이미지

| 역할 | 모델 | 상태 | 장당 비용 | 언제 |
|------|-------|--------|------------|----------|
| **image-default** | `google/nano-banana-2` | schema-verified | $0.067 (1K) · $0.101 (2K) · $0.151 (4K) | 전부. 아래 역할이 더 맞을 때만 벗어납니다. 참조 14장까지 합성 수정. 이제 스스로 4K를 냅니다. |
| **image-premium-4k** | `google/nano-banana-pro` | schema-verified | $0.15 (1K/2K) · $0.30 (4K) · 폴백 모델이 돌면 $0.035 | 히어로 스틸, 인쇄. NB2 자체 4K 위의 충실도 업그레이드이지, 유일한 4K 경로가 아닙니다. |
| **image-complex-prompt** | `openai/gpt-image-2.6-sunburst` (초안 `gpt-image-2.6-flare`) | schema-verified 2026-11-16 | $0.05 low · $0.09 medium · $0.128 high · $0.25 xhigh · $0.50 max, 둘 다 같음 (`quality`를 명시. `auto`가 기본이고 $0.25). GIF와 SVG는 토큰 과금 | 요소가 많은 구도, 지시가 빽빽한 프롬프트, 실제 장면 안의 정확한 글자, 휴대폰처럼 보이는 사진, 움직이는 GIF. Flare는 빠른 초안, Sunburst는 최종. |
| **image-instruct-edit** | `openai/gpt-image-2.6-sunburst` (초안 `gpt-image-2.6-flare`) | schema-verified 2026-11-16 | 위와 같음 | 실제 사진의 지시 수정과 레이아웃 합성, 한 제품을 여러 수정에서 같게 유지(이전 출력을 다시 넣고 한 번에 하나만). 실제 사진은 `input_images`. |
| **image-art-direction** | `black-forest-labs/flux-2-max` (프리미엄) / `flux-2-pro` (표준이자 가장 쌈) / `flux-2-flex` (조절 손잡이. 예산 선택이 아님) | schema-verified | 메가픽셀당. pro 약 $0.03 at 1 MP, 약 $0.08 at 4 MP · max 약 $0.07 / 약 $0.16 · flex 약 $0.06 / 약 $0.24 (참조 이미지도 입력 MP당) | 포토리얼 아트 디렉션, 프롬프트 준수, 스타일 폭, 다중 참조 수정. |
| **image-stylized** | `bytedance/seedream-4.5` | schema-verified | $0.04 | 미감이 높은 양식화, 편집 일러스트 결. 한 호출에 최대 15장 세트. |
| **image-vector** | `recraft-ai/recraft-v4` / `recraft-v4-svg` | schema-verified | $0.04 (래스터) · $0.08 (SVG) | 로고, 아이콘, 플랫 디자인. `-svg`는 실제 벡터 파일. |
| **image-text-render** | `ideogram-ai/ideogram-v3-turbo` | schema-verified | $0.03 | 모든 글자가 맞아야 하는, 타이포가 주인공인 그래픽. |

### 영상

단계 파이프라인의 흐름은 SKILL.md.

| 역할 | 모델 | 상태 | 비용 | 언제 |
|------|-------|--------|------|----------|
| **video-draft** | `wan-video/wan-2.5-i2v-fast` / `wan-2.5-t2v-fast` (720p가 바닥. 480p는 없음) | schema-verified | 720p $0.068/s · 1080p $0.102/s. 5초 초안 약 $0.35 | 기본 1차. 움직임 방향을 찾는 싼 초안 3~5개. 초안을 내보내지 않습니다. 명단에서 검증된 가장 싼 초당은 480p `seedance-1-pro`($0.03/s, 5초에 $0.15)입니다. 유효한 초안 대안. `wan-2.7-i2v`는 초안 모델이 아닙니다. 그 절을 보세요. |
| **video-ugc** | `bytedance/seedance-2.0` (대안 `google/veo-3.1`) | schema-verified | 비디오 입력 없는 Seedance 2.0, 720p $0.18/s (8초 $1.44) · Veo 3.1 오디오 포함 $0.40/s | UGC, 광고 네이티브. 피드에서 전환되는 손떨림·불완전. 둘 다 네이티브 오디오(기본 켜짐). Sora 2 API 종료(2026-09-24) 때 이 역할을 받았습니다. 아직 시험하지 않은 선행입니다. 첫 UGC 브리프에서 Seedance와 Veo를 겨루고 승자를 model-routing.md에 적습니다. |
| **video-production** | `kwaivgi/kling-v3-video` | schema-verified | `mode=pro`(기본) $0.224/s, 오디오 $0.336/s · `standard` $0.168 / $0.252 · `4k` 어느 쪽이든 $0.42. 5초 pro 약 $1.12 | 기본 최종. 3~15초, 네이티브 오디오, 멀티샷. 오디오는 약 +50%이지 2배가 아닙니다. |
| **video-reference** | `kwaivgi/kling-v3-omni-video` 또는 `bytedance/seedance-2.0` | schema-verified | Omni. pro $0.224/s (오디오 $0.28), standard $0.168 ($0.224), 4k $0.42 · Seedance 2.0 비디오 입력 있을 때 $0.10/s 480p · $0.22/s 720p · $0.55/s 1080p · $1.25/s 4k (없을 때 $0.08 · $0.18 · $0.45 · $1.00) | 참조 작업. 인물 일관성, 참조로 수정. Omni는 Kling 생태계(이미지·영상 참조, 편집, 인물 잠금). Seedance 2.0은 가장 강한 원참조 파이프라인(이미지 9, 영상 3, 오디오 3)이고 오디오가 기본 켜짐. |
| **video-locked-camera** | `bytedance/seedance-1-pro`, `camera_fixed: true` | schema-verified | $0.03/s 480p · $0.06/s 720p · $0.15/s 1080p | 카메라가 고정돼야 하는 깨끗한 제품 샷. 명단에서 가장 싼 초안 경로이기도 합니다. |
| **video-premium** | `runwayml/gen-4.5` + `google/veo-3.1` + `bytedance/seedance-2.0` 1080p, 병렬 | schema-verified | Runway $0.12/s · Veo 3.1 오디오 $0.40/s, 없이 $0.20/s (8초 $3.20 / $1.60) · 비디오 입력 없는 Seedance 2.0 1080p $0.45/s. 세 모델 8초 약 $7.70 | 명시적 "히어로"만. 셋을 돌리고 순위를 매기고 사용자가 고릅니다. `veo-3.1-fast`(오디오 $0.15/s, 없이 $0.10)는 트리오 안의 속도 교체입니다. |
| *더 새 것, 쓰기 전 확인* | `bytedance/seedance-2.5` | 미검증 | 아직 안 읽음 | 제공처에 있으면 Seedance 영상의 우리 선택. Replicate에 올라 있습니다(API 메타데이터 2026-11-13. 네이티브 오디오의 30초 클립). 아직 어떤 역할도 여기로 풀리지 않습니다. 위의 Seedance 역할은 2.0에 남습니다. 역할을 맡기 전에 replicate.com/bytedance/seedance-2.5에서 스키마와 가격을 읽고, 싼 시험 하나를 돌리고, 레지스트리 방식(명단 줄, 절, 검증)으로 추가합니다. |

### 립싱크

| 역할 | 모델 | 상태 | 비용 | 언제 |
|------|-------|--------|------|----------|
| **lipsync-default** | `sync/lipsync-2-pro` | schema-verified | $0.08325/s, 약 $5/분 (30초 약 $2.50) | 스튜디오 기본. 싱크 품질이 가장 좋고, 고개 움직임을 다루며, `active_speaker`로 여러 화자. |
| **lipsync-budget** | `pixverse/lipsync` | schema-verified | $0.04/s (10초 $0.40) | 싼 초안과 대본 반복. 오디오와 영상만. 텍스트·TTS 입력 없음. |
| **lipsync-kling** | `kwaivgi/kling-lip-sync` | schema-verified | $0.014/s (10초 $0.14). 명단에서 가장 싼 싱크 | Kling이 만든 소스(`video_id`), 또는 내장 TTS 퀵 테스트. |
| **digital-human** | `bytedance/omni-human` | schema-verified | $0.14/s (10초 $1.40) | 스틸 한 장과 오디오로 만드는 전신 디지털 휴먼(입이 아니라 몸). |

가격은 2026-11-13에 각 모델의 replicate.com 페이지에서, 거기에 표시된 초당·장당으로 읽었습니다. 여전히 계획용 숫자입니다. 비용은 길이, 해상도, 모드에 따라 늘고, Replicate는 예고 없이 가격을 바꿉니다. 갱신은 모델 페이지(`replicate.com/{owner}/{model}`)에서. `replicate.com/pricing`은 소개된 일부만 있습니다.

---

## 이미지 모델. 페이로드

### google/nano-banana-2 (image-default). schema-verified

`POST /v1/models/google/nano-banana-2/predictions`

```json
{
  "input": {
    "prompt": "{{prompt}}",
    "aspect_ratio": "{{ratio}}",
    "output_format": "jpg",
    "resolution": "2K",
    "image_input": []
  }
}
```

| 파라미터 | 타입 | 기본 | 옵션 | 메모 |
|-----------|------|---------|---------|-------|
| `prompt` | string | 없음 | 필수 | 약 300단어 안. 구성하는 법은 VISUAL_INTELLIGENCE.md. |
| `aspect_ratio` | string | `"match_input_image"` | `1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 4:5, 5:4, 21:9, 1:4, 4:1, 1:8, 8:1, match_input_image` | 유일한 크기 조절. width/height 없음. 극단 배너 비율(1:4 … 8:1)은 2026-07-21 버전과 함께 왔습니다. |
| `output_format` | string | `"jpg"` | `jpg, png` | `webp`는 빠졌습니다. 보내면 422. 품질은 PNG. |
| `resolution` | string | `"1K"` | `1K, 2K, 4K` | 기본이 1K로 내려갔고 4K가 왔습니다(2026-07-21). 가격은 해상도와 함께 오릅니다($0.067 / $0.101 / $0.151). 명시합니다. 위 페이로드는 2K로 고정합니다. |
| `image_input` | array | `[]` | 이미지 URL 최대 **14** | 합성, 수정, 참조. 한 장이어도 배열. |
| `image_search`, `google_search` | boolean | `false` | 없음 | 밖의 이미지나 사실을 생성에 끌어오는 새 접지 토글. 브랜드 작업에서는 끕니다. |

**422가 나는 실수.** `width`/`height`(미지원. aspect_ratio만), `negative_prompt`(이 계열에 없음. 원하는 것을 말하고 싫은 것을 말하지 않음), 문자열인 `image_input`(배열이어야 함), `2:1` 같은 미지원 비율, `output_format: "webp"`, `safety_filter_level`(이제 nano-banana-pro에만). 따옴표가 있는 프롬프트는 JSON 이스케이프.

### google/nano-banana-pro (image-premium-4k). schema-verified

nano-banana-2와 같은 계열 표면, 차이만. `resolution` 기본 `2K`(`1K, 2K, 4K`). 1:4 / 4:1 / 1:8 / 8:1 없음. 검색 토글 없음. `safety_filter_level`(`block_low_and_above / block_medium_and_above / block_only_high`, 기본 `block_only_high`. 그대로 둠). `allow_fallback_model`(boolean, 기본 `false`). `true`면 Google 용량이 부족할 때 Replicate가 다른 모델(Seedream lite, $0.035)로 바꿉니다. 세트의 룩이 맞아야 하면 `false`로 둡니다. 1K/2K $0.15, 4K $0.30.

### openai/gpt-image-2.6-flare와 openai/gpt-image-2.6-sunburst (image-complex-prompt, image-instruct-edit). schema-verified 2026-11-16

`POST /v1/models/openai/gpt-image-2.6-sunburst/predictions` (또는 `.../gpt-image-2.6-flare/predictions`)

Flare는 초안과 대화형 작업의 빠른 모델입니다. Sunburst는 세밀한 구도, 정밀 수정, 연속 수정입니다. Replicate에서 입력 표면과 장당 가격이 같습니다.

```json
{
  "input": {
    "prompt": "{{prompt}}",
    "quality": "medium",
    "complexity": "high",
    "aspect_ratio": "{{ratio}}",
    "output_format": "png",
    "input_images": []
  }
}
```

| 파라미터 | 타입 | 기본 | 옵션 | 메모 |
|-----------|------|---------|---------|-------|
| `prompt` | string | 없음 | 필수 | 레이아웃 스펙처럼 읽힙니다. 장면 안 정확한 단어는 따옴표. 광고 문구는 이미지 위 HTML. |
| `quality` | string | `"auto"` | `low, medium, high, xhigh, max, auto` | 가격을 결정합니다($0.05 / $0.09 / $0.128 / $0.25 / $0.50. `auto`는 $0.25). 초안은 `low`, 최종은 `xhigh` 또는 `max`. |
| `complexity` | string | `"high"` | `low, medium, high` | 렌더 전에 얼마나 계획하는지. 빽빽한 글자와 레이아웃은 `high`. 집중 수정은 `low`/`medium`. 가격은 안 변합니다. |
| `aspect_ratio` | string | `"1:1"` | `1:1, 3:2, 2:3, 4:3, 3:4, 16:9, 9:16, auto` 또는 `3840x2160` / `2160x3840`까지의 픽셀 | 2560x1440 초과는 실험적입니다. |
| `input_images` | array | 없음 | 이미지 URL | 실제 사진에서 수정·합성하고 제품 참조를 넘깁니다. 파라미터 이름은 **`input_images`**입니다. `image_input`이 아닙니다. 그것은 Google 계열 이름입니다. 높은 충실도로 읽습니다. 충실도 설정은 없습니다. |
| `output_format` | string | `"webp"` | `png, jpeg, webp, gif, svg` | `gif`는 움직이는 GIF. `svg`는 벡터 트레이스(생성만, 이미지 하나). 넘길 때는 PNG. |
| `frame_count` | integer | `9` | 2-16 | GIF만. 모든 프레임이 이미지 예산 하나. 1:1 GIF는 512x512, 16:9는 896x512. |
| `frame_duration_ms` | integer | `200` | 20-2000 | GIF만, 10ms 단위로 반올림. |
| `background` | string | `"auto"` | `auto, transparent, opaque` | 투명은 `png` 또는 `webp`. |
| `svg_model` | string | `"gpt-5.6-terra"` | 트레이스 모델 | SVG만. |
| `moderation` | string | `"auto"` | `auto, low` | 기본 유지. |
| `number_of_images` | integer | `1` | 1-10 | 한 호출의 변형, 각각 과금. |
| `output_compression` | integer | `90` | 0-100 | jpeg/webp만. |
| `openai_api_key` | string | 없음 | 선택 | 자기 OpenAI 키면 Replicate가 아니라 OpenAI에 직접 과금. |

GIF와 SVG는 OpenAI가 보고하는 토큰으로 과금됩니다. 프레임이 많고 품질이 높으면 더 비쌉니다. 루프는 마지막 프레임이 첫 프레임과 같아야 한다고 프롬프트에 말합니다. 파이썬 urllib로 API를 부르면 `User-Agent` 헤더가 필요합니다. 없으면 403입니다.

### black-forest-labs/flux-2-max, flux-2-pro, flux-2-flex (image-art-direction). schema-verified

공유 표면. `prompt`. `aspect_ratio`(`1:1, 16:9, 3:2, 2:3, 4:5, 5:4, 9:16, 3:4, 4:3, match_input_image, custom`. `custom`이 `width`/`height` 256-2048을 엽니다). `resolution`(`0.5 MP, 1 MP, 2 MP, 4 MP, match_input_image`, 기본 1 MP. 가격 레버). `input_images`(배열. 참조 또는 수정 소스. Replicate 기준 pro는 최대 8, flex는 최대 10). `output_format`(`webp, jpg, png`, 기본 webp). `output_quality`. `safety_tolerance` 1-5. `seed`(FLUX는 시드를 잘 존중합니다. 반복 규율에 씁니다). `flux-2-flex`는 `steps`(1-50, 기본 30), `guidance`(1.5-10, 기본 4.5), `prompt_upsampling`(기본 `true`. 글자 그대로면 `false`)를 더합니다. 네거티브 프롬프트 없음.

가격은 들어오는 메가픽셀과 나가는 메가픽셀 모두. pro는 실행 $0.015 + 입력 MP당 $0.015 + 출력 MP당 $0.015. max는 실행 $0.04 + 양방향 MP당 $0.03. flex는 양방향 MP당 $0.06. 그래서 flex가 픽셀당 셋 중 가장 비쌉니다. 손잡이가 필요할 때 고릅니다. 예산 옵션으로 고르지 않습니다. 예산 옵션은 pro입니다.

### bytedance/seedream-4.5 (image-stylized). schema-verified

`prompt`. `size`(`2K, 4K, custom`. `custom`이 `width`/`height` 1024-4096). `aspect_ratio`(`21:9`, `9:21`, `match_input_image` 추가). `image_input`(배열, 참조). `max_images` 1-15와 `sequential_image_generation: "auto"`로 한 호출에 일관된 세트. `disable_safety_checker`. **`seed` 파라미터 없음.** 4.5가 뺐습니다. 이전 승자를 `image_input`으로 되돌려 반복합니다. 양식화·편집 미감이 강하고, ideogram보다 정확한 글자는 약합니다. 장당 $0.04.

### recraft-ai/recraft-v4 / recraft-v4-svg (image-vector). schema-verified

`prompt`. `size`(고정 픽셀 프리셋, 기본 `1024x1024`). `aspect_ratio`(기본 `Not set`, 또는 `1:1` … `6:10`). **v4에는 `style` 파라미터가 없습니다.** v3에는 있었습니다. 스타일은 프롬프트에 넣습니다("flat vector illustration, two-colour, …"). `-svg` 변형은 실제 SVG 마크업을 돌려줍니다. 명단에서 유일한 모델입니다. v4 $0.04, v4-svg $0.08. 더 새 `recraft-v4.1` / `-pro` / `-utility` ID가 있습니다(2026-05). 명단 밖, 미시험.

### ideogram-ai/ideogram-v3-turbo (image-text-render). schema-verified

`prompt`(정확한 글자는 프롬프트 안 "큰따옴표"). `aspect_ratio`. `resolution`(명시적 픽셀 프리셋, 기본 `None`). `style_type`: `None, Auto, General, Realistic, Design` (**Title-case**. `AUTO/GENERAL/…`가 아닙니다. 열거가 대소문자를 가립니다). `magic_prompt_option`: `Auto, On, Off`(Title-case. 글자 그대로면 `Off`). `style_preset`(이름 있는 룩 60개 이상). `style_reference_images`(배열). 인페인트는 `image`와 `mask`. `seed`. 그래픽이 타이포 주인공이거나 이미지 안 글자가 6단어를 넘으면 여기로. 장당 $0.03. Ideogram v4(`ideogram-v4-quality`, `-balanced`. 2026-06)가 있습니다. 명단 밖, 미시험.

---

## 영상 모델. 페이로드

### wan-video/wan-2.5-i2v-fast / wan-2.5-t2v-fast (video-draft). schema-verified

`POST /v1/models/wan-video/wan-2.5-i2v-fast/predictions`

```json
{
  "input": {
    "prompt": "{{motion_description}}",
    "image": "{{start_image_url}}",
    "resolution": "720p",
    "duration": 5
  }
}
```

- 이미지 파라미터는 **`image`**입니다(i2v 필수. `start_image`가 아님).
- `resolution`은 **`720p` 또는 `1080p`만**. 480p는 스키마에서 빠졌습니다. README는 아직 광고합니다. `"480p"`는 422. 초안 해상도는 720p입니다.
- `duration`은 `5` 또는 `10`(정수 열거).
- 그 밖. `negative_prompt`, `seed`, `audio`(URL. 트랙과 동기로 생성), `enable_prompt_expansion`(기본 `true`. 모션 프롬프트를 글자 그대로 따라야 하면 `false`).
- **T2V 변형은 `resolution`/`aspect_ratio`가 아니라 `size`.** `1280*720`, `720*1280`, `1920*1080`, `1080*1920`(x가 아니라 별표). 그 외 본문은 같고 `image`가 없습니다.
- 720p $0.068/s, 1080p $0.102/s(두 변형 모두). 5초 720p 초안은 약 $0.34.
- 옛 `wan-2.2-*`는 `duration` 대신 `num_frames`를 썼습니다. 422가 `duration`을 말하면 API 페이지를 확인합니다. Wan의 duration 파라미터는 버전마다 흔들렸습니다.

### wan-video/wan-2.7-i2v. schema-verified. 초안 단계의 대체품이 아님

2.5와 표면이 다릅니다. 시작 이미지는 **`first_frame`**(`image`가 아님). `last_frame`이 끝 프레임. `first_clip`이 이전 클립을 이어 받습니다(ffmpeg 없는 프레임 잇기). `duration`은 2-15의 아무 정수. `resolution`은 `720p` / `1080p`. 기본 **1080p**. 720p로 두거나 1.5배를 냅니다. 그 밖 `audio`, `seed`, `negative_prompt`, `enable_prompt_expansion`. 720p $0.10/s, 1080p $0.15/s. 5초 720p는 $0.50. Wan-fast 초안보다 약 50% 비싸고, 15초 천장과 끝 프레임 제어가 있습니다. 2.7은 승인된 움직임의 중간 단계로 대합니다. 초안 모델로 대하지 않습니다. 2.7에 `-fast` 변형은 없습니다.

### kwaivgi/kling-v3-video (video-production). schema-verified

ID를 확인합니다. `kling-v3-video`입니다. `kling-v3.0`이 아닙니다. 점 있는 v3 ID는 404입니다.

`POST /v1/models/kwaivgi/kling-v3-video/predictions`

```json
{
  "input": {
    "prompt": "{{motion_description}}",
    "negative_prompt": "blurry, low quality, distorted, watermark, text overlay",
    "start_image": "{{image_url}}",
    "duration": 5,
    "aspect_ratio": "16:9",
    "mode": "pro",
    "generate_audio": false
  }
}
```

| 파라미터 | 타입 | 기본 | 옵션 | 메모 |
|-----------|------|---------|---------|-------|
| `prompt` | string | 없음 | 필수 | I2V는 움직임을 묘사합니다. 모델이 시작 이미지를 봅니다. 멀티샷은 샷을 순서대로("Shot 1: ... Cut to: ..."). |
| `mode` | string | `"pro"` | `standard, pro, 4k` | 가격 레버. 초당 $0.168 / $0.224 / $0.42. `standard`는 최종의 초안에 충분합니다. |
| `start_image` | URI | 없음 | 이미지 URL | Kling 계열 파라미터 이름. 이미지가 있으면 비율은 이미지를 따릅니다. |
| `duration` | integer | `5` | **3-15**의 아무 정수 | 5/10/15만이 아닙니다. 7초도 됩니다. 문자열 아님. |
| `aspect_ratio` | string | `"16:9"` | `16:9, 9:16, 1:1` | `start_image`가 있으면 무시. |
| `negative_prompt` | string | 없음 | 자유 텍스트 | 지원합니다(nano-banana 계열과 다름). |
| `generate_audio` | boolean | `false` | 없음 | 네이티브 오디오. standard +$0.084/s, pro +$0.112/s(약 +50%). 4k는 포함. 소리가 나갈 때만 켭니다. |
| `end_image` | URI | 없음 | 이미지 URL | 목표 마지막 프레임(보간). |
| `multi_prompt` | string | 없음 | 구조화된 샷 목록 | 명시적 멀티샷 입력. `prompt` 안의 산문 샷 목록도 됩니다. |

`guidance_scale`은 Kling API 2.5에서 빠졌습니다. 넣지 않습니다.

### kwaivgi/kling-v3-omni-video (video-reference). schema-verified

kling-v3-video 표면에 더함. `reference_images`(배열. 인물·사물 일관성), `reference_video`(URL)와 `video_reference_type`(`feature`는 룩·움직임을 빌림, `base`는 이 영상을 수정), `keep_original_sound`(기본 `true`). 대변인 팩(말하는 사람 모드)과 "같은 인물, 새 장면"에 씁니다. 가격. standard $0.168/s(오디오 $0.224), pro $0.224($0.28), 4k $0.42.

### bytedance/seedance-2.0 (video-reference). schema-verified

```json
{
  "input": {
    "prompt": "{{motion_description}}",
    "image": "{{start_image_url}}",
    "duration": 5,
    "resolution": "720p",
    "aspect_ratio": "9:16",
    "generate_audio": false,
    "reference_images": []
  }
}
```

- 시작 프레임은 **`image`**. 끝 프레임은 `last_frame_image`.
- 참조 배열. `reference_images`(최대 9), `reference_videos`(최대 3), `reference_audios`(최대 3). 명단에서 가장 강한 원참조 파이프라인.
- `duration`. 15까지의 정수, 또는 모델이 길이를 고르게 **`-1`**.
- `resolution`. `480p, 720p, 1080p, 4k`(기본 720p). `aspect_ratio`는 `21:9`, `9:21`, `adaptive`를 더합니다.
- **`generate_audio` 기본은 `true`.** 끄지 않으면 오디오가 켜집니다. 네거티브 프롬프트 없음. `seed` 지원.
- 비디오 입력을 넘겼는지로 과금. 없으면 480p $0.08/s, 720p $0.18/s, 1080p $0.45/s, 4k $1.00/s. `reference_videos`가 있으면 $0.10, $0.22, $0.55, $1.25.

### bytedance/seedance-1-pro (video-locked-camera). schema-verified

```json
{
  "input": {
    "prompt": "{{motion_description}}",
    "image": "{{image_url}}",
    "duration": 5,
    "resolution": "1080p",
    "aspect_ratio": "9:16",
    "camera_fixed": true
  }
}
```

`camera_fixed: true`가 이 모델이 명단에 남는 이유입니다. 카메라 드리프트 없는 고정 제품 샷. 길이 2-12초(가장 넓음). `resolution` `480p, 720p, 1080p`. 화면비 7개. 끝 프레임 `last_frame_image`. `seed`. 네거티브 프롬프트 없음, 오디오 없음. 480p $0.03/s, 720p $0.06/s, 1080p $0.15/s. 명단에서 가장 싼 초당이라, 정당한 초안 경로이기도 합니다.

### runwayml/gen-4.5 (video-premium). schema-verified

Replicate의 현재 Runway 기함(버전 2026-02-18). `prompt`. `image`(첫 프레임). `duration` `5` 또는 `10`. **`aspect_ratio`**(`16:9, 9:16, 4:3, 3:4, 1:1, 21:9`). `ratio`가 아닙니다. `seed`. 네거티브 프롬프트 없음, 오디오 없음, 끝 프레임 없음, 참조 없음. $0.12/s.

### google/veo-3.1 / veo-3.1-fast (video-premium). schema-verified

```json
{
  "input": {
    "prompt": "{{motion_description}}",
    "image": "{{image_url}}",
    "duration": 8,
    "aspect_ratio": "16:9",
    "resolution": "1080p",
    "generate_audio": true
  }
}
```

- 이미지 파라미터는 **`image`**(`start_image` 아님). `duration`은 `4, 6, 8`만.
- 정사각 없음(`16:9`/`9:16`만). 1:1은 후반에서 크롭. `resolution` `720p` / `1080p`. `negative_prompt` 지원. `seed` 지원.
- `reference_images`(URL 1-3)는 피사체 일관성을 안내합니다. 첫 프레임을 정하지 않습니다. `last_frame`이 끝 프레임. `generate_audio` 기본 `true`.
- `-fast` 변형. 같은 표면에서 `reference_images`만 없음. 충실도가 낮습니다.
- Veo 3.1. 오디오 $0.40/s, 없이 $0.20/s(8초 $3.20 / $1.60). Fast. 오디오 $0.15/s, 없이 $0.10/s.

### openai/sora-2 / sora-2-pro. 2026-11-13 제거

OpenAI가 Sora 2와 Sora 2 Pro API를 2026-09-24에 종료했고, 두 replicate.com 페이지는 404입니다. 모델 메타데이터 엔드포인트는 여전히 200이라 verify_models.sh만으로는 통과했을 것입니다. 종료가 가까운 모델은 공개 페이지를 확인합니다. Sora를 지명한 저장된 브리프나 스타일 락은 역할 맵의 `video-ugc`(Seedance 2.0) 또는 프리미엄 트리오로 풉니다.

### 모델 간 파라미터 표

같은 개념의 이름이 계열마다 다릅니다. 호출을 쓰기 전에 확인합니다.

| 개념 | Wan 2.5 fast | Wan 2.7 | Seedance 1-pro / 2.0 | Kling 3.0 (/Omni) | Veo 3.1 | Runway 4.5 |
|---------|-------------|---------|----------------------|-------------------|---------|------------|
| 시작 이미지 | `image` | `first_frame` | `image` | `start_image` | `image` | `image` |
| 길이 | `duration` (5/10) | `duration` (2-15) | `duration` (2-12 / -1 또는 15 이하) | `duration` (3-15) | `duration` (4/6/8) | `duration` (5/10) |
| 해상도 / 단계 | `resolution` 720p-1080p (t2v는 `size`) | `resolution` 720p-1080p | `resolution` 480p-1080p / -4k | `mode` standard/pro/4k | `resolution` 720p/1080p | 없음 |
| 화면비 | 이미지에서 (t2v는 `size`) | 이미지에서 | `aspect_ratio` (7 / 8, `adaptive` 포함) | `aspect_ratio` (3) | `aspect_ratio` (1:1 없음) | `aspect_ratio` (6) |
| 네거티브 | 있음 | 있음 | 없음 | 있음 | 있음 | 없음 |
| 네이티브 오디오 | `audio` 입력(트랙 동기) | `audio` 입력 | 1-pro 없음 · 2.0 `generate_audio`(기본 켜짐) | `generate_audio`(기본 꺼짐) | `generate_audio`(기본 켜짐) | 없음 |
| 끝 프레임 | 없음 | `last_frame` | `last_frame_image` | `end_image` | `last_frame` | 없음 |
| 참조 이미지 | 없음 | 없음 | 2.0 `reference_images`(9 이하) + `reference_videos` / `reference_audios`(3 이하) | Omni `reference_images`, `reference_video` | `reference_images`(1-3. -fast에는 없음) | 없음 |
| 카메라 잠금 | 없음 | 없음 | 1-pro `camera_fixed` | 없음 | 없음 | 없음 |
| 시드 | 있음 | 있음 | 있음 | 없음 | 있음 | 있음 |

---

## 립싱크 모델. 페이로드

### sync/lipsync-2-pro (lipsync-default). schema-verified

```json
{
  "input": {
    "video": "{{source_video_url}}",
    "audio": "{{audio_url}}",
    "sync_mode": "loop"
  }
}
```

스튜디오 기본. 파라미터 이름은 `video`/`audio`입니다. `video_url`/`audio_file`이 아닙니다. 그것은 Kling 모델입니다. `sync_mode`가 오디오와 영상 길이 불일치를 다룹니다. `loop`, `bounce`, `cut_off`, `silence`(무음으로 영상을 채움), `remap`(오디오에 맞춰 영상 시간을 다시 잡음). `temperature` 0-1(기본 0.5. 입 움직임의 표현). `active_speaker`(boolean. 여러 사람 샷에서 말하는 사람만 싱크). 고개 움직임과 긴 클립을 대안보다 잘 다룹니다. $0.08325/s, 약 $5/분.

### kwaivgi/kling-lip-sync (lipsync-kling). schema-verified

```json
{
  "input": {
    "video_url": "{{source_video_url}}",
    "audio_file": "{{audio_url}}"
  }
}
```

텍스트 변형. `audio_file`을 `text` + `voice_id`(예 `"en_AOT"`) + `voice_speed`(**0.8-2.0**, 기본 1)로 바꿉니다. 제약(이전 레지스트리에서 이어졌고 제공처가 아직 강제). 영상 2-10초, 720p-1080p, 100MB 미만. 오디오 5MB 미만. `audio_file`과 `text`는 양립하지 않음. `video_url`과 `video_id`는 양립하지 않음(Kling 소스는 `video_id`. 재업로드를 건너뜀). 정면, 조명, 한 사람. 옆모습은 실패합니다. $0.014/s. `en_AOT`는 영어 보이스 예시입니다. 한국어 목소리의 기본은 외부 TTS입니다.

### pixverse/lipsync (lipsync-budget). schema-verified

`audio`와 `video`(둘 다 필수). 표면의 전부입니다. `text`/TTS 입력이 없으니 목소리 트랙을 직접 가져옵니다. 초안과 대본 반복의 싼 싱크. $0.04/s.

### bytedance/omni-human (digital-human). schema-verified

전신 디지털 휴먼. `image`(스틸 하나)와 `audio`가 말하고 제스처하는 사람(입이 아니라 몸). 가장 비싼 립싱크 경로이고, 영상이 아니라 사진에서 되는 유일한 경로입니다. $0.14/s.

---

## Replicate에서 본 더 새 ID (2026-11-13). 명단 밖

여기서 미시험입니다. 역할을 맡기 전에 명단 줄, 절, 검증 실행이 필요합니다. 새로고침이 처음부터 다시 발견하지 않도록 적습니다. API 메타데이터는 2026-11-13에 확인했습니다. 스키마와 가격은 읽지 않았습니다.

- 영상. `kwaivgi/kling-v4.0`(2026-11-10. 텍스트, 키프레임, 참조에서 최대 1080p, 3-30초. 다음 video-production 후보로 보임)과 `kling-v4-flash`. `bytedance/seedance-2.5`(네이티브 오디오의 30초 클립), `seedance-2.0-fast`, `seedance-2.0-mini`. `wan-video/wan-2.7-t2v`, `wan-2.7-r2v`, `wan-2.7-videoedit`. `minimax/hailuo-2.3`(`-fast` 포함). `pixverse/pixverse-v6`. `runwayml/aleph-2`. `kwaivgi/kling-v3-motion-control`, `kling-avatar-v2`. `google/veo-3.1-lite`.
- 이미지. `google/nano-banana-2.1`(2026-11-05. 더 선명한 글자, 최대 4K)과 `nano-banana-2-lite`. `black-forest-labs/flux-3-image`(2026-10)와 예산 단계 `flux-2-klein-*`. `bytedance/seedream-5-lite`. `ideogram-ai/ideogram-4-5`(2026-11-09)와 `ideogram-v4-quality` / `-balanced`. `recraft-ai/recraft-v4.1` / `-pro` / `-svg` / `-utility`.
- 립싱크와 목소리, Replicate 공식. `bytedance/omni-human-1.5`. `sync/lipsync-2`(비프로). `heygen/avatar-v`, `heygen/lipsync-precision`, `heygen/lipsync-speed`, `heygen/video-translate`. `elevenlabs/v3`, `elevenlabs/flash-v2.5`, `elevenlabs/music`, `elevenlabs/dubbing`.

이 목록의 ID를 역할에 연결하지 않습니다. 검증 전에 명단에 올린 것처럼 부르지 않습니다.

---

## 비용 참고 (2026-11-13 가격의 계획 숫자)

| 작업 | 소재 | 비용 |
|-----|--------|------|
| 이미지 반복 (기본 모델 1K, 변형 5) | 이미지 5 | 약 $0.35 (2K 약 $0.50) |
| 4K 히어로 스틸 (nano-banana-pro) | 이미지 1 | 약 $0.30 (NB2 자체 4K $0.15) |
| 초안 패스 (초안 단계, 720p 5초, 모션 4) | 클립 4 | 약 $1.35 (480p seedance-1-pro 약 $0.60) |
| 제작 최종 (5초, 오디오 없음, Kling `pro`) | 클립 1 | 약 $1.12 (`standard` $0.84) |
| 제작 최종 (15초, 오디오, Kling `pro`) | 클립 1 | 약 $5.04 (`standard` $3.78) |
| 프리미엄 히어로 세 모델 (병렬, 각 8초) | 클립 3 | 약 $7.70 (오디오 Veo $3.20 + Runway $0.96 + 1080p Seedance 2.0 $3.60) |
| 립싱크 (스튜디오 기본, 30초) | 클립 1 | 약 $2.50 (예산 $1.20, Kling $0.42) |
| 광고 매트릭스 12칸, 스틸 비율 하나 (1K) | 이미지 12 | 약 $0.80 |
| 캠페인 전체 (이미지 20 + 제작 클립 5 + 립싱크 2) | 소재 27 | 약 $9-14 |

비용 규율(SKILL.md). 1달러 미만은 확인 없음. 1달러에서 2달러는 한 줄로 알리고 진행. 2달러 이상은 전에 확인. 이 가격에서 `pro` 모드 5초 제작 클립 하나가 이미 1달러 선을 넘습니다. 숫자를 말합니다.

---

## 고장 수리

| 증상 | 그럴듯한 원인 | 고침 |
|---------|-------------|-----|
| 401 | `REPLICATE_API_TOKEN`이 없거나 틀림 | 환경 변수 / .env |
| 모델 404 | 틀리거나 이름이 바뀐 모델 ID | `scripts/verify_models.sh`. 이 파일을 고침 |
| 지난달 통과한 모델의 404 | 제공처 종료 (Sora 2 / Sora 2 Pro, 2026-09-24) | 명단 블록과 그 절에서 삭제. 역할을 명단 모델로 |
| 422 | 이 계열의 파라미터 이름이 틀림 | 위의 모델 간 표 |
| 출력 URL 404 | 성공 1시간 뒤에 받음 | 다시 생성. 항상 즉시 받음 (api-workflow.md) |
| 영상에 움직임이 없음 | I2V 프롬프트가 장면은 말하고 움직임은 말하지 않음 | 프롬프트를 움직임만으로 다시 씀 |
| 정사각 비율 거절 | Veo에 1:1이 없음 | 16:9로 만들고 후반 크롭, 또는 Kling |
| 립싱크 거절 | 소스 영상의 길이, 해상도, 크기 제한 | 위 모델별 제약 |
| 429 | 레이트 리밋 | 60초 대기. 5~8개 파동 (api-workflow.md) |

---

크리에이티브 엔진의 단일 출처입니다. 상류에서 모델이 바뀌면 이 파일을 고치고, `registry_version`을 올리고, `scripts/verify_models.sh`를 다시 돌립니다. 모드 파일은 역할을 참조하므로 그때 바꿀 필요가 없습니다.

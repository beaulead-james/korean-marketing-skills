---
name: creative
description: 제품 사진, 제품 영상, 소셜 그래픽, 말하는 사람, 광고 소재를 하나의 단계 파이프라인으로 만들고, 실사나 생성 영상을 코드로 잘라 MP4로 무료 렌더합니다. 보여 주기 전에 비전 QA로 모든 소재를 봅니다. 광고 형식 어휘는 미국 메타 336건에서 가져오되 그 수치를 한국 성과로 옮기지 않습니다. 한국 자리는 메타 피드 1:1과 4:5와 9:16, 유튜브 쇼츠, 네이버 플레이스 소식 이미지, 카카오입니다.
when_to_use: generate an image, product shot, product video, hero video, social graphic, YouTube thumbnail, talking head, UGC video, lip sync, ad creative, ugc ads, ad concepts, static ads, video ad, hooks for ads, make ads, edit my product photo, animate this image, make visuals for this campaign, motion ad, kinetic text ad, turn my reviews into a video ad, video ad from screenshots, captions on my video, hyperframes, remotion, ad formats that work, us vs them ad, review stack ad, hook ideas for ads, 광고 이미지, 숏폼, 훅, 제품 사진, 제품 영상, 말하는 영상, 립싱크, 모션 광고, 메타 피드 소재, 유튜브 쇼츠 광고, 플레이스 소식 이미지, 카카오 배너, 비교 광고 이미지, 리뷰 카드 광고
argument-hint: "[만들 것. 비우면 종류에 맞춰 배정]"
metadata:
  boring:
    version: 1.0.0
    layer: execution
    reads: [creative-kit, positioning#chosen-angle, voice-profile#voice-summary]
    writes: [creative-kit]
    optional-keys: [REPLICATE_API_TOKEN, OPENAI_API_KEY, HF_API_KEY_ID, HF_API_KEY_SECRET, ELEVENLABS_API_KEY]
---

# 크리에이티브

브랜드가 내보내는 시각 소재를 한 엔진으로 만듭니다. 움직임과 스타일을 포지션에 맞추고, 최종에 돈을 쓰기 전에 방향을 싼 초안으로 찾고, 직접 보지 않은 소재는 보여 주지 않습니다. 끝난 상태는 받아 둔 파일, QA를 통과하고, 브랜드와 맞고, 다음 스킬이 경로로 찾는 이름입니다. 이건 바닥입니다. 상황이 더 나은 길을 가리키면 그 길을 가고 이유를 한 줄로 말합니다.

가격 숫자는 레지스트리의 달러입니다. 원화로 환산해 단정하지 않습니다. 사장님에게 보이는 가격만 원입니다. 광고 문안은 표시광고법을 봅니다. 거짓·과장, 기만, 부당 비교는 넣지 않습니다. 의료광고, 대부업, 금융, 건강기능식품은 업종 심의를 확인하라고 경고만 합니다. 조문 번호는 단정하지 않습니다.

하드 규칙은 적습니다. 지어내지 않습니다. 자동 게시와 자동 발송은 하지 않습니다. 고객 데이터는 워크스페이스 브랜드 폴더에만 둡니다. Replicate 키가 없어도 막지 않습니다. 콘셉트와 정확한 프롬프트를 씁니다.

한국에서 먼저 맞출 자리. 메타 피드 1:1, 4:5, 9:16. 유튜브 쇼츠. 네이버 플레이스 소식 이미지. 카카오.

## 맥락

`./brand/`, `./brands/`, `MARKETING.md` 중 하나가 있을 때만 실행합니다. 없으면 불러올 것이 없습니다.

`python3 ${CLAUDE_SKILL_DIR}/../start-here/scripts/brand_context.py --for creative`

스크립트나 python3가 없으면 `reads:`의 파일을 직접 읽습니다. 절이 지정되면 그 절만 봅니다. 아무것도 없으면 단독으로 진행합니다. 과제에 꼭 필요한 것만 묻습니다.

`learnings.md`에 크리에이티브 선례(먹힌 훅, 이긴 스타일)가 있으면 적용합니다. 일을 바꾼 것만 노트에 한 줄 적습니다.

## 준비

1. **키.** `$REPLICATE_API_TOKEN`(환경 또는 `.env`)을 확인합니다. 없으면 프롬프트 전용 모드입니다. `references/api-workflow.md` 6절. 같은 작업 흐름이고, 결과물은 파일이 아니라 정확한 프롬프트, 모델, 설정입니다. 키 때문에 멈추지 않습니다.
2. **스택.** `./brand/creative-stack.md`가 없거나 레지스트리 `ttl-days`보다 오래됐으면, 첫 유료 호출 전에 `bash ${CLAUDE_SKILL_DIR}/scripts/verify_models.sh`를 돌립니다. `./brand/creative-stack.md`를 다시 씁니다. start-here가 두는 `stack.md`와 다른 파일입니다.
3. **브랜드 키트.** `./brand/creative-kit.md`를 읽습니다. 없으면 단발 소재는 진행하고 끝난 뒤에 키트를 제안합니다. 캠페인 작업이면 먼저 키트를 만듭니다.

## 쓰는 것

필수는 없습니다. 키가 없으면 이미 가진 도구에 넣을 정확한 프롬프트, 모델, 설정을 씁니다. 파일을 대신 만들 때는 작업마다 하나를 고릅니다. 키 이름은 TOOLS.md. 페이로드와 모델별 가격은 `references/MODEL_REGISTRY.md`에만 있습니다.

- **이미지.** GPT Image 2.6(OpenAI). 빠른 초안은 Flare, 최종과 제품을 편집마다 같게 유지할 때는 Sunburst. 역할은 `image-complex-prompt`와 `image-instruct-edit`입니다. 정확한 레이아웃, 실제 사진 수정, 휴대폰처럼 보이는 사진, 움직이는 GIF. 장당 과금. OpenAI API(`OPENAI_API_KEY`) 또는 Replicate. 일상 스틸은 `image-default`. 광고 문자는 이미지 안이 아니라 이미지 위 HTML에 둡니다.
- **영상.** Seedance 2.5(ByteDance)를 Higgsfield 또는 Replicate로, 클립당 과금합니다. 공급자가 2.5를 올리면 2.5, 아니면 2.0입니다. 레지스트리에서 검증된 행은 Seedance 2.0이고, 2.5는 검증 전 "더 새 것" 행입니다. 역할을 맡기 전에는 2.0에 머뭅니다. 광고에서 Higgsfield Marketing Studio는 진행자나 UGC풍 영상, 스틸 형식을 빨리 탐색할 때 고릅니다. AI 진행자는 소개만 하고 후기를 말하지 않습니다. Seedance 2.5는 비롤, 효과음, 말하는 사물입니다. 설정과 시험, API 범위는 `references/ad-formats.md`.
- **목소리와 말하는 사람.** ElevenLabs. 목소리, 복제, 캠페인 전체의 같은 목소리. 무료 구간이 있고 그다음 요금제입니다(`ELEVENLABS_API_KEY`). 없으면 립싱크 모델의 내장 목소리나 짧은 TTS로 대본 시험을 덮습니다.
- **코드로 자르는 영상 광고.** HyperFrames(HeyGen, Apache-2.0). HTML과 GSAP 타임라인을 쓰고 CLI가 이 기계에서 MP4를 렌더합니다. 무료이고 키가 없으며 렌더당 요금이 없습니다. Node 22 이상과 FFmpeg가 필요합니다. 실사나 생성 영상에 자막, 리뷰 카드, 혜택, 엔드 카드를 붙이고 한 프로젝트에서 훅 변형을 렌더합니다. Remotion은 대안입니다. 회사 규모에 맞는 라이선스를 확인합니다. 모드 파일은 `modes/motion-ads.md`.
- **모델 여러 개에 키 하나.** Replicate가 레지스트리 페이로드와 비동기 패턴의 경로입니다(`REPLICATE_API_TOKEN`). Higgsfield는 키 하나의 대안입니다. 이미지·영상 모델 50개 이상, Seedance 포함, 쓴 만큼(`HF_API_KEY_ID`, `HF_API_KEY_SECRET`). Higgsfield에서는 역할과 프롬프트를 유지하고, 파라미터와 호출은 그 문서를 따릅니다.

## 참고 파일

| 파일 | 언제 읽나 |
|------|--------|
| `references/model-routing.md` | 모델 선택 전. 작업에서 모델로, i2v/i2i/t2v, 스타일 캡슐, 무드보드, 자리, Replicate를 떠날 때. |
| `references/MODEL_REGISTRY.md` | 생성 전 항상. 페이로드와 가격의 유일한 출처. 역할은 여기서 풉니다. |
| `references/api-workflow.md` | 세션의 첫 생성. 비동기, 1시간 안 다운로드, 파일 이름, 매니페스트, QA, 핸드오프. |
| `references/VISUAL_INTELLIGENCE.md` | 중요한 프롬프트. 시각 심리, 안티 슬롭(4부가 QA), 스타일, 일관성. |
| `references/ad-formats.md` | 광고 소재를 고르거나 만들거나 반복할 때. 형식, 세 경로, Higgsfield. 미국 수치는 한국 사실이 아닙니다. |
| `references/hooks.md` | 광고의 첫 1초. 오프닝 패턴, 맞는 경우, 채울 문장, 훅 변형. |
| `references/motion-ads-starter.html` | 코드로 영상 광고를 시작할 때. 9:16, 0프레임 훅, 자막, 리뷰 카드, 엔드 카드, 훅 변형. |
| `scripts/ad_library.py` | 계획 전에 경쟁 광고를 볼 때. 메타 광고 라이브러리. 기본 국가는 US. 한국 메타는 `--country KR`. 네이버는 조회하지 않습니다. |

## 모드

| 요청이 이런 느낌 | 모드 파일 |
|---------------------|-----------|
| 제품 스틸, 쇼핑몰 컷, 실제 제품 사진 수정 | `modes/product-photo.md` |
| 공개, 오빗, 시연, 제품이 움직이는 것 | `modes/product-video.md` |
| 게시물, 썸네일, 인용 카드, 콘텐츠 달력, 플레이스 소식 이미지 | `modes/social-graphics.md` |
| 진행자, 대변인, UGC풍 진행(고객 행세 금지), 립싱크 | `modes/talking-head.md` |
| 유료 광고, UGC, 콘셉트, 스틸 광고, 훅, 매트릭스 칸, A/B | `modes/ad-creative.md` |
| 실사·생성 영상을 자른 광고, 자막, 훅 변형 | `modes/motion-ads.md` |
| 그 밖의 시각 | 모드 파일 없음. 브랜드 키트, 레지스트리, 이 파일 |

퀵 모드. "호두 책상 위 병의 16:9 히어로"처럼 단발이 구체적이면 모드 절차를 건너뜁니다. 프롬프트, 생성, QA, 전달, 다음 한 줄.

## 역할로 고릅니다

모델 ID로 고르지 않습니다. 선택 전에 `references/model-routing.md`를 읽습니다. 페이로드와 가격은 `references/MODEL_REGISTRY.md`에만 있습니다. 모델이 바뀌면 레지스트리만 바뀝니다.

```
스틸
├─ 기본                         → image-default (시드가 있으면 시드로 반복)
├─ 4K로 내보냄                  → image-premium-4k
├─ 실제 사진 수정 / 여러 참조   → image-default 의 image_input
├─ 복잡한 구도 / 장면 안 정확한 글자 → image-complex-prompt
├─ 글자가 주인공인 평면 (6단어 초과) → image-text-render
├─ 로고 / 아이콘 / 실제 벡터    → image-vector
└─ 사용자가 모델을 지명         → 그 모델 (페이로드는 레지스트리)

영상. 아래 단계가 기본
├─ 초안                         → video-draft
├─ UGC / 광고 네이티브          → video-ugc
├─ 다듬은 최종                  → video-production
├─ 인물·참조 일관성             → video-reference
├─ 카메라 고정 제품 샷          → video-locked-camera
└─ 명시적 "히어로"              → video-premium (3모델 병렬)

음성
├─ 립싱크 기본                  → lipsync-default
├─ 싼 대본 테스트               → lipsync-budget
├─ video-production 소스        → lipsync-kling
└─ 스틸을 말하는 사람으로       → digital-human

코드로 만드는 영상 광고 (모델 없음, 키 없음)
└─ 실사·생성 영상에 자막, 리뷰 카드, 엔드 카드
   → modes/motion-ads.md
   글자만 움직이는 모션은 SaaS 화면 녹화나 혜택 범퍼에만.
   실물 제품의 본편에는 쓰지 않습니다.
```

사용자에게 모델을 묻지 않습니다. 역할을 고릅니다. 모델 이름, 시드, 장당 비용은 매니페스트에 두고, 채팅 노트에는 총액 한 줄만 적습니다.

## 단계 파이프라인

싼 초안이 방향을 찾고, 제작비는 고른 방향만 따라갑니다.

```
1. 소스 프레임  좋은 영상은 승인된 스틸에서 시작합니다 (I2V가 T2V보다 낫습니다).
                가능하면 이미지를 먼저 만들고 승인합니다.
2. 초안         초안 역할로 움직임 3~5개 (비용은 MODEL_REGISTRY, 720p).
                카메라와 에너지를 다르게. 각각 QA하고 순위를 매겨 보여 줍니다.
3. 선택         사용자가 방향을 고르거나 초안을 한 바퀴 더 요청합니다.
4. 제작         승자를 제작 역할의 풀 품질로 다시 만듭니다.
                프롬프트 골격과, 지원되면 시드 규칙을 유지합니다.
5. 프리미엄     명시적 "히어로"만. 이긴 프롬프트로 세 모델을 병렬로 돌리고
                QA한 뒤 순위를 매겨 보여 줍니다. 조용히 올리지 않습니다.
```

이미지는 단계를 건너뜁니다. `image-default`에서 만들고, 라운드마다 변수 하나만 바꿉니다. 시드가 있으면 재사용해 무엇이 바뀌었는지 알게 합니다.

**비용.** 합계 1달러 미만은 그냥 생성합니다. 1달러에서 2달러는 한 줄로 알리고 진행합니다. 2달러 이상은 실행 전에 확인합니다. 실제 지출은 매니페스트에 적습니다.

## 비전 QA

생성할 때마다 돕니다. 사용자가 보기 전에 봅니다. 날 URL만 던지지 않습니다.

1. 즉시 다운로드합니다. URL은 1시간이면 죽습니다. api-workflow.md 1절.
2. 봅니다. 이미지는 `Read`. 영상은 ffmpeg로 처음, 중간, 끝. api-workflow.md 2절. ffmpeg가 없으면 썸네일이라고 한 줄 말합니다. 모션 광고는 렌더 전 스냅샷 연락 시트를 보고, 최종 MP4에서 프레임을 다시 뽑습니다.
3. 1~10점을 조용히 매깁니다. 브랜드 키트, VISUAL_INTELLIGENCE.md 4부, 요청 스펙(비율, 글자 여백, 초점, 자리).
4. 7 미만이면 실패한 지점만 고치고 다시 만듭니다. 재시도는 대략 두 번입니다. 그 다음은 최선과 결함 이름을 보여 줍니다.
5. 통과본을 보여 줍니다. 무엇인지, 어디에 맞는지 한 줄. 남은 결함은 한 줄만. 여러 모델은 점수와 모델 이름 없이 이유를 달아 순위를 매깁니다.

7 미만으로 남는 소재는 결함을 이름 붙여 보여 줍니다. 점수는 매니페스트 `qa_score`에만 둡니다. 사장님에게 점수를 보여 주지 않습니다.

## 브랜드 키트

`./brand/creative-kit.md`. 색(hex와 이름), 타이포, 사진인지 일러스트인지, 무드, 피할 것, 로고 경로, 저장한 스타일 락·소셜 템플릿·승인 진행자.

만드는 법. 사이트나 소셜 URL을 먼저 받고, 본 것으로 제안합니다. 추론할 수 없는 것만 묻습니다. 저장은 `${CLAUDE_SKILL_DIR}/../start-here/references/brand-memory.md`를 따릅니다. 이전 파일 자동 버전, 변경 요약 3줄, brand.yaml 갱신.

쓰는 법. 팔레트와 무드를 모든 프롬프트에 넣습니다. 피할 것은 상시 가드입니다. 저장한 락과 진행자 스펙은 그대로 재사용합니다.

## 스타일 탐색

잠긴 스타일이 없고 캠페인 범위가 있으면 방향 탐색을 제안합니다. 강요하지 않습니다. 기본 다섯. 업종에서 안전한 것, 그 반대, 다른 업종에서 빌린 것, 감정이 먼저인 것, 관례를 깨는 것. 브리프가 좁으면 줄입니다. 작게 만들고, 방향마다 전략·분위기·위험을 붙여 보여 준 뒤 고르거나 섞게 합니다. 그다음 스타일 락을 캠페인 디렉터리에 쓰고 이후 프롬프트마다 참조합니다.

건너뛰는 때. 락이나 템플릿이 이미 있거나, 요청이 구체적이거나, 후속 소재이거나, 사용자가 건너뛰라고 할 때. 퀵 모드는 항상 건너뜁니다.

규모에서의 일관성은 브랜드 접두어, 잠근 문장, 고정 시드, 참조 이미지입니다. VISUAL_INTELLIGENCE.md 10부.

## 배치

소재 3개 이상이면 생성 전에 매니페스트를 씁니다. api-workflow.md 4절. 5~8개 파동으로 병렬 생성합니다. `done`은 건너뛰고, `failed`는 한 번 재시도하고, `pending`을 실행합니다.

## 산출물

파일 우선. `creative-output/…` 또는 캠페인 트리. 광고는 매트릭스 칸 ID. `./brand/assets.md`에 장당 한 줄. 모델, 프롬프트, 시드, 비용, QA 점수는 매니페스트에만 있습니다.

1. `## <DELIVERABLE>`과 날짜, 이 일이 무엇을 위한 것인지 한 줄
2. 소재. 끝난 것부터. 경로, 무엇인지, 어디에 맞는지. 남은 결함은 한 줄
3. 짧은 **출처와 가정** (최대 10줄). 총액, 기댄 것, 확인할 것, 만들지 않은 것
4. `**저장한 파일:**` 경로와 (새 것)/(갱신)
5. `**다음:**` 아래

다른 스킬에서 브리프가 왔으면 `creative_delivery`(api-workflow.md 5절)를 그 스킬에 넘깁니다. 사장님에게 보이는 글에는 넣지 않습니다.

## 사용자가 결과물을 고칠 때

수정을 반영하고 남깁니다. `./brand/gold/<this skill>/`에 골드 하나, `./brand/checks.md`에 예/아니오 1~3개, 확인은 한 줄. 넘기기 전에 불러온 체크에 조용히 답하고 아니오는 고칩니다. 방법은 `${CLAUDE_SKILL_DIR}/../start-here/references/taste-loop.md`.

## 다음

- `/content-atomizer`. 승인 소재를 자리별 게시로 자릅니다 (약 10분)
- `/paid-ads`. 매트릭스 칸이면 그 주위로 캠페인을 짭니다 (약 15분)
- `/direct-response-copy`. 비주얼과 짝이 되는 문안 (약 15분)
- `/performance-review`. 소재가 돈 뒤에 결과를 칸과 QA 점수에 되돌립니다

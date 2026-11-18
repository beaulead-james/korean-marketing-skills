# 브랜드 기억

브랜드 기억은 모든 스킬이 사용자가 누구인지, 말투가 어떤지, 누구에게 파는지, 무엇이 실제로 통했는지를 기억하는 방식입니다. 디스크에 쌓이고, 골라서 불러옵니다. 각 스킬이 프론트매터에 읽고 쓰는 것을 선언하면 `brand_context.py`가 그것만 냅니다.

## 배치

### MARKETING.md, 상시 브리프

`./MARKETING.md`는 워크스페이스 루트에 있고 사용자가 씁니다. 목표, 제안, 제약, 우선순위, 하지 말 것. 모든 스킬이 먼저, 그대로 읽습니다. `/start-here`가 기초 보고에서 쓰기를 제안할 수 있지만, 필수는 아닙니다.

### preferences.md, 상시 선호

`./brand/preferences.md`는 사용자가 정한 금지 말, 거부한 채널, 말투, 리뷰 규칙, 예산 천장입니다. `/start-here`가 교정 패스와 "기억해"에서 씁니다. 모든 스킬이 읽습니다. 뽑아낸 `voice-profile.md`, 데이터로 쓴 `learnings.md`와 다르고, 그 둘의 단일 작성자 규칙은 그대로입니다.

**브랜드 하나 (기본).**

```
./brand/
  brand.yaml              <- 매니페스트
  voice-profile.md        <- /brand-voice
  positioning.md          <- /positioning-angles
  audience.md             <- /audience-research
  voc.md                  <- /audience-research (고객 원문)
  competitors.md          <- /competitive-intel
  creative-kit.md         <- /creative 설정
  keyword-plan.md         <- /keyword-research
  stack.md                <- /start-here (도구, 키, MCP)
  preferences.md          <- 사용자가 정한 선호
  algo-cache.md           <- 어느 스킬이든 (기한이 있는 플랫폼 사실)
  assets.md               <- 덧붙이기만 (모든 스킬)
  learnings.md            <- 덧붙이기만 (/performance-review와 명시적 피드백)
  checks.md               <- 덧붙이기만, 사용자의 고침에서 온 예/아니오
  gold/<skill>/           <- 골드. 스킬이 쓴 것, 나간 것, 이유
  .history/               <- 프로필의 이전 복사본
```

**대행사, 여러 브랜드.**

```
./brands/
  active                  <- 슬러그 하나. 예시 "hanbit"
  hanbit/                 <- 한빛설비 (대구, 설비, 예시). ./brand/와 같은 배치
  buksan/                 <- 북산일정 (다지점 일정 소프트웨어, 예시)
```

**정하는 순서.** 모든 스킬, 모든 실행. `brand_context.py`의 dir 출력이 구현합니다.

1. brand 슬러그 인자이면 `./brands/<slug>/`
2. `./brands/active`가 가리키는 `./brands/<내용>/`
3. 없으면 `./brand/`

브랜드를 바꾸는 것은 `./brands/active`에 슬러그 하나를 쓰는 것입니다. 스킬은 `./brand/`를 하드코딩하지 않고 이 순서로 정합니다.

## brand.yaml, 매니페스트

디렉터리를 통째로 긁는 대신 오케스트레이터가 읽는 파일 하나. 프로필을 마지막으로 쓴 스킬이 주인입니다. **프로필을 쓰는 스킬은 같은 작업에서 맞는 `files:` 항목과 `updated:`를 고칩니다.**

키 이름은 영어 그대로입니다. 로더가 이 이름을 읽습니다. 아래 상호는 예시입니다. 전화번호는 지어 넣지 않습니다. 사이트에 있는 것만 적습니다.

```yaml
# ./brand/brand.yaml
brand:
  name: 한빛설비 (예시)
  slug: hanbit
  url: https://hanbit.example
  created: 2026-05-02
  updated: 2026-11-18
  # /start-here 첫 실행(라이트 또는 딥)이 쓰는 선택 사실.
  # brand_context.py가 이 brand: 블록 전체를 모든 스킬에 찍음
  category: 설비
  depth: lite
  phone: ""
  city: 대구
  service_area: [대구 수성구, 대구 달서구]
  services: [보일러, 누수, 배관]
  rating: "예시. 네이버 플레이스에서 본 별점과 리뷰 수를 그대로, 본 날짜와 함께"

files:
  voice-profile.md:  { updated: 2026-11-18, owner: brand-voice }
  positioning.md:    { updated: 2026-11-18, owner: positioning-angles }
  audience.md:       { updated: 2026-11-18, owner: audience-research }
  voc.md:            { updated: 2026-11-18, owner: audience-research }
  stack.md:          { updated: 2026-11-18, owner: start-here }
  preferences.md:    { updated: 2026-11-18, owner: start-here }

campaigns:
  - name: spring-check
    path: ./campaigns/spring-check/
    status: active        # planning | active | complete
    started: 2026-06-01
```

스키마는 이 폴더의 `schemas/brand-manifest.schema.json`입니다. 매니페스트가 없어도 오류가 아닙니다. `brand_context.py`는 신선도를 파일 수정 시각으로 돌리고, 스킬은 보통대로 진행합니다. /start-here가 첫 실행에 만듭니다.

## 강제. 프론트매터 reads / writes

"어느 스킬이 어느 파일을 읽나" 표는 없습니다. 계약은 각 스킬 프론트매터에 있고 로더가 실행합니다.

```yaml
metadata:
  boring:
    reads: [voice-profile, positioning#chosen-angle, voc, learnings]
    writes: [audience]
```

- 유효한 토큰. `voice-profile`, `positioning`, `audience`, `competitors`, `voc`, `creative-kit`, `keyword-plan`, `stack`, `assets`(덧붙이기만), `learnings`(덧붙이기만), `algo-cache`, `preferences`, `brand-manifest`(brand.yaml).
- `file#section`은 그 `##` 절만 불러 맥락을 얇게 유지합니다. 슬러그는 제목의 영문에서 만들어지므로, 하중 제목(Chosen Angle, Market Assessment, Pain Language, Voice Summary, Tone Spectrum, Watch baseline)은 영어 단어를 남깁니다.
- 브랜드 폴더나 `MARKETING.md`가 있을 때만, 한 줄로 맥락을 불러옵니다.

```
python3 ${CLAUDE_SKILL_DIR}/../start-here/scripts/brand_context.py --for <skill-name>
```

스크립트가 활성 브랜드 디렉터리를 정하고, 스킬의 `reads:`를 읽고, 앵커 절을 뽑아, 파일마다 신선도 표시가 있는 맥락 블록 하나를 냅니다.

- 스킬은 `writes:`에 있는 파일만 씁니다. `reads:` 밖을 읽는 것은 버그이고, `writes:` 밖을 쓰는 것은 더 나쁜 버그입니다. 고객 데이터는 이 브랜드 폴더 안에만 둡니다.

## 브랜드 기억 읽기

### 우아한 저하, 세 단계

1. **폴더도 파일도 있음.** 스크립트가 불러오고, 그것을 씁니다.
2. **폴더는 있는데 파일이 없음.** 오류가 아닙니다. 맥락 블록이 `absent`로 적습니다. 산출물에서 없는 파일을 늘어놓거나 알리지 않습니다. 빈칸이 일을 바꾸면 출처와 가정에 한 줄. 그 파일이 답했을 질문만 묻거나, 합리적인 기본으로 가고, 다음에 영향 큰 다음 하나("다음에 톤이 필요하면 /brand-voice").
3. **브랜드 폴더 자체가 없음.** 브랜드 불러오기를 통째로 건너뜁니다. 처음 사용자로 단독 진행하고 한 번 말합니다. "브랜드 프로필이 아직 없습니다. /start-here나 /brand-voice로 만들 수 있고, 없어도 진행합니다."

브랜드 파일이 없다고 스킬이 깨지지 않습니다. 맥락 0으로 첫날부터 되고, 쓸수록 좋아집니다. 빠른 모드는 여전히 이깁니다. 산출물 하나짜리는 설정 강의가 아니라 그 산출물입니다.

### 불러온 맥락은 조용히

일이 무엇이 빚었는지를 보여 줍니다. 어느 파일을 불러왔는지, "포지션을 사용합니다"를 알리지 않습니다. 오래됐거나 사용자가 지금 말하는 것과 싸우면 한 줄(파일, 나이, 고치는 스킬). 그 외 불러온 이야기는 산출물에 없습니다.

### 신선도

맥락 블록이 파일마다 나이를 표시합니다. brand.yaml `updated:`, 없으면 수정 시각.

| 나이 | 처리 |
|---|---|
| 30일 미만 | 그대로. 아무 말도 없음 |
| 30일에서 90일 | 그 파일이 일을 빚을 때만 한 줄. 오래됐을 수 있으니 이번 세션과 대조 |
| 90일 초과 | 고침을 권함. 믿기 전에 다시 돌릴 담당 스킬을 이름 붙임 |

파일 내용이 사용자가 지금 말하는 것과 싸우면 표시하고 묻습니다. 세션으로 브랜드 기억을 조용히 덮지 않고, 오래된 기억으로 세션을 조용히 덮지 않습니다.

## 브랜드 기억 쓰기

### 프로필. 자동 버전 다음 덮어쓰기

프로필(`voice-profile`, `positioning`, `audience`, `competitors`, `voc`, `creative-kit`, `keyword-plan`, `stack`, `algo-cache`)은 현재 상태입니다. 담당 스킬이 있는 파일의 새 버전을 만들면.

1. 현재 파일을 `./brand/.history/<file>.<YYYY-MM-DD>.md`로 복사합니다(같은 브랜드 디렉터리. 오늘 복사가 있으면 `-2`, `-3`).
2. 새 파일을 씁니다.
3. `brand.yaml`의 `files:` 항목을 고칩니다.
4. 바뀐 점을 3줄("대표 각도가 속도에서 단순함으로. 증거 2개 추가. 경쟁 명단은 같음.").

예/아니오 확인은 없습니다. 이력이 덮어쓰기를 되돌리게 하므로 취조는 없습니다. 스킬은 자기가 주인이 아닌 프로필을 쓰지 않습니다(`writes:`).

모든 프로필은 `## Last Updated`로 시작하고 날짜와 쓴 스킬을 담습니다. 사람이 읽게 둡니다. 마케터가 스킬을 돌리지 않고 편집기에서 어느 브랜드 파일이든 이해할 수 있어야 합니다.

### 취향 고리. checks.md와 gold/

사용자가 스킬의 일을 고치면, 그 스킬이 골드 케이스와 예/아니오 검사 하나에서 셋을 저장하고, 이후 그 스킬의 실행은 넘기기 전에 그 검사에 답합니다. 로더는 `preferences.md` 바로 뒤에, 실행 중인 스킬(그리고 `all`)에 달린 검사와 그 스킬의 최신 골드 세 개를 찍습니다. 전체 규칙은 이 폴더의 `taste-loop.md`. `learnings.md`는 데이터가 증명한 것, `checks.md`는 사장님이 원하는 것. 둘을 섞지 않습니다.

### 덧붙이기만. assets.md와 learnings.md

덮어쓰지 않고, 자르지 않고, 순서를 바꾸지 않습니다. 읽고, 해당 절 맨 아래에 붙입니다. 파일이 없으면 아래 템플릿으로 만든 뒤 붙입니다.

**assets.md.** 모든 스킬이 만든 산출마다 한 행.

```markdown
# Asset Registry

| Asset | Type | Created | Campaign | Status | Notes |
|---|---|---|---|---|---|
| welcome-sequence | 카카오·문자 5통 | 2026-06-04 | spring-check | draft | |
| MA-H2-B-9x16-v1.mp4 | 영상 광고 | 2026-06-09 | spring-check | live | matrix cell MA-H2-B |
```

상태는 `draft`로 시작하고, 사용자 또는 /performance-review가 `live` / `retired`로 옮깁니다. 광고 소재 이름은 광고 매트릭스 칸 ID입니다.

**learnings.md.** /performance-review(실제 데이터)와 명시적 사용자 피드백만 씁니다. 모든 생성기가 읽고, 맞는 사전을 적용합니다. 사전이 일을 바꿨으면 출처와 가정에 한 줄("4월 데이터에서 질문형 제목이 호기심형보다 나아서, 앞 제목은 질문입니다"). 아무것도 안 바꾼 사전은 말하지 않습니다. 한 줄 형식.

```markdown
- [2026-06-10] [email-sequences] subject-pattern=question outperformed curiosity 2.3x (n=4 sends, source: kit-api)
- [2026-06-08] [content-atomizer] instagram carousel > still for reach, 3.1x median (n=6 posts, source: export)
```

`[날짜] [스킬] 발견 (n=표본, source: 숫자가 온 곳)`. 구체적이고 행동 가능. "메일이 잘 됐다"가 아니라 패턴, 크기, 표본. 절은 `## What Works`, `## What Doesn't Work`, `## Audience Insights`(모르겠으면 기본), 그리고 `## PRIORS`(압축). 숫자는 출처가 있는 것만. 예시면 예시라고 적습니다. 통화는 원.

### 학습 압축

learnings.md가 약 50줄을 넘으면 /performance-review가 압축합니다.

1. **승격.** 반복 확인된 것을 맨 위 `## PRIORS`로. 한 줄, 뒷받침 날짜("이 명단에서는 증거형 제목이 질문형을 이김. 2026-03, 2026-05, 2026-06 확인").
2. **합침.** 중복은 가장 센 한 줄로(가장 큰 표본, 가장 최근).
3. **보관.** 오래됐거나 대체된 항목은 `./brand/.history/learnings.<YYYY-MM-DD>.md`로 옮깁니다. 지우지 않습니다.

생성기는 PRIORS를 먼저 읽고, 날것의 항목은 그 아래 증거입니다.

## voc.md, 고객의 말

/audience-research가 주인입니다. 출처가 있는 원문. /direct-response-copy, /positioning-angles, /lead-magnet, /email-sequences가 바꿔 쓰지 않고 인용합니다. 스키마는 이 폴더의 `schemas/voc.schema.json`.

```markdown
# Voice of Customer
## Last Updated: 2026-11-18 by /audience-research

## Pains
- "일요일 내내 제안서 썼는데 답도 없어요" · https://cafe.naver.com/example/1 (2026-05-22, 예시 문장)

## Desires
- "10분이면 보내는데 양식 티가 안 났으면" · https://hanbit.example/reviews (2026-04-30, 예시 문장)

## Objections
- "이런 도구 다 거기서 거기예요" · https://kin.naver.com/example (2026-05-12, 예시 문장)

## Vocabulary
- "비수기", "추가 공사", "단골": 공동체 말. 문안에 그대로
```

항목마다 원문, 소스 URL, 날짜. 지어낸 인용은 없습니다. 빈 절이 가짜보다 낫습니다. 위 세 문장은 형식 예시입니다.

## algo-cache.md, 기한이 있는 플랫폼 사실

알고리즘, 플랫폼 규격, 형식 가중처럼 상하는 사실의 브랜드별 캐시. 스킬이 박아 둔 지식 대신 고칩니다. 항목은 신선도 머리를 가집니다. `last-verified` 날짜, `ttl-days` 수, refresh 지시.

```markdown
# Algorithm & Platform Cache

## naver-blog-formats
last-verified: YYYY-MM-DD · ttl-days: 60 · refresh: 네이버 서치어드바이저와 "네이버 블로그 노출"을 이번 달로 검색해 형식별 가중을 고침
- 형식 가중은 확인한 뒤에만 적음. 영어 웹의 비율을 여기 옮기지 않음.
```

쓸 때 `last-verified` 더하기 `ttl-days`와 오늘을 비교합니다. 오래됐으면 지시대로 고치고, 항목을 갱신하고, 한 줄로 말합니다. "네이버 블로그 사실을 고쳤습니다. 캐시가 94일이었습니다." 상하는 사실은 SKILL.md 본문에 두지 않습니다.

## 캠페인

기간이 있는 프로젝트는 `./campaigns/<케밥-이름>/`와 `brief.md`(스키마 `campaign-brief.schema.json`). 브랜드 기억은 그것이 끌어 쓰는 지속 맥락입니다. 캠페인 산출을 만드는 스킬은 캠페인 디렉터리에 쓰고, assets.md에 행을 붙이고, brand.yaml `campaigns:`에 등록합니다.

## 조사 품질 신호

외부 데이터에 기대는 스킬(경쟁, 검색 결과, 검색량, 화제, 뉴스)은 조사 방식을 밝혀야 합니다. 사용자는 라이브인지 개념 분석인지 항상 압니다.

산출물마다 한 번, 평범한 말로, 끝의 출처와 가정에. 머리에도, 줄마다도 아닙니다.

- 라이브. "11월 18일에 소스 6개를 읽었습니다." 웹 검색, 스크랩, API.
- 모델 지식. "조사 도구가 없어서 일반 지식에 기댑니다. 돈을 쓰기 전에 확인하세요." 개념적이고 방향입니다.

`./brand/` 안 파일은 작업 기억이라 짧은 형태를 달 수 있습니다. `Data: LIVE (6 sources)` 또는 `Data: MODEL KNOWLEDGE`. 다음 스킬이 읽습니다.

규칙.

1. 항상 한 번 말합니다. 조용히 개념 데이터로 내려가지 않습니다.
2. 개념 데이터를 쓰면, 확인이 도움이 될 주장을 집습니다. "추정. 경쟁 X가 이 검색어에 있을 수 있습니다. 라이브 검색으로 확인."
3. 추정으로 가기 전에 묻습니다. "웹 검색이 연결되어 있지 않습니다. 개념 분석은 가능하고, 라이브가 더 정확합니다. 진행할까요, 검색을 먼저 켤까요?"
4. 사용자가 진행하면 조사에 달린 숫자 앞에 `~`를 답니다. `월 검색 약 2,400`이지, 확인 없이 `월 검색 2,400`이 아닙니다. 그림이면 예시. 통화는 원. 네이버 검색광고 키워드도구는 구간을 보여 주지 정확한 검색량이라고 단정하지 않습니다.

## 말투를 주입하는 방식

voice-profile.md가 불러와 있으면, 스킬 출력이 그 말투를 **보여 줍니다.** 인정만 하지 않습니다.

**틀림, 인정만.** "말투가 자신 있고 단호하군요. 포지션 각도입니다." 뒤에 평범한 출력.

**맞음, 보여 줌.** 알림이 없습니다. 머리가 시작이고, 그 말투로 씁니다. 프로필이 짧은 문장이면 짧은 문장, 브랜드 어휘, 금지 말은 어디에도 없음.

규칙.

1. 프로필이 "짧은 문장"이면 출력 자체가 짧은 문장입니다.
2. 브랜드가 피하는 말은 출력 어디에도 없습니다.
3. 말투 프로필을 불러왔다고 알리지 않습니다.
4. 문안만이 아니라 분석과 권고를 포함한 모든 내용 절에 적용됩니다. 사장님에게 나가는 문장은 합니다체나 해요체이고, 영어를 그대로 옮긴 문장은 쓰지 않습니다.

## 원칙

1. **사람이 먼저.** JSON이나 YAML 거울은, 마케터가 읽는 마크다운의 다음입니다.
2. **우아한 저하.** 맥락 0으로 되고, 맥락은 돕지 문을 잠그지 않습니다.
3. **조용한 사용.** 일이 빚은 것을 보여 주고, 무엇을 불러왔는지는 알리지 않습니다. 오래됐거나 싸우는 파일은 한 줄.
4. **덧붙이고, 부수지 않음.** 학습과 산출은 쌓입니다. 프로필은 덮기 전에 `.history/`로. 조용히 지우는 일은 없습니다.
5. **선언된 접근.** `reads:`와 `writes:`가 계약이고 로더가 지킵니다.
6. **스킬을 가로지르는 일관성.** /brand-voice가 쓴 말투를 다른 스킬이 지킵니다. 브랜드 기억이 공유된 참입니다.
7. **학습은 데이터에서.** /performance-review가 실제 숫자로 사전을 쓰고, 생성기는 맞는 사전을 적용하며, 일을 바꾼 사전만 적습니다. 명예 제도식 피드백 인터뷰는 없습니다.

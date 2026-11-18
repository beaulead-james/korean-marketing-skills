# 브랜드 메모리

브랜드 메모리는 모든 스킬이 사용자가 누구인지, 브랜드가 어떻게 말하는지, 누구에게 파는지, 무엇이 실제로 통했는지를 기억하는 방식이에요. 디스크에 쌓이고, 필요한 것만 불러요. 각 스킬이 프론트매터에 읽기와 쓰기를 선언하면 `brand_context.py`가 그것만 내보내요.

---

## 배치

### MARKETING.md: 상시 브리프

`./MARKETING.md`는 워크스페이스 루트에 있고 사용자가 써요. 목표, 제안, 제약, 우선순위, 하지 말 것. 모든 스킬이 먼저, 그대로 불러요. `/start-here`가 파운데이션 리포트로 초안을 제안할 수 있지만, 필수는 아니에요.

### preferences.md: 상시 선호

`./brand/preferences.md`는 사용자가 쓰는 상시 안내예요. 금지어, 거부하는 채널, 톤, 검토 규칙, 예산 한도. `/start-here`가 교정 패스와 "기억해 줘" 요청에서 쓰고, 모든 스킬이 읽어요. 뽑아 낸 `voice-profile.md`, 데이터로 쓰는 `learnings.md`와 다르고, 그 둘의 단일 작성자 규칙은 그대로예요.

**단일 브랜드 (기본):**

```
./brand/
  brand.yaml              <- 매니페스트 (아래 스펙)
  voice-profile.md        <- /brand-voice
  positioning.md          <- /positioning-angles
  audience.md             <- /audience-research
  voc.md                  <- /audience-research (고객 말 그대로)
  competitors.md          <- /competitive-intel
  creative-kit.md         <- /creative 설정
  keyword-plan.md         <- /keyword-research
  stack.md                <- /start-here (도구, 키 이름, MCP)
  preferences.md          <- 사용자가 쓰는 상시 선호
  algo-cache.md           <- 아무 스킬 (날짜 있는 플랫폼 사실, TTL)
  assets.md               <- append-only 대장 (모든 스킬)
  learnings.md            <- append-only 프라이어 (/performance-review + 명시적 사용자 피드백)
  checks.md               <- append-only. 사용자 수정에서 나온 예/아니오 점검 (아무 스킬)
  gold/<skill>/           <- 골드 케이스. 스킬이 쓴 것, 나간 것, 이유
  .history/               <- 프로필 파일의 자동 이전 사본
```

**대행사 / 멀티 브랜드:**

```
./brands/
  active                  <- 브랜드 슬러그 한 줄. 예: hanbit
  hanbit/                 <- 브랜드 디렉터리. ./brand/ 와 같은 배치
  buksan/
```

**해석 순서** (모든 스킬, 모든 실행. `brand_context.py --dir`이 구현):

1. 명시적 `--brand <slug>` 인자면 `./brands/<slug>/`
2. `./brands/active` 포인터가 있으면 `./brands/<내용>/`
3. 없으면 `./brand/`

브랜드를 바꾸는 일은 `./brands/active`에 슬러그 하나를 쓰는 것이에요. 스킬은 `./brand/` 경로를 하드코딩하지 않아요. 이 순서로 풀어요.

---

## brand.yaml: 매니페스트

오케스트레이터가 디렉터리를 훑지 않고 읽는 파일 하나예요. 프로필 파일을 마지막으로 쓴 스킬이 소유해요. **프로필 파일을 쓰는 스킬은 같은 작업에서 `files:` 항목과 `updated:`를 갱신해요.**

```yaml
# ./brand/brand.yaml
brand:
  name: 한빛설비 (예시)
  slug: hanbit
  url: https://example.co.kr
  created: 2026-05-02
  updated: 2026-11-18
  # 선택 사업 사실. /start-here 첫 실행 (lite 또는 deep)이 씀.
  # brand_context.py는 모든 스킬에 brand: 블록 전체를 출력
  category: 설비
  depth: lite
  phone: 053-000-0000
  city: 대구
  service_area: [중구, 수성구, 달서구]
  services: [온수기, 누수, 배관]
  rating: "예시. 플레이스 별점은 화면에서 본 날짜와 함께 적어요"

files:
  voice-profile.md:  { updated: 2026-06-08, owner: brand-voice }
  positioning.md:    { updated: 2026-06-10, owner: positioning-angles }
  audience.md:       { updated: 2026-05-14, owner: audience-research }
  voc.md:            { updated: 2026-05-14, owner: audience-research }
  stack.md:          { updated: 2026-05-02, owner: start-here }
  preferences.md:    { updated: 2026-11-18, owner: start-here }

campaigns:
  - name: spring-launch
    path: ./campaigns/spring-launch/
    status: active        # planning | active | complete
    started: 2026-06-01
```

스키마: 이 폴더의 `schemas/brand-manifest.schema.json`. 매니페스트가 없어도 에러가 아니에요. `brand_context.py`는 신선도를 파일 mtime으로 대체하고, 스킬은 그대로 진행해요. /start-here가 첫 실행에 만들어요.

위 전화번호와 URL은 예시예요. 실제 번호, 계정, 고객 이름을 라이브러리에 적지 마세요.

---

## 강제: 프론트매터 `reads` / `writes`

"어느 스킬이 어느 파일을 읽나"를 산문으로 늘어놓던 표는 없어요. 계약은 각 스킬 프론트매터에 있고, 로더가 실행해요.

```yaml
metadata:
  boring:
    reads: [voice-profile, positioning#chosen-angle, voc, learnings]
    writes: [audience]
```

- 유효 토큰: `voice-profile`, `positioning`, `audience`, `competitors`, `voc`, `creative-kit`, `keyword-plan`, `stack`, `assets` (append-only), `learnings` (append-only), `algo-cache`, `preferences`, `brand-manifest` (= brand.yaml).
- `file#section` 앵커는 그 `##` 섹션만 불러요. 부분 읽기가 컨텍스트를 얇게 유지해요.
- 스킬은 브랜드 폴더나 `MARKETING.md`가 있을 때만 한 줄로 컨텍스트를 불러요. `python3 ${CLAUDE_SKILL_DIR}/../start-here/scripts/brand_context.py --for <skill-name>`
  스크립트는 활성 브랜드 디렉터리를 풀고, 스킬의 `reads:`를 읽고, 앵커 섹션을 뽑고, 파일별 신선도 플래그가 있는 컨텍스트 블록 하나를 내보내요.
- 스킬은 `writes:`에 있는 파일만 써요. `reads:` 밖을 읽는 것은 버그이고, `writes:` 밖을 쓰는 것은 더 나쁜 버그예요.

---

## 브랜드 메모리 읽기

### 없을 때의 세 단계

1. **브랜드 디렉터리도 있고 파일도 있다** → 스크립트가 불러오고, 그것을 써요.
2. **디렉터리는 있는데 파일이 없다** → 에러가 아니에요. 컨텍스트 블록이 `absent`로 적어요. 산출물에서 빠진 파일을 늘어놓지 마세요. 공백이 작업을 바꾸면 출처와 가정 노트에 한 줄. 그 파일이 답했을 질문만 묻거나, 합리적인 기본으로 진행하고, 다음에 하나만 제안해요 ("다음번에 톤이 필요하면 /brand-voice를 돌리면 돼요").
3. **브랜드 디렉터리가 없다** → 브랜드 로딩을 통째로 건너뛰어요. 처음 사용자처럼 단독으로 진행하고 한 번만 말해요. "브랜드 프로필이 아직 없어요. /start-here나 /brand-voice로 만들 수 있고, 없어도 작업은 해요."

브랜드 파일이 없다고 스킬이 깨지면 안 돼요. 시스템은 컨텍스트 0으로 첫날부터 동작하고, 쓸수록 나아져요. 퀵 모드는 여전히 이겨요. 에셋 하나를 콕 집어 요청하면 그 에셋을 주고, 설정 강의는 하지 마세요.

### 불러온 컨텍스트는 조용히

작업이 무엇이 그것을 만들었는지 보여요. 어떤 파일을 불러왔는지, "포지셔닝을 사용합니다"를 선언하지 마세요. 낡은 데이터는 잡아요. 파일이 오래됐거나 사용자가 지금 말하는 것과 충돌하면 한 줄 (파일, 나이, 새로 고칠 스킬). 그 외 로딩 이야기는 산출물 밖에 둬요.

### 신선도 플래그

컨텍스트 블록은 파일 나이로 표시해요. brand.yaml `updated:` 시각, 없으면 mtime.

| 나이 | 처리 |
|-----|-----------|
| 30일 미만 | 그대로 불러오고, 말하지 않아요 |
| 30일에서 90일 | 그 파일이 작업을 만들 때만 한 줄. 낡았을 수 있으니 이번 세션과 대조 |
| 90일 초과 | 새로 고침을 권해요. 의지하기 전에 다시 돌릴 소유 스킬의 이름 |

파일 내용이 사용자가 지금 말하는 것과 충돌하면 표시하고 물어요. 세션 맥락으로 브랜드 메모리를 조용히 덮지 말고, 오래된 메모리로 세션을 조용히 덮지 마세요.

---

## 브랜드 메모리 쓰기

### 프로필 파일: 자동 버전, 그다음 덮어쓰기

프로필 파일 (`voice-profile`, `positioning`, `audience`, `competitors`, `voc`, `creative-kit`, `keyword-plan`, `stack`, `algo-cache`)은 현재 상태예요. 소유 스킬이 기존 파일의 새 버전을 만들면:

1. 현재 파일을 `./brand/.history/<file>.<YYYY-MM-DD>.md`로 복사해요 (같은 브랜드 디렉터리. 오늘 사본이 있으면 `-2`, `-3`).
2. 새 파일을 써요.
3. `brand.yaml`의 `files:` 항목을 갱신해요.
4. 무엇이 바뀌었는지 3줄로 보여요 ("대표 각도가 속도에서 단순함으로 옮겨졌어요. 증거 2개를 더했어요. 경쟁 목록은 그대로예요.").

예/아니오 확인은 없어요. 이력이 덮어쓰기를 되돌리게 하므로 심문 의식은 없어요. 스킬은 소유하지 않은 프로필 파일을 쓰지 않아요 (`writes:`).

모든 프로필 파일은 `## Last Updated` 줄로 시작해요. 날짜와 쓴 스킬. 사람이 읽게 유지해요. 마케터가 스킬을 돌리지 않고 텍스트 편집기에서 브랜드 파일을 이해할 수 있어야 해요.

### 취향 루프: checks.md와 gold/

사용자가 스킬의 작업을 고치면, 그 스킬은 골드 케이스와 예/아니오 점검 1개에서 3개를 저장해요. 이후 그 스킬의 모든 실행은 작업을 넘기기 전에 그 점검에 답해요. 로더는 실행 중인 스킬 (그리고 `all`)에 태그된 점검과 최신 골드 케이스 셋을 `preferences.md` 다음에 출력해요. 전문은 이 폴더의 `taste-loop.md`. `learnings.md`는 데이터가 증명한 것, `checks.md`는 오너가 원하는 것. 둘을 섞지 마세요.

### append-only: assets.md와 learnings.md

덮어쓰지 마세요. 자르지 마세요. 순서를 바꾸지 마세요. 읽고, 해당 섹션 맨 아래에 붙여요. 파일이 없으면 아래 템플릿으로 만든 다음 붙여요.

**assets.md**: 모든 스킬이 만든 에셋마다 한 행을 붙여요.

```markdown
# Asset Registry

| Asset | Type | Created | Campaign | Status | Notes |
|-------|------|---------|----------|--------|-------|
| welcome-sequence | 알림톡·문자·이메일 (5통) | 2026-06-04 | spring-launch | draft | |
| MA-H2-B-9x16-v1.mp4 | 영상 광고 | 2026-06-09 | spring-launch | live | matrix cell MA-H2-B |
```

상태는 `draft`로 시작해요. 사용자 또는 /performance-review가 `live` / `retired`로 옮겨요. 광고 크리에이티브 이름은 광고 매트릭스 셀 id예요.

**learnings.md**: /performance-review (실제 데이터)와 명시적 사용자 피드백만 써요. 모든 생성 스킬이 읽고, 맞는 프라이어를 적용해요. 프라이어가 작업을 바꿨으면 출처와 가정 노트에 한 줄 ("4월 데이터에서 질문형 제목이 호기심형보다 낮아서, 대표 제목은 질문형으로 했어요"). 아무것도 바꾸지 않은 프라이어는 언급하지 마세요. 한 줄 형식:

```markdown
- [2026-06-10] [email-sequences] subject-pattern=question outperformed curiosity 2.3x (n=4 sends, source: kit-api)
- [2026-06-08] [content-atomizer] linkedin carousel > text post for reach, 3.1x median (n=6 posts, source: linkedin-csv)
```

위 배율은 형식 예시예요. 실제 사업의 숫자처럼 옮기지 마세요.

`[날짜] [스킬] 발견 (n=표본, source: 숫자가 온 곳)`. 구체적이고 실행 가능해야 해요. "이메일이 잘 됐다"가 아니라 패턴, 크기, 표본. 섹션: `## What Works`, `## What Doesn't Work`, `## Audience Insights` (모르겠으면 여기), 그리고 `## PRIORS` (압축 참고).

### Learnings 압축

learnings.md가 약 50항목을 넘으면 /performance-review가 압축해요.

1. **승격.** 반복 확인된 durable 발견을 맨 위 `## PRIORS`로. 한 줄, 뒷받침 날짜 ("이 리스트에서는 증거형 제목이 질문형보다 나았어요. 확인 2026-03, 2026-05, 2026-06").
2. **병합.** 중복이나 거의 같은 항목을 가장 강한 하나 (표본이 크고 최근인 것)로.
3. **보관.** 낡거나 대체된 항목은 `./brand/.history/learnings.<YYYY-MM-DD>.md`로 옮겨요. 지우지 마세요.

생성 스킬은 PRIORS를 먼저 읽어요. 원문 항목은 그 아래 증거 자취예요.

---

## voc.md: 고객의 말

/audience-research가 소유해요. 출처가 있는 고객 말 그대로. /direct-response-copy, /positioning-angles, /lead-magnet, /email-sequences가 인용하고, 바꾸어 말하지 않아요. 스키마: 이 폴더의 `schemas/voc.schema.json`.

```markdown
# Voice of Customer
## Last Updated: 2026-11-18 by /audience-research

## Pains
- "일요일 하루를 견적 쓰는데 답도 없어요" · 예시. 실제 URL은 그 글을 읽은 뒤에만

## Desires
- "10분이면 보내고, 템플릿 티가 안 났으면 해요" · 예시

## Objections
- "이런 키트는 다 똑같은 문서 복사예요" · 예시

## Vocabulary
- "비수기", "단골", "콜 놓침": 커뮤니티가 쓰는 말. 카피에서 그대로
```

항목마다 인용 원문, 출처 URL, 날짜. 지어낸 인용은 없어요. 빈 섹션이 가짜 섹션보다 나아요. 네이버 영수증 리뷰, 카페, 지식iN, 블로그 댓글, 통화 메모가 한국 소스예요. 영어권 리뷰 사이트를 기본 광산으로 두지 마세요.

---

## algo-cache.md: 날짜 있는 플랫폼 사실

스킬이 본문에 박아 두지 않고 새로 고치는, 수명 짧은 사실 (알고리즘, 플랫폼 스펙, 형식 가중치)의 브랜드별 캐시. 항목은 신선도 헤더를 가져요 (`last-verified` 날짜, `ttl-days` 숫자, refresh 지시).

```markdown
# Algorithm & Platform Cache

## naver-place
last-verified: YYYY-MM-DD · ttl-days: 90 · refresh: 네이버 스마트플레이스 도움말과 플레이스 광고 안내를 검색
- 업종 검색, 리뷰, 예약, 스마트콜이 로컬의 기본 표면이에요. 구글 프로필은 보조.
```

쓸 때 `last-verified` + `ttl-days`와 오늘을 비교해요. 낡았으면 적힌 지시로 새로 고치고 항목을 갱신한 뒤 한 줄. "네이버 플레이스 사실을 새로 고쳤어요 (캐시가 94일이었어요)." 수명 짧은 사실은 SKILL.md 본문에 두지 마세요.

---

## 캠페인 (브랜드 메모리는 아니지만, 그것이 참조)

기간이 있는 프로젝트는 `./campaigns/<kebab-name>/`와 `brief.md` (스키마 `campaign-brief.schema.json`). 브랜드 메모리는 그 프로젝트가 끌어 쓰는 지속 컨텍스트예요. 캠페인 에셋을 만드는 스킬은 캠페인 디렉터리에 쓰고, assets.md에 행을 붙이고, brand.yaml `campaigns:`에 등록해요.

---

## 리서치 품질 신호

외부 데이터에 기대는 스킬 (경쟁 분석, 검색 결과, 키워드 검색량, 화제, 뉴스)은 리서치 모드를 밝혀야 해요. 사용자는 라이브 데이터인지 개념 분석인지 항상 알아야 해요.

산출물마다 한 번, 평범한 말로, 끝의 출처와 가정 노트에 선언해요. 헤더에 두지 말고, 줄마다 달지 마세요.

- 라이브: "11월 13일에 출처 6개를 읽었어요." 웹 검색, 스크랩, API를 썼어요.
- 모델 지식: "리서치 도구가 없어서 일반 지식에 기대요. 돈을 쓰기 전에 확인하세요." 분석은 개념적이고 방향이에요.

`./brand/` 안 파일은 작업 메모리라서 다음 스킬을 위해 짧은 형태 (`Data: LIVE (6 sources)` 또는 `Data: MODEL KNOWLEDGE`)를 쓸 수 있어요.

규칙:

1. 항상 한 번 말해요. 개념 데이터로 조용히 떨어지지 마세요.
2. 개념 데이터를 쓸 때, 확인이 필요한 주장을 짚어요. "추정: 경쟁 A가 이 검색어에 올라 있을 수 있어요 (라이브 검색으로 확인)."
3. 추정으로 진행하기 전에 물어요. "웹 검색이 연결되지 않았어요. 개념 분석은 드릴 수 있고, 라이브가 더 정확해요. 진행할까요, 웹 검색을 먼저 둘까요?"
4. 사용자가 진행하면 리서치에 의존하는 숫자에 `~`를 붙여요. `월 검색 ~2,400`이지, 확정된 `월 검색 2,400`이 아니에요. 네이버 키워드도구의 값은 구간이에요. 정확한 월간 검색수처럼 쓰지 마세요. 통화는 원이에요.

---

## 보이스 주입

voice-profile.md가 불러와지면, 스킬 출력은 브랜드 보이스를 **보여 줘요.** 인정만 하고 끝나지 않아요.

**틀린 예, 보이스를 언급만:** "브랜드 보이스가 자신 있고 단정하네요. 포지셔닝 각도는 여기 있습니다." 뒤에 평범한 문장.

**맞는 예, 보이스를 실행:** 선언이 없어요. 출력은 헤더에서 시작하고, 그 보이스로 쓰여요. 프로필이 짧은 문장이면 짧은 문장, 브랜드 어휘가 깔리고, 금지어는 어디에도 없어요.

규칙:

1. 프로필이 "짧은 문장"이면 출력 자체가 짧은 문장이에요.
2. 브랜드가 피하는 단어는 출력 어디에도 없어요.
3. 보이스 프로필을 불러왔다고 알리지 마세요.
4. 카피뿐 아니라 분석과 추천을 포함한 모든 내용 섹션에 적용해요.

---

## 원칙

1. **사람이 먼저 읽어요.** JSON이나 YAML 거울은, 마케터가 읽는 마크다운의 다음이에요.
2. **없어도 동작해요.** 컨텍스트 0으로 일하고, 컨텍스트는 강화하지 관문이 아니에요.
3. **조용한 사용.** 작업이 무엇이 그것을 만들었는지 보여요. 불러온 파일을 선언하지 마세요. 낡거나 충돌하는 파일만 한 줄.
4. **덧붙이고, 부수지 마세요.** learnings와 assets는 쌓여요. 프로필 파일은 덮어쓰기 전에 `.history/`로 버전해요. 아무것도 조용히 지워지지 않아요.
5. **선언된 접근.** `reads:` / `writes:` 프론트매터가 계약이고, 로더가 강제해요.
6. **스킬 사이 일관.** /brand-voice가 쓴 보이스를 다른 모든 스킬이 지켜요. 브랜드 메모리가 공유된 진실이에요.
7. **Learnings는 데이터에서.** /performance-review가 실제 숫자로 프라이어를 써요. 생성 스킬은 맞는 프라이어를 적용하고, 작업을 바꾼 프라이어만 언급해요. 명예 시스템 피드백 인터뷰는 없어요.

# 크리에이티브 시각 판단

이미지를 "만든다"와 "그 자리에서 작동한다" 사이의 층입니다. 시각 심리, 범용 AI 룩을 피하는 법, 스타일 어휘, 자리 전략, 프롬프트 구성, 여러 장 일관성입니다.

```
last-verified: 2026-11-18
ttl-days: 90
refresh: 아래 영어권 참여율 숫자를 사장님에게 인용하기 전에, 그 플랫폼의 최신 형식별 벤치마크를 검색합니다. 네이버, 카카오, 한국 인스타·쇼츠 수치로 옮기지 않습니다. 한국 자리의 비율과 안전 영역은 각 공식 가이드를 확인합니다.
changes: 2026-09-02에 인스타와 링크드인 형식 벤치마크를 Socialinsider 2026년 2분기에 다시 묶었습니다. 인스타는 모든 형식이 전년 대비 하락. 링크드인은 여러 장이 문서를 앞섰고, 투표는 올랐고, 링크가 바닥이었습니다. 유튜브 얼굴 통계는 vidIQ의 2026년 썸네일 500장 연구. 65%와 45% 유지율은 페이스북 2016년 출처. 틱톡 음소거와 릴스 트렌드 오디오는 범위를 다시 잡았습니다. 핀터레스트 스펙은 그 스펙 페이지와 맞췄습니다. 2026-11-18 본문을 한국어로 옮기고, 그 숫자는 영어권 관찰로 가두었습니다. 한국 기본 자리는 메타 피드 1:1·4:5·9:16, 유튜브 쇼츠, 네이버 플레이스 소식 이미지, 카카오입니다.
```

**날짜가 있는 사실.** 이 파일의 원칙은 오래 갑니다. 숫자는 아닙니다. 아래 참여율, 형식 순위, 플랫폼 통계는 2025~2026 주기의 영어권 닻입니다(2026-09-02에 2026년 2분기 보고서에 다시 묶음). 판단을 보정하는 데 쓰고, 새로고침 없이 현재 벤치마크라고 인용하지 않습니다. 한국 네이버·카카오·국내 인스타의 사실이 아닙니다. 모델 ID와 페이로드는 `MODEL_REGISTRY.md`에만 있습니다. 이 파일은 역할로 모델을 부릅니다.

---

## 목차

1. 사람이 멈추는 이유
2. 반응을 부르는 시각 원칙
3. 범용 AI 미학을 피하는 원칙
4. 안티 슬롭. QA가 쓰는 부분
5. 스타일 어휘
6. 참고할 브랜드 비주얼
7. 자리별 전략
8. 기본 이미지 모델의 프롬프트
9. 이미지 안 글자와 타이포
10. 여러 장의 브랜드 일관성
11. 프롬프트 템플릿
12. 품질 체크

---

## 1부. 사람이 멈추는 이유

### 눈이 가는 순서

뇌는 시각을 예측 가능한 순서로 처리합니다. 피드에서 멈추는 이미지와 녹아 버리는 이미지의 차이입니다.

1. **얼굴.** 가장 먼저. 신경이 그렇게 배선돼 있습니다.
2. **움직임, 또는 움직임처럼 보이는 것.**
3. **대비가 큰 요소.**
4. **예상 밖, 새로운 것.** 패턴을 끊습니다.
5. **글자.** 마지막. 의식적 처리가 필요합니다.

### 얼굴

사람은 다른 무엇보다 얼굴을 먼저 알아챕니다. 표정을 보면 거울 뉴런이 그 느낌을 따라갑니다.

잘 쓰는 법. 과장된 표정이 미세한 표정보다 잘 멈춥니다(놀람, 신남, 호기심). 시선은 CTA를 보면 보는 사람의 주의가 그쪽으로 갑니다. 감정에는 클로즈업이 전신보다 낫습니다. 비대칭 각도가 정면보다 흥미롭습니다.

피할 것. 범용 스톡 미소. 콘텐츠의 감정에 맞는 구체적 표정을 씁니다.

### 처음 3초

영어권에서 자주 인용되는 닻입니다. 페이스북이 2016년에 공개한 영상 데이터에서, 처음 3초를 본 사람의 65%가 10초까지 가고 45%가 30초에 닿습니다. 10년이 지나도 가장 많이 인용되고, 플랫폼이 더 새로운 같은 숫자를 내지 않았습니다. 모양(초반에 급락, 그다음 긴 꼬리)은 버티고, 정확한 퍼센트는 오래된 것입니다. 한국 쇼츠의 유지율로 쓰지 않습니다. 첫인상은 의식 전, 약 50밀리초에 생긴다는 연구가 있습니다. 역시 한국 광고 성과 숫자가 아닙니다.

함의. 의식적 처리가 시작되기 전에 가치, 호기심, 감정 중 하나가 전달돼야 합니다.

### 스크롤을 멈추는 패턴 중단

뇌는 예상한 패턴을 걸러 냅니다. 멈추려면 혼란 없는 새로움이 필요합니다.

되는 것. 의도된 색 충돌(무작위가 아님). 크기 위반(아주 작은 사람, 거대한 물건). 시간 불일치(레트로와 미래가 한 프레임). 맥락 이탈(있을 수 없는 장소의 제품). 한 프레임의 반대.

예시. 이끼 초록 질감 위의 금속 별표. 디지털과 유기물이 한 화면이라 주의가 갑니다. 글로벌 제품 브랜드의 참고이지, 설비 사장님의 기본 룩이 아닙니다.

### 각성이 높은 감정이 공유를 부릅니다

중립보다, 각성이 높은 감정(긍정과 부정 모두)이 더 공유된다는 것은 심리학의 오래된 관찰입니다. 한국 공유율을 숫자로 지어내지 않습니다.

각성이 높음. 경외, 설렘, 분노(조심), 놀람, 기쁨.
각성이 낮음. 만족, 슬픔, 차분.

시각으로. 경외는 거대한 스케일과 드라마틱한 빛. 설렘은 움직임, 선명한 색, 동적 구도. 놀람은 예상 밖 병치.

지역 사업의 기본은 각성보다 분명함입니다. 한 장에 하는 일, 지역, 결과가 보이면 경외 연출보다 먼저입니다.

---

## 2부. 반응을 부르는 시각 원칙

오래된 광고 시험이 아직 맞는 것.

**이미지는 힘.** 즉각적인 감정. 의식 전에 작동. 욕망을 만들고 정당화를 만들지 않습니다.
**문안은 정밀.** 구체적 주장. 반론을 넘음. 감정 결정에 이성의 뼈대를 줍니다.

이미지가 끌고, 문안이 간격을 닫습니다. 광고 문안은 이미지 안이 아니라 HTML이 기본입니다.

아직 맞는 규칙.

1. **끝난 결과가 과정을 이깁니다.** 일을 보여 주지 말고 결과를 보여 줍니다. 맛있는 한 끼가 재료보다 낫고, 고친 뒤가 고치기 전보다 낫습니다. 전후는 둘 다 필요할 때만, 같은 각도와 빛으로.
2. **구체가 범용을 이깁니다.** "대구의 40대 설비 사장님"이 "사업가"보다 자기를 알아보게 합니다. 실명은 예시로만, 실제 고객 이름을 지어내지 않습니다.
3. **보는 순서를 따릅니다.** 그림, 헤드라인, 본문. 위계가 이 순서와 맞아야 합니다.
4. **광택보다 진짜.** 무균 스튜디오보다 실제 맥락. 라이프 이미지가 심리적 거리를 줄입니다. 손님이 찍은 듯한 결이 프로 촬영을 이기는 자리가 있습니다. 쇼츠와 네이티브가 그 자리입니다.

전환 위계.

```
1. 주 초점 (훅)
2. 받치는 맥락 (왜 신경 쓰나)
3. 다음 행동 (전화, 카카오, 예약)
```

선택이 늘면 결정이 느려집니다. 지배적인 시각 요소 하나, 메시지 하나, 다음 행동 하나.

삼분할. 프레임을 3×3으로 나누고 핵심을 교차점에 둡니다. 정중앙은 정적이고 아마추어로 읽히기 쉽습니다. 히어로 대칭을 의도할 때만 중앙입니다.

---

## 3부. 범용 AI 미학

AI 슬롭은 많은 양, 적은 노력, 통계적 평균입니다. 기억에 남지 않습니다.

왜 생기나. 모델은 "가장 그럴듯한" 출력을 예측하도록 학습됩니다. 구체적 지시가 없으면 학습 데이터의 평균으로 갑니다. 범용 프롬프트는 범용 결과입니다. "패션을 입은 아름다운 여성"은 유럽 중심 기본, 상투적 포즈, 무균 구도로 갑니다.

보이는 표식. 완벽한 중앙 구도. 방향 없는 균일 조명. 지나치게 매끈한 피부. 모든 것의 대칭. 너무 완벽한 만화 미학. 어색한 손. 깨진 글자. 반복되는 배경. 부자연스러운 반사.

미학 표식. 전략 없는 높은 채도. 아무 데도 안 가는 그라데이션. 범용 "기술 파랑". 스톡 포즈. 노을 위 명언.

벗어나는 틀.

**1. 전략적 구체.** 시각을 이름 붙입니다. 하루의 정확한 시간, 예술 사조나 참조, hex나 이름이 있는 팔레트, 닻 요소 하나나 둘, 구체적인 감정.

약한 문장. "전문적으로 보이는 사무실"
강한 문장. "오후 늦게 베네치안 블라인드 사이로 골든아워가 들어오는 작업실, 닳은 마호가니 책상 위의 줄무늬 그림자, Muted earth tones, medium format film"

**2. 제약이 도구.** "No typical poses", "Avoid centered composition", "Non-uniform lighting only", "Imperfect textures".

**3. 여러 차원의 스타일.** 키워드 하나에 기대지 않습니다.

```
조명 (방향, 질, 색온도)
팔레트 (구체적 팔레트)
구도 (규칙, 프레이밍, 깊이)
예술 참조 (사조, 작가, 시대)
기술 (카메라, 필름, 현상)
질감 (재질, 흠)
감정 (구체적인 무드)
```

예시. 역광과 림, 깊은 그림자. 채도 낮은 녹슨 주황과 슬레이트 블루. 더치 앵글, 타이트 크롭. 환경 인물. 하셀블라드, 얕은 심도. 필름 그레인, 자연 피부. 조용한 긴장.

**4. 반복.** 생성, 비판, 다듬기. 범용 패턴에 빠졌나. 가장 독특한 요소는 뭔가. 무시할 수 없게 하려면. 의도인가 사고인가.

---

## 4부. 안티 슬롭

QA 루브릭이 이 부를 씁니다. AI로 만든 티가 피드의 소음이 된 뒤, 사람은 그것을 알아보고 넘깁니다. 이 패턴을 피하는 것이 경쟁 조건입니다.

**1. 과한 채도.** 모델은 현실보다 채도를 밀어 "사탕"처럼 만듭니다. 고침. 채도를 낮추는 말을 넣고, 범용 색 이름 대신 죽은 색을 씁니다. "vibrant red" 대신 "muted terracotta" 또는 "burgundy". "bright blue" 대신 "slate blue" 또는 "dusty navy". "desaturated color palette", "natural color grading", "muted tones".

**2. 플라스틱 피부.** 모공과 결이 사라집니다. "natural skin texture", "visible pores", "realistic skin". "shot on film" 또는 "film grain". 주근깨, 웃는 주름, 햇볕에 그을린 피부처럼 흠을 지정합니다.

**3. 너무 완벽한 대칭.** 현실은 완전 대칭이 아닙니다. "asymmetrical composition", "off-center subject", "slightly turned head", "casual posture", "weight on one foot". "portrait"보다 "candid moment".

**4. AI 글로우.** 모든 방향에서 고르게 밝고 실제 광원이 없습니다. "single light source from upper left", "deep shadows", "chiaroscuro", "motivated lighting", "overcast daylight", "window light from the right". "well-lit", "bright lighting"은 평면 AI 빛을 부릅니다.

**5. 스톡 구도.** 카메라에 미소 지으며 엄지를 드는 사람, 회의실의 다양한 전문가. 서사를 말합니다. "team in meeting" 대신 "founder sketching on a whiteboard at 2am, coffee cups scattered, laptop glow on face". 지역이면 "technician kneeling at a water heater, phone flash off, late afternoon window".

**6. 불가능한 배경, 물건 수프.** 배경이 흐린 형태로 녹거나 논리가 없습니다. 전경만큼 배경을 말합니다. "on surface"가 아니라 "on weathered concrete". "urban background"가 아니라 "brick wall with peeling paint".

**7. AI 아트 스테이션.** 컨셉 아트, CGI, 일러스트가 섞인 과한 광택. 하이라이트, 블룸, 파티클이 너무 많습니다. 실제 사진 참조로 땅에 붙입니다. "shot on Fujifilm X-T5", "35mm film photography", "minimal post-processing", "straight out of camera". "ultra-detailed", "hyper-realistic", "8K"는 과처리로 밉니다. 대신 "professional photography", "editorial quality", "commercial photography".

진짜에 가까운 쪽. 필름 그레인, 자연 질감, 보이는 마모, 캔디드. 인공에 가까운 쪽. HDR, 플라스틱, 스톡 포즈, 완벽한 대칭, 판타지 블룸. 피드는 오른쪽이 넘치므로 왼쪽이 구분됩니다. 쇼핑몰 대표 이미지는 예외로 깨끗하고 정확해야 합니다. 그것도 글로우가 아니라 통제된 스튜디오 빛입니다.

어떤 프롬프트에든 2~3개.

```
natural color grading, not over-saturated
realistic lighting with visible shadows
shot on [카메라], [렌즈]
natural skin texture
slight film grain
asymmetrical composition
candid, not posed
environmental context, not studio
minimal post-processing
```

---

## 5부. 스타일 어휘

2025~2026 주기에 상업 이미지에서 보인 방향입니다. 방향은 통계보다 천천히 낡습니다. 업종 선두가 지금 내는 것을 보고 한 층에 기대기 전에 확인합니다. 사장님 기본 룩이 아닙니다. 브리프가 요구할 때의 어휘입니다.

**1. 크롬과 금속.** 반사 금속, 액체 금속. 프리미엄, 기술, 미래. 럭셔리와 기술 제품. 키워드. chrome, liquid metal, mercury-like, polished chrome, brushed aluminum, iridescent metal. 조명을 정확히 말하고, 반사될 배경을 넣고, 어둡거나 미니멀한 배경이 잘 됩니다.

**2. 유기·생체.** 자연에서 온 형태, 이끼, 산호, 불완전한 성장. 진정, 따뜻함. 웰니스와 기술을 사람답게. 유기와 기술의 긴장이 주의를 끕니다.

**3. 초현실.** 꿈의 논리, 크기 위반. 창의, 대담, 기억. 패션과 위험을 감수하는 브랜드. surreal, impossible scene, floating objects, Magritte-inspired. 거대 가방이 거리로 들어오는 식의 캠페인은 그 브랜드의 참고입니다.

**4. 3D 포토리얼.** 사진과 구분되지 않는 제품 시각화. 정밀, 품질, 신뢰. 쇼핑몰과 카탈로그. photorealistic 3D render, studio lighting, physically accurate materials, realistic reflections. 재질과 빛이 환경과 맞아야 하고, 현실감을 위해 표면 흠을 넣습니다. 실제 제품 사진이 있으면 이 층으로 제품을 다시 만들지 않습니다. 수정합니다.

**5. 추상·뉴럴.** 데이터, 네트워크, 빛나는 경로. 지능, 혁신. 기술과 데이터 제품. neural network visualization, bioluminescent, computational aesthetic.

**6. 레트로퓨처.** 1980년대와 미래. 노스탤지어와 혁신. 게임, 엔터. synthwave, neon grid, vaporwave, outrun aesthetic.

**7. 미니멀 프리미엄.** 극도의 절제, 여백, 타이포. 세련, 자신, 럭셔리. minimal composition, negative space, single accent, Swiss design. 한 색의 낮은 채도와 숨 쉴 공간이 자신감입니다.

**8. 촉감과 재료.** 천, 점토, 도자, 콘크리트, 나무결. 디지털이 물리적으로 느껴지게. 공예, 품질, 만질 수 있음. tactile texture, raw ceramic, linen, aged patina, wabi-sabi, material honesty. AI 슬롭의 반대 경향입니다. 지역 매장과 설비, 음식에 자주 맞습니다.

---

## 6부. 참고할 브랜드 비주얼

글로벌 제품 브랜드입니다. 베끼지 않습니다. 왜 구분되는지 보고, 사장님 키트에 필요한 한 가지만 가져옵니다.

**Perplexity.** 따뜻한 흙색과 기술적인 어두운 파랑, 조각 같은 금속 별표, 디지털과 유기의 질감 대비. AI 회사치고 차갑지 않아서 작동합니다.

**Anthropic.** 녹슨 주황(#C15F3C). 기술 파랑이 아닙니다. 극도의 절제, 둥근 휴머니스트 서체. 따뜻함이 신뢰를, 절제가 자신을 말합니다.

**Figma.** 커다란 도형, 움직임이 표현의 핵, 원색·네온·흙색. 다양한 시선이 모이고, 변형되고, 증폭됩니다.

**Notion.** 일하는 모습이 아니라 생각하는 옆모습 일러스트. 원색. 입체파의 영향. 제품 화면에서 마음 상태로 옮긴 것이 작동했습니다.

**Linear.** 채도 낮은 파랑 하나, 극단적 미니멀, 다크 모드, 타이포가 일함. 개발자 청중에게 절제가 세련입니다.

**Vercel.** 그리드, 맞춤 서체, 높은 대비, 체계적 색. 디자인 시스템이 브랜드이고, 정밀이 엔지니어링을 말합니다.

지역 사업이 여기서 가져갈 것 하나. 색은 적게, 결과는 크게, 기술 파랑 기본에 기대지 않기.

---

## 7부. 자리

영어권 숫자는 한 상자에 가둡니다. 한국 운영은 그 아래입니다.

**영어권 닻. 한국 수치 아님.** 인스타(Socialinsider 2026년 2분기, 팔로워 기준 참여율). 캐러셀 0.50%, 릴스 0.48%, 단일 이미지 0.33%. 모든 형식이 전년 대비 하락(캐러셀 0.55%, 릴스 0.52%, 이미지 0.37%에서). 플랫폼 평균 0.45%, 전년 대비 -24%. 릴스는 도달 형식(2026년 정리에서 단일 이미지의 대략 2배). 캐러셀은 이미 있는 청중에게 더 일을 합니다. 스토리·릴스. 60~90초가 더 짧은 것보다 완주를 보상한다는 관찰, 트렌드 사운드의 초기 도달 가산은 연구마다 15~40%. 유튜브 썸네일. vidIQ 2026, 롱폼 브레이크아웃 썸네일 500장 중 69%가 얼굴, 가장 큰 초과 성과의 80%, 얼굴 또는 고대비 89%. 얼굴의 CTR 가산 25~50%는 2차 출처의 방향이지 그 연구의 측정이 아닙니다. 링크드인(노출 기준, 같은 분기). 여러 장 6.90%, 네이티브 문서 6.60%, 영상 5.90%, 단일 이미지 5.20%, 투표 4.50%, 텍스트만 3.95%, 링크 3.30%. 틱톡. 훅은 0.3초, 음소거 시청이 소셜 영상의 약 80~85%(2026년 정리), 자막이 완주를 약 30% 올린다는 정리와, 소리는 핵심이라는 틱톡 자신의 연구가 함께 있습니다. 둘 다 되게 디자인합니다. X. 2026년 이후 랭커에서 옛 리트윗 가중은 죽었습니다. 답글을 부르는 네이티브 영상, 외부 링크의 도달 불이익, 주제 일관. 핀터레스트. 2:3, 스펙 페이지 2026-09-02 확인. 2:3보다 긴 핀은 잘립니다.

이 상자를 한국 제안서의 근거로 쓰지 않습니다.

**한국에서 만들 때.**

| 자리 | 비율 | 판단 |
|------|------|------|
| 메타 피드 | 4:5가 면적, 1:1은 재사용 | 대비, 초점 하나. 캐러셀이면 첫 장이 혼자 섭니다 |
| 메타 릴스·스토리 | 9:16 | 위 약 14%, 아래 약 35%를 비움. 첫 프레임에 움직임이나 얼굴 |
| 유튜브 쇼츠 | 9:16 | 휴대폰 결. 과한 마감은 광고로 읽힘. 자막은 음소거를 전제 |
| 유튜브 썸네일 | 16:9, 1280×720 이상 | 얼굴 또는 결과, 3~5단어 이하, 사이드바에서 읽힘. 제목과 같은 색으로 맞추지 않음 |
| 플레이스 소식 이미지 | 정사각으로 시작 | 매장·작업·상품. 슬로건은 본문. 이미지 안 글자 최소 |
| 카카오 | 가이드의 정사각·세로 | 혜택 한 줄, 제품 또는 매장, 다음 행동. 픽셀은 가이드 확인 |

쇼츠와 릴스의 훅은 첫 1초입니다. 영어권의 0.3초, 0.5초를 한국 법칙으로 단정하지 않습니다. 첫 프레임이 소리 없이 성립하면 충분합니다.

링크드인, X, 핀터레스트, 틱톡은 그 채널을 쓸 때만 5부와 위 상자를 참고합니다. 사장님 기본 세트가 아닙니다.

---

## 8부. 기본 이미지 모델의 프롬프트

`image-default` 역할용입니다. 모델 이름은 MODEL_REGISTRY.md에서 풉니다.

```
[구체적인 주제] + [환경] + [스타일 참조] + [방향과 질이 있는 조명]
+ [이름 있는 팔레트] + [정확한 감정] + [질감의 기술 참조]
```

잘 하는 것. 자세한 자연어, 스타일 참조 여러 개, 대부분의 모델보다 나은 글자, 카메라·렌즈를 심도와 원근으로 번역, 구체적 색 이름, 요소가 여러 개인 구도.

어려워하는 것. 500단어가 넘는 프롬프트. 300단어 안이 안정적입니다. 시각 닻 없는 추상. 물건이 많은 정확한 공간 관계. 요소는 2~3개. 여러 세대에 걸친 같은 얼굴(아래 브랜드 키트). 복잡한 손. 손을 단순하게 하거나 크롭합니다.

약함과 강함.

```
"a coffee cup"
"handmade ceramic coffee cup with matte sage green glaze, slight irregularity
in the rim, latte art rosetta, wisps of steam catching the light"

"a laptop"
"silver laptop on aged oak desk, screen showing a scheduling board with
today's crews, desk lamp casting a warm pool from the left"

"a person working"
"plumber in his 40s, kneeling beside an open water heater, work shirt
sleeves rolled, late afternoon window light, phone on the floor as scale"
```

조명이 주제 다음으로 가장 큰 레버입니다.

| 말 | 무드 | 언제 |
|----|------|------|
| "soft natural daylight from a window" | 차분, 진짜, 다가감 | 라이프, 편집 |
| "golden hour light, long shadows" | 따뜻, 그리움 | 브랜드 이야기 |
| "single dramatic spotlight from upper left" | 프리미엄, 집중 | 제품 히어로 |
| "overcast diffused light, no harsh shadows" | 고르고 깨끗 | 쇼핑몰, 카탈로그 |
| "backlit with rim lighting, deep shadows" | 드라마, 하이엔드 | 패션, 럭셔리, 기술 |
| "neon accent lighting, cyan and magenta" | 에너지, 밤 | 엔터, 젊은 브랜드 |
| "chiaroscuro, dramatic light-dark contrast" | 예술, 진지 | 편집 |
| "flat even studio lighting" | 깨끗, 드라마 없음 | 제품 기록, UI 목업 |

"colorful", "vibrant colors"라고 말하지 않습니다. 팔레트를 지정합니다. 기본 이미지 모델은 hex를 이해합니다.

```
"warm palette of terracotta (#C4704A), cream (#F5F0E8), and deep forest (#1B3A2D)"
"muted earth tones: sand, warm grey, dried sage, soft clay"
```

사진다움. "shot on Fujifilm X-T5 with 56mm f/1.2 lens", "medium format film photography, slight grain", "editorial photography", "commercial product photography".

일러스트. "digital illustration, clean vector style", "watercolor with visible brush strokes", "risograph print, slight misregistration", "Japanese woodblock print aesthetic".

닳은 품질 부스터를 쓰지 않습니다. "ultra-detailed", "8K resolution", "hyper-realistic", "masterpiece", "best quality". 대신 "professional photography", "editorial quality", "commercial campaign quality", 구체적인 작가나 매체.

---

## 9부. 글자와 타이포

기본 이미지 모델은 이전 세대보다 글자를 잘 그립니다. 타이포가 주인공이면 텍스트 렌더 역할이 더 갑니다. 어느 쪽이든 기술이 필요합니다. 광고 문구의 기본은 이미지 위 HTML입니다.

| 상황 | 방법 | 이유 |
|------|------|------|
| 장면 안의 글자 (간판, 라벨, 포장) | 이미지 안 | 빛, 원근, 재질과 만나야 함 |
| UI나 오버레이 (헤드라인, CTA, 자막) | 후반 또는 HTML | 서체, 크기, 위치를 통제 |
| 짧은 글자 (1~4단어) | 이미지 안이 가능 | 짧은 글자를 잘 다룸 |
| 긴 글자, 문단, 가격, 전화번호 | 후반 | 길수록 오류 |
| 장식 글자 (네온, 각인) | 이미지 안 | 스타일 통합이 생성 일 |

짧게. 1~4단어가 깨끗합니다. 단어가 늘면 오류가 늘습니다. 정확한 글자는 따옴표. "large neon sign reading \"OPEN\" in red cursive". "a sign that says something about being open"은 약합니다.

서체를 말합니다. "bold sans-serif text reading \"LAUNCH\" in white, condensed uppercase". 재질도 말합니다. "embossed text reading \"PREMIUM\" pressed into thick cotton paper".

| 문제 | 고침 |
|------|------|
| 글자가 바뀌거나 중복 | 다시 생성. 확률적입니다. 같은 프롬프트가 다음에 맞기도 합니다 |
| 일부만 읽힘 | 글자를 줄입니다 |
| 서체가 틀림 | "bold geometric sans-serif". "modern font"은 약합니다 |
| 빛과 따로 놈 | "text catching the same light as the scene" |
| 공중에 뜸 | "text painted on the wall", "text engraved in the surface" |

서체 말. elegant serif, geometric sans, condensed gothic, bold display, brush script, art deco type, monospace. 한글 광고 문구는 이미지 안에 맡기지 않고 HTML로 올립니다. 모델의 한글 오탈자를 완성본으로 내지 않습니다.

---

## 10부. 여러 장의 일관성

각 API 호출은 독립입니다. 모델은 이전 출력을 기억하지 않습니다. 기억 없이 일관성을 만드는 기술입니다.

**브랜드 접두어.** 프로젝트의 모든 프롬프트 앞에 붙입니다.

```
"In the [Brand] visual style: warm terracotta (#C4704A) and cream (#F5F0E8),
soft natural lighting, minimal composition with generous negative space,
shot on medium format film with subtle grain, editorial quality. "
```

주제가 시작되기 전에 미학을 고정합니다.

**스타일 락.** 탐색(선택, SKILL.md) 뒤에 만듭니다.

```markdown
## Style Lock: [프로젝트]

### Color Anchors
- Primary surface: [색 + hex]
- Accent: [색 + hex]
- Background: [색 + hex]

### Lighting Lock
- Direction: [예 "upper left, 45 degrees"]
- Quality: [예 "soft diffused, no harsh shadows"]
- Temperature: [예 "warm, 4000K equivalent"]

### Composition Rules
- Framing: [예 "rule of thirds, subject on left intersection"]
- Negative space: [예 "right side for text overlay"]
- Depth: [예 "shallow depth of field, f/2.8 equivalent"]

### Texture/Processing
- Base: [예 "slight film grain"]
- Color grade: [예 "warm shadows, cool highlights"]
- Avoid: [예 "HDR look, over-saturation, plastic smoothing"]

### Prompt Template
[주제에 {{변수}}가 있는 정확한 구조]
```

기술.

1. **hex로 색을 닻.** "warm orange and cream"보다 "terracotta #C4704A and cream #F5F0E8"이 더 일정합니다.
2. **조명 문장을 그대로.** 바꿔 말하지 않습니다. 모든 프롬프트에 같은 구절.
3. **카메라 참조를 그대로.** "shot on Hasselblad X2D, 90mm f/3.2, slight film emulation"을 프로젝트 전체에.
4. **시드.** 마음에 드는 생성의 시드를 적고, 고친 프롬프트에 같은 시드. 확률을 올리지 보장은 아닙니다. 시드가 없는 모델은 레지스트리 표를 봅니다.
5. **참조 이미지.** 기본 이미지 모델의 참조 입력(페이로드는 레지스트리). 첫 장을 승인하고, 다음 장에 그 이미지를 `image_input`으로 넘기며 변화를 말합니다.

일관성을 깨는 것. 프롬프트마다 다른 조명 문장. 같은 색의 다른 이름. 한 장은 "shot on iPhone", 다른 장은 "Hasselblad". "warm"과 "cool-toned"가 충돌. 접두어를 뺀 프롬프트.

---

## 11부. 템플릿

프롬프트에 넣는 영어입니다. 대괄호만 바꿉니다.

**제품.**

```
A [재질·색·디테일이 있는 제품] positioned [구도],
[방향과 질이 있는 조명],
in [구체적 환경],
[이름 또는 hex 팔레트],
[구체적 감정],
shot on [카메라],
natural color grading, not over-saturated,
professional commercial photography
```

**편집 인물.**

```
[나이, 표정, 자세가 있는 사람],
[Rembrandt, butterfly, split 등],
[타이트, 미디엄, 환경],
[팔레트],
[작가 참조],
film grain, natural skin texture, visible pores, asymmetrical composition
```

**브랜드 라이프.**

```
[서사가 있는 장면],
featuring [순간에 자연스럽게 들어간 제품],
[시간과 빛],
[hex 팔레트],
candid, authentic feel, not posed,
editorial quality
```

**초현실 캠페인.** 브리프가 요구할 때만.

```
[정밀하게 묘사한 불가능한 장면],
photorealistic rendering of [그 불가능],
[불가능해도 빛은 물리적으로],
[브랜드 색과 제품],
dream-like clarity, commercial campaign quality
```

**글자 있는 소셜.** 짧은 장식 글자만. 광고 문구는 HTML.

```
[배경],
bold [서체] text reading "[정확한 글자]" in [색],
[위치],
clean, legible at mobile size,
graphic design quality
```

**쇼핑몰 평면.**

```
[재질과 색],
on pure white seamless background,
slightly elevated angle,
soft diffused studio lighting, no harsh shadows,
product fills 85 percent of the frame,
commercial product photography, accurate color, not enhanced
```

마켓별 흰 배경 규칙은 제품 사진 모드. 숫자를 마켓이 말하지 않았으면 지어내지 않습니다.

---

## 12부. 품질 체크

승인 전에 조용히. 사장님은 승인된 그림을 보지, 이 목록을 보지 않습니다.

**구분.** 스크롤이 멈추나. AI라고 바로 티가 나나. 독특한 요소를 말로 할 수 있나. 이 브랜드인지 아나. 4부 항목을 피했나.

**기술.** 구도가 의도인가(기본 중앙이 아닌가). 빛이 방향이 있고 이유가 있나. 자연 흠이 있나. 재질이 물리적으로 맞나. 색이 자연스러운가. 글자가 있으면 모바일에서 읽히고 철자가 맞나.

**전략.** creative-kit.md와 맞나. 감정이 메시지와 맞나. 전달 목표를 섬기나. 경쟁과 구분되나.

**자리.** 비율이 맞나. 썸네일 크기에서 되나. 영상은 3초, 피드 이미지는 한눈에 훅이 되나. 모바일에서 글자가 읽히나. 다크 모드 자리(X, 링크드인)는 양쪽에서 되나. 플레이스 소식은 매장이 먼저인가. 카카오는 혜택이 읽히나.

**일관성.** hex가 팔레트와 맞나. 조명이 스타일 락과 맞나. 카메라 처리가 다른 소재와 같나. 나란히 두어도 한 브랜드인가.

---

## 결별 키워드

프리미엄. editorial, luxury restraint, negative space, muted palette, natural materials, confident minimalism.

따뜻함. golden hour, natural light, organic texture, authentic, candid, imperfect beauty.

대담. high contrast, unexpected color, scale violation, pattern interrupt, visual tension.

기술. chrome, precision, systematic, engineered. 범용 기술 파랑만은 피합니다.

그리움. film grain, vintage color grade, analog texture, gentle light.

손맛. raw ceramic, linen, wood grain, wabi-sabi, visible process marks.

---

## 쓰는 법

고정된 체계가 아닙니다.

1. 전달 목표에서 시작합니다. 무엇이 느껴지고 이해돼야 하나.
2. 미학을 전략에 맞춥니다.
3. 여러 차원을 지정합니다. 키워드 하나에 기대지 않습니다.
4. 안티 슬롭을 기본으로. 프롬프트에 2~3개.
5. 생성, 비판, 다듬기를 반복합니다.
6. 첫 아이디어를 의심합니다.
7. 접두어, 스타일 락, 같은 기술 참조로 브랜드를 유지합니다.

규칙은 따르라고 있는 것이 아닙니다. 의도적으로 깨려면 원칙을 알아야 합니다. 깨는 이유를 한 줄로 적습니다.

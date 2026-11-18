# 변경 기록

## 1.0.0 (2026-11-18)

한국 시장용 첫 공개본. [boringmarketer/boring-marketing-skills](https://github.com/boringmarketer/boring-marketing-skills) 4.1.1 (James Dickerson, MIT)의 구조와 스킬 32개를 유지하고, 본문과 기준을 한국 채널로 다시 썼다.

### 유지

- 스킬 폴더 id 32개, `npx skills add` 레이아웃, Claude Code 플러그인 매니페스트, `_system` 런타임, 헬퍼 스크립트.
- MIT 라이선스와 Boring Marketing, LLC 저작권 고지.
- 브랜드 파일 계약 (`voice-profile`, `positioning`, `voc` 등)과 스킬 간 `/skill-name` 참조.

### 각색

- 지역 프로필의 기본 무대는 네이버 스마트플레이스, 카카오맵, 당근 비즈프로필. `google-business-profile` id는 호환을 위해 두고, 하는 일은 플레이스 진단과 소식 글이다. 구글 비즈니스 프로필은 구글·해외 수요가 있을 때만 보조로 다룬다.
- 키워드는 네이버 자동완성, 연관검색어, 데이터랩, 검색광고 키워드도구가 기본. `suggest.py`는 구글 자동완성 보조로 남겼다.
- 광고는 파워링크, 플레이스 광고, 브랜드검색, 메타, 구글 광고.
- 메시지는 알림톡·친구톡·문자(LMS)를 이메일과 함께 설계하고, 정보통신망법 광고성 정보((광고), 수신거부, 야간 21시~08시), 표시광고법, 개인정보보호법, 의료·대부 등 업종 심의 경고를 넣었다.
- AI 답변은 네이버 Cue:, AI 브리핑, ChatGPT, Perplexity, Google AI Overview. 영어권 인용 통계를 한국 사실처럼 쓰지 않는다.
- 대행사 스킬은 소상공인 사장님 대상의 제안 톤으로 바꿨다.
- 라우터가 `when_to_use`의 한글 구도 점수를 매긴다.

### 뺀 것

- Yelp, 미국 맵팩을 목표로 두는 지역 SEO, 미국 수신 규제(10DLC)를 기본 절차로 두는 설명.
- 원작자 유료 상품과 하우스 툴로 보내는 문장. 이 팩은 그 상품을 팔지 않는다.

## 원본 4.1.1 이전

원본 저장소의 CHANGELOG를 이 각색본에 반복하지 않는다. 이전 이력은 업스트림을 본다.

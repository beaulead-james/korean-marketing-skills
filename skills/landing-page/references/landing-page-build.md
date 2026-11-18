# 빌드. 랜딩 페이지

**구조가 끝나고 페이지를 만들 준비가 되면 불러옵니다.** 승인 카피와 `architecture.md`가 스펙이고, 이 파일이 빌드 기준입니다. 빌드 중에 메시지를 다시 디자인하지 않습니다. 섹션이 약해 보이면 `/direct-response-copy` 관문으로 되돌립니다.

## 1. 대상을 고른다

- **기본은 HTML 한 파일.** `index.html` 하나, CSS 인라인, 프레임워크 없음, 빌드 단계 없음. 어디든 올리고(Vercel, Netlify, S3, `python -m http.server` 미리보기) 나중에 고치기 쉽습니다. 프로젝트가 다르게 말하지 않으면 이것을 고릅니다.
- **Next.js 페이지 컴포넌트**는 작업 디렉터리 `package.json`에 `next`가 있을 때. `page.tsx`(App Router) 또는 `pages/<slug>.tsx`(Pages Router, 프로젝트가 쓰는 쪽). 프로젝트가 이미 쓰는 스타일(Tailwind가 있으면 Tailwind, CSS 모듈이 있으면 그것). 페이지 하나 때문에 새 스타일 시스템을 들이지 않습니다.

출력 위치. 단독 HTML은 `./campaigns/{name}/page/`. Next.js는 프로젝트 라우트 디렉터리(경로를 사용자와 먼저 확인).

## 2. 카피를 섹션에 올린다

`architecture.md`가 정한 섹션만, 그 순서로, 승인 카피를 1대 1로 올립니다.

| 카피 섹션 | 페이지 섹션 | 빌드 메모 |
|---|---|---|
| 헤드라인 + 서브 + 주 버튼 | `<header>` 히어로 | H1은 헤드라인 그대로. 접힌 선 위 버튼 하나. 캐러셀 없음, 영상 자동재생 없음. |
| 문제 / 비용 계산 | 문제 블록 | 계산은 문단이 아니라 짧은 목록이나 쌓인 줄. "= 22시간 이상" 줄에 시각적 무게. |
| 방법 / 해결 | 방법 블록 | 짧은 하위 2~4개, 또는 아이콘 없는 3열. 기능 그리드로 퍼지지 않게. "그래서 뭐가 좋은데"가 앞. |
| 만든 사람 이야기 (있을 때) | 이야기 블록 | 한 열, 폭 약 60ch, 편지처럼. 자산이 없으면 주석으로 사진 자리. |
| 증거 / 후기 | 증거 블록 | 카드. 인용, 이름, 역할, 결과를 굵게. 합계 통계는 출처 링크가 있는 자기 줄. |
| 오퍼 / 가격 | 오퍼 블록 | 가격(원), 포함, 위험 제거. 여기 두 번째 버튼. |
| FAQ / 대상 아님 | FAQ 블록 | 기본 `<details>/<summary>`. JS 아코디언 없음. AI가 물을 이의(환불, 누구를 위한 것이 아닌지, 비교)를 넣는다. |
| 마지막 버튼 + 마찰 제거 | 닫는 버튼 | 버튼과 그 아래 한 줄 제거 스택. |

함께 냅니다. 헤드라인·서브에서 온 `<title>`과 메타 설명, OG(제목, 설명, og:image 자리 경로), FAQ 카피로 만든 **FAQ JSON-LD**. 오늘 가치는 LLM이 읽기 쉬운 것이고, AI 독자 층에 직접 닿습니다. `lang`은 `ko`입니다.

## 3. 디자인 토큰

`./brand/creative-kit.md`가 있으면 가져옵니다. 주색·강조·배경, 글꼴(키트가 이름을 말할 때만 Google Fonts 링크), 모서리, 로고 경로. CSS 변수로 두어 한곳에서 테마를 바꿉니다.

키트가 없으면 수수한 기본. 시스템 글꼴, 오프화이트 위 거의 검정(`#1a1a1a` on `#fafaf8`), 버튼에만 강조색 하나, 여백을 넉넉히. 보라 그라데이션 유리 모핑 기본은 내보내지 않습니다. 카피가 이끄는 페이지는 잘 조판된 문서에 분명한 버튼 하나여야 합니다.

```css
:root {
  --bg: #fafaf8; --text: #1a1a1a; --muted: #555;
  --accent: #0d6e5f;
  --radius: 8px; --measure: 64ch;
  --font: system-ui, -apple-system, "Apple SD Gothic Neo", "Noto Sans KR", sans-serif;
}
```

## 4. HTML 한 파일 기준

- 모바일 먼저. 작은 화면 기본, `@media (min-width: 720px)` 한 번으로 데스크톱. 히어로를 375px로 머릿속에서 테스트. 헤드라인 줄바꿈, 버튼은 전체 폭.
- 시맨틱. `header`, `main` 안에 카피 블록마다 `section` (`id`: `problem`, `mechanism`, `proof`, `offer`, `faq`, `cta`), `footer`는 법적·연락 최소.
- 본문 17~18px, 줄간격 약 1.6, 최대 폭 약 64ch. 섹션 리듬은 일정한 세로 패딩이지 장식 구분선이 아닙니다.
- 외부 JS 라이브러리 없음. 허용 스크립트는 변형 분할(아래)과 분석 스텁뿐입니다.
- 실제 자산이 없으면 모든 이미지는 의도를 적은 주석 자리. `<!-- IMAGE: 작업 차량, 약 800x600, /creative -->`
- `file://`에서 열려야 합니다. 절대 경로 없음, 서버 측 없음.

**뼈대.** 슬롯은 승인 카피 파일에서 글자 그대로 채웁니다. 다시 쓰지 않습니다.

```html
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{headline, 약 30자}</title>
  <meta name="description" content="{subhead, 약 80자}">
  <meta property="og:title" content="{headline}">
  <meta property="og:description" content="{subhead}">
  <meta property="og:image" content="/og.png">
  <style>
    :root { /* tokens from section 3 */ }
    html[data-variant="a"] .v-b, html[data-variant="b"] .v-a { display: none; }
  </style>
  <script type="application/ld+json">{ "@type": "FAQPage" }</script>
</head>
<body>
  <header class="hero">
    <h1><span class="v-a">{headline A}</span><span class="v-b">{headline B}</span></h1>
    <p>{subhead}</p>
    <a href="{cta-url}" data-cta="hero">{버튼 문구 그대로}</a>
  </header>
  <main>
    <section id="problem"></section>
    <section id="mechanism"></section>
    <section id="proof"></section>
    <section id="offer"><a href="{cta-url}" data-cta="offer">{버튼}</a></section>
    <section id="faq"><details><summary>{질문}</summary><p>{답}</p></details></section>
    <section id="cta">
      <a href="{cta-url}" data-cta="closing">{버튼}</a>
      <p class="reducers">{위험 제거} · {증거} · {시간}</p>
    </section>
  </main>
  <footer></footer>
  <script>/* variant split + analytics stubs */</script>
</body>
</html>
```

지역 페이지의 전화 막대와 `tel:`은 `references/local-pages.md`를 따릅니다. 한국어 버튼은 "제출"이 아니라 일어나는 일을 말합니다. "견적 받기", "전화하기", "카카오 채널 열기".

## 5. Next.js 컴포넌트 기준

같은 섹션, 같은 토큰. 세부입니다.

- 기본은 서버 컴포넌트. 변형·분석만 클라이언트 섬(`"use client"`의 작은 `VariantGate` 또는 인라인 `<Script>`). 페이지는 정적으로 남습니다.
- 메타데이터는 `metadata` export(App Router)와 OG. FAQ JSON-LD는 타입이 있는 객체에서 렌더한 `<script type="application/ld+json">`.
- 변형은 라우트. `app/{slug}/a/page.tsx`와 `b/page.tsx`가 공유 `LandingPage({ variant })`를 얇게 감싸고, `app/{slug}/page.tsx`가 고정 배정과 리다이렉트를 합니다. Next.js에서는 쿼리보다 낫습니다. 각 변형이 정적으로 렌더되고 공유됩니다.

```tsx
// app/{slug}/a/page.tsx
import { LandingPage } from "../landing-page";
export const metadata = { title: "{headline A}", description: "{subhead}" };
export default function Page() { return <LandingPage variant="a" />; }

// app/{slug}/page.tsx
"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
export default function Assign() {
  const router = useRouter();
  useEffect(() => {
    const v = localStorage.getItem("lp_variant")
           ?? (Math.random() < 0.5 ? "a" : "b");
    localStorage.setItem("lp_variant", v);
    // ANALYTICS: capture lp_view here with { variant: v }
    router.replace(`/{slug}/${v}`);
  }, [router]);
  return null;
}
```

공유 `LandingPage`는 4절 HTML과 같은 섹션입니다. 버튼은 `data-cta`를 가지고, 클릭 핸들러 스텁은 `// ANALYTICS:`로 6절과 같습니다.

## 6. A/B 분할 (HTML)

승인 카피 변형이 둘이면 페이지 하나, 쿼리 분할, localStorage로 고정해 손님이 변형 사이를 오가지 않게 합니다. 이 패턴을 그대로 실습니다.

```html
<script>
  (function () {
    var KEY = "lp_variant";
    var forced = new URLSearchParams(location.search).get("v");
    var v = (forced === "a" || forced === "b") ? forced
          : localStorage.getItem(KEY) || (Math.random() < 0.5 ? "a" : "b");
    localStorage.setItem(KEY, v);
    document.documentElement.dataset.variant = v;

    // ANALYTICS: wire pageview here, tag the variant.
    // e.g. posthog.capture("lp_view", { variant: v })
    //      or gtag("event", "lp_view", { variant: v });

    document.querySelectorAll("[data-cta]").forEach(function (el) {
      el.addEventListener("click", function () {
        // ANALYTICS: conversion event, same variant tag
        // posthog.capture("lp_cta_click", { variant: v, cta: el.dataset.cta });
      });
    });
  })();
</script>
```

변형 내용은 CSS로 바꿉니다. 두 헤드라인 마크업을 문서에 두고 `html[data-variant="a"] .v-b { display:none }`와 그 반대. 분할은 승인 변형이 실제로 다른 섹션만(보통 히어로와 첫머리). 페이지 전체를 복제하지 않습니다. 모든 버튼에 `data-cta="hero|offer|closing"`을 달아 클릭이 위치를 알게 합니다.

사용자에게 분명히 말합니다. 표시된 스텁 두 곳을 잇기 전에는 페이지가 추적을 내지 않습니다. A/B 표본 정직을 가리킵니다. 주 방문자 약 1,000명 미만이면 크게 다른 변형만 돌립니다.

## 7. 끝났다는 뜻

보여 주기 전에 렌더 확인 한 번만, 조용히. 손님은 끝난 페이지를 보고 확인 로그를 보지 않습니다. 파일을 파싱하거나 `next dev` 라우트를 한 번 열어 렌더를 확인합니다. 스크린샷 루프, 시각 QA 반복, 다른 플러그인은 없습니다. 예외는 지역 페이지이고, 첫 화면 목록을 위해 휴대폰 폭 스크린샷 한 장입니다. SKILL.md 배포를 봅니다. 그다음 카피 섹션이 글자 그대로 들어갔는지(헤드라인, 가격, 마찰 제거를 승인 파일과 대조), `?v=a` / `?v=b`로 두 변형이 렌더되는지 확인합니다. 넘길 때 파일 경로, 한 줄 테마(`:root` 토큰), 분석 스텁 두 곳, 이미지 자리는 `/creative`를 제안합니다.

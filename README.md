# popol — 김유미 개발 포트폴리오

웹사이트를 중심으로 구성한 2026년 개발 포트폴리오입니다. 테나아이 AI 서비스 백엔드 신입 지원을 고려해 웹 서비스 기능 구현, 서버·REST API 연동, AI 서비스 연계, 오류 대응 경험을 강조했습니다.

## 구성

| 파일 | 내용 |
| --- | --- |
| `index.html` | **기본 포트폴리오 웹사이트** — 스크롤형 About / Projects / 상세 구현 기록 |
| `styles.css` | 웹사이트 반응형 스타일 · 화이트/아이스블루 |
| `script.js` | 모바일 메뉴 동작 |
| `print.html` | **별도 제출용 문서 보기** — 12장 구성 |
| `print.css` | A4 가로 인쇄 스타일 |
| `print.js` | 페이지 탐색·브라우저 PDF 인쇄 |

프로젝트 순서: **GIGANG(기강) → 쉬엄쉬엄 → 오늘의짐**

## 웹 포트폴리오 보기

`index.html`을 브라우저에서 열거나, GitHub Pages에서 **Settings → Pages → Deploy from a branch → main / (root)**를 선택해 공개할 수 있습니다.

Pages를 활성화한 경우 예상 공개 경로는 `https://youmjjang.github.io/popol/`입니다. 활성화 이전에는 URL이 동작하지 않을 수 있습니다.

## 별도 PDF로 제출하려면

`print.html`을 브라우저에서 열고 상단 **PDF로 저장 / 인쇄** 버튼을 누릅니다. 프린터를 'PDF로 저장'으로 선택하고 용지를 A4 가로, 여백 없음, 배경 그래픽 인쇄로 설정합니다.

PDF 문서는 웹사이트 메인에 섞지 않고 별도 문서로 유지했습니다. 저장소에 PDF 바이너리 자체를 추가한 것은 아닙니다.

## 사실 검증 기준

- GIGANG은 팀 프로젝트입니다. 이벤트 수집·DB/서버 연동·판단 흐름 보완·단말 대응 연결을 중심으로 참여 범위를 기술했습니다.
- GIGANG의 점수 예시는 규칙 구조 설명용이며 실제 운영 환경의 탐지 성능을 뜻하지 않습니다.
- 쉬엄쉬엄은 외부 지도 데이터와 API 상태에 따라 기능이 제한될 수 있습니다. 경로 조회 실패 시 직선거리를 보행 경로로 표시하지 않습니다.
- 오늘의짐은 물품보관함 제공 범위와 실시간 점유 여부의 한계를 명시합니다.
- 채용 공고에 Java/Spring Boot가 중요하지만, 실제 프로젝트에 사용한 적 없는 기술을 사용했다고 표시하지 않았습니다. 포트폴리오의 주력 경험은 Python/FastAPI, Node.js, React와 AI 연동입니다.
- 프로젝트 화면은 본인 공개 저장소의 실제 스크린샷으로 연결했습니다. 원본 파일을 이동·삭제하면 이미지 URL도 변경해야 합니다.

## 프로젝트 자료

- [GIGANG — 상세 구현 정리](https://github.com/youmjjang/youmjjang-lab/blob/main/gigang.html)
- [쉬엄쉬엄 — 소스 코드](https://github.com/youmjjang/swieogalgot) · [서비스](https://swieogalgot.vercel.app/)
- [오늘의짐 — 소스 코드](https://github.com/youmjjang/oneurui-jim) · [서비스](https://oneurui-jim.vercel.app/)
- [GitHub](https://github.com/youmjjang) · [블로그](https://blog.naver.com/youumii2595)

# Bible Anywhere 웹사이트

Mac·iPhone·iPad 앱 Bible Anywhere의 소개 · 개인정보 처리방침 · 지원 페이지입니다. PawShelf와 같은 방식으로 GitHub Pages(`https://archivelab-kr.github.io/bibleanywhere/`)에 올리는 것을 전제로 만들었고, 아직 공개하지 않았습니다.

- 문구는 `i18n/<언어>.json`(영어 `en.json`이 원본)에 있습니다. `python3 build.py`가 언어별 `index.html` · `privacy.html` · `support.html`, 맨 위 `index.html`(브라우저 언어로 이동), `sitemap.xml`을 만듭니다. 만든 HTML은 손으로 고치지 않습니다. 모든 언어 파일이 영어와 같은 항목을 가졌는지 빌드할 때 검사합니다.
- `assets/shots/`: 앱 화면. Mac은 `../VerseShelf/AppStore/screenshots/`, iPhone·iPad는 `../VerseShelf/Docs/ios/`에서 변환했습니다. 그 언어의 화면이 없으면 다른 언어의 화면을 씁니다.
- 공개 전에 `build.py`의 `APP_STORE_URL`(비우면 "출시 예정")을 채웁니다. `SITE_URL`과 `SUPPORT_EMAIL`은 PawShelf 사이트와 같은 계정 기준입니다.
- 외부 라이브러리 · 웹 글꼴 · 방문 통계 · 쿠키를 쓰지 않습니다(외부 요청 0개).

```sh
python3 build.py
python3 -m http.server   # 로컬에서 열기
```

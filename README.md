# -TOY-SNCreator

나만의 단편소설 생성 웹프로젝트

사용 기술 현황(2024.04.26 기준)
언어: Python, JavaScript
프레임워크: Flask, Bootstrap
DB: MongoDB
API: OpenAIAPI

ETC: Git, jwt, hasglib

패치노트
v0.1
ChatGPT 기반 나만의 소설 생성 프로젝트

- (BACK) PDF 다운로드 기능
- (BACK) OpenAI API 연동
- (FRONT) 개발(Modal, HTML, JavaScript, CSS, Jquery)

v0.2 (2024.04.25)

- (BACK) MongoDB(Atlas) 연동
- (BACK) 회원가입 기능 개발

v 0.3 (2024.04.26)

- (BACK) 로그인 기능 개발
- (FRONT)로그인, 회원가입 Modal 개발

v 0.4 (2024.04.27)

- (FRONT) 모달 UI 개선
- (BACK) 비밀번호 토큰화 및 로그인 로직 개선
- (BACK) jwt 토큰을 이용한 session 처리

v 0.5 (2024.04.28)

- (FRONT) intro 페이지 개발
- (FRONT) Modal 컴포넌트 분리

v 0.6 (2024.04.29)

- (BACK) 회원DB 속성 추가 (role, grade, count)
- (FRONT) grade에 따른 이모지 사용

v 0.7 (2024.04.30)

- 소설에서 사용할 수 있는 키워드를 장르당 30개씩 120개 수집
- (FRONT) carousel을 이용한 디자인 개선
- (FRONT) 기존 버튼식 로그아웃에서 드롭다운식으로 개선

---

TODO LIST (MUST, 중요도 순)

- 1. MongoDB uri 처리 (환경변수로 처리 할 예정)
- 2. 마이페이지 제작 (해당 유저가 생성한 소설 목록 로딩 가능)
- 3. 금칙어 수집 및 적용 (비정상 이용을 제제할 목적으로 사용)
- 4. 게시판, 댓글 기능 구현

TODO LIST (WISH)

- 로고 만들기
- 회원 등급 개발하기 -> 등급을 통한 서비스 기능 확장
- 글자 수 제한 늘리기 (최대 4000토큰 예정)
- 더 다양한 장르 제공
- GCP 혹은 AWS에 배포하기

IDEA

- 시각장애인을 위한 TTS를 사용해보면 어떨까?
- 사용자에게 여러개의 키워드를 주워주고 그에 맞게 소설을 작성할 수 있다면?
- 엔딩을 설정할 수 있으면 좋겠다 (등급별 해금)

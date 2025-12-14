# 메이플스토리 캐릭터 검색 & 랭킹 웹페이지

넥슨 Open API를 사용하여 메이플스토리 캐릭터 정보를 조회하고 월드 랭킹을 표시하는 웹 애플리케이션입니다.

## 🚀 빠른 시작

### 방법 1: Python 서버 사용 (추천 - 더 간단함)

1. **프록시 서버 시작**
   - `start_server.bat` 파일을 더블클릭하거나
   - 터미널에서 다음 명령 실행:
     ```bash
     python proxy_server.py
     ```

2. **브라우저에서 접속**
   - 브라우저에서 `http://localhost:8000` 열기
   - 또는 자동으로 브라우저가 열릴 수 있습니다.

3. **사용 시작**
   - API Key 입력 및 저장
   - 캐릭터 검색 또는 랭킹 조회

### 방법 2: Node.js 서버 사용

1. **의존성 설치**
   ```bash
   npm install
   ```

2. **서버 시작**
   ```bash
   npm start
   ```

3. **브라우저에서 접속**
   - `http://localhost:3000` 열기

## ⚠️ 중요: CORS 문제 해결

넥슨 Open API는 브라우저에서 직접 호출할 수 없습니다 (CORS 제한).

**반드시 프록시 서버를 실행한 후 사용해야 합니다!**

- Python 서버: `start_server.bat` 실행 (포트 8000)
- Node.js 서버: `npm start` 실행 (포트 3000)

## 📝 사용 방법

### 1. API Key 입력
- 넥슨 Open API Key를 입력하고 "저장" 버튼 클릭
- API Key는 자동으로 저장되어 다음에 다시 입력할 필요 없음

### 2. 캐릭터 검색
- 캐릭터 이름 입력 후 "검색" 버튼 클릭
- 캐릭터의 기본 정보(레벨, 직업, 길드명 등) 표시

### 3. 월드 랭킹 조회
- 월드 선택 후 "랭킹 조회" 버튼 클릭
- 선택한 월드의 상위 100위 랭킹 표시

## 🛠️ 기술 스택

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (http.server) 또는 Node.js (Express)
- **API**: 넥슨 Open API

## 📦 파일 구조

```
newsite/
├── index.html           # 프론트엔드 HTML 파일
├── proxy_server.py      # Python 프록시 서버 (추천)
├── start_server.bat     # Python 서버 시작 스크립트 (Windows)
├── server.js            # Node.js 프록시 서버
├── package.json         # Node.js 의존성 설정
└── README_한국어.md    # 프로젝트 설명 문서 (이 파일)
```

## 🔧 문제 해결

### Q: CORS 오류가 발생합니다
**A:** 프록시 서버가 실행 중인지 확인하세요.
- Python 서버: `start_server.bat` 실행
- Node.js 서버: `npm start` 실행

### Q: Python이 설치되어 있지 않습니다
**A:** Python을 설치하세요:
- 다운로드: https://www.python.org/downloads/
- 설치 시 "Add Python to PATH" 옵션 체크

### Q: 캐릭터 검색이 실패합니다
**A:** 다음을 확인하세요:
1. 프록시 서버가 실행 중인가요?
2. API Key가 올바르게 입력되고 저장되었나요?
3. 브라우저 개발자 도구(F12)의 콘솔에서 오류 메시지 확인
4. 넥슨 Open API Key가 유효한가요?

### Q: 서버가 시작되지 않습니다
**A:**
- Python 버전 확인: `python --version`
- 포트가 이미 사용 중인지 확인 (8000 또는 3000)
- 방화벽이 포트를 차단하지 않는지 확인

## 📄 라이선스

MIT License

## 🙏 참고사항

- 넥슨 Open API는 API Key가 필요합니다.
- API Key는 [넥슨 개발자 센터](https://open.nexon.com/)에서 발급받을 수 있습니다.
- API 사용량 제한이 있을 수 있으니 주의하세요.



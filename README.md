# 🏨 글로벌 호텔 키오스크 시스템 (Hotel Kiosk System)

**2024-1 소프트웨어공학 프로젝트**

[![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://hotel-kiosk.onrender.com)
> **🚀 라이브 데모**: [https://hotel-kiosk.onrender.com](https://hotel-kiosk.onrender.com) (초기 로딩 시 약 50초 정도 소요될 수 있습니다)

Flask 기반의 경량화된 웹 서버로 구축된 **다국어 지원 호텔 키오스크 및 통합 관리자 시스템**입니다.  
사용자에게는 직관적인 체크인/아웃 경험을 제공하고, 관리자에게는 실시간 객실 및 매출 관리를 위한 효율적인 대시보드를 제공합니다.

---

## 💡 프로젝트 개요
- **진행 기간**: 2024.03 ~ 2024.06
- **주요 역할**: 풀스택 개발 (Backend 로직 설계, Frontend UI/UX 디자인 및 구현)
- **개발 목표**: 글로벌 사용자를 위한 언어 장벽 없는 서비스 제공 및 호텔 운영 효율화

## ✨ 주요 기능 (Key Features)

### 1. 사용자 경험 중심의 키오스크 (Client Side)
- **🌏 동적 다국어 지원 (i18n)**: 한국어, 영어, 중국어 3개 국어를 지원하며, 세션이나 URL 파라미터에 따라 UI 텍스트를 실시간으로 맵핑하여 번역합니다.
- **🛏️ 직관적인 객실 선택**: 객실의 청소 상태(Clean/Dirty)를 실시간으로 확인하여 예약 가능한 객실만 그리드 뷰로 제공합니다.
- **💳 간편 체크인/아웃 프로세스**: 조식 선택, 결제 방식 선택부터 최종 영수증 발급까지의 흐름을 단계별로 구현했습니다.
- **📱 반응형 UI & UX 개선 (Refactoring)**:
  - 기존의 딱딱한 UI를 **Black & Gray 테마**의 모던한 디자인으로 전면 리팩토링했습니다.
  - 모바일 접근성을 고려한 시설 안내 페이지(가로 스크롤 카드 UI) 및 커스텀 드롭다운 컴포넌트를 직접 구현하여 심미성을 높였습니다.

### 2. 효율적인 통합 관리 시스템 (Admin Side)
- **📊 관리자 대시보드**: 전체 객실 점유율, 매출 현황 등을 한눈에 파악할 수 있습니다.
- **💰 유동적 요금 정책**: 성수기, 주말, 조식 요금 등을 관리자가 실시간으로 조정하여 비즈니스 상황에 대응할 수 있습니다.
- **🧹 객실 상태 관리**: 체크아웃 시 자동으로 '청소 필요(Dirty)' 상태로 전환되며, 청소 완료 후 상태를 업데이트하는 워크플로우를 구현했습니다.

## 🛠️ 기술 스택 (Tech Stack)
- **Backend**: Python 3.x, Flask (Jinja2 Template)
- **Frontend**: HTML5, CSS3 (Custom Design System), JavaScript (Vanilla)
- **Database**: In-memory Data Structure (학습용 경량화)
- **Deployment**: Render Cloud, Gunicorn WSGI Server

## 🚀 설치 및 실행 방법

### 로컬 환경 (Local)
```bash
# 1. 저장소 클론
git clone https://github.com/2024-1-University-SEProject/hotel_kiosk.git

# 2. 의존성 패키지 설치
pip install -r requirements.txt

# 3. 애플리케이션 실행
python app.py
```

### 배포 환경 (Production)
이 프로젝트는 **Render** 클라우드 플랫폼에 최적화되어 있습니다.
- `Procfile`: Gunicorn 프로덕션 서버 실행 설정 포함
- `requirements.txt`: 필수 라이브러리 명시

---
*Created by SE Project Team*

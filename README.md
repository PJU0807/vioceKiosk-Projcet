﻿# vioceKiosk-Projcet
## 음성으로 주문하는 키오스크
### 프로젝트 기간
2023.09 ~ 2023.10.22
### 개발인원
4명 -> 1명(팀원들의 개인사정으로 변경)
### 프로젝트의 목적
키오스크의 주문이 어려운 디지털 약자를 위한 음성인식 키오스크  

---
### 개발환경
os : windows11 22H2  
Tools : Visual Studio 2022, Figma, Illustrator
Language : Python 3.11  
pip : PyQt5, gTTS, PyAudio, ctypes, playsound, numpy...
### 구현 및 기여 부분
- 키오스크 화면
  -  4가지의 메뉴 버튼
  -  각 메뉴들 표시
  -  win32 API를 사용하여 마이크 제어하는 버튼
  -  언어 변경 ( 영어, 한글 )
  -  초기화 버튼 ( 주문내역 및 언어 초기화 )
  -  음성 주문 시 주문 내용 표시
  -  현제 주문내역 및 총 가격 표시
  -  결제 버튼 누를 시 총 주문내역 및 가격 표시, 주문내역 초기화
- 음성
  - 구글 API를 사용하여 음성데이터 받기
  - 음성데이터를 필터링하여 음식과 개수를 리스트에 저장
  - 음성으로 주문한 내역을 음성으로 표시
- 디자인
  - Figma를 사용하여 UI 설계 및 디자인
  - Illustrator와 Photoshop 사용하여 사진 편집 
- 멀티프로세싱
  - UI와 음성인식을 동시에 작동하기 위해 멀티프로세싱

---
### 실제 구동 화면
![스크린샷 2024-04-21 011738](https://github.com/PJU0807/vioceKiosk-Projcet/assets/167528682/bdbd31b5-3326-46d6-8412-58c91f56b045)
![스크린샷 2023-10-21 180439](https://github.com/PJU0807/vioceKiosk-Projcet/assets/167528682/92ab953f-740c-450b-9f4c-dd666a86f9dc)

from ast import Name
import multiprocessing
import os
from pickletools import unicodestring1
import time
import msvcrt
import speech_recognition as sr
import sys, psutil, comtypes, ctypes

from gtts import gTTS
from playsound import playsound
from multiprocessing import Process 
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QGraphicsDropShadowEffect, QPushButton, QFrame, QDialog, QMainWindow, QSizePolicy
from PyQt5.QtGui import QColor, QFont, QFontDatabase, QIcon, QPixmap
from PyQt5.QtCore import QPointF, Qt, QSize, QRect, QPropertyAnimation, pyqtSlot
from enum import Enum
from ctypes import HRESULT, POINTER, Structure, Union, c_uint32, c_longlong, c_float
from ctypes.wintypes import BOOL, VARIANT_BOOL, WORD, DWORD, UINT, INT, LONG, ULARGE_INTEGER, LPWSTR, LPCWSTR
from comtypes import IUnknown, GUID, COMMETHOD
from comtypes.automation import VARTYPE, VT_BOOL, VT_LPWSTR, VT_UI4, VT_CLSID

price_kr = [3200, 4200, 4200, 4500, 4500, 4500], [4700, 5200, 5500, 5300, 5300, 4200, 4200, 4200], [4500, 4700, 4700, 3900, 3900, 4500], [2500, 2900, 3200, 2900, 3200, 3200, 1500, 1500, 2500, 2500, 2500, 4500, 4500, 4500, 5200, 5400, 2100, 2500, 2500, 2500]
price_eng = [236, 310, 310, 333, 333, 333], [347, 384, 407, 392, 392, 310, 310, 310], [333, 347, 347, 288, 288, 333], [185, 214, 237, 214, 237, 237, 111, 111, 185, 185, 185, 333, 333, 333, 384, 399, 155, 185, 185, 185]
Names_r = ['아메리카노', '카페 라떼', '바닐라 라떼', '카라멜 마끼야또', '콜드브루 라떼', '흑당 콜드브루'], ['오리진 쉐이크', '딸기 쉐이크', '더블 초코칩 쉐이크', '초코쿠키 쉐이크', '피스타치오 쉐이크', '레몬에이드', '자몽에이드', '청포도에이드'], ['플레인 요거트 플랫치노', '블루베리 요거트 플랫치노', '딸기 요거트 플랫치노', '망고 플랫치노', '꿀복숭아 플랫치노', '초콜릿 칩 플랫치노'], ['소금빵', '플레인 크로플', '토피넛 크로플', '생크림 와플', '플레인 와플', '메이플 와플', '초콜릿 마카롱', '산딸기 마카롱', '스트로베리 치즈 마카롱', '쿠키 앤 크림 마카롱','햄앤치즈샌드위치', '초코 티라미수', '수플레 치즈 케이크', '데블스 초코 케이크', '허니 카라멜 브레드', '메이플 넛 브레드', '스노우 쿠키슈', '초코칩 머핀', '크림치즈 머핀', '블루베리 머핀']
Names_r2 = [['아메리카노', '아메리카노'], ['카페 라떼', '카페 나떼', '카페나떼'], ['바닐라 라떼', '바닐나 라떼', '바닐나라떼', '바닐라 나떼', '바닐라나떼', '바닐나 나떼', '바닐나나떼'], ['카라멜 마끼야또', '카라멜 마끼아또', '카라멜마끼아또', '캬라멜 마끼야또', '캬라멜마끼야또', '캬라멜 마끼아또', '캬라멜마끼아또 '], ['콜드브루 라떼', '콜드 브루 라떼', '콜드 부루 라떼', '콜드부루 라떼', '콜드부루라떼', '콜드 브루 나떼', '콜드브루 나떼', '콜드브루나떼', '콜드 부루 나떼', '콜드부루 나떼', '콜드부루나떼'], ['흑당 콜드브루', '흑당 콜드 브루', '흑당콜드 브루', '흑당콜드브루', '흑땅 콜드 브루', '흑땅 콜드브루', '흑땅콜드 브루', '흑땅콜드브루', '흑당 콜드 부루', '흑당 콜드부루', '흑당콜드 부루', '흑당콜드부루', '흑땅 콜드 부루', '흑땅 콜드부루', '흑땅콜드 부루', '흑땅콜드부루']], [['오리진 쉐이크', '오리진 쉐이커', '오리진쉐이커', '오리진 셰이크',  '오리진셰이크', '오리진 셰이커', '오리진셰이커', '오리진 shaken', '오리진shaken'], ['딸기 쉐이크', '딸기 쉐이커', '딸기쉐이커', '딸기 셰이크',  '딸기셰이크', '딸기 셰이커', '딸기셰이커', '딸기 shaken', '딸기shaken'], ['더블 초코칩 쉐이크', '더블초코칩 쉐이크', '더블 초코칩쉐이크', '더블초코칩쉐이크', '더블 초코칩 쉐이커', '더블초코칩 쉐이커', '더블 초코칩쉐이커', '더블초코칩쉐이커', '더블 초코칩 셰이크', '더블초코칩 셰이크', '더블 초코칩셰이크', '더블초코칩셰이크', '더블 초코칩 셰이커', '더블초코칩 셰이커', '더블 초코칩셰이커', '더블초코칩셰이커', '더블 초코칩 shaken', '더블초코칩 shaken', '더블 초코칩shaken', '더블초코칩shaken'], ['초코쿠키 쉐이크', '초코 쿠키 쉐이크', '초코 쿠키쉐이크', '초코쿠키쉐이크', '초코 쿠키 쉐이커', '초코쿠키 쉐이커', '초코 쿠키쉐이커', '초코쿠키칩쉐이커', '초코 쿠키 셰이크', '초코쿠키 셰이크', '초코 쿠키셰이크', '초코쿠키칩셰이크', '초코 쿠키 셰이커', '초코쿠키 셰이커', '초코 쿠키셰이커', '초코 쿠키 셰이커', '초코 쿠키 shaken', '초코쿠키 shaken', '초코 쿠키shaken', '초코쿠키shaken', '초코 국기 shaken', '초코국기 shaken', '초코 국기shaken', '초코국기shaken', '축구 쿠키 shaken', '축구쿠키 shaken', '축구 쿠키shaken', '축구쿠키shaken', '축구 국기 shaken', '축구국기 shaken', '축구 국기shaken', '축구국기shaken'], ['피스타치오 쉐이크', '피스타치오 쉐이커', '피스타치오쉐이커', '피스타치오 셰이크',  '피스타치오셰이크', '피스타치오 셰이커', '피스타치오셰이커', '피스타치오 shaken', '피스타치오shaken'], ['레몬에이드', '레몬 에이드', '레모네이드', '레모 네이드'], ['자몽에이드', '자몽 에이드'], ['청포도에이드', '청포도 에이드']], [['플레인 요거트 플랫치노', '플레인요거트 플랫치노', '플레인 요거트플랫치노', '플레임 요거트 플랫치노', '플레임요거트 플랫치노', '플레임 요거트플랫치노', '플레임요거트플랫치노', '플레이 요거트 플랫치노', '플레이요거트 플랫치노', '플레이 요거트플랫치노', '플레이요거트플랫치노', '플라잉 요거트 플랫치노', '플라잉요거트 플랫치노', '플라잉 요거트플랫치노', '플라잉요거트플랫치노', '플레잉 요거트 플랫치노', '플레잉요거트 플랫치노', '플레잉 요거트플랫치노', '플레잉요거트플랫치노', '클레이 요거트 플랫치노', '클레이요거트 플랫치노', '클레이 요거트플랫치노', '클레이요거트플랫치노', '클레임 요거트 플랫치노', '클레임요거트 플랫치노', '클레임 요거트플랫치노', '클레임요거트플랫치노', '풀네임 요거트 플랫치노', '풀네임요거트 플랫치노', '풀네임 요거트플랫치노', '풀네임요거트플랫치노', '플랜 요거트 플랫치노', '플랜요거트 플랫치노', '플랜 요거트플랫치노', '플랜요거트플랫치노', '블랙 요거트 플랫치노', '블랙요거트 플랫치노', '블랙 요거트플랫치노', '블랙요거트플랫치노', '프레임 요거트 플랫치노', '프레임요거트 플랫치노', '프레임 요거트플랫치노', '프레임요거트플랫치노', '플레인 요거트 플래티넘', '플레인요거트 플래티넘', '플레인 요거트플래티넘', '플레인요거트플래티넘', '플레임 요거트 플래티넘', '플레임요거트 플래티넘', '플레임 요거트플래티넘', '플레임요거트플래티넘', '플레이 요거트 플래티넘', '플레이요거트 플래티넘', '플레이 요거트플래티넘', '플레이요거트플래티넘', '플라잉 요거트 플래티넘', '플라잉요거트 플래티넘', '플라잉 요거트플래티넘', '플라잉요거트플래티넘', '플레잉 요거트 플래티넘', '플레잉요거트 플래티넘', '플레잉 요거트플래티넘', '플레잉요거트플래티넘', '클레이 요거트 플래티넘', '클레이요거트 플래티넘', '클레이 요거트플래티넘', '클레이요거트플래티넘', '클레임 요거트 플래티넘', '클레임요거트 플래티넘', '클레임 요거트플래티넘', '클레임요거트플래티넘', '풀네임 요거트 플래티넘', '풀네임요거트 플래티넘', '풀네임 요거트플래티넘', '풀네임요거트플래티넘', '플랜 요거트 플래티넘', '플랜요거트 플래티넘', '플랜 요거트플래티넘', '플랜요거트플래티넘', '블랙 요거트 플래티넘', '블랙요거트 플래티넘', '블랙 요거트플래티넘', '블랙요거트플래티넘',  '프레임 요거트 플래티넘', '프레임요거트 플래티넘', '프레임 요거트플래티넘', '프레임요거트플래티넘'], ['블루베리 요거트 플랫치노', '블루베리요거트 플랫치노', '블루베리 요거트플랫치노', '블루베리요거트플랫치노', '블루 베리 요거트 플랫치노', '블루 베리요거트 플랫치노', '블루 베리 요거트플랫치노', '블루 베리요거트플랫치노', '블루베리 요거트 플래티넘', '블루베리요거트 플래티넘', '블루베리 요거트플래티넘', '블루베리요거트플래티넘', '블루 베리 요거트 플래티넘', '블루 베리요거트 플래티넘', '블루 베리 요거트플래티넘', '블루 베리요거트플래티넘'], ['딸기 요거트 플랫치노', '딸기요거트 플랫치노', '딸기 요거트플랫치노', '딸기요거트플랫치노', '딸기 요거트 플래티넘', '딸기요거트 플래티넘', '딸기 요거트플래티넘', '딸기요거트플래티넘'], ['망고 플랫치노', '망고 플래티넘', '망고플래티넘'], ['꿀복숭아 플랫치노', '꿀 복숭아 플랫치노', '꿀 복숭아플랫치노', '꿀복숭아 플래티넘', '꿀복숭아플래티넘', '꿀 복숭아 플래티넘', '꿀 복숭아플래티넘'], ['초콜릿 칩 플랫치노', '초콜릿 칩플랫치노', '초콜릿칩 플랫치노', '초콜릿칩플랫치노', '초콜릿이 플랫치노', '초콜릿이플랫치노', '초콜릿 칩 플래티넘', '초콜릿 칩플래티넘', '초콜릿칩 플래티넘', '초콜릿칩플래티넘', '초콜릿이 플래티넘', '초콜릿이플래티넘']], [['소금빵', '소금방', '소금법', '좋은 방', '좋은방'], ['플레인 크로플', '플레임 크로플', '플레임크로플', '플레이 크로플', '플레이크로플', '플라잉 크로플', '플라잉크로플', '플레잉 크로플', '플레잉크로플', '클레이 크로플', '클레이크로플', '클레임 크로플', '클레임크로플', '풀네임 크로플', '풀네임크로플', '플랜 크로플', '플랜크로플', '블랙 크로플', '블랙크로플', '프레임 크로플', '프레임크로플', '플레인 프로필', '플레인프로필', '플레임 프로필', '플레임프로필', '플레이 프로필', '플레이프로필', '플라잉 프로필', '플라잉프로필', '프레임 프로필', '프레임프로필', '플레잉 프로필', '플레잉프로필', '클레이 프로필', '클레이프로필', '클레임 프로필', '클레임프로필', '풀네임 프로필', '풀네임프로필', '플랜 프로필', '플랜프로필', '블랙 프로필', '블랙프로필', '플레인 클오클', '플레인클오클', '플레임 클오클', '플레임클오클', '플레이 클오클', '플레이클오클', '플라잉 클오클', '플라잉클오클', '플레잉 클오클', '플레잉클오클', '클레이 클오클', '클레이클오클', '클레임 클오클', '클레임클오클', '풀네임 클오클', '풀네임클오클', '플랜 클오클', '플랜클오클', '블랙 클오클', '블랙클오클', '프레임 클오클', '프레임클오클', '플랭크 로플', '플랭크로플'], ['토피넛 크로플', '토피노 크로플', '토피노크로플', '토피넛 프로필', '토피넛프로필', '토피노 프로필', '토피노프로필', '토피넛 클오클', '토피넛클오클', '토피노 클오클', '토피노클오클'], ['생크림 와플', '생크림 어플', '생크림어플'], ['플레인 와플', '플레임 와플', '플레임와플', '플레이 와플', '플레이와플', '플라잉 와플', '플라잉와플', '플레잉 와플', '플레잉와플', '클레이 와플', '클레이와플', '클레임 와플', '클레임와플', '풀네임 와플', '풀네임와플', '플랜 와플', '플랜와플', '블랙 와플', '블랙와플', '프레인 와플', '프레임 와플', '플레인 어플', '플레인어플', '플레임 어플', '플레임어플', '플레이 어플', '플레이어플', '플라잉 어플', '플라잉어플', '플레잉 어플', '플레잉어플', '클레이 어플', '클레이어플', '클레임 어플', '클레임어플', '풀네임 어플', '풀네임어플', '플랜 어플', '플랜어플', '블랙 어플', '블랙어플', '프레인 어플', '프레임 어플'], ['메이플 와플', '메이플 어플', '메이플어플'], ['초콜릿 마카롱', '초콜릿 마카롱'], ['산딸기 마카롱', '산 딸기 마카롱', '산 딸기마카롱'], ['스트로베리 치즈 마카롱', '스트로베리치즈 마카롱', '스트로베리 치즈마카롱'], ['쿠키 앤 크림 마카롱', '쿠키앤 크림 마카롱', '쿠키 앤 크림마카롱'],['햄앤치즈샌드위치', '햄 앤 치즈 샌드위치', '햄 앤 치즈샌드위치', '햄 앤치즈 샌드위치', '햄앤 치즈 샌드위치', '햄 앤치즈샌드위치', '햄앤 치즈샌드위치', '햄앤치즈 샌드위치', '헬렌치즈샌드위치', '헬렌 치즈샌드위치', '헬렌치즈 샌드위치', '헬렌 치즈 샌드위치', '헤맨치즈샌드위치', '헤맨 치즈샌드위치', '헤맨치즈 샌드위치', '헤맨 치즈 샌드위치'], ['초코 티라미수', '초코 티라미슈', '초코티라미슈'], ['수플레 치즈 케이크', '수플레치즈 케이크', '수플레 치즈케이크', '수플레치즈케이크', '스플릿 치즈 케이크', '스플릿치즈 케이크', '스플릿 치즈케이크', '스플릿치즈케이크', '수플레 치즈 케익', '수플레치즈 케익', '수플레 치즈케익', '수플레치즈케익', '스플릿 치즈 케익', '스플릿치즈 케익', '스플릿 치즈케익', '스플릿치즈케익'], ['데블스 초코 케이크', '데블스초코 케이크', '데블스 초코케이크', '데블스초코케이크', '데빌스 초코 케이크', '데빌스초코 케이크', '데빌스 초코케이크', '데빌스초코케이크', '데비스 초코 케이크', '데비스초코 케이크', '데비스 초코케이크', '데비스초코케이크', '데블스 초코 케익', '데블스초코 케익', '데블스 초코케익', '데블스초코케익', '데빌스 초코 케익', '데빌스초코 케익', '데빌스 초코케익', '데빌스초코케익', '데비스 초코 케익', '데비스초코 케익', '데비스 초코케익', '데비스초코케익'], ['허니 카라멜 브레드', '허니카라멜 브레드', '허니 카라멜브레드', '허니카라멜브레드', '허니카라 브레드', '허니카라브레드', '허니카라 메일 브레드', '허니카라 메일브레드', '허니카라메일 브레드', '허니카라메일브레드', '코니카 밀브레드', '코니카밀브레드'], ['메이플 넛 브레드', '메이플넛 브레드', '메이플 넛브레드', '메이플넛브레드', '메이플 러브 브레드', '메이플러브 브레드', '메이플 러브브레드', '메이플러브브레드', '메이플로 브레드', '메이플로브레드'], ['스노우 쿠키슈', '스노우쿠키슈', '스노우 쿠키즈', '스노우쿠키즈', '스노우 쿠키 주', '스노우쿠키 주'], ['초코칩 머핀', '초코칩 먹긴', '초코칩먹긴'], ['크림치즈 머핀', '크림 치즈 머핀', '크림 치즈머핀', '크림치즈머핀', '크림 치즈 먹긴', '크림 치즈먹긴', '크림치즈 먹긴', '크림치즈먹긴'], ['블루베리 머핀', '블루베리 먹긴', '블루베리먹긴']]
Names = ['아메리카노', '카페라떼', '바닐라라떼', '카라멜마끼야또', '콜드브루라떼', '흑당콜드브루'], ['오리진쉐이크', '딸기쉐이크', '더블초코칩 쉐이크', '초코쿠키쉐이크', '피스타치오쉐이크', '레몬에이드', '자몽에이드', '청포도에이드'], ['플레인요거트플랫치노', '블루베리요거트플랫치노', '딸기요거트플랫치노', '망고플랫치노', '꿀복숭아플랫치노', '초콜릿칩플랫치노'], ['소금빵', '플레인크로플', '토피넛크로플', '생크림와플', '플레인와플', '메이플와플', '초콜릿마카롱', '산딸기마카롱', '스트로베리치즈마카롱', '쿠키앤크림마카롱','햄앤치즈샌드위치', '초코티라미수', '수플레치즈케이크', '데블스초코케이크', '허니카라멜브레드', '메이플넛브레드', '스노우쿠키슈', '초코칩머핀', '크림치즈머핀', '블루베리머핀']
Names_eng = ['Americano', 'Caffe Latte', 'Vanilla Latte', 'Caramel Macchiato', 'Cold Brew Latte', 'Black Sugar Cold Brew'], ['Origin Shake', 'Strawberry Shake', 'Double ChocoChip Shake', 'Choco Cookie Shake', 'Pistachio Shake', 'Lemon Ade', 'Grapefruit Ade', 'White Grape Ade'], ['Plain Yogurt Flatccino', 'Blueberry Yogurt Flatccino', 'Strawberry Yogurt Flatccino', 'Mango Flatccino', 'Honey Peach Flatccino', 'Chocolate Chip Flatccino'], ['Salted Butter Rolls', 'Plain Croffle', 'Toffeenut Croffle', 'Whipped Cream Waffle', 'Plain Waffle', 'Maple Waffle', 'Chocolate Macaron', 'Raspberry Macaron', 'Strawberry Cheese Macaron', 'Cookies & Cream Macaron', 'Ham & Cheese Sandwich', 'Choco Tiramisu', 'Souffle Cheese Cake', "Devil's Choco Cake", 'Honey Caramel Bread', 'Maple Nut Bread', 'Snow Cookie Choux', 'Choco Chip Muffin', 'Cream Cheese Muffin', 'Blueberry Muffin']
CntNames_r = [['한 잔',  '한 장', '한장', '한 전', '한전', '환전', '환 전', '한 정', '한정', '한 점', '한점', '1 잔', '1잔', '1 장', '1장', '1 전', '1전', '1정', '1 정', '1 점', '1점', '환기', '황제'], ['두 잔',  '두 장', '두장', '두 전', '두전', '두 정', '두정', '두 점', '두점', '2 잔', '2잔', '2 장', '2장', '2 전', '2전', '2정', '2 정', '2 점', '2점', '도전'], ['세 잔',  '세 장', '세장', '새 장', '새장', '세 전', '세전', '새 전', '새전', '세 정', '세정', '새 정', '새정', '세 점', '세점', '새 점', '새점', '3 잔', '3잔', '3 장', '3장', '3 전', '3전', '3정', '3 정', '3 점', '3점', '사전'], ['네 잔',  '네 장', '네장', '내 장', '내장', '네 전', '네전', '내 전', '내전', '네 정', '네정', '내 정', '내정', '네 점', '네점', '내 점', '내점', '4 잔', '4잔', '4 장', '4장', '4 전', '4전', '4정', '4 정', '4 점', '4점', '매장'], ['다섯 잔',  '다섯 장', '다섯장', '다섯 전', '다섯전', '다섯 정', '다섯정', '다섯 점', '다섯점', '5 잔', '5잔', '5 장', '5장', '5 전', '5전', '5정', '5 정', '5 점', '5점'], ['여섯 잔',  '여섯 장', '여섯장', '여섯 전', '여섯전', '여섯 정', '여섯정', '여섯 점', '여섯점', '6 잔', '6잔', '6 장', '6장', '6 전', '6전', '6정', '6 정', '6 점', '6점'], ['일곱 잔',  '일곱 장', '일곱장', '일곱 전', '일곱전', '일곱 정', '일곱정', '일곱 점', '일곱점', '7 잔', '7잔', '7 장', '7장', '7 전', '7전', '7정', '7 정', '7 점', '7점', '일곡점'], ['여덟 잔',  '여덟 장', '여덟장', '여덟 전', '여덟전', '여덟 정', '여덟정', '여덟 점', '여덟점', '8 잔', '8잔', '8 장', '8장', '8 전', '8전', '8정', '8 정', '8 점', '8점', '오늘 전', '오늘점', '오늘 잔', '오늘잔'], ['아홉 잔',  '아홉 장', '아홉장', '아홉 전', '아홉전', '아홉 정', '아홉정', '아홉 점', '아홉점', '9 잔', '9잔', '9 장', '9장', '9 전', '9전', '9정', '9 정', '9 점', '9점', '마곡점', '마곡전', '옥션'], ['열 잔',  '열 장', '열장', '열 전', '열전', '열 정', '열정', '열 점', '열점', '10 잔', '10잔', '10 장', '10장', '10 전', '10전', '10정', '10 정', '10 점', '10점']], [['한 개', '한길', '한 길'], ['두 개', '두 개'], ['세 개', '세 개'], ['네 개', '네 개'], ['다섯 개', '다섯 개'], ['여섯 개', '여섯 개'], ['일곱 개', '일곱 개'], ['여덟 개', '여덟 개'], ['아홉 개', '아홉 개'], ['열 개', '열 개']]
CntNames = ['한잔', '두잔', '세잔', '네잔', '다섯잔', '여섯잔', '일곱잔', '여덟잔', '아홉잔', '열잔'], ['한개', '두개', '세개', '네개', '다섯개', '여섯개', '일곱개', '여덟개', '아홉개', '열개'], [1, 2, 3, 4, 5, 6, 7, 8, 9 ,10]
NamesCnt = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
myOrders = [[], []]
input_text = ''

global microphone_on

microphone_on = False

file = open("txt/txtDetail.txt", "w")
file.write('음성 주문을 하시려면 버튼을 누르시오. ')
file.close()

fON = open("txt/ordName.txt", "w")
fON.write('')
fON.close()

fOC = open("txt/ordName.txt", "w")
fOC.write('')
fOC.close()

hereTogo = open("txt/hereTogo.txt", 'w')
hereTogo.write("togo")
hereTogo.close()

fSelLang = open('txt/selLang.txt', "w")
fSelLang.write("kr")
fSelLang.close()

fMyCnt = open('txt/myCnt.txt', "w")
fMyCnt.write("0")
fMyCnt.close()

fPay = open('txt/pay.txt', "w")
fPay.write("no")
fPay.close()

def code1_function():
    # 코드 1 내용을 여기에 넣으세요
    stop_listening = None  # stop_listening 변수를 전역으로 선언
    global microphone_on  # Add a global variable to track microphone state
    def listen(recognizer, audio):
        try:
            global input_text
            text = recognizer.recognize_google(audio, language='ko')
            answer(text)
        except sr.UnknownValueError:
            print('인식 실패')
            text = '죄송합니다. 인식에 실패하였습니다. 다시 말씀해주세요.'
            file = open("txt/txtDetail.txt", "w")
            file.write(text)
            file.close()
            speak(text)
        except sr.RequestError as e:
            print('요청 실패: {0}'.format(e))
        

    
    def start_listening():
        global stop_listening
        r = sr.Recognizer()
        m = sr.Microphone()
        stop_listening = r.listen_in_background(m, listen)

    def repName(Names, Names_r, input_text):
        for i in range(len(Names_r)):
            for j in range(len(Names_r[i])):
                for n in range(len(Names_r[i][j])):
                    input_text = input_text.replace(Names_r[i][j][n], Names[i][j])
        return input_text
 
    def voiceNameCnt(Names, CntNames, input_text):
        global myOrders
        answer_text = ''
        words = input_text.split()
        for i in range(len(words)):
            for a in range(len(Names)):
                for b in Names[a]:
                    if b in words[i]:
                        myOrders[0].append(b)
                        if (i+1 < len(words) ):
                            a = 1
                            for c in range(len(CntNames[0])):
                                if ( CntNames[0][c] in words[i+1] ):
                                    myOrders[1].append(CntNames[2][c])
                                    answer_text += '{} {} '.format(b, CntNames[0][c])
                                    a = 0
                                elif ( CntNames[1][c] in words[i+1] ):
                                    myOrders[1].append(CntNames[2][c])
                                    answer_text += '{} {} '.format(b, CntNames[1][c])
                                    a = 0
                            if ( words[i+1] == '하나'):
                                myOrders[1].append(CntNames[2][0])
                                answer_text += '{} 하나 '.format(b)
                                a = 0
                            elif a == 1 :
                                myOrders[1].append(CntNames[2][0])
                                answer_text += '{} 하나 '.format(b)
                        else:
                            myOrders[1].append(CntNames[2][0])
                            answer_text += '{} 하나 '.format(b)
        
        Orders(myOrders)

        if ('결제' in input_text):
            fON = open("txt/ordName.txt", "r")
            uOrdN = fON.readlines()
            fON.close()
            for i in range(0,len(uOrdN)):
                uOrdN='실행'
                break

        
            file = open("txt/txtDetail.txt", "w")
            if (uOrdN=='실행'):
                answer_text = "결제가 완료되었습니다."
                fPay = open('txt/pay.txt', "w")
                fPay.write("yes")
                fPay.close()
            else:
                answer_text = "죄송합니다. 물건을 담고 결제를 진행해 주세요."
                file.write('[VoiceOrder] : ' + answer_text)
            file.close()

        elif (answer_text != ''):
            answer_text += '추가하였습니다.'
            file = open("txt/txtDetail.txt", "w")
            file.write('[VoiceOrder] : ' + answer_text)
            file.close()
                            
        elif (answer_text == ''):
            answer_text = '죄송합니다. 다시 말씀해주세요.'
            file = open("txt/txtDetail.txt", "w")
            file.write(answer_text)
            file.close()
        speak(answer_text)
        myOrders = [[], []]
        

    # 대답
    def Orders(myOrders):
        for i in range(len(myOrders[0])):
            for a in range(len(Names)):
                for b in range(len(Names[a])):
                    if myOrders[0][i] == Names[a][b]:
                        NamesCnt[a][b] += myOrders[1][i]
                        
        fON = open("txt/ordName.txt", "w")
        fOC = open("txt/ordCnt.txt", "w") 
        for a in range(len(Names_r)):
            for b in range(len(Names_r[a])):
                if NamesCnt[a][b] != 0:
                    fON.write("{}\n".format(Names_r[a][b]))
                    fOC.write("{}\n".format(NamesCnt[a][b]))
        fON.close()
        fOC.close()

    def uOrdUpdate():
        global NamesCnt
        NamesCnt = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        fON = open("txt/ordName.txt", "r")
        fOC = open("txt/ordCnt.txt", "r")
        uOrdN = fON.readlines()
        uOrdC = fOC.readlines()
        fON.close()
        fOC.close()

        for i in range(0, len(uOrdN)):
            uOrdN[i]=uOrdN[i].strip('\n')
            uOrdC[i]=int(uOrdC[i].strip('\n'))
            for a in range(len(Names_r)):
                for b in range(len(Names_r[a])):
                    if (uOrdN[i]==Names_r[a][b]):
                        NamesCnt[a][b]=uOrdC[i]
                            

    def answer(input_text):
        answer_text = ''
        global myOrders
        if '안녕' in input_text:
            answer_text = '어서오세요 주문을 도와드리겠습니다.'

        input_text = repName(Names, Names_r2, input_text)
        input_text = repName(CntNames, CntNames_r, input_text)
        voiceNameCnt(Names, CntNames, input_text)
        if '종료' in input_text:
            answer_text = '종료하겠습니다'
            stop_listening(wait_for_stop=False)  # 더이상 듣지 않음
        else:
            answer_text = '죄송합니다 다시 말씀해주세요.'

    def speak(text):
        file_name = 'voice.mp3'
        tts = gTTS(text=text, lang='ko')
        tts.save(file_name)
        playsound(file_name)
        if os.path.exists(file_name):  # voice.mp3 파일 삭제
            os.remove(file_name)

    r = sr.Recognizer()
    m = sr.Microphone()

    speak('무엇을 도와드릴까요?')
    stop_listening = r.listen_in_background(m, listen)
    
    while True:
        uOrdUpdate()
        time.sleep(0.1)

def code2_function():
    # All this stuff is to interface with the Win32 API
    ###
    IID_Empty = GUID(
        '{00000000-0000-0000-0000-000000000000}')

    CLSID_MMDeviceEnumerator = GUID(
        '{BCDE0395-E52F-467C-8E3D-C4579291692E}')


    UINT32 = c_uint32
    REFERENCE_TIME = c_longlong


    class PROPVARIANT_UNION(Union):
            _fields_ = [
                ('lVal', LONG),
                ('uhVal', ULARGE_INTEGER),
                ('boolVal', VARIANT_BOOL),
                ('pwszVal', LPWSTR),
                ('puuid', GUID),
            ]


    class PROPVARIANT(Structure):
        _fields_ = [
            ('vt', VARTYPE),
            ('reserved1', WORD),
            ('reserved2', WORD),
            ('reserved3', WORD),
            ('union', PROPVARIANT_UNION),
        ]

        def GetValue(self):
            vt = self.vt
            if vt == VT_BOOL:
                return self.union.boolVal != 0
            elif vt == VT_LPWSTR:
                # return Marshal.PtrToStringUni(union.pwszVal)
                return self.union.pwszVal
            elif vt == VT_UI4:
                return self.union.lVal
            elif vt == VT_CLSID:
                # TODO
                # return (Guid)Marshal.PtrToStructure(union.puuid, typeof(Guid))
                return
            else:
                return "%s:?" % (vt)


    class WAVEFORMATEX(Structure):
        _fields_ = [
            ('wFormatTag', WORD),
            ('nChannels', WORD),
            ('nSamplesPerSec', WORD),
            ('nAvgBytesPerSec', WORD),
            ('nBlockAlign', WORD),
            ('wBitsPerSample', WORD),
            ('cbSize', WORD),
        ]


    class ERole(Enum):
        eConsole = 0
        eMultimedia = 1
        eCommunications = 2
        ERole_enum_count = 3


    class EDataFlow(Enum):
        eRender = 0
        eCapture = 1
        eAll = 2
        EDataFlow_enum_count = 3


    class DEVICE_STATE(Enum):
        ACTIVE = 0x00000001
        DISABLED = 0x00000002
        NOTPRESENT = 0x00000004
        UNPLUGGED = 0x00000008
        MASK_ALL = 0x0000000F


    class AudioDeviceState(Enum):
        Active = 0x1
        Disabled = 0x2
        NotPresent = 0x4
        Unplugged = 0x8


    class STGM(Enum):
        STGM_READ = 0x00000000


    class AUDCLNT_SHAREMODE(Enum):
        AUDCLNT_SHAREMODE_SHARED = 0x00000001
        AUDCLNT_SHAREMODE_EXCLUSIVE = 0x00000002

    class IAudioEndpointVolume(IUnknown):
        _iid_ = GUID('{5CDF2C82-841E-4546-9722-0CF74078229A}')
        _methods_ = (
            # HRESULT RegisterControlChangeNotify(
            # [in] IAudioEndpointVolumeCallback *pNotify);
            COMMETHOD([], HRESULT, 'NotImpl1'),
            # HRESULT UnregisterControlChangeNotify(
            # [in] IAudioEndpointVolumeCallback *pNotify);
            COMMETHOD([], HRESULT, 'NotImpl2'),
            # HRESULT GetChannelCount([out] UINT *pnChannelCount);
            COMMETHOD([], HRESULT, 'GetChannelCount',
                      (['out'], POINTER(UINT), 'pnChannelCount')),
            # HRESULT SetMasterVolumeLevel(
            # [in] float fLevelDB, [in] LPCGUID pguidEventContext);
            COMMETHOD([], HRESULT, 'SetMasterVolumeLevel',
                      (['in'], c_float, 'fLevelDB'),
                      (['in'], POINTER(GUID), 'pguidEventContext')),
            # HRESULT SetMasterVolumeLevelScalar(
            # [in] float fLevel, [in] LPCGUID pguidEventContext);
            COMMETHOD([], HRESULT, 'SetMasterVolumeLevelScalar',
                      (['in'], c_float, 'fLevel'),
                      (['in'], POINTER(GUID), 'pguidEventContext')),
            # HRESULT GetMasterVolumeLevel([out] float *pfLevelDB);
            COMMETHOD([], HRESULT, 'GetMasterVolumeLevel',
                      (['out'], POINTER(c_float), 'pfLevelDB')),
            # HRESULT GetMasterVolumeLevelScalar([out] float *pfLevel);
            COMMETHOD([], HRESULT, 'GetMasterVolumeLevelScalar',
                      (['out'], POINTER(c_float), 'pfLevelDB')),
            # HRESULT SetChannelVolumeLevel(
            # [in] UINT nChannel,
            # [in] float fLevelDB,
            # [in] LPCGUID pguidEventContext);
            COMMETHOD([], HRESULT, 'SetChannelVolumeLevel',
                      (['in'], UINT, 'nChannel'),
                      (['in'], c_float, 'fLevelDB'),
                      (['in'], POINTER(GUID), 'pguidEventContext')),
            # HRESULT SetChannelVolumeLevelScalar(
            # [in] UINT nChannel,
            # [in] float fLevel,
            # [in] LPCGUID pguidEventContext);
            COMMETHOD([], HRESULT, 'SetChannelVolumeLevelScalar',
                      (['in'], DWORD, 'nChannel'),
                      (['in'], c_float, 'fLevelDB'),
                      (['in'], POINTER(GUID), 'pguidEventContext')),
            # HRESULT GetChannelVolumeLevel(
            # [in]  UINT nChannel,
            # [out] float *pfLevelDB);
            COMMETHOD([], HRESULT, 'GetChannelVolumeLevel',
                      (['in'], UINT, 'nChannel'),
                      (['out'], POINTER(c_float), 'pfLevelDB')),
            # HRESULT GetChannelVolumeLevelScalar(
            # [in]  UINT nChannel,
            # [out] float *pfLevel);
            COMMETHOD([], HRESULT, 'GetChannelVolumeLevelScalar',
                      (['in'], DWORD, 'nChannel'),
                      (['out'], POINTER(c_float), 'pfLevelDB')),
            # HRESULT SetMute([in] BOOL bMute, [in] LPCGUID pguidEventContext);
            COMMETHOD([], HRESULT, 'SetMute',
                      (['in'], BOOL, 'bMute'),
                      (['in'], POINTER(GUID), 'pguidEventContext')),
            # HRESULT GetMute([out] BOOL *pbMute);
            COMMETHOD([], HRESULT, 'GetMute',
                      (['out'], POINTER(BOOL), 'pbMute')),
            # HRESULT GetVolumeStepInfo(
            # [out] UINT *pnStep,
            # [out] UINT *pnStepCount);
            COMMETHOD([], HRESULT, 'GetVolumeStepInfo',
                      (['out'], POINTER(DWORD), 'pnStep'),
                      (['out'], POINTER(DWORD), 'pnStepCount')),
            # HRESULT VolumeStepUp([in] LPCGUID pguidEventContext);
            COMMETHOD([], HRESULT, 'VolumeStepUp',
                      (['in'], POINTER(GUID), 'pguidEventContext')),
            # HRESULT VolumeStepDown([in] LPCGUID pguidEventContext);
            COMMETHOD([], HRESULT, 'VolumeStepDown',
                      (['in'], POINTER(GUID), 'pguidEventContext')),
            # HRESULT QueryHardwareSupport([out] DWORD *pdwHardwareSupportMask);
            COMMETHOD([], HRESULT, 'QueryHardwareSupport',
                      (['out'], POINTER(DWORD), 'pdwHardwareSupportMask')),
            # HRESULT GetVolumeRange(
            # [out] float *pfLevelMinDB,
            # [out] float *pfLevelMaxDB,
            # [out] float *pfVolumeIncrementDB);
            COMMETHOD([], HRESULT, 'GetVolumeRange',
                      (['out'], POINTER(c_float), 'pfMin'),
                      (['out'], POINTER(c_float), 'pfMax'),
                      (['out'], POINTER(c_float), 'pfIncr')))
    class PROPERTYKEY(Structure):
        _fields_ = [
            ('fmtid', GUID),
            ('pid', DWORD),
        ]

        def __str__(self):
            return "%s %s" % (self.fmtid, self.pid)


    class IPropertyStore(IUnknown):
        _iid_ = GUID('{886d8eeb-8cf2-4446-8d02-cdba1dbdcf99}')
        _methods_ = (
            # HRESULT GetCount([out] DWORD *cProps);
            COMMETHOD([], HRESULT, 'GetCount',
                      (['out'], POINTER(DWORD), 'cProps')),
            # HRESULT GetAt(
            # [in] DWORD iProp,
            # [out] PROPERTYKEY *pkey);
            COMMETHOD([], HRESULT, 'GetAt',
                      (['in'], DWORD, 'iProp'),
                      (['out'], POINTER(PROPERTYKEY), 'pkey')),
            # HRESULT GetValue(
            # [in] REFPROPERTYKEY key,
            # [out] PROPVARIANT *pv);
            COMMETHOD([], HRESULT, 'GetValue',
                      (['in'], POINTER(PROPERTYKEY), 'key'),
                      (['out'], POINTER(PROPVARIANT), 'pv')),
            # HRESULT SetValue([out] LPWSTR *ppstrId);
            COMMETHOD([], HRESULT, 'SetValue',
                      (['out'], POINTER(LPWSTR), 'ppstrId')),
            # HRESULT Commit();
            COMMETHOD([], HRESULT, 'Commit'))

    class IMMDevice(IUnknown):
        _iid_ = GUID('{D666063F-1587-4E43-81F1-B948E807363F}')
        _methods_ = (
            # HRESULT Activate(
            # [in] REFIID iid,
            # [in] DWORD dwClsCtx,
            # [in] PROPVARIANT *pActivationParams,
            # [out] void **ppInterface);
            COMMETHOD([], HRESULT, 'Activate',
                      (['in'], POINTER(GUID), 'iid'),
                      (['in'], DWORD, 'dwClsCtx'),
                      (['in'], POINTER(DWORD), 'pActivationParams'),
                      (['out'],
                       POINTER(POINTER(IUnknown)), 'ppInterface')),
            # HRESULT OpenPropertyStore(
            # [in] DWORD stgmAccess,
            # [out] IPropertyStore **ppProperties);
            COMMETHOD([], HRESULT, 'OpenPropertyStore',
                      (['in'], DWORD, 'stgmAccess'),
                      (['out'],
                      POINTER(POINTER(IPropertyStore)), 'ppProperties')),
            # HRESULT GetId([out] LPWSTR *ppstrId);
            COMMETHOD([], HRESULT, 'GetId',
                      (['out'], POINTER(LPWSTR), 'ppstrId')),
            # HRESULT GetState([out] DWORD *pdwState);
            COMMETHOD([], HRESULT, 'GetState',
            (['out'], POINTER(DWORD), 'pdwState')))

    class IMMDeviceCollection(IUnknown):
        _iid_ = GUID('{0BD7A1BE-7A1A-44DB-8397-CC5392387B5E}')
        _methods_ = (
            # HRESULT GetCount([out] UINT *pcDevices);
            COMMETHOD([], HRESULT, 'GetCount',
                      (['out'], POINTER(UINT), 'pcDevices')),
            # HRESULT Item([in] UINT nDevice, [out] IMMDevice **ppDevice);
            COMMETHOD([], HRESULT, 'Item',
                      (['in'], UINT, 'nDevice'),
            (['out'], POINTER(POINTER(IMMDevice)), 'ppDevice')))

    class IMMDeviceEnumerator(IUnknown):
        _iid_ = GUID('{A95664D2-9614-4F35-A746-DE8DB63617E6}')
        _methods_ = (
            # HRESULT EnumAudioEndpoints(
            # [in] EDataFlow dataFlow,
            # [in] DWORD dwStateMask,
            # [out] IMMDeviceCollection **ppDevices);
            COMMETHOD([], HRESULT, 'EnumAudioEndpoints',
                      (['in'], DWORD, 'dataFlow'),
                      (['in'], DWORD, 'dwStateMask'),
                      (['out'],
                      POINTER(POINTER(IMMDeviceCollection)), 'ppDevices')),
            # HRESULT GetDefaultAudioEndpoint(
            # [in] EDataFlow dataFlow,
            # [in] ERole role,
            # [out] IMMDevice **ppDevice);
            COMMETHOD([], HRESULT, 'GetDefaultAudioEndpoint',
                      (['in'], DWORD, 'dataFlow'),
                      (['in'], DWORD, 'role'),
                      (['out'], POINTER(POINTER(IMMDevice)), 'ppDevices')),
            # HRESULT GetDevice(
            # [in] LPCWSTR pwstrId,
            # [out] IMMDevice **ppDevice);
            COMMETHOD([], HRESULT, 'GetDevice',
                      (['in'], LPCWSTR, 'pwstrId'),
                      (['out'],
                      POINTER(POINTER(IMMDevice)), 'ppDevice')),
            # HRESULT RegisterEndpointNotificationCallback(
            # [in] IMMNotificationClient *pClient);
            COMMETHOD([], HRESULT, 'NotImpl1'),
            # HRESULT UnregisterEndpointNotificationCallback(
            # [in] IMMNotificationClient *pClient);
            COMMETHOD([], HRESULT, 'NotImpl2'))



    # Real Control Code

    class AudioUtilities(object):

        # Constructor
        def __init__(self):
            self.is_muted = False
    
        def GetMicrophones(self):
            deviceEnumerator = comtypes.CoCreateInstance(CLSID_MMDeviceEnumerator, IMMDeviceEnumerator, comtypes.CLSCTX_INPROC_SERVER)
            audio_input_devices = deviceEnumerator.GetDefaultAudioEndpoint(EDataFlow.eCapture.value, DEVICE_STATE.ACTIVE.value)
            if audio_input_devices is None:
                print("ERROR: No Active Audio Input devices detected!")
                sys.exit(0)
            return audio_input_devices
    
        def MuteMicrophone(self):
            mics = self.GetMicrophones()
            try:
                interface = mics.Activate(IAudioEndpointVolume._iid_, comtypes.CLSCTX_ALL, None)
                volume_control_ptr = ctypes.cast(interface, POINTER(IAudioEndpointVolume))
                volume_control_ptr.SetMute(True, None)
                self.is_muted = True
            except Exception as e:
                print("EXCEPTION [MuteMicrophone]: {}".format(e))
                #unhandled
        def UnMuteMicrophone(self):
            mics = self.GetMicrophones()
            try:
                interface = mics.Activate(IAudioEndpointVolume._iid_, comtypes.CLSCTX_ALL, None)
                volume_control_ptr = ctypes.cast(interface, POINTER(IAudioEndpointVolume))
                volume_control_ptr.SetMute(False, None)
                self.is_muted = False
            except Exception as e:
                print("EXCEPTION [MuteMicrophone]: {}".format(e))
                
    class CustomLabel(QLabel):
        def __init__(self, parent=None):
            super().__init__(parent)

            # 배경 이미지를 QLabel의 크기에 맞게 조절
            pixmap = QPixmap("image/this.jpg")  # 이미지 파일 경로를 적절하게 수정
            self.setPixmap(pixmap)
            self.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)  # 수평 및 수직 가운데 정렬
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # 확장 정책 설정

    class payWin(QDialog):

        def __init__(self):
            super().__init__()
            self.initUI()

        def initUI(self):

            def repName(Names, Names_r, input_text):
                for i in range(len(Names_r)):
                    for j in range(len(Names_r[i])):
                        input_text = input_text.replace(Names_r[i][j], Names[i][j])
                return input_text

            fOrdName = open('txt/ordName.txt', "r")
            fOrdCnt = open('txt/ordCnt.txt', "r")
            fTotalPrice = open('txt/totalPrice.txt', "r")
            fHereTogo = open('txt/hereTogo.txt', "r")
            fSelLang = open('txt/selLang.txt', "r")
            fMyCnt = open('txt/myCnt.txt', "r")

            ordName = fOrdName.readlines()
            ordCnt = fOrdCnt.readlines()
            totalPrice = fTotalPrice.read()
            HereTogo = fHereTogo.read()
            selLang = fSelLang.read()
            myCnt = fMyCnt.read()

            fOrdName.close()
            fOrdCnt.close()
            fTotalPrice.close()
            fHereTogo.close()
            fSelLang.close()
            fMyCnt.close()

            myCnt = int(myCnt)

            ordBool = 1 if selLang == 'kr' else 0
            ordDetail = '┏━━━━━━ 주 문  내 역 ━━━━━━┓\n\n' if selLang == 'kr' else '┏━━━━━  Order Detail  ━━━━━┓\n\n'
            
            if (ordBool):
                text = "주문번호 : {:>02}".format(myCnt)
                ordDetail += "{:^}\n".format(text)
                if (HereTogo=='here'):
                    text = "매장, 총금액 : {} ￦".format(totalPrice)
                elif (HereTogo=='togo'):
                    text = "포장, 총금액 : {} ￦".format(totalPrice)
                ordDetail += "{:^}\n".format(text)
            else:
                text = "Your No. {:>02}".format(myCnt)
                ordDetail += "{:^}\n".format(text)
                if (HereTogo=='here'):
                    text = "For Here, Total : $ {}".format(totalPrice)
                elif (HereTogo=='togo'):
                    text = "To Go, Total : $ {}".format(totalPrice)
                ordDetail += "{:^}\n".format(text)

            ordDetail +='\n'

            for i in range(0, 21):
                if (i<len(ordName)):
                    ordName[i]=ordName[i].strip('\n')
                    ordCnt[i]=(ordCnt[i].strip('\n'))

                    if(ordBool):
                        ordName[i] = repName(Names_r, Names_eng, ordName[i])
                        text = "{} {}".format(ordName[i], ordCnt[i])
                        ordDetail += "{:^}\n".format(text)
                    else:
                        ordName[i] = repName(Names_eng, Names_r, ordName[i])
                        text = "{} {}".format(ordName[i], ordCnt[i])
                        ordDetail += "{:^}\n".format(text)
                        

            ordDetail +='\n┗━━━━━━━━━━━━━━━━━┛'
            myCnt += 1

            fMyCnt = open('txt/myCnt.txt', "w")
            fMyCnt.write(str(myCnt))

            self.label = CustomLabel(self)
            self.label.setText(ordDetail)
            self.label.setStyleSheet("color: black;"
                "font-size: 18px;"
                "font-family: 'Noto Sans KR Medium', sans-serif;"
                "background-color: transparent")
            self.setWindowTitle(' ')
            self.setStyleSheet("color: black;"
                         "border-style: solid;"
                         "border-width: 0px;"
                         "border-color: #FA8072;"
                         "border-radius: 22px;"
                         "background-color: #F8FDFF")
            
            layout = QVBoxLayout()
            layout.addWidget(self.label)
            self.setLayout(layout)
            self.show()


    class MyApp(QWidget):

        def __init__(self):
            super().__init__()
            self.initUI()

        def initUI(self):

            self.selMenu = [0, 0, 0]
            self.menuImage = [['/coffee/아메리카노.png', '/coffee/카페라떼.png', '/coffee/바닐라라떼.png', '/coffee/카라멜마끼야또.png', '/coffee/콜드브루라떼.png', '/coffee/흑당콜드브루.png'],
                              ['/shake_ade/오리진쉐이크.png', '/shake_ade/딸기쉐이크.png', '/shake_ade/더블초코칩쉐이크.png', '/shake_ade/초코쿠키쉐이크.png', '/shake_ade/피스타치오쉐이크.png','/shake_ade/레몬에이드.png', '/shake_ade/자몽에이드.png', '/shake_ade/청포도에이드.png'],
                              ['/flatccino/플레인요거트플랫치노.png', '/flatccino/블루베리요거트플랫치노.png', '/flatccino/딸기요거트플랫치노.png', '/flatccino/망고플랫치노.png', '/flatccino/꿀복숭아플랫치노.png', '/flatccino/초콜릿칩플랫치노.png'],
                              ['/bread_dessert/소금빵.png', '/bread_dessert/플레인크로플.png', '/bread_dessert/토피넛크로플.png','/bread_dessert/생크림와플.png' ,'/bread_dessert/플레인와플.png', '/bread_dessert/메이플와플.png', '/bread_dessert/초콜릿마카롱.png',
                               '/bread_dessert/산딸기마카롱.png', '/bread_dessert/스트로베리치즈마카롱.png', '/bread_dessert/쿠키앤크림마카롱.png', '/bread_dessert/햄앤치즈샌드위치.png', '/bread_dessert/초코티라미수.png', '/bread_dessert/수플레치즈케이크.png',
                               '/bread_dessert/데블스초코케이크.png', '/bread_dessert/허니카라멜브레드.png', '/bread_dessert/메이플넛브레드.png', '/bread_dessert/스노우쿠키슈.png', '/bread_dessert/초코칩머핀.png', '/bread_dessert/크림치즈머핀.png',
                               '/bread_dessert/블루베리머핀.png']]

            self.VoiceOrder = QLabel('VoiceOrder', self)
            self.micRctng = QWidget(self)
            self.microphoneBtn = QPushButton('', self)
            self.txtRctng = QWidget(self)
            self.txtLabel = QLabel('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',self)
            self.srchRctng = QWidget(self)
            self.searchSmBtn =  QPushButton('', self)
            self.globeAltBtn =  QPushButton('', self)
            self.refreshBtn =  QPushButton('', self)
            self.menuBtn =  QPushButton('', self)
            self.slctRctng = QFrame(self)
            self.coffeeBtn =  QPushButton('커피', self)
            self.shakeAdeBtn = QPushButton('쉐이크 && 에이드', self)
            self.flatccinoBtn = QPushButton('플랫치노', self)
            self.breadDessertBtn = QPushButton('빵 && 디저트', self)
            self.menuBckgrRctng = QWidget(self)
            self.btmRctng = QWidget(self)
            self.ordTopRctng = QPushButton('주문내역', self)
            self.ordBckgrRctng = QWidget(self)
            self.sumTxtRctng = QWidget(self)
            self.hereBtnRctng = QPushButton('매장', self)
            self.goBtnRctng = QPushButton('포장', self)
            self.ordBtnRctng = QPushButton('결제', self)
            self.uOrd = QLabel('0000000000000000000000000000000000000000\n0000000000000000000000000000000000000000\n0000000000000000000000000000000000000000\n0000000000000000000000000000000000000000\n0000000000000000000000000000000000000000\n0000000000000000000000000000000000000000\n0000000000000000000000000000000000000000\n0000000000000000000000000000000000000000\n0000000000000000000000000000000000000000\n0000000000000000000000000000000000000000\n0000000000000000000000000000000000000000\n0000000000000000000000000000000000000000\n0000000000000000000000000000000000000000\n0000000000000000000000000000000000000000\n0000000000000000000000000000000000000000\n0000000000000000000000000000000000000000\n0000000000000000000000000000000000000000\n0000000000000000000000000000000000000000\n0000000000000000000000000000000000000000\n0000000000000000000000000000000000000000\n0000000000000000000000000000000000000000', self)
            self.sumTxt1 = QLabel('0000000000000', self)
            self.sumTxt2 = QLabel('0000000000000', self)

            self.ordVal = [[] for _ in range(21)]

            for row in range(0, 21):
                inp0 = f"minus{row}"
                inp1 = f"count{row}"
                inp2 = f"plus{row}"
                self.ordVal[row].append(inp0)
                self.ordVal[row].append(inp1)
                self.ordVal[row].append(inp2)

                button0 = QPushButton('', self)
                button2 = QPushButton('', self)
                label1 = QPushButton('12', self)
                button0.setStyleSheet("color: black;"
                                        "border-style: solid;"
                                        "background-color: transparent;")
                button2.setStyleSheet("color: black;"
                                        "border-style: solid;"
                                        "background-color: transparent;")
                label1.setStyleSheet("color: black;"
                         "font-size: 16px;"
                         "font-family: 'Noto Sans KR Medium', sans-serif;"
                         "background-color: transparent;") 

                self.ordVal[row][0] = button0
                self.ordVal[row][1] = label1
                self.ordVal[row][2] = button2
                setattr(self, inp0, button0)
                setattr(self, inp1, label1)
                setattr(self, inp2, button2)

            for i in range(0, 21):
                self.ordVal[i][0].setGeometry(1711, 234+(i*24), 24, 24)
                self.ordVal[i][1].setGeometry(1739, 233+(i*24), 23, 24)
                self.ordVal[i][2].setGeometry(1766, 234+(i*24), 24, 24)
                
                self.ordVal[i][0].setIcon(QIcon('icon/minus.png'))
                self.ordVal[i][0].setIconSize(QSize(11, 11))
                self.ordVal[i][0].clicked.connect(self.minusButton)
                            
                self.ordVal[i][2].setIcon(QIcon('icon/plus.png'))
                self.ordVal[i][2].setIconSize(QSize(11, 11))
                self.ordVal[i][2].clicked.connect(self.plusButton)

            self.sel1 =  QPushButton('', self)
            self.sel2 =  QPushButton('', self)
            self.sel3 =  QPushButton('', self)
        
            self.menuVal = []

            for row in range(10):
                inp = f"menu{row}"
                self.menuVal.append(inp)
                # 버튼 생성
                button = QPushButton('', self)
                # 버튼 스타일 설정
                button.setStyleSheet("color: black;"
                                        "border-style: solid;"
                                        "background-color: transparent;")
                # 버튼을 리스트에 추가
                self.menuVal[row] = button
                setattr(self, inp, button)
            for row in range(10):
                if(row<5):
                    self.menuVal[row].setGeometry(115+(row*258), 220, 248, 355)
                    self.menuVal[row].clicked.connect(self.menuButton)
                else:
                    self.menuVal[row].setGeometry(115+((row-5)*258), 220+365, 248, 355)
                    self.menuVal[row].clicked.connect(self.menuButton)
        
            self.menu0.setIcon(QIcon('image_kr'+self.menuImage[0][0]))
            self.menu0.setIconSize(QSize(248, 355))

            self.menu1.setIcon(QIcon('image_kr'+self.menuImage[0][1]))
            self.menu1.setIconSize(QSize(248, 355))

            self.menu2.setIcon(QIcon('image_kr'+self.menuImage[0][2]))
            self.menu2.setIconSize(QSize(248, 355))

            self.menu3.setIcon(QIcon('image_kr'+self.menuImage[0][3]))
            self.menu3.setIconSize(QSize(248, 355))

            self.menu4.setIcon(QIcon('image_kr'+self.menuImage[0][4]))
            self.menu4.setIconSize(QSize(248, 355))

            self.menu5.setIcon(QIcon('image_kr'+self.menuImage[0][5]))
            self.menu5.setIconSize(QSize(248, 355))


            self.VoiceOrder.setStyleSheet("color: black;"
                         "font-size: 36px;"
                         "font-family: 'Noto Sans KR Medium', sans-serif;") 

            self.micRctng.setStyleSheet("color: black;"
                         "border-style: solid;"
                         "border-width: 0px;"
                         "border-color: #FA8072;"
                         "border-radius: 22px;"
                         "background-color: #FD2222;")

            self.microphoneBtn.setStyleSheet("color: black;"
                         "border-style: solid;"
                         "background-color: transparent;")

            self.txtRctng.setStyleSheet("color: black;"
                         "border-style: solid;"
                         "border-width: 0px;"
                         "border-color: #FA8072;"
                         "border-radius: 22px;"
                         "background-color: #FFFFFF;")

            self.txtLabel.setStyleSheet("color: #7C7C7C;"
                         "font-size: 14px;"
                         "font-family: 'Noto Sans KR Medium', sans-serif;"
                         "background-color: transparent;") 

            self.srchRctng.setStyleSheet("color: black;"
                         "border-style: solid;"
                         "border-width: 0px;"
                         "border-color: #FA8072;"
                         "border-radius: 22px;"
                         "background-color: #FFFFFF;")

            self.searchSmBtn.setStyleSheet("color: black;"
                         "border-style: solid;"
                         "background-color: transparent;")

            self.globeAltBtn.setStyleSheet("color: black;"
                         "border-style: solid;"
                         "background-color: transparent;") 

            self.refreshBtn.setStyleSheet("color: black;"
                         "border-style: solid;"
                         "background-color: transparent;")
        
            self.menuBtn.setStyleSheet("color: black;"
                         "border-style: solid;"
                         "background-color: transparent;")

            self.slctRctng.setStyleSheet("color: black;"
                         "border-style: solid;"
                         "border-width: 0px;"
                         "border-radius: 30px;"
                         "background-color: #FEFFE4;")

            self.coffeeBtn.setStyleSheet("color: black;"
                         "font-size: 20px;"
                         "font-family: 'Noto Sans KR Medium', sans-serif;"
                         "background-color: transparent;")

            self.shakeAdeBtn.setStyleSheet("color: black;"
                         "font-size: 20px;"
                         "font-family: 'Noto Sans KR Medium', sans-serif;"
                         "background-color: transparent;")

            self.flatccinoBtn.setStyleSheet("color: black;"
                         "font-size: 20px;"
                         "font-family: 'Noto Sans KR Medium', sans-serif;"
                         "background-color: transparent;")

            self.breadDessertBtn.setStyleSheet("color: black;"
                         "font-size: 20px;"
                         "font-family: 'Noto Sans KR Medium', sans-serif;"
                         "background-color: transparent;")

            self.menuBckgrRctng.setStyleSheet("color: black;"
                         "border-style: solid;"
                         "border-width: 0px;"
                         "border-color: #FA8072;"
                         "border-top-left-radius: 25px;"
                         "border-top-right-radius: 25px;"
                         "background-color: #E8F9FF;")

            self.btmRctng.setStyleSheet("color: black;"
                         "border-style: solid;"
                         "border-width: 0px;"
                         "border-color: #FA8072;"
                         "border-bottom-left-radius: 25px;"
                         "border-bottom-right-radius: 25px;"
                         "background-color: #FFFFFF;")

            self.ordTopRctng.setStyleSheet("color: black;"
                         "font-size: 20px;"
                         "border-style: solid;"
                         "font-family: 'Noto Sans KR Medium', sans-serif;"
                         "border-style: solid;"
                         "border-width: 0px;"
                         "border-color: #FA8072;"
                         "border-top-left-radius: 25px;"
                         "border-top-right-radius: 25px;"
                         "background-color: #FFFFFF;")

            self.ordBckgrRctng.setStyleSheet("color: black;"
                         "border-style: solid;"
                         "border-width: 0px;"
                         "border-color: #FA8072;"
                         "background-color: #E8F9FF;")

            self.sumTxtRctng.setStyleSheet("color: black;"
                         "border-style: solid;"
                         "border-width: 0px;"
                         "border-color: #FA8072;"
                         "background-color: #FFFFFF;")

            self.hereBtnRctng.setStyleSheet("color: black;"
                         "font-size: 20px;"
                         "border-style: solid;"
                         "font-family: 'Noto Sans KR Medium', sans-serif;"
                         "border-style: solid;"
                         "border-width: 0px;"
                         "border-color: #FA8072;"
                         "background-color: #FFFFFF;")

            self.goBtnRctng.setStyleSheet("color: black;"
                         "font-size: 20px;"
                         "border-style: solid;"
                         "font-family: 'Noto Sans KR Medium', sans-serif;"
                         "border-style: solid;"
                         "border-width: 0px;"
                         "border-color: #FA8072;"
                         "background-color: #FEFFE4;")

            self.ordBtnRctng.setStyleSheet("color: black;"
                         "font-size: 36px;"
                         "border-style: solid;"
                         "font-family: 'Noto Sans KR Medium', sans-serif;"
                         "border-width: 0px;"
                         "border-color: #FA8072;"
                         "border-bottom-left-radius: 25px;"
                         "border-bottom-right-radius: 25px;"
                         "background-color: #FFFFFF;")

            self.sumTxt1.setStyleSheet("color: black;"
                         "font-size: 16px;"
                         "font-family: 'Noto Sans KR Medium', sans-serif;"
                         "background-color: transparent;") 

            self.sumTxt2.setStyleSheet("color: black;"
                         "font-size: 16px;"
                         "font-family: 'Noto Sans KR Medium', sans-serif;"
                         "background-color: transparent;") 

            self.uOrd.setStyleSheet("color: black;"
                         "font-size: 16px;"
                         "font-family: 'Noto Sans KR Medium', sans-serif;"
                         "background-color: transparent;") 
        
            self.sel1.setStyleSheet("color: black;"
                         "border-style: solid;"
                         "background-color: transparent;")

            self.sel2.setStyleSheet("color: black;"
                         "border-style: solid;"
                         "background-color: transparent;")

            self.sel3.setStyleSheet("color: black;"
                         "border-style: solid;"
                         "background-color: transparent;")
        
            shadows = []

            for i in range(20):
                inp = f"shadows{i}"
                shadow = QGraphicsDropShadowEffect()
                shadow.setBlurRadius(20)
                shadow.setColor(QColor(0, 0, 0, 100))
                shadow.setOffset(QPointF(0, 3))
                shadows.append(shadow)
                setattr(self, inp, shadow)

        
        
            self.VoiceOrder.setGeometry(105, 60, 194, 60)

            self.micRctng.setGraphicsEffect(self.shadows0)
            self.micRctng.setGeometry(321, 68, 44, 44)

            self.microphoneBtn.setIcon(QIcon('icon/microphone-off.png'))
            self.microphoneBtn.setIconSize(QSize(40, 40))
            self.microphoneBtn.setGeometry(323, 70, 40, 40)
            self.microphoneBtn.pressed.connect(self.muteButton)
            self.microphoneBtn.released.connect(self.muteButton)
            

            self.txtRctng.setGraphicsEffect(self.shadows1)
            self.txtRctng.setGeometry(385, 68, 1020, 44)

            self.txtLabel.move(405, 80)

            self.srchRctng.setGraphicsEffect(self.shadows2)
            self.srchRctng.setGeometry(1465, 68, 170, 44)

            self.searchSmBtn.setIcon(QIcon('icon/search-sm.png'))
            self.searchSmBtn.setIconSize(QSize(40, 40))
            self.searchSmBtn.setGeometry(1468, 70, 40, 40)

            self.globeAltBtn.setIcon(QIcon('icon/globe-alt.png'))
            self.globeAltBtn.setIconSize(QSize(40, 40))
            self.globeAltBtn.setGeometry(1655, 70, 40, 40)
            self.globeAltBtn.clicked.connect(self.langButton)

            self.refreshBtn.setIcon(QIcon('icon/refresh.png'))
            self.refreshBtn.setIconSize(QSize(40, 40))
            self.refreshBtn.setGeometry(1715, 70, 40, 40)
            self.refreshBtn.clicked.connect(self.refreshButton)

            self.menuBtn.setIcon(QIcon('icon/menu.png'))
            self.menuBtn.setIconSize(QSize(40, 40))
            self.menuBtn.setGeometry(1775, 70, 40, 40)

            self.slctRctng.setGraphicsEffect(self.shadows3)
            self.slctRctng.setGeometry(105, 140, 325, 60)

            self.coffeeBtn.setGeometry(105, 140, 325, 60)
            self.coffeeBtn.clicked.connect(self.moveButton)
            self.shakeAdeBtn.setGeometry(430, 140, 325, 60)
            self.shakeAdeBtn.clicked.connect(self.moveButton)
            self.flatccinoBtn.setGeometry(755, 140, 325, 60)
            self.flatccinoBtn.clicked.connect(self.moveButton)
            self.breadDessertBtn.setGeometry(1080, 140, 325, 60)
            self.breadDessertBtn.clicked.connect(self.moveButton)

            self.menuBckgrRctng.setGraphicsEffect(self.shadows4)
            self.menuBckgrRctng.setGeometry(105, 210, 1300, 740)

            self.btmRctng.setGraphicsEffect(self.shadows5)
            self.btmRctng.setGeometry(105, 960, 1300, 60)

            self.ordTopRctng.setGraphicsEffect(self.shadows6)
            self.ordTopRctng.setGeometry(1465, 140, 350, 60)

            self.ordBckgrRctng.setGraphicsEffect(self.shadows7)
            self.ordBckgrRctng.setGeometry(1465, 210, 350, 550)

            self.sumTxtRctng.setGraphicsEffect(self.shadows8)
            self.sumTxtRctng.setGeometry(1465, 770, 350, 60)

            self.hereBtnRctng.setGraphicsEffect(self.shadows9)
            self.hereBtnRctng.setGeometry(1465, 840, 175, 60)
            self.hereBtnRctng.clicked.connect(self.hereTogoButton)

            self.goBtnRctng.setGraphicsEffect(self.shadows10)
            self.goBtnRctng.setGeometry(1640, 840, 175, 60)
            self.goBtnRctng.clicked.connect(self.hereTogoButton)
            
            self.ordBtnRctng.setGraphicsEffect(self.shadows11)
            self.ordBtnRctng.setGeometry(1465, 910, 350, 110)
            self.ordBtnRctng.clicked.connect(lambda: self.openPayWin())
            self.ordBtnRctng.clicked.connect(self.refreshButton)

            self.uOrd.move(1493, 233)

            self.sumTxt1.setText('총      ')
            self.sumTxt1.move(1490, 787)

            self.sumTxt2.setText('￦')
            self.sumTxt2.setAlignment(Qt.AlignRight)
            self.sumTxt2.setGeometry(1552, 790, 250, 24)

            self.sel1.setIcon(QIcon("image/none.png"))
            self.sel1.setIconSize(QSize(248, 355))
            self.sel1.setGeometry(728, 983, 14, 14)
            self.sel1.clicked.connect(self.moveButton)

            self.sel2.setIcon(QIcon("icon/Ellipse 13.png"))
            self.sel2.setIconSize(QSize(248, 355))
            self.sel2.setGeometry(748, 983, 14, 14)

            self.sel3.setIcon(QIcon("image/none.png"))
            self.sel3.setIconSize(QSize(248, 355))
            self.sel3.setGeometry(768, 983, 14, 14)
            self.sel3.clicked.connect(self.moveButton)
            
            self.setWindowTitle('Stylesheet')
            self.setWindowFlag(Qt.FramelessWindowHint)
            self.setStyleSheet("background-color: #F8FDFF;")
            self.setGeometry(0, 0, 1920, 1080)
            self.show()
        
        def LabelUpdate(self, txt):
            self.txtLabel.setText(txt)

        def muteButton(self):
            global microphone_on

            if (self.selMenu[0]==0):
                if self.sender()==self.microphoneBtn:
                    if microphone_on is False:
                        test_audio_control.UnMuteMicrophone()
                        microphone_on = True
                        self.microphoneBtn.setIcon(QIcon('icon/microphone-on.png'))
                        self.microphoneBtn.setIconSize(QSize(40, 40))
                        self.microphoneBtn.setGeometry(323, 70, 40, 40)
                        self.micRctng.setStyleSheet("color: black;"
                             "border-style: solid;"
                             "border-width: 0px;"
                             "border-color: #FA8072;"
                             "border-radius: 22px;"
                             "background-color: #FFFFFF;")
                    else:
                        test_audio_control.MuteMicrophone()
                        microphone_on = False
                        self.microphoneBtn.setIcon(QIcon('icon/microphone-off.png'))
                        self.microphoneBtn.setIconSize(QSize(40, 40))
                        self.microphoneBtn.setGeometry(323, 70, 40, 40)
                        self.micRctng.setStyleSheet("color: black;"
                             "border-style: solid;"
                             "border-width: 0px;"
                             "border-color: #FA8072;"
                             "border-radius: 22px;"
                             "background-color: #FD2222;")
            elif (self.selMenu[0]==1):
                if self.sender()==self.microphoneBtn:
                    file = open("txt/txtDetail.txt", "w")
                    file.write('Sorry. We only support Korean for voice orders If you want to order by voice, Please change the language to Korean')
                    file.close()

        def langButton(self):
            
            self.selMenu[0] = 1 if self.selMenu[0] == 0 else 0
            lang = 'image_kr' if self.selMenu[0] == 0 else 'image_eng'
            txtDetail = "음성 주문을 하시려면 버튼을 누르시오." if self.selMenu[0] == 0 else 'Press the button to order with voice. '
            Cnt = 10 if self.selMenu[2] == 1 else 0

            file = open("txt/txtDetail.txt", "w")
            file.write(txtDetail)
            file.close()

            if(self.selMenu[0]==1):
                self.coffeeBtn.setText('COFFEE')
                self.shakeAdeBtn.setText('SHAKE && ADE')
                self.flatccinoBtn.setText('FLATCCINO')
                self.breadDessertBtn.setText('BREAD && DESSERT')
                self.ordTopRctng.setText('Your  Order')
                self.hereBtnRctng.setText('For Here')
                self.goBtnRctng.setText('To Go')
                self.ordBtnRctng.setText('Pay')
                fSelLang = open('txt/selLang.txt', "w")
                fSelLang.write("eng")
                fSelLang.close()


            else:
                self.coffeeBtn.setText('커피')
                self.shakeAdeBtn.setText('쉐이크 && 에이드')
                self.flatccinoBtn.setText('플랫치노')
                self.breadDessertBtn.setText('빵 && 디저트')
                self.ordTopRctng.setText(' 주문내역')
                self.hereBtnRctng.setText('매장')
                self.goBtnRctng.setText('포장')
                self.ordBtnRctng.setText('결제')
                fSelLang = open('txt/selLang.txt', "w")
                fSelLang.write("kr")
                fSelLang.close()

            if(self.slctRctng.geometry() == self.coffeeBtn.geometry()):
                for i in range(0, 10):
                    if(i<len(self.menuImage[0])):
                        self.menuVal[i].setIcon(QIcon(lang+self.menuImage[0][i]))
                        self.menuVal[i].setIconSize(QSize(248, 355))
                    else:
                        self.menuVal[i].setIcon(QIcon('image/none.png'))
                        self.menuVal[i].setIconSize(QSize(248, 355))

            elif(self.slctRctng.geometry() == self.shakeAdeBtn.geometry()):
                for i in range(0, 10):
                    if(i<len(self.menuImage[1])):
                        self.menuVal[i].setIcon(QIcon(lang+self.menuImage[1][i]))
                        self.menuVal[i].setIconSize(QSize(248, 355))
                    else:
                        self.menuVal[i].setIcon(QIcon('image/none.png'))
                        self.menuVal[i].setIconSize(QSize(248, 355))

            elif(self.slctRctng.geometry() == self.flatccinoBtn.geometry()):
                for i in range(0, 10):
                    if(i<len(self.menuImage[2])):
                        self.menuVal[i].setIcon(QIcon(lang+self.menuImage[2][i]))
                        self.menuVal[i].setIconSize(QSize(248, 355))
                    else:
                        self.menuVal[i].setIcon(QIcon('image/none.png'))
                        self.menuVal[i].setIconSize(QSize(248, 355))

            elif(self.slctRctng.geometry() == self.breadDessertBtn.geometry()):
                for i in range(0, 10):
                    if(i+Cnt<len(self.menuImage[3])):
                        self.menuVal[i].setIcon(QIcon(lang+self.menuImage[3][i+Cnt]))
                        self.menuVal[i].setIconSize(QSize(248, 355))
                    else:
                        self.menuVal[i].setIcon(QIcon('image/none.png'))
                        self.menuVal[i].setIconSize(QSize(248, 355))

            

            if (self.selMenu[0]==0):
                self.sumTxt1.setText('총      ')
            if (self.selMenu[0]==1):
                self.sumTxt1.setText('Total')

        def moveButton(self):
            lang = 'image_kr' if self.selMenu[0] == 0 else 'image_eng'
            if self.sender() in (self.coffeeBtn, self.shakeAdeBtn, self.flatccinoBtn, self.breadDessertBtn):
                current_rect = self.sender().geometry()
        
                new_rect = QRect(current_rect.x(), current_rect.y(),
                                 current_rect.width(), current_rect.height())
        
                animation = QPropertyAnimation(self.slctRctng, b'geometry')
                animation.setStartValue(new_rect)
                animation.setEndValue(current_rect)
                animation.start()

            if(self.sender().geometry() == self.coffeeBtn.geometry()):
                for i in range(0, 10):
                    if(i<len(self.menuImage[0])):
                        self.menuVal[i].setIcon(QIcon(lang+self.menuImage[0][i]))
                        self.menuVal[i].setIconSize(QSize(248, 355))
                    else:
                        self.menuVal[i].setIcon(QIcon('image/none.png'))
                        self.menuVal[i].setIconSize(QSize(248, 355))
                self.selMenu[1] = 0
                self.sel1.setIcon(QIcon("image/none.png"))
                self.sel2.setIcon(QIcon("icon/Ellipse 13.png"))
                self.sel3.setIcon(QIcon("image/none.png"))

            if(self.sender().geometry() == self.shakeAdeBtn.geometry()):
                for i in range(0, 10):
                    if(i<len(self.menuImage[1])):
                        self.menuVal[i].setIcon(QIcon(lang+self.menuImage[1][i]))
                        self.menuVal[i].setIconSize(QSize(248, 355))
                    else:
                        self.menuVal[i].setIcon(QIcon('image/none.png'))
                        self.menuVal[i].setIconSize(QSize(248, 355))
                self.selMenu[1] = 1
                self.sel1.setIcon(QIcon("image/none.png"))
                self.sel2.setIcon(QIcon("icon/Ellipse 13.png"))
                self.sel3.setIcon(QIcon("image/none.png"))

            if(self.sender().geometry() == self.flatccinoBtn.geometry()):
                for i in range(0, 10):
                    if(i<len(self.menuImage[2])):
                        self.menuVal[i].setIcon(QIcon(lang+self.menuImage[2][i]))
                        self.menuVal[i].setIconSize(QSize(248, 355))
                    else:
                        self.menuVal[i].setIcon(QIcon('image/none.png'))
                        self.menuVal[i].setIconSize(QSize(248, 355))
                self.selMenu[1] = 2
                self.sel1.setIcon(QIcon("image/none.png"))
                self.sel2.setIcon(QIcon("icon/Ellipse 13.png"))
                self.sel3.setIcon(QIcon("image/none.png"))

            if(self.sender().geometry() == self.breadDessertBtn.geometry()):
                for i in range(0, 10):
                    if(i<len(self.menuImage[3])):
                        self.menuVal[i].setIcon(QIcon(lang+self.menuImage[3][i]))
                        self.menuVal[i].setIconSize(QSize(248, 355))
                    else:
                        self.menuVal[i].setIcon(QIcon('image/none.png'))
                        self.menuVal[i].setIconSize(QSize(248, 355))
                self.selMenu[1] = 3
                self.sel1.setIcon(QIcon("icon/Ellipse 13.png"))
                self.sel2.setIcon(QIcon("image/none.png"))
                self.sel3.setIcon(QIcon("icon/Ellipse 16.png"))

            if(self.sender().geometry() == self.sel1.geometry() and self.selMenu[1] == 3):
                self.selMenu[2]=0
                for i in range(0, 10):
                    if(i<len(self.menuImage[3])):
                        self.menuVal[i].setIcon(QIcon(lang+self.menuImage[3][i]))
                        self.menuVal[i].setIconSize(QSize(248, 355))
                    else:
                        self.menuVal[i].setIcon(QIcon('image/none.png'))
                        self.menuVal[i].setIconSize(QSize(248, 355))
                self.sel1.setIcon(QIcon("icon/Ellipse 13.png"))
                self.sel3.setIcon(QIcon("icon/Ellipse 16.png"))

            elif(self.sender().geometry() == self.sel3.geometry() and self.selMenu[1] == 3):
                self.selMenu[2]=1
                for i in range(0, 10):
                    if(i+10<len(self.menuImage[3])):
                        self.menuVal[i].setIcon(QIcon(lang+self.menuImage[3][i+10]))
                        self.menuVal[i].setIconSize(QSize(248, 355))
                    else:
                        self.menuVal[i].setIcon(QIcon('image/none.png'))
                        self.menuVal[i].setIconSize(QSize(248, 355))
                self.sel1.setIcon(QIcon("icon/Ellipse 16.png"))
                self.sel3.setIcon(QIcon("icon/Ellipse 13.png"))

        def refreshButton(self):

            fON = open("txt/ordName.txt", "r")
            uOrdN = fON.readlines()
            fON.close()
            for i in range(0,len(uOrdN)):
                uOrdN='실행'
                break

            lang = 'image_kr' if self.selMenu[0] == 0 else 'image_eng'
            txtDetail = "음성 주문을 하시려면 버튼을 누르시오." if self.selMenu[0] == 0 else 'Press the button to order with voice. '
            if(self.sender().geometry() == self.refreshBtn.geometry() or (self.sender().geometry() == self.ordBtnRctng.geometry() and uOrdN=='실행')):
                for i in range(0, 10):
                    if(i<len(self.menuImage[0])):
                        self.menuVal[i].setIcon(QIcon(lang+self.menuImage[0][i]))
                        self.menuVal[i].setIconSize(QSize(248, 355))
                    else:
                        self.menuVal[i].setIcon(QIcon('image/none.png'))
                        self.menuVal[i].setIconSize(QSize(248, 355))
                self.selMenu[1] = 0
                self.sel1.setIcon(QIcon("image/none.png"))
                self.sel2.setIcon(QIcon("icon/Ellipse 13.png"))
                self.sel3.setIcon(QIcon("image/none.png"))
                current_rect = self.coffeeBtn.geometry()
                new_rect = QRect(current_rect.x(), current_rect.y(),
                                 current_rect.width(), current_rect.height())
                animation = QPropertyAnimation(self.slctRctng, b'geometry')
                animation.setStartValue(new_rect)
                animation.setEndValue(current_rect)
                animation.start()

                fON = open("txt/ordName.txt", "w")
                fON.write('')
                fON.close()

                fOC = open("txt/ordCnt.txt", "w")
                fOC.write('')
                fOC.close()

                file = open("txt/txtDetail.txt", "w")
                file.write(txtDetail)
                file.close()

                if (self.selMenu[0]==0):
                    self.sumTxt2.setText("0 ￦")
                elif (self.selMenu[0]==1):
                    self.sumTxt2.setText("$ 0")

                hereTogo = open("txt/hereTogo.txt", 'w')
                hereTogo.write("togo")
                hereTogo.close()

        

        def uOrdUpdate(self):

            def repName(Names, Names_r, input_text):
                for i in range(len(Names_r)):
                    for j in range(len(Names_r[i])):
                        input_text = input_text.replace(Names_r[i][j], Names[i][j])
                return input_text

            fON = open('txt/ordName.txt', "r")
            fOC = open('txt/ordCnt.txt', "r")
            uOrdN = fON.readlines()
            uOrdC = fOC.readlines()
            fON.close()
            fOC.close()
            uOrdN2=''

            for i in range(0, 21):
                if (i<len(uOrdN)):
                    uOrdN[i]=uOrdN[i].strip('\n')
                    uOrdC[i]=(uOrdC[i].strip('\n'))
                    self.ordVal[i][1].setText(str(uOrdC[i]))
                    self.ordVal[i][0].setIcon(QIcon('icon/minus.png'))
                    self.ordVal[i][0].setIconSize(QSize(11, 11))
                    self.ordVal[i][2].setIcon(QIcon('icon/plus.png'))
                    self.ordVal[i][2].setIconSize(QSize(11, 11))
                    if(self.selMenu[0]==0):
                        uOrdN[i] = repName(Names_r, Names_eng, uOrdN[i])
                    elif(self.selMenu[0]==1):
                        uOrdN[i] = repName(Names_eng, Names_r, uOrdN[i])
                    uOrdN2 += uOrdN[i] + '\n'
                else:
                    self.ordVal[i][0].setIcon(QIcon('image/none.png'))
                    self.ordVal[i][2].setIcon(QIcon('image/none.png'))
                    self.ordVal[i][1].setText('')
            self.uOrd.setText(uOrdN2)
            self.uOrd.setAlignment(Qt.AlignTop)
            
        def priceUpdate(self):
            NamesCnt = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
            fON = open("txt/ordName.txt", "r")
            fOC = open("txt/ordCnt.txt", "r")
            fTP = open("txt/totalPrice.txt", 'w')
            cntTP = 0
            uOrdN = fON.readlines()
            uOrdC = fOC.readlines()
            fON.close()
            fOC.close()

            for i in range(0, len(uOrdN)):
                uOrdN[i]=uOrdN[i].strip('\n')
                uOrdC[i]=int(uOrdC[i].strip('\n'))
                for a in range(len(Names_r)):
                    for b in range(len(Names_r[a])):
                        if (uOrdN[i]==Names_r[a][b]):
                            NamesCnt[a][b]=uOrdC[i]
                            if(self.selMenu[0]==0):
                                cntTP += price_kr[a][b]*NamesCnt[a][b]
                            elif(self.selMenu[0]==1):
                                cntTP += price_eng[a][b]*NamesCnt[a][b]
            
            if (self.selMenu[0]==0):
                txt = '{} ￦'.format(cntTP)
                self.sumTxt2.setText(txt)
            elif (self.selMenu[0]==1):
                cntTP /= 100
                txt = '$ {}'.format(cntTP)
                self.sumTxt2.setText(txt)
            fTP.write(str(cntTP))
            fTP.close()


        def minusButton(self):
            fON = open("txt/ordName.txt", "r")
            fOC = open("txt/ordCnt.txt", "r")
            uOrdN = fON.readlines()
            uOrdC = fOC.readlines()
            fON.close()
            fOC.close()
            for i in range(0, 21):
                if (i<len(uOrdN)):
                    uOrdN[i]=uOrdN[i].strip('\n')
                    uOrdC[i]=int(uOrdC[i].strip('\n'))
            for i in range(0, 21):
                if (i<len(uOrdN)):
                    if(self.sender().geometry() == self.ordVal[i][0].geometry()):
                        uOrdC[i] += -1
                        if (uOrdC[i]==0):
                            uOrdC.pop(i)
                            uOrdN.pop(i)
            
            wON = open("txt/ordName.txt", "w")
            wOC = open("txt/ordCnt.txt", "w")
            wONtxt = ''
            wOCtxt = ''
            for i in range(0, len(uOrdN)):
                wONtxt += '{}\n'.format(uOrdN[i])
                wOCtxt += '{}\n'.format(uOrdC[i])
            wON.write(wONtxt);
            wOC.write(wOCtxt);
            wON.close();
            wOC.close();

        def plusButton(self):
            fOC = open("txt/ordCnt.txt", "r")
            uOrdC = fOC.readlines()
            fOC.close()
            for i in range(0, 21):
                if (i<len(uOrdC)):
                    uOrdC[i]=int(uOrdC[i].strip('\n'))
                    if(self.sender().geometry() == self.ordVal[i][2].geometry()):
                        if (uOrdC[i]<99):
                            uOrdC[i] += 1
                        elif (uOrdC[i]>99):
                            uOrdC[i]=99
            wOC = open("txt/ordCnt.txt", "w")
            wOCtxt = ''
            for i in range(0, len(uOrdC)):
                wOCtxt += '{}\n'.format(uOrdC[i])
            wOC.write(wOCtxt);
            wOC.close();
        
        


        def menuButton(self):
            NamesCnt = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
            fON = open("txt/ordName.txt", "r")
            fOC = open("txt/ordCnt.txt", "r")
            uOrdN = fON.readlines()
            uOrdC = fOC.readlines()
            fON.close()
            fOC.close()

            for i in range(0, len(uOrdN)):
                uOrdN[i]=uOrdN[i].strip('\n')
                uOrdC[i]=int(uOrdC[i].strip('\n'))
                for a in range(len(Names_r)):
                    for b in range(len(Names_r[a])):
                        if (uOrdN[i]==Names_r[a][b]):
                            NamesCnt[a][b]=uOrdC[i]

            if (self.selMenu[1]==0):
                for i in range(0, len(NamesCnt[0])):
                    if (self.sender().geometry() == self.menuVal[i].geometry() and NamesCnt[0][i]<99):
                        NamesCnt[0][i] += 1
            elif (self.selMenu[1]==1):
                for i in range(0, len(NamesCnt[1])):
                    if (self.sender().geometry() == self.menuVal[i].geometry() and NamesCnt[1][i]<99):
                        NamesCnt[1][i] += 1
            elif (self.selMenu[1]==2):
                for i in range(0, len(NamesCnt[2])):
                    if (self.sender().geometry() == self.menuVal[i].geometry() and NamesCnt[2][i]<99):
                        NamesCnt[2][i] += 1
            elif (self.selMenu[1]==3 and self.selMenu[2]==0):
                for i in range(0, 10):
                    if (self.sender().geometry() == self.menuVal[i].geometry() and NamesCnt[3][i]<99):
                        NamesCnt[3][i] += 1
            elif (self.selMenu[1]==3 and self.selMenu[2]==1):
                for i in range(0, 10):
                    if (self.sender().geometry() == self.menuVal[i].geometry() and NamesCnt[3][i+10]<99):
                        NamesCnt[3][i+10] += 1
            
            fON = open("txt/ordName.txt", "w")
            fOC = open("txt/ordCnt.txt", "w")
            for a in range(len(Names_r)):
                for b in range(len(Names_r[a])):
                    if NamesCnt[a][b] != 0:
                        fON.write("{}\n".format(Names_r[a][b]))
                        fOC.write("{}\n".format(NamesCnt[a][b]))
            fON.close()
            fOC.close()
            
        def hereTogoUpdate(self):
            hereTogo = open("txt/hereTogo.txt", 'r')
            hTG = hereTogo.read()
            hereTogo.close()

            if (hTG=='here'):
                self.hereBtnRctng.setStyleSheet("color: black;"
                         "font-size: 20px;"
                         "border-style: solid;"
                         "font-family: 'Noto Sans KR Medium', sans-serif;"
                         "border-style: solid;"
                         "border-width: 0px;"
                         "border-color: #FA8072;"
                         "background-color: #FEFFE4;")
                self.goBtnRctng.setStyleSheet("color: black;"
                         "font-size: 20px;"
                         "border-style: solid;"
                         "font-family: 'Noto Sans KR Medium', sans-serif;"
                         "border-style: solid;"
                         "border-width: 0px;"
                         "border-color: #FA8072;"
                         "background-color: #FFFFFF;")

            elif (hTG=='togo'):
                self.hereBtnRctng.setStyleSheet("color: black;"
                         "font-size: 20px;"
                         "border-style: solid;"
                         "font-family: 'Noto Sans KR Medium', sans-serif;"
                         "border-style: solid;"
                         "border-width: 0px;"
                         "border-color: #FA8072;"
                         "background-color: #FFFFFF;")
                self.goBtnRctng.setStyleSheet("color: black;"
                         "font-size: 20px;"
                         "border-style: solid;"
                         "font-family: 'Noto Sans KR Medium', sans-serif;"
                         "border-style: solid;"
                         "border-width: 0px;"
                         "border-color: #FA8072;"
                         "background-color: #FEFFE4;")
            else:
                hereTogo = open("txt/hereTogo.txt", 'w')
                hereTogo.write("togo")
                hereTogo.close()


        def hereTogoButton(self):
            hereTogo = open("txt/hereTogo.txt", 'w')
            if (self.sender().geometry() == self.hereBtnRctng.geometry()):
                hereTogo.write("here")
            elif (self.sender().geometry() == self.goBtnRctng.geometry()):
                hereTogo.write("togo")
            hereTogo.close()

        def PayWinUpdate(self):
            fPay = open('txt/pay.txt', "r")
            pay = fPay.read()
            fPay.close()

            if (pay=='yes'):
                modal_dialog = payWin()
                modal_dialog.exec_()

                lang = 'image_kr' if self.selMenu[0] == 0 else 'image_eng'
                txtDetail = "음성 주문을 하시려면 버튼을 누르시오." if self.selMenu[0] == 0 else 'Press the button to order with voice. '

                for i in range(0, 10):
                    if(i<len(self.menuImage[0])):
                        self.menuVal[i].setIcon(QIcon(lang+self.menuImage[0][i]))
                        self.menuVal[i].setIconSize(QSize(248, 355))
                    else:
                        self.menuVal[i].setIcon(QIcon('image/none.png'))
                        self.menuVal[i].setIconSize(QSize(248, 355))
                self.selMenu[1] = 0
                self.sel1.setIcon(QIcon("image/none.png"))
                self.sel2.setIcon(QIcon("icon/Ellipse 13.png"))
                self.sel3.setIcon(QIcon("image/none.png"))
                current_rect = self.coffeeBtn.geometry()
                new_rect = QRect(current_rect.x(), current_rect.y(),
                                 current_rect.width(), current_rect.height())
                animation = QPropertyAnimation(self.slctRctng, b'geometry')
                animation.setStartValue(new_rect)
                animation.setEndValue(current_rect)
                animation.start()

                fON = open("txt/ordName.txt", "w")
                fON.write('')
                fON.close()

                fOC = open("txt/ordCnt.txt", "w")
                fOC.write('')
                fOC.close()

                file = open("txt/txtDetail.txt", "w")
                file.write(txtDetail)
                file.close()

                if (self.selMenu[0]==0):
                    self.sumTxt2.setText("0 ￦")
                elif (self.selMenu[0]==1):
                    self.sumTxt2.setText("$ 0")

                hereTogo = open("txt/hereTogo.txt", 'w')
                hereTogo.write("togo")
                hereTogo.close()

                fPay = open('txt/pay.txt', "w")
                fPay.write("no")
                fPay.close()

        def openPayWin(self):
            fON = open("txt/ordName.txt", "r")
            uOrdN = fON.readlines()
            fON.close()
            for i in range(0,len(uOrdN)):
                modal_dialog = payWin()
                modal_dialog.exec_()
                break


    if __name__ == '__main__':

        test_audio_control = AudioUtilities()
        app = QApplication(sys.argv)
        ex = MyApp()
        ex.show()
        ex2 = payWin()
        while True:
        
            file = open("txt/txtDetail.txt", "r")
            txtDetail = file.read()
            file.close()
            ex.LabelUpdate(txtDetail)
            ex.uOrdUpdate()
            ex.priceUpdate()
            ex.hereTogoUpdate()
            ex.PayWinUpdate()

            app.processEvents()
        sys.exit(app.exec_())

if __name__ == '__main__':
    
    p1 = Process(target=code1_function).start()
    p2 = Process(target=code2_function()).start()



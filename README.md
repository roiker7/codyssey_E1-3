# codyssey_E1-3
> AI가 계산하는 방식을 흉내 내는 작은 계산기 만들기 

## [프로젝트 한줄 설명]
서로 다른 N x N 행렬을 MAC 연산 구현 통해 패턴을 판별하는 Mini NPU 시뮬레이터   

## [개발 환경]
- Python 3.8 이상
- 외부 라이브러리 사용 금지(NumPy, pandas 등)
- 표준 라이브러리(json, time 등)만 허용
```
$python --version
Python 3.12.13

import sys
import time
import json
import re
```
## [실행 방법]
1. 저장소 복제
2. 메인 파일로 이동
3. 실행
```
$ git clone https://github.com/roiker7/codyssey_E1-3.guit
$ cd main
$ python main.py
```

## [프로젝트 목표]
- MAC(Multiply-Accumulate) 연산이 무엇이고, AI에서 왜 중요한지 설명할 수 있다.
- 입력 패턴과 필터를 곱하고 더해서 유사도(점수)를 계산하는 원리를 설명할 수 있다.
- data.json의 “키 규칙/라벨 규칙”을 해석하고, 프로그램 내부에서 라벨을 표준화(정규화)하는 이유를 설명할 수 있다.
- 부동소수점 오차가 판정에 어떤 영향을 주는지, 그리고 허용오차(epsilon) 기반 비교 정책이 필요한 이유를 설명할 수 있다.
- 크기별 연산 시간을 측정하고, 패턴 크기 증가에 따른 시간 복잡도 O(N²)를 근거와 함께 설명할 수 있다.
- 실패 케이스가 발생했을 때 원인을 “데이터/스키마 문제 vs 로직 문제 vs 수치 비교 문제”로 분리해 진단하고 개선할 수 있다.

## [프로젝트 구조와 각 파일 기능 설명]
├── code/                # 소스 코드 파일 
│   └── main.py
├── data/                # 데이터 파일 
│   └── data.json
└── README.md




































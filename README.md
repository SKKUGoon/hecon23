# Health Econ Project 2023

## Prep necessary modules

- Preproessor module
- Database connection module
- Distance calculation

## Follow up

In asset 

- EDI.xlsx: 약재 설명 파일. Info file

## 기존 연구

### Step 0. Data Preprocessing

Original user did the following:
1. Remove duplicates
  - Guranteed that there cannot be a duplicate.
  - Only keep the latest order-data.
2. Exclude data points
  - In a data-point, if the percentage of 0 >= 0.9, call it a Zero-inflation and remove.
  - Over-dispersion
  - Train set and test set pattern difference (wtf?)
3. Reduce Variables with PCA
  - 물류_OP, 물류_DX needs dimension downsizing. Use of Principal Component Analysis.
  - Timeseries index 1~215 is used for PCA. 
    - Cumulative proportion?
    - Broken-stick model
    - 19 Principal Components.  (75%)
    - ADD 물류_PT, and use 34 patient variables. 
4. Add time-series variables. 
  - date, month, and day.

Original user's result should be
* time-series: 56
* time points 243 days
* Training data: 181 days
* Test data: 28 days

<b>Additional Process</b>
1. SQL의 활용
  - 데이터 처리 및 불러오기에 최적화가 잘 되어 있어 적은 메모리 사용량을 유지하면서 데이터 조작 가능
  - 현재 데이터 사이즈가 작지만, 만약 큰 사이즈의 데이터가 들어왔을때 작업을 편리하게 할 수 있음. 
2. Python의 활용
  - Python ensures better performance than `R`.
  - Compatibility with `scikit-learn` package, `pytorch` 등 다양한 라이브러리 사용 가능.

## 연구 결과 복제 하는 법

### Step 0. Installation

1. Git을 이용해서 해당 코드 및 데이터파일을 가지고 온다. `asset` 폴더 만든 후, EDI, 및 물류 csv 파일 삽입. 
2. Python 설정 환경: `requirements.txt` 안의 pip 파일들 모두 설치 (`pyenv` 사용 권장)
3. MySQL 설정 환경: `macOS`의 경우, `homebrew`를 이용하여 `mysql`설치. 윈도우의 경우, mysqlworkbench를 이용하여 설치 권장. 
  - 대부분의 data storage 및 processing 은 mysql을 이용하여 이루어질 것이기 때문에 필수. 

### Step 1. Preprocessing

사용파일: `./data_lake.py`

1. SQL 안에 테이블들을 만든다. (사용 함수: `builder.create_table`, `builder.create_index`)
2. EDI, 물류_DX, OP, PT csv 파일에서 정리된 데이터를 업로드한다. (사용 함수: `builder.create_data`)
3. 기존 연구자가 수행한 프로세스 사용
  - Add Ts series: 
    * DX, OP, PT 의 날짜들 (YYYY-MM-DD)를 모두 포괄하는 dt (날짜) 테이블을 생성한후, Foreign key 를 이용해서 이어준다. (사용 함수: `builder.send_raw`)
  - Remove duplicates:
    * blah
  - Exclude data points:
    * Zero inflation: Remove if '0' populates more than 90% of the time series. 
  - Reducing Variables with PCA

사용파일: 

1. 기존 분석자가 수행한 Remove duplicates, Exclude data points, Reducing Variables with PCA, Add ts series 수행.
  - Add ts series: date, month, and day 를 나눠서 Column 형성. 

### Step 2. Replicate Distance Calc

[Original paper for distance calculation](http://www.cs.columbia.edu/~gravano/Papers/2015/sigmod2015.pdf) 에서 연구자가 참고문헌으로 사용한 논문 찾을 수 있음. 
[Github Repository](https://github.com/asardaes/dtwclust/blob/master/R/DISTANCES-sbd.R)는 참고문헌에 나온 SBD(Shape Based Distance)를 R로 재현함.
`./mod/distance` 는 참고문헌과, 깃헙을 참고하여 거리 계산 함수들을 파이썬으로 재현함. 재현한 함수는 다음과 같음:

1. Function that calculates NCC (Normalized Cross Correletion) sequence.
2. Function that calculates Shape Based Distance with NCC.

`1`는 연구자가 제시한 `cc_maker(ts1, ts2, w)` 함수와 동일. 
함수에서 `w` 는 Time lag로, `w` 가 음수라면, `ts1` 이 `0` 으로 padded 됨 (양수일 시 반대).
해당 함수는 `./mod/distance/ncc.py` 에서 `ncc_calculation`으로 재현되었으며, `w` 는 상위 함수에서 구현. 
`ncc_calculation` 함수의 `project_override` 변수 사용시, 논문의 `ncc_calculation` 함수에서, 분자에 절대값을 씌운
연구자가 제시한 distance calculation 방법 사용. 

`2` 는 연구자가 제시한`cc_distance` 함수의 core 부분을 재현함. 연구자에 따르면 `cc_distance(data)` 은 `(n * n)` Matrix of distance 를 생성함. 
이때 data는 `(n * p)` data matrix 사용. (where `n` denotes the number of time frame and `p` denotes the number of time series sequence.) 

### Step 3.


### Step 4. 

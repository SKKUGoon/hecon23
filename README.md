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

## Step 2. Replicate Distance Calc

The original paper for distance calculation can be found [here](http://www.cs.columbia.edu/~gravano/Papers/2015/sigmod2015.pdf). 
Also the github link that has the original source code can be found [here](https://github.com/asardaes/dtwclust/tree/master/R).
In the github repository, [this file](https://github.com/asardaes/dtwclust/blob/master/R/DISTANCES-sbd.R) replicates the aformentioned paper.
With the paper and github repository, `./mod/distance` replicates the essential part of the calculation, which is

1. Function that calculates NCC (Normalized Cross Correletion) sequcne
2. Function that calculates Shape Based Distance with NCC.

Essentially `1` replicates the original work's function of `cc_maker(ts1, ts2, w)`. 
`w` is time lag. If `w` is negative, `ts1` is padded with `0` and vice-versa.

`2` replicates the inner part of `cc_distance`. `cc_distance` Creates a `(n * n)` Matrix of distance 
with `(n * p)` data matrix, where `n` denotes the number of time frame and `p` denotes the number of time series sequence. 

## Step 3.


## Step 4. 

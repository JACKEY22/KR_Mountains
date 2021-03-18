# 팀 프로젝트 - 한국 100대 명산 게시판 [https://youtu.be/RAwLuS_L0nA]

### 적용기술
- 언어 : python
- 웹프레임워크 : django
- 데이터베이스 : mongodb
- 스크래핑 : bs4, selenium, schedule
  
### 기능
- 100대 명산을 군집화해 지도에 표기
- 등산에 필요한 날씨(온도, 풍향, 풍속, 일출, 일몰) 정보 및 정상 높이 제공
- 위급사항을 대비해 반경 10km 약국, 병원을 지도에 표기
- 숙박시설을 지도에 표기
- 산 검색  
 
 ### 데이터 
- 100대 명산 데이터 (블랙야크 openAPI)
- 100대 명산 반경 10km이내 약국 병원 데이터 (카카오 openAPI)
- 100대 명산 기상 데이터 (openweather openAPI)

### 피드백
- 반복해서 사용하는 코드는 함수를 만들어 하나의 기능으로 사용할 것
- 코드를 간결하게 작성하고 변수와 함수를 직관적으로 사용해 코드를 보고 흐름을 알 수 있게
- html, css, js 기본 지식 
- 1/10 페이지네이션이 아닌 보편적으로 사용되는 페이지네이션 구현
- 모델과 관계형 데이터베이스를 사용 


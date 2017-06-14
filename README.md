# Project#2 2014038059 오경수
* PyGame을 이용해서 나만의 테트리스를 구현하자
* 오픈소스로 웹상에 돌아다는 Tetrimino의 코드를 베이스로 별도로 추가하고 싶은 기능을 추가해 나만의 테트리스로 바꿔보자

## Tetris
![](http://postfiles16.naver.net/MjAxNzA2MTRfMjAz/MDAxNDk3NDE2MjA5ODA4.44xyEaiCS2EUz0If9sUHTU65L9kseIsmerxWyd7k4Kwg.cnRzF2crGaR5owsSPl9CnGxUh4VyjgCg-XNOx4AkGIEg.PNG.dhrudtn7187/noname01.png?type=w3)

![](http://postfiles10.naver.net/MjAxNzA2MTRfMTU3/MDAxNDk3NDE2MjEwMTIw.EmY6agUnSGU_Zp-ZmFC3pNFEFph7RzPLBfwP8Je69KIg.oHAmTCFyRoMiLTHvev46wV2IJG3TZBTK0P5dLbNwrGUg.PNG.dhrudtn7187/noname02.png?type=w3)

![](http://postfiles8.naver.net/MjAxNzA2MTRfMzcg/MDAxNDk3NDE2MjEwNTE2.IQVehzpjG-K3Ar5E0f2UQHziWCq9shn2PT2BUCsIypsg.on3SRC7zAanVSGoA6lFIL03xVZj6N4C6bnYExWtVvF0g.PNG.dhrudtn7187/noname03.png?type=w3)

### 기본기능
* 7종류의 블럭이 랜덤하게 내려옵니다.
* 특정 키를 눌러 블럭을 회전시킬 수 있습니다.
* 회전한 블럭이 아래에 쌓입니다.
* 한 줄 가득 블럭이 쌓이면 그 줄이 지워집니다.
#### 추가기능 
* 게임 시작시 저장한 노래 중 랜덤으로 재생
* 게임 시작화면을 생성하고 아무키나 클릭시 시작
* 스페이스바 클릭시 블럭이 한번에 바닥 또는 블럭에 충돌전까지 한번에 내려가면서 효과음 재생
* 한 줄 가득 블럭이 쌓여서 그 줄이 지워질 때 효과음 재생
* SCORE가 높아지다보면 LEVEL이 높아지는데 LEVEL이 높아지면 블럭의 떨어지는 속도 증가
* SCORE가 특정 범위안에 들어가면 블럭의 내려오는 속도 증가 및 다른 노래 재생
* 숫자키 0과 -로 볼륨 조절가능
* Q클릭시 음소거 다시 클릭시 음소거 해제
* P클릭시 게임 일시정지 아무키나 클릭시 게임 시작
* R클릭시 첫 화면으로 가면서 게임 재시작 가능
* P를 3번이상 클릭시 특정이벤트 발생(차후설명)
* NEXT인터페이스를 추가해서 다음 블럭이 무엇이 나오는지 알 수 있음
* 위에 기술한 버튼 클릭시의 기능들을 게임화면에 표시
* 게임화면에 현재시간표시
* 블럭을 손쉽게 쌓기 위해서 시간적인 도움이 되고자 화면에 라인을 표시
* 블럭이 충돌이 되서 움직이지 못하면 블럭색깔이 회색으로 변경

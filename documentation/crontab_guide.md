Crontab 사용
================

`cron`은 특정 시간에 원하는 작업들을 작동시키게 해주는 프로그램이다. 먼저 `crontab`을 사용하려면 아래 코드를 실행한
후 원하는 편집기를 고르면 된다.

    $ crontab -e

그리고 편집기에 들어가게 되면 실행하고 싶은 작업들을 아래와 같이 명령어를 사용해서 적으면 된다.

    * * * * *  수행할 명령어
    ┬ ┬ ┬ ┬ ┬
    │ │ │ │ │
    │ │ │ │ │
    │ │ │ │ └───────── 요일 (0 - 6) (0:일요일, 1:월요일, 2:화요일, …, 6:토요일)
    │ │ │ └───────── 월 (1 - 12)
    │ │ └───────── 일 (1 - 31)
    │ └───────── 시 (0 - 23)
    └───────── 분 (0 - 59)

예를 들면 `testing.py`라는 파이썬 파일이 `/home/somefolder/`라는 파일 안에 있다고 가정하자. 이 파일을
매분 돌리고 싶다면 아래와 같이 적으면 된다.

    * * * * * /home/somefolder/testing.py

그 외에도 다양한 명려어들을 사용할 수 있다.

**특정한 시간에 (매일 16시 25분) 실행**

    25 16 * * * /home/somefolder/testing.py

**매시 20분, 40분 마다 실행**

    20,40 * * * * /home/somefolder/testing.py

**매일 6시간 마다 실행 (00:00, 06:00, 12:00, 18:00)**

    * /6 * * * /home/somefolder/testing.py

**매일 6시간 마다 실행 (00:15, 06:15, 12:15, 18:15)**

    15 /6 * * * /home/somefolder/testing.py

**주말 (토요일, 일요일) 10시15분 마다 실행**

    15 10 * * 0,6 /home/somefolder/testing.py

-----

<br>

스케줄을 작성한 후 파이썬 파일을 실행시키고 싶으며 먼저 파이썬 스크립트 시작부분에 shebang (셔뱅)을 사용해서 가상환경에
파이썬이 있는 경로를 설정해야된다.

**testing.py**

    #!/home/somefolder/virtualenv/bin/python3
    
    파이썬 코드......

그리고 `chmod`를 사용하여 스크립트가 실행될 수 있게 한다.

    chmod u+x /home/somefolder/testing.py

-----

<br>

이번 프로젝트에서는 아래와 같이 `crontab`을 작성하였다. `.sh` 파일들은 `scp`로 파일이 모델 서버에서 왭 서버로
이동하는 코드가 적힌 쉘 스크립트이다.

    # PROJECT TELLUS CRONTAB
    
    #########################################
    # CURRENCY
    #########################################
    
    # running currency rates api every 6 hours 
    * */6 * * * /ProjectTellus/database/currency_auto.py
    
    # sending file to web server every 6 hours
    1 */6 * * * /ProjectTellus/database/autogencurrency.sh
    
    
    #########################################
    # MODEL
    #########################################
    
    # running model script at 00:00 every day 1 of the month
    0 0 1 * * /ProjectTellus/model/db2model.py
    
    # sending model files to web server at 00:15 every day 1 of the month
    15 0 1 * * /ProjectTellus/model/autogenmodel.sh
    
    
    #########################################
    # WEB CRAWLING
    #########################################
    
    # running crawling every 12 hours
    * */12 * * * /ProjectTellus/webcrawl/kicktraq_webcrawl.py

# PLP
for nlp project
## SECTION : Installation and User Guide

### [ 1 ] System Environment Requirement

1. Install [PostgreSQL](https://www.postgresql.org/download/) on the computer

2. Install [python >=3.9](https://www.python.org/downloads/)

3. Google Chrome (latest version)

4. Install latest git version

### [ 2 ] Prepare basic project enviorment and create an virtual enviorment of python

1. Create a folder in computer to storage the project file and open a terminal in this folder:

 >git clone https://github.com/dtepp/SMR.git

 >cd SMR

 >python -m venv venv

 >venv\Scripts\activate(windows) OR: source venv/bin/activate(mac)

 >pip install -r requirements.txt

2. Open pgAdmin program on your computer and create a Databases call SchoolMajor

3. Use the DataBase file to restore the SchoolMajor database
![image](https://user-images.githubusercontent.com/38468080/221105304-a615db54-6ae5-44c5-b949-60bee7ed187b.png)


### [ 3 ] Deploy the School Major Recommend system locally with virtual enviorment just created

1. Change the defalut PostgreSQL username and password to your database username and password in app.py:
![image](https://user-images.githubusercontent.com/38468080/221110246-98e99f15-b72b-4b43-95aa-52dd76ac143f.png)



1. In project folder terminal using virtual environment: 

 >flask db init

 >flask db migrate
 
 >flask db upgrade
 
 >flask run


### [ 4 ] Run the systems on browser
Go to URL using web browser**http://127.0.0.1:5000
Or: Directly click the link on the frontend terminal

### [ 5 ] DialogFlow configuration

1. Download the **mycryptobot.zip** file.

2. Open the [DialogFlow](https://dialogflow.cloud.google.com/) website and sign in with your account.

3. Go to **Settings**, and click **Export and Import**, and choose **IMPORT FROM ZIP**:
![img](https://raw.githubusercontent.com/Stanley7096/MD_Picture/main/dialog_set.png)

4. Download *ngrok.exe* or ngrok binary to your machine from ngrok.com, then:

>cd into the folder holding ngrok.exe

>ngrok.exe http 5000


5. Click **Fulfillment** on DialogFlow, and click the **Enable** button of the Webhook. Then copy the Forwarding link of the ngrok, and paste it in the URL line. Don't forget to add **/webhook** after the link: (Also DON'T forget to click SAVE at the bottom of the page)
![img](https://raw.githubusercontent.com/Stanley7096/MD_Picture/main/webhook.png)

### [ 6 ] Telegram Bot configuration

In your Dialogflow, please note the left sidebar, and click **Integrations** and scroll down, find **Telegram**.

Click **Telegram**, and paste the **Telegram Token**: 

6029920369:AAH43WlnyDpQCx6zHi0o0N2mG_tW9zezrzc

![img](https://raw.githubusercontent.com/Stanley7096/MD_Picture/main/telegram_set.png)

Then you can open your Telegram app, and search **"UniversityRecommenderBot"**, you will find a bot named **University_bot**, click it and talk to it!

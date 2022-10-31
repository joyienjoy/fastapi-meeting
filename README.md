# fastapi-meeting
Meeting Room Application using FastApi and Postgres Database

METHOD 1 - USING CONTAINERS (works in both Ubuntu n Centos)

Install Docker and Docker compose (https://github.com/joyienjoy/Installationfiles/tree/main/Docker-Installtion)
Install Git
mkdir Project      #Create a directory named Project
cd Project         #GO inside directory
git clone https://github.com/joyienjoy/fastapi-meeting.git        #Clone the project files into the directory

IMPORTANT:
If using Ubuntu 22.04, comment psycopg-binary in requirements file.

docker compose up       #command to build containers using docker compose

You can see the status of screen in image below. The application can be accessed on port 8000.
![image](https://user-images.githubusercontent.com/92083624/198936199-92ec3f95-81d0-49c2-a339-fd8e5cfa4c44.png)

Output screen when One post command is executed.
![image](https://user-images.githubusercontent.com/92083624/198936431-40f3c44b-5ade-4aed-ae52-6ff166a1684c.png)

DOCKERHUB Image: https://hub.docker.com/repository/docker/joydeep2022/fastapi-meeting for Application




METHOD 2 - Without Container - worked in Ubuntu 22.04

apt-get -y install python3-pip            #Install pip

#Install pip requirements

pip3 install fastapi

pip3 install pydantic

pip3 install uvicorn[standard]

pip3 install psycopg2-binary

pip3 install flask-sqlalchemy

#Install Postgres Database - Open Port 5432

sudo apt install postgresql postgresql-contrib

pg_ctlcluster 12 main start

sudo -u postgres psql           #enter inside database

postgres=# \password postgres     #Change password to 12345678 or as in database.py file

#Run the application

uvicorn main:app --host=0.0.0.0

![image](https://user-images.githubusercontent.com/92083624/198978873-7a1d060c-a6b6-4955-ad9b-afa82f3525a3.png)



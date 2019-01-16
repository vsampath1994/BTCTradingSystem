# BitcoinTradingSystem
CS 6360 Term Project 
* Michael Holcomb (mjh170630)
* Harshavardhan Nalajala (hxn170230)
* Vigneshwaran Sampath (vxs180021)


## Tools:
* Python 2
* Flask
* MySql
* Python2 Packages:
   * flask
   * flask-sqlalchemy
   * mysql-python
   * flask-login
   * flask-migrate
   * flask-wtf
   * flask-bootstrap
   * werkzeug.security
   * waitress (WSGI server)
   * configparser
   * WTForms
   * apscheduler (runs Gold/Silver update once a month)


## Install:
The application first requires that Python2, pip and MySQL are installed.  With a running instance of MySQL,  the following scripts should be run via the command-line in the root folder of the application.

```
mysql -u [root user] -p < MySql_Statements.sql
pip2 install -r requirements.txt
source ./set_env.sh
bash start_prod.sh 
```

Alternative to the last command, we can run it with `flask run`.

Optionally, at this point we can run a `flask shell` instance, and then we  run a set of scripts to create fake users and activity.

```
flask shell
>> import create_user
>> create_user.create_manager()
>> create_user.create_clients()
>> create_user.create_traders()
```

These commands create:
 1) 100 users with the usernames like 'abc12' and password 'hacker'; 
 2) 100 traders with usernames like 'trader23' and password 'hacker'; and 
 3) 1 manager with username 'manager' and password 'bitcoin.'

## Run:
```
flask run
```

## Demo
A live demo of the webpage is running at: [http://107.152.100.212:8080](http://107.152.100.212:8080).

Super-user access via SSH can be had with:
```
ssh cs6360@107.152.100.212 -p 2244
Password: bitcointrademanagementsystem
```


## References:
https://scotch.io/tutorials/build-a-crud-web-app-with-python-and-flask-part-one

export FLASK_CONFIG=development export FLASK_APP=run.py flask run

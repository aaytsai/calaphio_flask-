Hey everyone! Thanks for contributing to developing on Calaphio! PLEASE READ THIS BEFORE DOING ANYTHING ON THIS REPOSITORY

# What is this repository for? #

Calaphio By Flask (And Python)

# How do I get set up? #

### Setting Up Python Environment ###

We use Python 2.7 for compatibility with Dreamhost Python version. To install additional modules required to run the app, I recommend you use a virtualenv https://virtualenv.pypa.io/en/latest/ so you have a specialized Python environment to use for this webapp. Once you activate your environment, you can cd into the root of the repository and run

```
#!bash

pip install -r requirements.txt
```
to install all modules required by the app. Please update requirements.txt by running

```
#!bash

pip freeze > requirements.txt
```
whenever you add in a new required module.

### Setting up MySQL database for development ###
The webapp expects the database to be named website and accessible by the "website" user. Start up downloading a copy of the database from the calaphio server by running

```
#!bash

scp calaphio2@calaphio.com:~/website.tar.bz2 . 
```
Then untar this file

```
#!bash

tar -jxvf website.tar.bz2   
```
website.sql should be now in your directory.

Now you need to load the sql file into your database. To do so first create the website database. Type mysql on your console to start the mysql command line.

```
#!mysql
sudo mysql

mysql> CREATE DATABASE website;
mysql> GRANT ALL ON website.* TO 'website'@'localhost';
mysql> quit;
```
Now that your database is created, load the data into your database by running. This command should take awhile to finish

```
#!bash

sudo mysql website < website.sql
```

You should now have a database ready for development!

### Running Calaphio Server for development ###

Simply run

```
#!bash

python manage.py runserver
```
to start the development server. You should be able to reach your home page at http://localhost:5000.

### Starting Flask Shell ###
Occasionally, you would want to start a Python interpreter and interact with database models of our calaphio webapp. To do so, run

```
#!bash

python manage.py shell
```
to start an interpreter that would automatically set up connections with the local database for you to interact with.

### Deploying a new version of the webapp to Dreamhost ###
Just run 

```
#!bash

fab deploy
```
and it should automatically deploy the app on Dreamhost. Please don't deploy broken code and check if the website is fine after any deployment

# Contribution guidelines #

Please just make sure code is tested and is written well enough for other people to read it. Code quality is very important to make sure this codebase doesn't become unmanageable. PEP8 style guidelines are preferred https://www.python.org/dev/peps/pep-0008/ for nicely structured Python code. Don't do too many hacky things like hardcoding values or whatever so we can make this code nice and simple too. Also please use a rebase workflow for git http://randyfay.com/content/rebase-workflow-git so we don't have ugly merges in our git log.

# Who do I talk to if I need help? #

Talk to people in this older until someone can help you

* Current Webmasters
* Current AVP
* Past Webmasters
* Past AVP's
* BenjaminHoanLe at googlely mail dot com (Master Ben). Don't bother me too much though
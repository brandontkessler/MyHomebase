# Flask Template to Kick Start Application Build
This has wired up the configuration file, the database and migrations, basic user and auth models along with routing. Once configured, this structure can be used to build any application.

# Configuration
Follow the below steps to configure a clone of this repo to run as a flask application.

### Env Vars to Create for Dev
* export FLASK_APP=run.py
* export FLASK_DEBUG=True

### Configuration requires a file: dev_config.json
This gets stored in project root level directory.
Use the below JSON object and simply replace the values with ones specific to your app.

```
{
    "SECRET_KEY": "secret-ish_key",
    "MAIL_USERNAME": "flask_template_email@gmail.com",
    "MAIL_PASSWORD": "password",
    "MAIL_SUBJECT_PREFIX": "[Flask Template]",
    "MAIL_SENDER":  "Admin <flask_templates@gmail.com>",
    "DEV_DATABASE_URL": "postgresql://dev:dev@localhost/flask_template_dev",
    "TEST_DATABASE_URL": "postgresql://dev:dev@localhost/flask_template_test"
}
```

Note that the database URLs for Dev and Test should be updated with the user/password and the database name for the database you build like below:

```
"postgresql://{username}:{password}@localhost/{database_name}"
```

### Create postgres DBs for dev and test
From the psql command line use:

```
{user}=> create database flask_template_dev;
{user}=> create database flask_template_test;
```

Or replace with whatever you'd like to use to name the database.

Then, back in the terminal, creates the tables:

```
$ flask shell

>>> db.create_all()
>>> exit()
```

### API Keys
Create a file named "api_keys.json" that consists of the following:

```
{
  "GEOCODING_API": "<insert api key here>"
}
```

# APIs Used

### Geocoding
Geocoding uses the Mapquest API

The url is https://developer.mapquest.com/user/me/apps


### Weather
DarkSky is the API used to access weather

The url is https://darksky.net/dev/account



# Deployment

### Deploy Locally with Ngrok
1. Download ngrok from ngrok.com/download
2. Unzip the file, easy way for mac/linux:
  * go to downloads folder, right click file and click 'Copy "ngrok-stable....zip"'
  * go to terminal run `$ unzip <paste filepath/name here>`
  * test that it worked running `$ ./ngrok`
3. (Optional) Create an account and connect using the authtoken
4. Open another terminal, run application
  * `$ flask run`
5. Open tunnel on ngrok
  * `$ ./ngrok http 5000`
  * If you connected to your account, you can refresh the status page and see the tunnels online.
6. Copy the forwarding https address and paste in browser
  * Try accessing from your phone disconnected from wifi

Note: If you shut down the ngrok tunnel the app will no longer be available


### Deploy via Linode

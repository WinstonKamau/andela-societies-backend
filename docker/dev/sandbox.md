## Step 1 Clone the frontend and backend repositories.
e.g.
```
mkdir soc-app
cd soc-app
git clone https://github.com/AndelaOSP/andela-societies-frontend
git clone https://github.com/AndelaOSP/andela-societies-backend
```
Ensure port 4021, 4022 and 4023 are not running on your machine.
## Step 2 Start the frontend application
Change directory into the andela-societies-frontend application and run the command below:
```
cd andela-societies-frontend
make start
```

## Step 3 Set up the backend: Environment Variables
Change directory to the backend
```
cd ../andela-societies-backend
```
Ensure you have **ALL** your environment variables set in the src/.env file. 
```
PRIVATE_KEY_TEST=""
PUBLIC_KEY_TEST=""
PUBLIC_KEY=""
DEV_DATABASE=""
DATABASE_URL=""
APP_SETTINGS=""
ANDELA_API_URL=
DEV_TOKEN=
MAIL_GUN_URL=
MAIL_GUN_API_KEY=
MAIL_GUN_TEST="'Insert MailGun test thingy here'"
CELERY_BROKER_URL=""
CELERY_BACKEND="rpc://"
SENDER_CREDS=""
CIO=""
```

The value of these variables are obtained from the TTL, fellow developers in the team or the DevOps engineer in the team.

For the sandbox environment strictly:
* Do not place **export** before the variable assignment in the .env file as this application uses [dot-env](https://pypi.org/project/python-dotenv/)
e.g. This will not work as docker picks even the export name.
```
export PRIVATE_KEY_TEST=""
export PUBLIC_KEY_TEST=""
```
* Do not assign double quotes[""] to the DEV_TOKEN variable .
e.g
```
Wrong implementation:
DEV_TOKEN="ewogICIrKysrKysrKysrKyI6IHsKICAgICItLS0tLS0tLS0tIjogIj09PT09PT09PT09PSIsCiAgICAiLS0tLS0tLS0iOiAiwqLCosKiwqLCosKiwqLCosKiwqLCosKiIiwKICAgICItLS0tLS0tLS0iOiAiIyMjIyMjIyMjIyMjIyMiLAogICAgIi0tLS0tLS0tIjogIsKjwqPCo8KjwqPCo8KjwqPCo8KjwqPCo8KjwqPCo8KjIiwKICAgICItLS0tLS0tLSI6ICItLS0tLS0tLS0tLS0iLAogICAgIi0tLS0tLS0tLS0tLS0iOiAiZW1wdHkiLAogICAgIi0tLS0tLS0tLS0tLSI6IHsKICAgICAgIi0tLS0tLS0tLS0tIjogIi0tLS0tLS0tLS0tLS0tLS0iLAogICAgICAiLS0tLS0tLS0tIjogIi0tLS0tLS0tLS0tLS0tLS0tLS0tIgogICAgfQogICAgIioqKioqKioqKioiOiB7CiAgICAgICJub3RoaW5nIjogIm5vdGhpbmciLAogICAgICAiemlwIjogInppcCB6aXAgemlwIgp9CiAgfSwKICAiaWF0IjogMDAwMDAwMDAwMDAwLAogICJleHAiOiAwMDAwMDAwMDAwMDAwLAp9Cg=="

Correct implementation:
DEV_TOKEN=ewogICIrKysrKysrKysrKyI6IHsKICAgICItLS0tLS0tLS0tIjogIj09PT09PT09PT09PSIsCiAgICAiLS0tLS0tLS0iOiAiwqLCosKiwqLCosKiwqLCosKiwqLCosKiIiwKICAgICItLS0tLS0tLS0iOiAiIyMjIyMjIyMjIyMjIyMiLAogICAgIi0tLS0tLS0tIjogIsKjwqPCo8KjwqPCo8KjwqPCo8KjwqPCo8KjwqPCo8KjIiwKICAgICItLS0tLS0tLSI6ICItLS0tLS0tLS0tLS0iLAogICAgIi0tLS0tLS0tLS0tLS0iOiAiZW1wdHkiLAogICAgIi0tLS0tLS0tLS0tLSI6IHsKICAgICAgIi0tLS0tLS0tLS0tIjogIi0tLS0tLS0tLS0tLS0tLS0iLAogICAgICAiLS0tLS0tLS0tIjogIi0tLS0tLS0tLS0tLS0tLS0tLS0tIgogICAgfQogICAgIioqKioqKioqKioiOiB7CiAgICAgICJub3RoaW5nIjogIm5vdGhpbmciLAogICAgICAiemlwIjogInppcCB6aXAgemlwIgp9CiAgfSwKICAiaWF0IjogMDAwMDAwMDAwMDAwLAogICJleHAiOiAwMDAwMDAwMDAwMDAwLAp9Cg==
```

## Step 4 Start the backend
Ensure you are on the root of the folder andela-societies-backend and run the command below to start the backend application:
```
make start
```
If running the sandbox for the **first** time seed the database.
```
make seed
```

## Step 5 Other commands for the sandbox
While on the root of the folder for the frontend you can run the command: 
* `make help`: To determine all the commands you can run on the frontend.
* `make stop`: To stop the frontend application and delete running containers.
* `make tear`: To destroy resources for the frontend application. *Sometimes the network may not be deleted if the backend is running. Just ignore the error*

While on the root of the folder for the backend you can run the command:
* `make stop`: To stop the backend application and delete running containers.
* `make tear`: To destroy resources for the backend application. *Sometimes the network may not be deleted if the frontend is running. Just ignore the error. Also while starting the application again after running this command you'll have to seed the database since the postgres database is deleted with this command.*
* `make seed`: To seed the database and link cohorts to societies. Should be done once after running `make start` for the first time or when a `make tear` has been run before and you desire to start the sandbox again.
* `make help`: To determine all the commands you can run on the backend. **Note:** *you'll meet a plethora of commands that do not relate to the sandbox.*

## Step 6 View the database 
To view the database use the following credentials. (The database should be running.)
* host: 127.0.0.1
* user: soc
* password: soc
* database: soc-sandbox
* port: 4023

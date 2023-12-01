# Card Pay

## Setup instructions

### Backend DDD

- To run the flask app locally, run `./scripts/deploy_local.sh` from `backend_ddd` directory
    - Make sure to `source venv/bin/activate` in `backend_dd` before running the command to activate your virtual env
- Install packages for backend using `pip install -r requirements.txt` from `backend_ddd`
- To start the ngrok tunnel, run the command `ngrok http 5000`
    - Add auth token to get the verified http url or whatever that is but required warna weird errors
- Prod deployment `gcloud app deploy`

### Cloud SQL
- To connect to the PostgreSQL instance on the cloud, run `./cloud-sql-proxy cardpay-1:asia-south1:cardpay-dev -p 5433`
- To setup AVD: `gcloud auth application-default login`
- To run migrations run `pg-migrator postgres://postgres:"-3vjMTP4s>*aEDuG"@127.0.0.1:5433/cardpay-dev-db` in `backend_ddd/db/migrations` directory

### Frontend

#### Flutter

-   To create json serializable models for your dart classes run `flutter pub run build_runner build` in frontend-flutter directory
-   To add a package in flutter run `flutter pub add <package-name>` in frontend-flutter directory

### Admin scripts

-   To run the script, run `npm run start` in the admin directory
-   To run the script on dev db, run `npm run start-dev` in the admin directory

## Release steps

-   Increment the version in `pubspec.yaml` in frontend-flutter directory
-   Create an app bundle (android) using `flutter build appbundle` in frontend-flutter directory
-   Create an app bundle (iOS) using `flutter build ipa` in frontend-flutter directory





### Steps to backup the database:

-   1. Open the file `admin/src/index.ts`
-   2. Uncomment the line `saveFirestoreState();`
-   3. Open the terminal in `admin` directory
-   4. Run the following command, `npm run start` to run the script
-   5. A new file will be created with the name as the timestamp
-   6. In the file `admin/data_analytics.py`, uncomment the line `saveTransactionsToCsv()` at the end of file
-   7. Run `python data_analytics.py` in the admin directory
-   8. Viola! The `transactions.csv` will contain the updated transactions fresh from the database


## DEPRECATED

### Cardpay Web App

-   To run the localhost server on dev db, set `RUN_DEV = true` in `initialize-firebase.tsx`
    in the services folder

### Firebase functions

-   To deploy your cloud functions run `firebase deploy --only functions` in the backend directory
-   To run functions locally run `npm run serve` in the backend/functions directory
-   Run this command to sync backend with backend-dev `rsync -av --delete "backend/functions/src/" "backend-dev/functions/src"`
-   Functions structure:
    -   Log to display the arguments passed to the function
    -   Arguments check including authentication
    -   Log on all types of error occured


### Sync prod and dev db on CloudSQL on GCP
- Run prod proxy
- Create a backup of the prod db:
`pg_dump -h localhost -p 5433 -U postgres -d cardpay-prod-db -f dumpfile.sql`
- Close prod proxy

- Run dev proxy
- Restore from backup to the dev db
`psql -h localhost -p 5433 -U postgres -d cardpay-dev-db -f dumpfile.sql`
- Close dev proxy

### Setup GCP Application Default Credentials
- Install gcloud CLI
- Follow installation steps
- Setup credentials
`./google-cloud-sdk/bin/gcloud auth application-default login`
- Add project to path
`export GCLOUD_PROJECT=cardpay-1`

### Dev deployment
- Run `gcloud init` and initialize the development project
- Replace the connections in db with dev ones from env

#### Getting started, DEV onboarding
- Install python
- Create python venv
- Install requirements from `requirement.txt`
- Install and setup Github SSH keys if not already done
- Install PostgreSQL
- Setup db
- Run migrations
- Setup ADC, Application default credentials
- Add `.env`, `credentials-dev.json`, `credentials-prod.json` 
- Install Datagrip


#### Load testing
- Run the following command in `backend_ddd` to load test the APIs
- `locust -f locust_our_system.py --headless -u 100 -r 5 -t 1m --html report_doha.html`


#### API status codes
200 OK
The request succeeded. The result meaning of "success" depends on the HTTP method:

201 Created
The request succeeded, and a new resource was created as a result.
This is typically the response sent after POST requests, or some PUT requests.

400 Bad Request
The server cannot or will not process the request due to something
that is perceived to be a client error (e.g., malformed request syntax,
invalid request message framing, or deceptive request routing).

401 Unauthorized
Although the HTTP standard specifies "unauthorized", semantically this response means
"unauthenticated". That is, the client must authenticate itself to get the requested response.

404 Not Found
The server cannot find the requested resource. In the browser, this means the URL is
not recognized. In an API, this can also mean that the endpoint is valid but the resource
itself does not exist. Servers may also send this response instead of 403 Forbidden to hide
the existence of a resource from an unauthorized client. This response code is probably the most
well known due to its frequent occurrence on the web.

500 Internal Server Error
The server has encountered a situation it does not know how to handle.
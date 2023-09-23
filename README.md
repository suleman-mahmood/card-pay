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

shhh, triggering vendor portal deployment
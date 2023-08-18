# Card Pay

## Setup instructions

## Frontend (frontend-flutter)

-   To create json serializable models for your dart classes run `flutter pub run build_runner build` in frontend-flutter directory
-   To add a package in flutter run `flutter pub add <package-name>` in frontend-flutter directory

## Frontend (frontend-web)

-   To run the localhost server on dev db, set `RUN_DEV = true` in `initialize-firebase.tsx`
    in the services folder

### Release steps

-   Increment the version in `pubspec.yaml` in frontend-flutter directory
-   Create an app bundle using `flutter build appbundle` in frontend-flutter directory

## Backend

-   To deploy your cloud functions run `firebase deploy --only functions` in the backend directory
-   To run functions locally run `npm run serve` in the backend/functions directory
-   Run this command to sync backend with backend-dev `rsync -av --delete "backend/functions/src/" "backend-dev/functions/src"`
-   Functions structure:
    -   Log to display the arguments passed to the function
    -   Arguments check including authentication
    -   Log on all types of error occured


## Backend DDD
- To run the flask app server locally, run the command `flask --app api --debug run` in `backend_dd/api` directory
    - Make sure to `source venv/bin/activate` before running the command to activate your virtual env
- To start the ngrok tunnel, run the command `ngrok http 5000`
    - Add auth token to get the verified http url or whatever that is but required warna weird errors

## Admin

-   To run the script, run `npm run start` in the admin directory
-   To run the script on dev db, run `npm run start-dev` in the admin directory

### Steps to backup the database:

-   1. Open the file `admin/src/index.ts`
-   2. Uncomment the line `saveFirestoreState();`
-   3. Open the terminal in `admin` directory
-   4. Run the following command, `npm run start` to run the script
-   5. A new file will be created with the name as the timestamp
-   6. In the file `admin/data_analytics.py`, uncomment the line `saveTransactionsToCsv()` at the end of file
-   7. Run `python data_analytics.py` in the admin directory
-   8. Viola! The `transactions.csv` will contain the updated transactions fresh from the database

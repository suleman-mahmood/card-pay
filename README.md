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

## Admin

-   To run the script, run `npm run start` in the admin directory
-   To run the script on dev db, run `npm run start-dev` in the admin directory

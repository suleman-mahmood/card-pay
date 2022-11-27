# Card Pay

## Setup instructions

## Frontend (frontend-flutter)

-   To create json serializable models for your dart classes run `flutter pub run build_runner build` in frontend-flutter directory
-   To add a package in flutter run `flutter pub add <package-name>` in frontend-flutter directory

### Release steps

-   Increment the version in `pubspec.yaml` in frontend-flutter directory
-   Create an app bundle using `flutter build appbundle` in frontend-flutter directory

## Backend

-   To deploy your cloud functions run `firebase deploy --only functions` in the backend directory
-   To run functions locally run `npm run serve` in the backend/functions directory

## Admin

-   To run the script, run `npm run start` in the admin directory

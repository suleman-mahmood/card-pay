# Card Pay

## Setup instructions
## Frontend (flutter-frontend)
- To create json serializable models for your dart classes run `flutter pub run build_runner build`
- To add a package in flutter run `flutter pub add <package-name>`
### Release steps
- Increment the version in `pubspec.yaml`
- Create an app bundle using `flutter build appbundle`

## Backend
- To deploy your cloud functions run `firebase deploy --only functions` in the backend directory
- To run functions locally run `npm run serve` in the backend/functions directory
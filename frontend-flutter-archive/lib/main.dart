import 'package:cardpay/routes.dart';
import 'package:cardpay/services/firestore.dart';
import 'package:cardpay/services/models.dart' as model;
import 'package:cardpay/services/utils.dart';
import 'package:cardpay/shared/shared.dart';
import 'package:cardpay/theme/theme.dart';
import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:package_info_plus/package_info_plus.dart';
import 'package:provider/provider.dart';
import 'firebase_options.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const App());
}

/// We are using a StatefulWidget such that we only create the [Future] once,
/// no matter how many times our widget rebuild.
/// If we used a [StatelessWidget], in the event where [App] is rebuilt, that
/// would re-initialize FlutterFire and make our application re-enter loading state,
/// which is undesired.
class App extends StatefulWidget {
  const App({super.key});

  @override
  State<App> createState() => _AppState();
}

class _AppState extends State<App> {
  /// The future is part of the state of our widget. We should not call `initializeApp`
  /// directly inside [build].
  final Future<FirebaseApp> _initialization = Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );

  Future<bool> checkAppVersion() async {
    PackageInfo packageInfo = await PackageInfo.fromPlatform();
    final info = await FirestoreService().getAppVersionInfo();
    final bool isAppVersionLatest = isVersionGreaterThan(
      packageInfo.version,
      info.versionNumber,
    );

    return Future.value(info.breakingChanges ? isAppVersionLatest : true);
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
      // Initialize FlutterFire:
      future: _initialization,
      builder: (context, snapshot) {
        // Connects with firebase emulator instead of firebase cloud
        // FirebaseFunctions.instance.useFunctionsEmulator('localhost', 5001);

        // Check for errors
        if (snapshot.hasError) {
          return const Text(
            'error',
            textDirection: TextDirection.ltr,
          );
        }

        // Once complete, show your application
        if (snapshot.connectionState == ConnectionState.done) {
          return FutureBuilder<bool>(
            future: checkAppVersion(),
            builder: (context, snapshot) {
              if (snapshot.hasData && snapshot.data!) {
                return MultiProvider(
                  providers: [
                    StreamProvider<model.User>(
                      create: (_) => FirestoreService().streamUser(),
                      initialData: model.User(),
                    ),
                    ChangeNotifierProvider<model.ErrorModel>(
                      create: (_) => model.ErrorModel(),
                    ),
                    ChangeNotifierProvider<model.Loading>(
                      create: (_) => model.Loading(),
                    ),
                  ],
                  child: MaterialApp(
                    routes: appRoutes,
                    theme: appTheme,
                  ),
                );
              } else if (snapshot.hasData && !snapshot.data!) {
                return MaterialApp(
                  home: SafeArea(
                    child: Scaffold(
                      body: Center(
                        child: MainHeadingTypographyCustomWidget(
                          content:
                              "Please update the app from Play/App store in order to continue using the application",
                        ),
                      ),
                    ),
                  ),
                );
              } else {
                return const Text(
                  'loading',
                  textDirection: TextDirection.ltr,
                );
              }
            },
          );
        }

        // Otherwise, show something whilst waiting for initialization to complete
        return const Text(
          'loading',
          textDirection: TextDirection.ltr,
        );
      },
    );
  }
}

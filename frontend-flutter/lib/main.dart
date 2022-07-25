import 'package:cardpay/routes.dart';
import 'package:cardpay/theme.dart';
import 'package:flutter/material.dart';

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
  @override
  Widget build(BuildContext context) {
    return FutureBuilder<int>(
      future: Future.value(23),
      builder: (context, snapshot) {
        return MaterialApp(
          routes: appRoutes,
          theme: appTheme,
        );
      },
    );
  }
}

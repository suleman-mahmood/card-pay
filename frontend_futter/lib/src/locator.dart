import 'package:awesome_dio_interceptor/awesome_dio_interceptor.dart';
import 'package:cardpay/firebase_options.dart';
import 'package:cardpay/src/all_listeners.dart';
import 'package:cardpay/src/config/firebase/analytics_service.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/data/datasources/local/app_database.dart';
import 'package:cardpay/src/data/datasources/remote/python_api_service.dart';
import 'package:cardpay/src/data/repositories/api_repository_fake.dart';
import 'package:cardpay/src/data/repositories/api_repository_imp.dart';
import 'package:cardpay/src/data/repositories/database_repository_impl.dart';
import 'package:cardpay/src/domain/repositories/api_repository.dart';
import 'package:cardpay/src/domain/repositories/database_repository.dart';
import 'package:dio/dio.dart';
import 'package:dio_smart_retry/dio_smart_retry.dart';
import 'package:flutter/material.dart';
import 'package:get_it/get_it.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_crashlytics/firebase_crashlytics.dart';
import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

final locator = GetIt.instance;

Future<void> initializeDependencies() async {
  WidgetsFlutterBinding.ensureInitialized();

  final db = await $FloorAppDatabase.databaseBuilder('zambeel').build();
  locator.registerSingleton<AppDatabase>(db);

  locator.registerSingleton<DatabaseRepository>(
    DatabaseRepositoryImpl(locator<AppDatabase>()),
  );

  final dio = Dio();
  dio.interceptors.add(AwesomeDioInterceptor());
  dio.interceptors.add(RetryInterceptor(
    dio: dio,
    logPrint: print, // specify log function (optional)
    retries: 3, // retry count (optional)
    retryDelays: const [
      // set delays between retries (optional)
      Duration(seconds: 1), // wait 1 sec before first retry
      Duration(seconds: 2), // wait 2 sec before second retry
      Duration(seconds: 2), // wait 2 sec before third retry
      Duration(seconds: 2), // wait 2 sec before fourth retry
      Duration(seconds: 2), // wait 2 sec before fifth retry
    ],
  ));

  locator.registerSingleton<Dio>(dio);

  locator.registerSingleton<PythonApiService>(PythonApiService(locator<Dio>()));

  locator.registerSingleton<ApiRepository>(
    ApiRepositoryImpl(locator<PythonApiService>()),
    //FakeApiRepositoryImpl(),
  );
  locator.registerSingleton<SharedPreferences>(
    await SharedPreferences.getInstance(),
  );

  locator.registerSingleton<AppRouter>(AppRouter());

  locator.registerSingleton<AllListeners>(AllListeners());

  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);
  FirebaseCrashlytics.instance.setCrashlyticsCollectionEnabled(true);

  FlutterError.onError = (errorDetails) {
    FirebaseCrashlytics.instance.recordFlutterFatalError(errorDetails);
  };

  // Pass all uncaught asynchronous errors that aren't handled by the Flutter framework to Crashlytics
  PlatformDispatcher.instance.onError = (error, stack) {
    FirebaseCrashlytics.instance.recordError(error, stack, fatal: true);
    return true;
  };

  locator.registerSingleton<AnalyticsService>(AnalyticsService());
}

import 'package:awesome_dio_interceptor/awesome_dio_interceptor.dart';
import 'package:cardpay/firebase_options.dart';
import 'package:cardpay/src/data/datasources/remote/python_api_service.dart';
import 'package:cardpay/src/data/repositories/api_repository_fake.dart';
import 'package:cardpay/src/data/repositories/api_repository_imp.dart';
import 'package:cardpay/src/domain/repositories/api_repository.dart';
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:get_it/get_it.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_crashlytics/firebase_crashlytics.dart';
import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

final locator = GetIt.instance;

Future<void> initializeDependencies() async {
  WidgetsFlutterBinding.ensureInitialized();

  final dio = Dio();
  dio.interceptors.add(AwesomeDioInterceptor());

  locator.registerSingleton<Dio>(dio);

  locator.registerSingleton<PythonApiService>(
    PythonApiService(locator<Dio>()),
  );

  locator.registerSingleton<ApiRepository>(
    // ApiRepositoryImpl(locator<PythonApiService>()),
    FakeApiRepositoryImpl(),
  );
  locator.registerSingleton<SharedPreferences>(
    await SharedPreferences.getInstance(),
  );

  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  FirebaseCrashlytics.instance.setCrashlyticsCollectionEnabled(true);

  FlutterError.onError = (errorDetails) {
    FirebaseCrashlytics.instance.recordFlutterFatalError(errorDetails);
  };

  // Pass all uncaught asynchronous errors that aren't handled by the Flutter framework to Crashlytics
  PlatformDispatcher.instance.onError = (error, stack) {
    FirebaseCrashlytics.instance.recordError(error, stack, fatal: true);
    return true;
  };
}

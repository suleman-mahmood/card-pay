import 'package:awesome_dio_interceptor/awesome_dio_interceptor.dart';
import 'package:cardpay/firebase_options.dart';
import 'package:cardpay/src/data/datasources/remote/python_api_service.dart';
import 'package:cardpay/src/data/repositories/api_repository_imp.dart';
import 'package:cardpay/src/domain/repositories/api_repository.dart';
import 'package:dio/dio.dart';
import 'package:get_it/get_it.dart';
import 'package:firebase_core/firebase_core.dart';

final locator = GetIt.instance;

Future<void> initializeDependencies() async {
  final dio = Dio();
  dio.interceptors.add(AwesomeDioInterceptor());

  locator.registerSingleton<Dio>(dio);

  locator.registerSingleton<PythonApiService>(
    PythonApiService(locator<Dio>()),
  );

  locator.registerSingleton<ApiRepository>(
    ApiRepositoryImpl(locator<PythonApiService>()),
  );

  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
}

import 'package:cardpay/src/domain/models/login.dart';
import 'package:cardpay/src/presentation/cubits/base/base_cubit.dart';
import 'package:dio/dio.dart';
import 'package:firebase_auth/firebase_auth.dart' as firebase_auth;
import 'package:flutter/services.dart';
import 'package:meta/meta.dart';
import 'package:local_auth/local_auth.dart';
import 'package:shared_preferences/shared_preferences.dart';

part 'login_state.dart';

class LoginCubit extends BaseCubit<LoginState, Login> {
  final SharedPreferences _prefs;

  LoginCubit(this._prefs) : super(LoginInitial(), Login());

  Future<void> login(
    String phoneNumber,
    String password,
  ) async {
    if (isBusy) return;

    await run(() async {
      emit(LoginLoading());

      final String emailAddress = '92$phoneNumber@cardpay.com.pk';
      try {
        await firebase_auth.FirebaseAuth.instance.signInWithEmailAndPassword(
          email: emailAddress,
          password: password,
        );
        emit(ManualLoginSuccess(
          message: "Sign in was successful",
        ));
      } on firebase_auth.FirebaseAuthException catch (e) {
        emit(LoginFailed(errorMessage: e.message ?? ''));
      }
    });
  }

  Future<void> loginWithBiometric() async {
    if (isBusy) return;

    await run(() async {
      emit(LoginLoading());
      final LocalAuthentication auth = LocalAuthentication();
      bool didAuthenticate = false;

      try {
        didAuthenticate = await auth.authenticate(
          localizedReason: 'Please authenticate to log in',
        );

        if (didAuthenticate) {
          final userPhoneNumber = _prefs.getString('user_phone_number');
          final password = _prefs.getString('user_password');

          if (userPhoneNumber == null || password == null) {
            emit(LoginFailed(errorMessage: 'Credentials not linked on device'));
            return;
          }

          data.phoneNumber = userPhoneNumber;
          data.password = password;

          emit(
            BiometricLoginSuccess(
              message: "Sign in was successful",
              login: data,
            ),
          );
        } else {
          emit(LoginFailed(errorMessage: 'Authentication failed'));
        }
      } on PlatformException catch (e) {
        emit(LoginFailed(errorMessage: e.message ?? ''));
      }
    });
  }
}

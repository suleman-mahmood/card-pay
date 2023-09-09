import 'package:cardpay/src/domain/models/requests/create_customer_request.dart';
import 'package:cardpay/src/domain/models/requests/verify_phone_number_request.dart';
import 'package:cardpay/src/domain/repositories/api_repository.dart';
import 'package:cardpay/src/presentation/cubits/base/base_cubit.dart';
import 'package:cardpay/src/utils/constants/event_codes.dart';
import 'package:cardpay/src/utils/data_state.dart';
import 'package:dio/dio.dart';
import 'package:meta/meta.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:firebase_auth/firebase_auth.dart' as firebase_auth;

part 'signup_state.dart';

class SignupCubit extends BaseCubit<SignupState, void> {
  final ApiRepository _apiRepository;
  final SharedPreferences _prefs;

  SignupCubit(this._apiRepository, this._prefs) : super(SignupInitial(), null);

  Future<void> createCustomer(
    String personalEmail,
    String phoneNumber,
    String fullName,
    String password,
  ) async {
    if (isBusy) return;

    await run(() async {
      emit(SignupLoading());

      final response = await _apiRepository.createCustomer(
        request: CreateCustomerRequest(
          fullName: fullName,
          password: password,
          personalEmail: personalEmail,
          phoneNumber: phoneNumber,
        ),
      );

      if (response is DataSuccess) {
        final userId = response.data!.userId;

        await _prefs.setString('user_id', userId);
        await _prefs.setString('user_phone_number', phoneNumber);
        await _prefs.setString('user_password', password);

        emit(SignupSuccess(
          message: response.data!.message,
          eventCodes: response.data!.eventCode,
        ));
      } else if (response is DataFailed) {
        if (response.error?.type.name == "unknown") {
          emit(SignupUnknownFailure(
            errorMessage: "Unknown error, check internet connections",
          ));
        } else {
          emit(SignupFailed(
            error: response.error,
            errorMessage: response.error?.response?.data["message"],
          ));
        }
      }
    });
  }

  Future<void> verifyPhoneNumber(String otp) async {
    if (isBusy) return;

    await run(() async {
      emit(SignupLoading());

      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';

      final response = await _apiRepository.verifyPhoneNumber(
        request: VerifyPhoneNumberRequest(
          otp: otp,
        ),
        token: token,
      );

      if (response is DataSuccess) {
        emit(SignupSuccess(
          message: response.data!.message,
          eventCodes: EventCodes.OTP_VERIFIED,
        ));
      } else if (response is DataFailed) {
        if (response.error?.type.name == "unknown") {
          emit(SignupUnknownFailure(
            errorMessage: "Unknown error, check internet connections",
          ));
        } else {
          emit(SignupFailed(
            error: response.error,
            errorMessage: response.error?.response?.data["message"],
          ));
        }
      }
    });
  }
}

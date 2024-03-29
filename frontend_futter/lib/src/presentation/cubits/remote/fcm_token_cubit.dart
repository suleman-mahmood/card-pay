import 'package:bloc/bloc.dart';
import 'package:cardpay/src/domain/models/requests/set_fcm_token_request.dart';
import 'package:cardpay/src/domain/repositories/api_repository.dart';
import 'package:cardpay/src/presentation/cubits/base/base_cubit.dart';
import 'package:cardpay/src/utils/data_state.dart';
import 'package:dio/dio.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:meta/meta.dart';
import 'package:firebase_auth/firebase_auth.dart' as firebase_auth;

part 'fcm_token_state.dart';

class FcmTokenCubit extends BaseCubit<FcmTokenState, void> {
  final ApiRepository _apiRepository;

  FcmTokenCubit(this._apiRepository) : super(FcmTokenInitial(), null);

  Future<void> setFcmTokem() async {
    if (isBusy) return;

    await run(() async {
      emit(FcmTokenLoading());

      await FirebaseMessaging.instance.requestPermission(
        alert: true,
        announcement: true,
        badge: true,
        carPlay: false,
        criticalAlert: false,
        provisional: false,
        sound: true,
      );

      final fcmToken = await FirebaseMessaging.instance.getToken();

      if (fcmToken == null) return;

      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';
      final response = await _apiRepository.setFcmToken(
        request: SetFcmTokenRequest(fcmToken: fcmToken),
        token: token,
      );

      if (response is DataSuccess) {
        emit(FcmTokenSuccess(message: response.data!.message));
      } else if (response is DataFailed) {
        if (response.error?.type.name == "unknown") {
          emit(FcmTokenUnknownFailure(
            errorMessage: "Unknown error, check internet connections",
          ));
        } else {
          emit(FcmTokenFailed(
            error: response.error,
            errorMessage: response.error?.response?.data["message"],
          ));
        }
      }
    });
  }
}

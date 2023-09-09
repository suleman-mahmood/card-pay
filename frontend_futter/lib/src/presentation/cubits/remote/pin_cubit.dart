import 'package:cardpay/src/domain/models/requests/change_pin_request.dart';
import 'package:cardpay/src/domain/repositories/api_repository.dart';
import 'package:cardpay/src/presentation/cubits/base/base_cubit.dart';
import 'package:cardpay/src/utils/data_state.dart';
import 'package:dio/dio.dart';
import 'package:meta/meta.dart';
import 'package:firebase_auth/firebase_auth.dart' as firebase_auth;

part 'pin_state.dart';

class PinCubit extends BaseCubit<PinState, void> {
  final ApiRepository _apiRepository;

  PinCubit(this._apiRepository) : super(PinInitial(), null);

  Future<void> changePin(
    String newPin,
  ) async {
    if (isBusy) return;

    await run(() async {
      emit(PinLoading());

      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';
      final response = await _apiRepository.changePin(
        request: ChangePinRequest(
          newPin: newPin,
        ),
        token: token,
      );

      if (response is DataSuccess) {
        emit(PinSuccess(message: response.data!.message));
      } else if (response is DataFailed) {
        if (response.error?.type.name == "unknown") {
          emit(PinUnknownFailure(
            errorMessage: "Unknown error, check internet connections",
          ));
        } else {
          emit(PinFailed(
            error: response.error,
            errorMessage: response.error?.response?.data["message"],
          ));
        }
      }
    });
  }
}

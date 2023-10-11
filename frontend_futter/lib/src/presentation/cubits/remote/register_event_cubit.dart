import 'package:cardpay/src/domain/models/requests/register_event_request.dart';
import 'package:cardpay/src/domain/repositories/api_repository.dart';
import 'package:cardpay/src/presentation/cubits/base/base_cubit.dart';
import 'package:cardpay/src/utils/data_state.dart';
import 'package:dio/dio.dart';
import 'package:meta/meta.dart';
import 'package:firebase_auth/firebase_auth.dart' as firebase_auth;

part 'register_event_state.dart';

class RegisterEventCubit extends BaseCubit<RegisterEventState, void> {
  final ApiRepository _apiRepository;

  RegisterEventCubit(this._apiRepository) : super(RegisterEventInitial(), Null);

  Future<void> registerEvent(String eventId) async {
    if (isBusy) return;

    await run(() async {
      emit(RegisterEventLoading());

      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';
      final response = await _apiRepository.registerEvent(
        registerEventRequest: RegisterEventRequest(eventId: eventId),
        token: token,
      );

      if (response is DataSuccess) {
        emit(RegisterEventSuccess(message: response.data!.message));
      } else if (response is DataFailed) {
        if (response.error?.type.name == "unknown") {
          emit(RegisterEventUnknownFailure(
            errorMessage: "Unknown error, check internet connections",
          ));
        } else {
          emit(RegisterEventFailed(
            error: response.error,
            errorMessage: response.error?.response?.data["message"],
          ));
        }
      }
    });
  }
}

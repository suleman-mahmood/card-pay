import 'package:cardpay/src/domain/models/event.dart';
import 'package:cardpay/src/domain/repositories/api_repository.dart';
import 'package:cardpay/src/presentation/cubits/base/base_cubit.dart';
import 'package:cardpay/src/utils/data_state.dart';
import 'package:dio/dio.dart';
import 'package:meta/meta.dart';
import 'package:firebase_auth/firebase_auth.dart' as firebase_auth;

part 'registered_events_state.dart';

class RegisteredEventsCubit
    extends BaseCubit<RegisteredEventsState, List<Event>> {
  final ApiRepository _apiRepository;

  RegisteredEventsCubit(this._apiRepository)
      : super(RegisteredEventsInitial(), []);

  Future<void> getRegisteredEvents() async {
    if (isBusy) return;

    await run(() async {
      emit(RegisteredEventsLoading());

      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';
      final response = await _apiRepository.getRegisteredEvents(token: token);

      if (response is DataSuccess) {
        data.clear();
        data.addAll(response.data!.events);

        emit(RegisteredEventsSuccess(
          message: response.data!.message,
          events: data,
        ));
      } else if (response is DataFailed) {
        if (response.error?.type.name == "unknown") {
          emit(RegisteredEventsUnknownFailure(
            errorMessage: "Unknown error, check internet connections",
          ));
        } else {
          emit(RegisteredEventsFailed(
            error: response.error,
            errorMessage: response.error?.response?.data["message"],
          ));
        }
      }
    });
  }
}

import 'package:cardpay/src/domain/models/event.dart';
import 'package:cardpay/src/domain/repositories/api_repository.dart';
import 'package:cardpay/src/presentation/cubits/base/base_cubit.dart';
import 'package:cardpay/src/utils/data_state.dart';
import 'package:dio/dio.dart';
import 'package:meta/meta.dart';
import 'package:firebase_auth/firebase_auth.dart' as firebase_auth;

part 'live_events_state.dart';

class LiveEventsCubit extends BaseCubit<LiveEventsState, List<Event>> {
  final ApiRepository _apiRepository;

  LiveEventsCubit(this._apiRepository) : super(LiveEventsInitial(), []);

  Future<void> getLiveEvents() async {
    if (isBusy) return;

    await run(() async {
      emit(LiveEventsLoading());

      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';
      final response = await _apiRepository.getLiveEvents(token: token);

      if (response is DataSuccess) {
        data.clear();
        data.addAll(response.data!.events);

        emit(LiveEventsSuccess(
          message: response.data!.message,
          events: data,
        ));
      } else if (response is DataFailed) {
        if (response.error?.type.name == "unknown") {
          emit(LiveEventsUnknownFailure(
            errorMessage: "Unknown error, check internet connections",
          ));
        } else {
          emit(LiveEventsFailed(
            error: response.error,
            errorMessage: response.error?.response?.data["message"],
          ));
        }
      }
    });
  }
}

import 'package:cardpay/src/domain/models/user_info.dart';
import 'package:cardpay/src/domain/repositories/api_repository.dart';
import 'package:cardpay/src/presentation/cubits/base/base_cubit.dart';
import 'package:cardpay/src/utils/data_state.dart';
import 'package:dio/dio.dart';
import 'package:meta/meta.dart';
import 'package:firebase_auth/firebase_auth.dart' as firebase_auth;

part 'frequent_users_state.dart';

class FrequentUsersCubit extends BaseCubit<FrequentUsersState, List<UserInfo>> {
  final ApiRepository _apiRepository;

  FrequentUsersCubit(this._apiRepository) : super(FrequentUsersInitial(), []);

  Future<void> getFrequentUsers({required String closedLoopId}) async {
    if (isBusy) return;

    await run(() async {
      emit(FrequentUsersLoading());

      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';
      final response = await _apiRepository.getFrequentUsers(
        closedLoopId: closedLoopId,
        token: token,
      );

      if (response is DataSuccess) {
        emit(FrequentUsersSuccess(
          frequentUsers: response.data!.frequentUsers,
        ));
      } else if (response is DataFailed) {
        if (response.error?.type.name == "unknown") {
          emit(FrequentUsersUnknownFailure(
            errorMessage: "Unknown error, check internet connections",
          ));
        } else {
          emit(FrequentUsersFailed(
            error: response.error,
            errorMessage: response.error?.response?.data["message"],
          ));
        }
      }
    });
  }
}

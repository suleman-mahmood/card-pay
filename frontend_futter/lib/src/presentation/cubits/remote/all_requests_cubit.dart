import 'package:cardpay/src/domain/models/p2p_request_info.dart';
import 'package:cardpay/src/domain/repositories/api_repository.dart';
import 'package:cardpay/src/presentation/cubits/base/base_cubit.dart';
import 'package:cardpay/src/utils/data_state.dart';
import 'package:dio/dio.dart';
import 'package:meta/meta.dart';
import 'package:firebase_auth/firebase_auth.dart' as firebase_auth;

part 'all_requests_state.dart';

class AllRequestsCubit
    extends BaseCubit<AllRequestsState, List<P2PRequestInfo>> {
  final ApiRepository _apiRepository;

  AllRequestsCubit(this._apiRepository) : super(AllRequestsInitial(), []);

  Future<void> getP2PPullRequests() async {
    if (isBusy) return;

    await run(() async {
      emit(AllRequestsLoading());

      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';
      final response = await _apiRepository.getP2PPullRequests(token: token);

      if (response is DataSuccess) {
        emit(AllRequestsSuccess(
          message: response.data!.message,
          requestInfo: response.data!.p2pRequestInfo,
        ));
      } else if (response is DataFailed) {
        if (response.error?.type.name == "unknown") {
          emit(AllRequestsUnknownFailure(
            errorMessage: "Unknown error, check internet connections",
          ));
        } else {
          emit(AllRequestsFailed(
            error: response.error,
            errorMessage: response.error?.response?.data["message"],
          ));
        }
      }
    });
  }
}

import 'package:cardpay/src/domain/models/requests/get_full_name_request.dart';
import 'package:cardpay/src/domain/repositories/api_repository.dart';
import 'package:cardpay/src/presentation/cubits/base/base_cubit.dart';
import 'package:cardpay/src/utils/data_state.dart';
import 'package:dio/dio.dart';
import 'package:meta/meta.dart';
import 'package:firebase_auth/firebase_auth.dart' as firebase_auth;

part 'full_name_state.dart';

class FullNameCubit extends BaseCubit<FullNameState, void> {
  final ApiRepository _apiRepository;

  FullNameCubit(this._apiRepository) : super(FullNameInitial(), null);

  Future<void> getFullName(
      {required String uniqueIdentifier, required String closedLoopId}) async {
    if (isBusy) return;

    await run(() async {
      emit(FullNameLoading());

      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';
      final response = await _apiRepository.getFullNameRequest(
        request: GetFullNameRequest(
          uniqueIdentifier: uniqueIdentifier,
          closedLoopId: closedLoopId,
        ),
        token: token,
      );

      if (response is DataSuccess) {
        emit(FullNameSuccess(
          fullName: response.data!.fullName,
        ));
      } else if (response is DataFailed) {
        if (response.error?.type.name == "unknown") {
          emit(FullNameUnknownFailure(
            errorMessage: "Unknown error, check internet connections",
          ));
        } else {
          emit(FullNameFailed(
            error: response.error,
            errorMessage: response.error?.response?.data["message"],
          ));
        }
      }
    });
  }
}

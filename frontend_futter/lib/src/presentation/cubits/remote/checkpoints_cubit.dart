import 'package:cardpay/src/domain/models/checkpoints.dart';
import 'package:cardpay/src/domain/repositories/api_repository.dart';
import 'package:cardpay/src/presentation/cubits/base/base_cubit.dart';
import 'package:cardpay/src/utils/data_state.dart';
import 'package:firebase_auth/firebase_auth.dart' as firebase_auth;
import 'package:dio/dio.dart';
import 'package:meta/meta.dart';

part 'checkpoints_state.dart';

class CheckpointsCubit extends BaseCubit<CheckpointsState, Checkpoints> {
  final ApiRepository _apiRepository;

  CheckpointsCubit(this._apiRepository)
      : super(
          CheckpointsInitial(),
          Checkpoints(),
        );

  Future<void> init() async {
    emit(CheckpointsInitial());
  }

  Future<void> getCheckpoints() async {
    if (isBusy) return;

    await run(() async {
      emit(CheckpointsLoading());
      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';
      final response = await _apiRepository.getCheckpoints(token);

      if (response is DataSuccess) {
        data.verifiedPhoneOtp = response.data!.checks.verifiedPhoneOtp;
        data.verifiedClosedLoop = response.data!.checks.verifiedClosedLoop;
        data.pinSetup = response.data!.checks.pinSetup;

        emit(CheckpointsSuccess(
          message: response.data!.message,
          checkPoints: data,
        ));
      } else if (response is DataFailed) {
        emit(CheckpointsFailed(
          error: response.error,
          errorMessage: response.error?.response?.data["message"],
        ));
      }
    });
  }
}

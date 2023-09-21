import 'package:cardpay/src/domain/models/closed_loop.dart';
import 'package:cardpay/src/domain/models/requests/register_closed_loop_request.dart';
import 'package:cardpay/src/domain/models/requests/verify_closed_loop_request.dart';
import 'package:cardpay/src/domain/repositories/api_repository.dart';
import 'package:cardpay/src/presentation/cubits/base/base_cubit.dart';
import 'package:cardpay/src/utils/constants/event_codes.dart';
import 'package:cardpay/src/utils/data_state.dart';
import 'package:firebase_auth/firebase_auth.dart' as firebase_auth;
import 'package:dio/dio.dart';
import 'package:meta/meta.dart';

part 'closed_loop_state.dart';

class ClosedLoopCubit extends BaseCubit<ClosedLoopState, List<ClosedLoop>> {
  final ApiRepository _apiRepository;

  ClosedLoopCubit(this._apiRepository) : super(ClosedLoopInitial(), []);

  Future<void> getAllClosedLoops() async {
    if (isBusy) return;

    await run(() async {
      emit(const ClosedLoopLoading());

      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';
      final response = await _apiRepository.getAllClosedLoops(token);

      if (response is DataSuccess) {
        data.clear();
        data.addAll(response.data!.closedLoops);

        emit(ClosedLoopSuccess(
          message: response.data!.message,
          closedLoops: data,
        ));
      } else if (response is DataFailed) {
        if (response.error?.type.name == "unknown") {
          emit(const ClosedLoopUnknownFailure(
            errorMessage: "Unknown error, check internet connections",
          ));
        } else {
          emit(ClosedLoopFailed(
            error: response.error,
            errorMessage: response.error?.response?.data["message"],
          ));
        }
      }
    });
  }

  Future<void> registerClosedLoop(
    String closedLoopId,
    String uniqueIdentifier,
  ) async {
    if (isBusy) return;

    await run(() async {
      emit(ClosedLoopLoading());

      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';
      final response = await _apiRepository.registerClosedLoop(
        request: RegisterClosedLoopRequest(
          closedLoopId: closedLoopId,
          uniqueIdentifier: uniqueIdentifier,
        ),
        token: token,
      );

      if (response is DataSuccess) {
        emit(ClosedLoopSuccess(
          message: response.data!.message,
          eventCodes: EventCodes.ORGANIZATION_REGISTERED,
          closedLoops: data,
        ));
      } else if (response is DataFailed) {
        if (response.error?.type.name == "unknown") {
          emit(const ClosedLoopUnknownFailure(
            errorMessage: "Unknown error, check internet connections",
          ));
        } else {
          emit(ClosedLoopFailed(
            error: response.error,
            errorMessage: response.error?.response?.data["message"],
          ));
        }
      }
    });
  }

  Future<void> verifyClosedLoop(
    String closedLoopId,
    String uniqueIdentifierOtp,
    String referralUniqueIdentifier,
  ) async {
    if (isBusy) return;

    await run(() async {
      emit(const ClosedLoopLoading());

      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';
      final response = await _apiRepository.verifyClosedLoop(
        request: VerifyClosedLoopRequest(
          closedLoopId: closedLoopId,
          uniqueIdentifierOtp: uniqueIdentifierOtp,
          referralUniqueIdentifier: referralUniqueIdentifier,
        ),
        token: token,
      );

      if (response is DataSuccess) {
        emit(ClosedLoopSuccess(
          message: response.data!.message,
          eventCodes: EventCodes.ORGANIZATION_VERIFIED,
          closedLoops: data,
        ));
      } else if (response is DataFailed) {
        if (response.error?.type.name == "unknown") {
          emit(ClosedLoopUnknownFailure(
            errorMessage: "Unknown error, check internet connections",
          ));
        } else {
          emit(ClosedLoopFailed(
            error: response.error,
            errorMessage: response.error?.response?.data["message"],
          ));
        }
      }
    });
  }
}

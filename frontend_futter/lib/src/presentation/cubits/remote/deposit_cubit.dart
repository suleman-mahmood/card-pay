import 'package:cardpay/src/domain/models/deposit.dart';
import 'package:cardpay/src/domain/models/requests/create_deposit_request.dart';
import 'package:cardpay/src/domain/repositories/api_repository.dart';
import 'package:cardpay/src/presentation/cubits/base/base_cubit.dart';
import 'package:cardpay/src/utils/data_state.dart';
import 'package:firebase_auth/firebase_auth.dart' as firebase_auth;
import 'package:dio/dio.dart';
import 'package:meta/meta.dart';

part 'deposit_state.dart';

class DepositCubit extends BaseCubit<DepositState, Deposit> {
  final ApiRepository _apiRepository;

  DepositCubit(this._apiRepository) : super(DepositInitial(), Deposit());

  Future<void> createDepositRequest(int amount) async {
    if (isBusy) return;

    await run(() async {
      emit(DepositLoading());

      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';
      final response = await _apiRepository.createDepositRequest(
        request: CreateDepositRequest(amount: amount),
        token: token,
      );

      if (response is DataSuccess) {
        emit(DepositSuccess(
          message: response.data!.message,
          checkoutUrl: response.data!.checkoutUrl,
        ));
      } else if (response is DataFailed) {
        if (response.error?.type.name == "unknown") {
          emit(DepositUnknownFailure(
            errorMessage: "Unknown error, check internet connections",
          ));
        } else {
          emit(DepositFailed(
            error: response.error,
            errorMessage: response.error?.response?.data["message"],
          ));
        }
      }
    });
  }
}

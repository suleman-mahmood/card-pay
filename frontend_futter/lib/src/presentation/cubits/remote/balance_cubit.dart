import 'package:cardpay/src/domain/models/balance.dart';
import 'package:cardpay/src/domain/repositories/api_repository.dart';
import 'package:cardpay/src/presentation/cubits/base/base_cubit.dart';
import 'package:cardpay/src/utils/data_state.dart';
import 'package:dio/dio.dart';
import 'package:meta/meta.dart';
import 'package:firebase_auth/firebase_auth.dart' as firebase_auth;

part 'balance_state.dart';

class BalanceCubit extends BaseCubit<BalanceState, Balance> {
  final ApiRepository _apiRepository;

  BalanceCubit(this._apiRepository) : super(BalanceInitial(), Balance());

  Future<void> getUserBalance() async {
    if (isBusy) return;

    await run(() async {
      emit(BalanceLoading());

      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';
      final response = await _apiRepository.getUserBalance(token);

      if (response is DataSuccess) {
        data.amount = response.data!.balance;

        emit(BalanceSuccess(
          message: response.data!.message,
          balance: data,
        ));
      } else if (response is DataFailed) {
        if (response.error?.type.name == "unknown") {
          emit(BalanceUnknownFailure(
            errorMessage: "Unknown error, check internet connections",
          ));
        } else {
          emit(BalanceFailed(
            error: response.error,
            errorMessage: response.error?.response?.data["message"],
          ));
        }
      }
    });
  }
}

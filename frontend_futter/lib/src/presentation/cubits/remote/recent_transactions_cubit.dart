import 'package:cardpay/src/domain/models/transaction.dart';
import 'package:cardpay/src/domain/repositories/api_repository.dart';
import 'package:cardpay/src/presentation/cubits/base/base_cubit.dart';
import 'package:cardpay/src/utils/data_state.dart';
import 'package:dio/dio.dart';
import 'package:meta/meta.dart';
import 'package:firebase_auth/firebase_auth.dart' as firebase_auth;

part 'recent_transactions_state.dart';

class RecentTransactionsCubit
    extends BaseCubit<RecentTransactionsState, List<Transaction>> {
  final ApiRepository _apiRepository;

  RecentTransactionsCubit(this._apiRepository)
      : super(RecentTransactionsInitial(), []);

  Future<void> getUserRecentTransactions() async {
    if (isBusy) return;

    await run(() async {
      emit(RecentTransactionsLoading());

      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';
      final response = await _apiRepository.getUserRecentTransactions(token);

      if (response is DataSuccess) {
        data.clear();
        data.addAll(response.data!.recentTransactions);

        emit(RecentTransactionsSuccess(
          message: response.data!.message,
          recentTransactions: data,
        ));
      } else if (response is DataFailed) {
        if (response.error?.type.name == "unknown") {
          emit(RecentTransactionsUnknownFailure(
            errorMessage: "Unknown error, check internet connections",
          ));
        } else {
          emit(RecentTransactionsFailed(
            error: response.error,
            errorMessage: response.error?.response?.data["message"],
          ));
        }
      }
    });
  }
}

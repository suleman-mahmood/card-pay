import 'package:cardpay/src/domain/models/requests/execute_p2p_push_transaction_request.dart';
import 'package:cardpay/src/domain/models/transfer.dart';
import 'package:cardpay/src/domain/repositories/api_repository.dart';
import 'package:cardpay/src/presentation/cubits/base/base_cubit.dart';
import 'package:cardpay/src/utils/data_state.dart';
import 'package:cardpay/src/utils/pretty_logs.dart';
import 'package:dio/dio.dart';
import 'package:meta/meta.dart';
import 'package:firebase_auth/firebase_auth.dart' as firebase_auth;

part 'transfer_state.dart';

class TransferCubit extends BaseCubit<TransferState, Transfer> {
  final ApiRepository _apiRepository;

  TransferCubit(this._apiRepository) : super(TransferInitial(), Transfer());

  Future<void> executeP2PPushTransaction(String recipientUniqueIdentifier,
      double amount, String closedLoopId) async {
    if (isBusy) return;

    await run(() async {
      emit(TransferLoading());

      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';
      final response = await _apiRepository.executeP2PPushTransaction(
        request: ExecuteP2PPushTransactionRequest(
          recipientUniqueIdentifier: recipientUniqueIdentifier,
          amount: amount,
          closedLoopId: closedLoopId,
        ),
        token: token,
      );

      if (response is DataSuccess) {
        emit(TransferSuccess(message: response.data!.message));
      } else if (response is DataFailed) {
        emit(TransferFailed(
          error: response.error,
          errorMessage: response.error?.response?.data["message"],
        ));
      }
    });
  }
}
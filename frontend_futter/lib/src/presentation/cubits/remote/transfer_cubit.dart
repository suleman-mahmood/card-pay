import 'package:cardpay/src/domain/models/requests/accept_p2p_pull_transaction_request.dart';
import 'package:cardpay/src/domain/models/requests/create_p2p_pull_transaction_request.dart';
import 'package:cardpay/src/domain/models/requests/decline_p2p_pull_transaction_request.dart';
import 'package:cardpay/src/domain/models/requests/execute_p2p_push_transaction_request.dart';
import 'package:cardpay/src/domain/models/requests/execute_qr_transaction_request.dart';
import 'package:cardpay/src/domain/models/transfer.dart';
import 'package:cardpay/src/domain/repositories/api_repository.dart';
import 'package:cardpay/src/presentation/cubits/base/base_cubit.dart';
import 'package:cardpay/src/utils/data_state.dart';
import 'package:dio/dio.dart';
import 'package:meta/meta.dart';
import 'package:firebase_auth/firebase_auth.dart' as firebase_auth;

part 'transfer_state.dart';

class TransferCubit extends BaseCubit<TransferState, Transfer> {
  final ApiRepository _apiRepository;

  TransferCubit(this._apiRepository) : super(TransferInitial(), Transfer());

  Future<void> init() async {
    emit(TransferInitial());
  }

  Future<void> executeP2PPushTransaction(
    String recipientUniqueIdentifier,
    int amount,
    String closedLoopId,
  ) async {
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
        if (response.error?.type.name == "unknown") {
          emit(TransferUnknownFailure(
            errorMessage: "Unknown error, check internet connections",
          ));
        } else {
          emit(TransferFailed(
            error: response.error,
            errorMessage: response.error?.response?.data["message"],
          ));
        }
      }
    });
  }

  Future<void> createP2PPullTransaction(
    String senderUniqueIdentifier,
    int amount,
    String closedLoopId,
  ) async {
    if (isBusy) return;

    await run(() async {
      emit(TransferLoading());

      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';
      final response = await _apiRepository.createP2PPullTransaction(
        request: CreateP2PPullTransactionRequest(
          senderUniqueIdentifier: senderUniqueIdentifier,
          amount: amount,
          closedLoopId: closedLoopId,
        ),
        token: token,
      );

      if (response is DataSuccess) {
        emit(TransferSuccess(message: response.data!.message));
      } else if (response is DataFailed) {
        if (response.error?.type.name == "unknown") {
          emit(TransferUnknownFailure(
            errorMessage: "Unknown error, check internet connections",
          ));
        } else {
          emit(TransferFailed(
            error: response.error,
            errorMessage: response.error?.response?.data["message"],
          ));
        }
      }
    });
  }

  Future<void> acceptP2PPullTransaction(String transactionId) async {
    if (isBusy) return;

    await run(() async {
      emit(TransferLoading());

      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';
      final response = await _apiRepository.acceptP2PPullTransaction(
        request: AcceptP2PPullTransactionRequest(transactionId: transactionId),
        token: token,
      );

      if (response is DataSuccess) {
        emit(TransferSuccess(message: response.data!.message));
      } else if (response is DataFailed) {
        if (response.error?.type.name == "unknown") {
          emit(TransferUnknownFailure(
            errorMessage: "Unknown error, check internet connections",
          ));
        } else {
          emit(TransferFailed(
            error: response.error,
            errorMessage: response.error?.response?.data["message"],
          ));
        }
      }
    });
  }

  Future<void> declineP2PPullTransaction(String transactionId) async {
    if (isBusy) return;

    await run(() async {
      emit(TransferLoading());

      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';
      final response = await _apiRepository.declineP2PPullTransaction(
        request: DeclineP2PPullTransactionRequest(transactionId: transactionId),
        token: token,
      );

      if (response is DataSuccess) {
        emit(TransferPullDeclined(message: response.data!.message));
      } else if (response is DataFailed) {
        if (response.error?.type.name == "unknown") {
          emit(TransferUnknownFailure(
            errorMessage: "Unknown error, check internet connections",
          ));
        } else {
          emit(TransferFailed(
            error: response.error,
            errorMessage: response.error?.response?.data["message"],
          ));
        }
      }
    });
  }

  Future<void> executeQrTransaction(String qrId, int amount, int v) async {
    if (isBusy) return;

    await run(() async {
      emit(TransferLoading());

      if (qrId.isEmpty) {
        emit(TransferFailed(
          errorMessage: "Invalid QR id",
        ));

        return;
      }

      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';
      final response = await _apiRepository.executeQrTransaction(
        request: ExecuteQrTransactionRequest(qrId: qrId, amount: amount, v: v),
        token: token,
      );

      if (response is DataSuccess) {
        emit(TransferSuccess(message: response.data!.message));
      } else if (response is DataFailed) {
        if (response.error?.type.name == "unknown") {
          emit(TransferUnknownFailure(
            errorMessage: "Unknown error, check internet connections",
          ));
        } else {
          emit(TransferFailed(
            error: response.error,
            errorMessage: response.error?.response?.data["message"],
          ));
        }
      }
    });
  }
}

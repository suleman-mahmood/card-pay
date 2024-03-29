import 'package:cardpay/src/domain/models/requests/create_p2p_pull_transaction_request.dart';
import 'package:cardpay/src/domain/models/transaction.dart';
import 'package:cardpay/src/domain/models/user.dart';
import 'package:cardpay/src/domain/repositories/api_repository.dart';
import 'package:cardpay/src/presentation/cubits/base/base_cubit.dart';
import 'package:cardpay/src/utils/constants/event_codes.dart';
import 'package:cardpay/src/utils/data_state.dart';
import 'package:dio/dio.dart';
import 'package:firebase_auth/firebase_auth.dart' as firebase_auth;
import 'package:meta/meta.dart';

part 'user_state.dart';

class UserCubit extends BaseCubit<UserState, User> {
  final ApiRepository _apiRepository;

  UserCubit(this._apiRepository) : super(UserInitial(), User());

  Future<void> getUser() async {
    if (isBusy) return;

    await run(() async {
      emit(UserLoading());

      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';
      final response = await _apiRepository.getUser(token);

      if (response is DataSuccess) {
        data.fullName = response.data!.user.fullName;
        data.closedLoops = response.data!.user.closedLoops;

        emit(UserSuccess(
          message: response.data!.message,
          user: data,
          transactions: data.recentTransactions,
        ));
      } else if (response is DataFailed) {
        if (response.error?.type.name == "unknown") {
          emit(UserUnknownFailure(
            errorMessage: "Unknown error, check internet connections",
          ));
        } else {
          emit(UserFailed(
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
  ) async {
    if (isBusy) return;

    await run(() async {
      emit(UserLoading());

      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';
      final response = await _apiRepository.createP2PPullTransaction(
        request: CreateP2PPullTransactionRequest(
          senderUniqueIdentifier: senderUniqueIdentifier,
          amount: amount,
          closedLoopId: data.closedLoops[0].closedLoopId, // TODO: fix this
        ),
        token: token,
      );

      if (response is DataSuccess) {
        emit(UserSuccess(message: response.data!.message));
      } else if (response is DataFailed) {
        if (response.error?.type.name == "unknown") {
          emit(UserUnknownFailure(
            errorMessage: "Unknown error, check internet connections",
          ));
        } else {
          emit(UserFailed(
            error: response.error,
            errorMessage: response.error?.response?.data["message"],
          ));
        }
      }
    });
  }

  // TODO: DEPRECATE this
  Future<void> initialize() async {
    if (isBusy) return;

    await run(() async {
      emit(UserInitial(user: data));
    });
  }
}

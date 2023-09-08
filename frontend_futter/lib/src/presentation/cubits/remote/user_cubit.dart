import 'package:cardpay/src/domain/models/requests/change_pin_request.dart';
import 'package:cardpay/src/domain/models/requests/create_customer_request.dart';
import 'package:cardpay/src/domain/models/requests/create_p2p_pull_transaction_request.dart';
import 'package:cardpay/src/domain/models/requests/register_closed_loop_request.dart';
import 'package:cardpay/src/domain/models/requests/verify_closed_loop_request.dart';
import 'package:cardpay/src/domain/models/requests/verify_phone_number_request.dart';
import 'package:cardpay/src/domain/models/transaction.dart';
import 'package:cardpay/src/domain/models/user.dart';
import 'package:cardpay/src/domain/repositories/api_repository.dart';
import 'package:cardpay/src/presentation/cubits/base/base_cubit.dart';
import 'package:cardpay/src/utils/constants/event_codes.dart';
import 'package:cardpay/src/utils/data_state.dart';
import 'package:dio/dio.dart';
import 'package:firebase_auth/firebase_auth.dart' as firebase_auth;
import 'package:meta/meta.dart';
import 'package:shared_preferences/shared_preferences.dart';

part 'user_state.dart';

class UserCubit extends BaseCubit<UserState, User> {
  final ApiRepository _apiRepository;
  final SharedPreferences _prefs;

  UserCubit(this._apiRepository, this._prefs) : super(UserInitial(), User());

  Future<void> createCustomer(
    String personalEmail,
    String phoneNumber,
    String fullName,
    String password,
  ) async {
    if (isBusy) return;

    await run(() async {
      emit(UserLoading());

      final response = await _apiRepository.createCustomer(
        request: CreateCustomerRequest(
          fullName: fullName,
          password: password,
          personalEmail: personalEmail,
          phoneNumber: phoneNumber,
        ),
      );

      if (response is DataSuccess) {
        final userId = response.data!.userId;
        data.id = userId;

        await _prefs.setString('user_id', userId);
        await _prefs.setString('user_phone_number', phoneNumber);
        await _prefs.setString('user_password', password);

        emit(UserSuccess(
          message: response.data!.message,
          eventCodes: response.data!.eventCode,
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

  Future<void> verifyPhoneNumber(String otp) async {
    if (isBusy) return;

    await run(() async {
      emit(UserLoading());

      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';

      final response = await _apiRepository.verifyPhoneNumber(
        request: VerifyPhoneNumberRequest(
          otp: otp,
        ),
        token: token,
      );

      if (response is DataSuccess) {
        data.isPhoneNumberVerified = true;

        emit(UserSuccess(
          message: response.data!.message,
          eventCodes: EventCodes.OTP_VERIFIED,
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

  Future<void> registerClosedLoop(
    String closedLoopId,
    String uniqueIdentifier,
  ) async {
    if (isBusy) return;

    await run(() async {
      emit(UserLoading());

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
        emit(UserSuccess(
          message: response.data!.message,
          eventCodes: EventCodes.ORGANIZATION_REGISTERED,
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

  Future<void> verifyClosedLoop(
    String closedLoopId,
    String uniqueIdentifierOtp,
  ) async {
    if (isBusy) return;

    await run(() async {
      emit(UserLoading());

      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';
      final response = await _apiRepository.verifyClosedLoop(
        request: VerifyClosedLoopRequest(
          closedLoopId: closedLoopId,
          uniqueIdentifierOtp: uniqueIdentifierOtp,
        ),
        token: token,
      );

      if (response is DataSuccess) {
        data.closedLoopVerified = true;

        emit(UserSuccess(
          message: response.data!.message,
          eventCodes: EventCodes.ORGANIZATION_VERIFIED,
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

  Future<void> changePin(
    String newPin,
  ) async {
    if (isBusy) return;

    await run(() async {
      emit(UserLoading());

      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';
      final response = await _apiRepository.changePin(
        request: ChangePinRequest(
          newPin: newPin,
        ),
        token: token,
      );

      if (response is DataSuccess) {
        data.pinSetup = true;

        emit(UserSuccess(
          message: response.data!.message,
          eventCodes: EventCodes.PIN_REGISTERED,
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

  Future<void> getUserBalance() async {
    if (isBusy) return;

    await run(() async {
      emit(UserLoading());

      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';
      final response = await _apiRepository.getUserBalance(token);

      if (response is DataSuccess) {
        data.balance = response.data!.balance;

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

  Future<void> getUserRecentTransactions() async {
    if (isBusy) return;

    await run(() async {
      emit(UserLoading());

      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';
      final response = await _apiRepository.getUserRecentTransactions(token);

      if (response is DataSuccess) {
        data.recentTransactions = response.data!.recentTransactions;
        emit(UserSuccess(
          user: data,
          message: response.data!.message,
          transactions: response.data!.recentTransactions,
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

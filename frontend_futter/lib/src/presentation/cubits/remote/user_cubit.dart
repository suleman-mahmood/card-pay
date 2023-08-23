import 'package:cardpay/src/domain/models/requests/change_pin_request.dart';
import 'package:cardpay/src/domain/models/requests/create_customer_request.dart';
import 'package:cardpay/src/domain/models/requests/create_deposit_request.dart';
import 'package:cardpay/src/domain/models/requests/create_p2p_pull_transaction_request.dart';
import 'package:cardpay/src/domain/models/requests/execute_p2p_push_transaction_request.dart';
import 'package:cardpay/src/domain/models/requests/register_closed_loop_request.dart';
import 'package:cardpay/src/domain/models/requests/verify_closed_loop_request.dart';
import 'package:cardpay/src/domain/models/requests/verify_phone_number_request.dart';
import 'package:cardpay/src/domain/models/responses/get_user_recent_transactions_response.dart';
import 'package:cardpay/src/domain/models/user.dart';
import 'package:cardpay/src/domain/repositories/api_repository.dart';
import 'package:cardpay/src/presentation/cubits/base/base_cubit.dart';
import 'package:cardpay/src/utils/constants/event_codes.dart';
import 'package:cardpay/src/utils/data_state.dart';
import 'package:dio/dio.dart';
import 'package:firebase_auth/firebase_auth.dart' as firebase_auth;
import 'package:flutter/services.dart';
import 'package:meta/meta.dart';
import 'package:local_auth/local_auth.dart';
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
        data.id = response.data!.userId;

        await _prefs.setString('user_id', response.data!.userId);
        await _prefs.setString('user_full_name', fullName);
        await _prefs.setString('user_personal_email', personalEmail);
        await _prefs.setString('user_phone_number', phoneNumber);
        await _prefs.setString('user_password', password);

        emit(UserSuccess(
          message: response.data!.message,
          eventCodes: response.data!.eventCode,
        ));
      } else if (response is DataFailed) {
        emit(UserFailed(error: response.error));
      }
    });
  }

  Future<void> verifyPhoneNumber(String otp) async {
    if (isBusy) return;

    await run(() async {
      emit(UserLoading());

      final response = await _apiRepository.verifyPhoneNumber(
        request: VerifyPhoneNumberRequest(
          userId: data.id,
          otp: otp,
        ),
      );

      if (response is DataSuccess) {
        data.isPhoneNumberVerified = true;

        emit(UserSuccess(
          message: response.data!.message,
          eventCodes: EventCodes.OTP_VERIFIED,
        ));
      } else if (response is DataFailed) {
        emit(UserFailed(error: response.error));
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

      final response = await _apiRepository.registerClosedLoop(
        request: RegisterClosedLoopRequest(
          userId: data.id,
          closedLoopId: closedLoopId,
          uniqueIdentifier: uniqueIdentifier,
        ),
      );

      if (response is DataSuccess) {
        emit(UserSuccess(
          message: response.data!.message,
          eventCodes: EventCodes.ORGANIZATION_REGISTERED,
        ));
      } else if (response is DataFailed) {
        emit(UserFailed(error: response.error));
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

      final response = await _apiRepository.verifyClosedLoop(
        request: VerifyClosedLoopRequest(
          userId: data.id,
          closedLoopId: closedLoopId,
          uniqueIdentifierOtp: uniqueIdentifierOtp,
        ),
      );

      if (response is DataSuccess) {
        data.closedLoopVerified = true;

        emit(UserSuccess(
          message: response.data!.message,
          eventCodes: EventCodes.ORGANIZATION_VERIFIED,
        ));
      } else if (response is DataFailed) {
        emit(UserFailed(error: response.error));
      }
    });
  }

  Future<void> changePin(
    String newPin,
  ) async {
    if (isBusy) return;

    await run(() async {
      emit(UserLoading());

      final response = await _apiRepository.changePin(
        request: ChangePinRequest(
          userId: data.id,
          newPin: newPin,
        ),
      );

      if (response is DataSuccess) {
        data.pinSetup = true;

        emit(UserSuccess(
          message: response.data!.message,
          eventCodes: EventCodes.PIN_REGISTERED,
        ));
      } else if (response is DataFailed) {
        emit(UserFailed(error: response.error));
      }
    });
  }

  Future<void> termsDenied() async {
    if (isBusy) return;

    String errorMessage = 'Please accept the terms and conditions to continue';

    await run(() async {
      emit(UserSuccess(
        eventCodes: EventCodes.TERMS_DENIED,
        message: errorMessage,
      ));
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

        emit(UserSuccess(
          message: response.data!.message,
          user: data,
          transactions: data.recentTransactions,
        ));
      } else if (response is DataFailed) {
        emit(UserFailed(error: response.error));
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
        emit(UserFailed(error: response.error));
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

      data.recentTransactions = response.data!.recentTransactions;

      if (response is DataSuccess) {
        emit(UserSuccess(
          user: data,
          message: response.data!.message,
          transactions: response.data!.recentTransactions,
        ));
      } else if (response is DataFailed) {
        emit(UserFailed(error: response.error));
      }
    });
  }

  Future<void> createDepositRequest(double amount) async {
    if (isBusy) return;

    await run(() async {
      emit(UserLoading());

      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';
      final response = await _apiRepository.createDepositRequest(
        request: CreateDepositRequest(userId: data.id, amount: amount),
        token: token,
      );

      if (response is DataSuccess) {
        emit(UserSuccess(
          message: response.data!.message,
          checkoutUrl: response.data!.checkoutUrl,
        ));
      } else if (response is DataFailed) {
        emit(UserFailed(error: response.error));
      }
    });
  }

  Future<void> executeP2PPushTransaction(
      String recipientUniqueIdentifier, double amount) async {
    if (isBusy) return;

    await run(() async {
      emit(UserLoading());

      final token =
          await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
              '';
      final response = await _apiRepository.executeP2PPushTransaction(
        request: ExecuteP2PPushTransactionRequest(
          recipientUniqueIdentifier: recipientUniqueIdentifier,
          amount: amount,
          closedLoopId: '',
        ),
        token: token,
      );

      if (response is DataSuccess) {
        emit(UserSuccess(message: response.data!.message));
      } else if (response is DataFailed) {
        emit(UserFailed(error: response.error));
      }
    });
  }

  Future<void> createP2PPullTransaction(
    String senderUniqueIdentifier,
    double amount,
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
        ),
        token: token,
      );

      if (response is DataSuccess) {
        emit(UserSuccess(message: response.data!.message));
      } else if (response is DataFailed) {
        emit(UserFailed(error: response.error));
      }
    });
  }

  Future<void> login(
    String phoneNumber,
    String password,
  ) async {
    if (isBusy) return;

    await run(() async {
      emit(UserLoading());

      final String emailAddress = '92$phoneNumber@cardpay.com.pk';
      try {
        await firebase_auth.FirebaseAuth.instance.signInWithEmailAndPassword(
          email: emailAddress,
          password: password,
        );
        emit(UserSuccess(
          message: "Sign in was successful",
          eventCodes: EventCodes.USER_AUTHENTICATED,
        ));
      } on firebase_auth.FirebaseAuthException catch (e) {
        emit(UserFailed(errorMessage: e.message ?? ''));
      }
    });
  }

  Future<void> loginWithBiometric() async {
    if (isBusy) return;

    await run(() async {
      emit(UserLoading());
      final LocalAuthentication auth = LocalAuthentication();
      bool didAuthenticate = false;

      try {
        didAuthenticate = await auth.authenticate(
          localizedReason: 'Please authenticate to log in',
        );

        if (didAuthenticate) {
          final personalEmail = _prefs.getString('user_personal_email');
          final password = _prefs.getString('user_password');

          emit(UserSuccess(
            message: "Sign in was successful",
            eventCodes: EventCodes.USER_AUTHENTICATED_WITH_BIOMETRIC,
            email: personalEmail,
            password: password,
          ));
        } else {
          emit(UserFailed(errorMessage: 'Authentication failed'));
        }
      } on PlatformException catch (e) {
        emit(UserFailed(errorMessage: e.message ?? ''));
      }
    });
  }

  Future<void> logout() async {
    if (isBusy) return;

    await run(() async {
      emit(UserLoading());

      try {
        await firebase_auth.FirebaseAuth.instance.signOut();
        emit(UserSuccess(
          message: "Log out was successful",
          eventCodes: EventCodes.LOGOUT_SUCCESSFUL,
        ));
      } on firebase_auth.FirebaseAuthException catch (e) {
        emit(UserFailed(errorMessage: e.message ?? ''));
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

  Future<void> fetchQrInfo(
    String qrData,
  ) async {
    if (isBusy) return;

    await run(() async {
      emit(UserLoading());

      Future.delayed(const Duration(seconds: 1), () {
        emit(
          UserSuccess(
            qrTitle: 'The Bunker',
            eventCodes: EventCodes.QR_DATA_FETCHED,
          ),
        );
      });

      // TODO: Proper API implementation
    });
  }
}

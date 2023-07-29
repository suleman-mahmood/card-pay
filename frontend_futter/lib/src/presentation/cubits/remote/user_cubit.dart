import 'package:cardpay/src/domain/models/requests/change_pin_request.dart';
import 'package:cardpay/src/domain/models/requests/create_customer_request.dart';
import 'package:cardpay/src/domain/models/requests/create_deposit_request.dart';
import 'package:cardpay/src/domain/models/requests/create_p2p_pull_transaction_request.dart';
import 'package:cardpay/src/domain/models/requests/execute_p2p_push_transaction_request.dart';
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

part 'user_state.dart';

class UserCubit extends BaseCubit<UserState, User> {
  final ApiRepository _apiRepository;

  UserCubit(this._apiRepository) : super(UserInitial(), User());

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

      Future.delayed(const Duration(seconds: 1), () {
        data.fullName = "Suleman";
        emit(UserSuccess(user: data));
      });

      // TODO: uncomment in production
      // final token =
      //     await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
      //         '';
      // final response = await _apiRepository.getUser(token);

      // if (response is DataSuccess) {
      //   data.fullName = response.data!.user.fullName;

      //   emit(UserSuccess(
      //     message: response.data!.message,
      //     user: data,
      //   ));
      // } else if (response is DataFailed) {
      //   emit(UserFailed(error: response.error));
      // }
    });
  }

  Future<void> getUserBalance() async {
    if (isBusy) return;

    await run(() async {
      emit(UserLoading());

      Future.delayed(const Duration(seconds: 1), () {
        data.balance = 500;
        emit(UserSuccess(user: data));
      });

      // TODO: uncomment in production
      // final token =
      //     await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
      //         '';
      // final response = await _apiRepository.getUserBalance(token);

      // if (response is DataSuccess) {
      //   data.balance = response.data!.balance;

      //   emit(UserSuccess(
      //     message: response.data!.message,
      //     user: data,
      //   ));
      // } else if (response is DataFailed) {
      //   emit(UserFailed(error: response.error));
      // }
    });
  }

  Future<void> getUserRecentTransactions() async {
    if (isBusy) return;

    await run(() async {
      emit(UserLoading());

      Future.delayed(const Duration(seconds: 1), () {
        final recentTransactions = [
          Transaction(
            id: '',
            amount: 251,
            mode: TransactionMode.APP_TRANSFER,
            transactionType: TransactionType.P2P_PUSH,
            status: TransactionStatus.SUCCESSFUL,
            createdAt: DateTime.now(),
            lastUpdated: DateTime.now(),
            senderWalletId: 'Suleman',
            recipientWalletId: 'Namelus',
          ),
          Transaction(
            id: '',
            amount: 501,
            mode: TransactionMode.APP_TRANSFER,
            transactionType: TransactionType.P2P_PUSH,
            status: TransactionStatus.SUCCESSFUL,
            createdAt: DateTime.now(),
            lastUpdated: DateTime.now(),
            senderWalletId: 'Suleman',
            recipientWalletId: 'Namelus',
          )
        ];
        data.recentTransactions = recentTransactions;
        emit(UserSuccess(user: data));
      });

      // final token =
      //     await firebase_auth.FirebaseAuth.instance.currentUser?.getIdToken() ??
      //         '';
      // final response = await _apiRepository.getUserRecentTransactions(token);

      // if (response is DataSuccess) {
      //   emit(UserSuccess(
      //     message: response.data!.message,
      //     transactions: response.data!.recentTransactions,
      //   ));
      // } else if (response is DataFailed) {
      //   emit(UserFailed(error: response.error));
      // }
    });
  }

  Future<void> createDepositRequest(double amount) async {
    if (isBusy) return;

    await run(() async {
      emit(UserLoading());

      Future.delayed(const Duration(seconds: 1), () {
        emit(
          UserSuccess(
            checkoutUrl:
                'https://marketplace.paypro.com.pk/pyb?bid=MTIzNTIzMjA3MDAwMDE%3d',
            user: data,
          ),
        );
      });

      // TODO: uncomment in production
      // final response = await _apiRepository.createDepositRequest(
      //   request: CreateDepositRequest(userId: data.id, amount: amount),
      // );

      // if (response is DataSuccess) {
      //   emit(UserSuccess(
      //     message: response.data!.message,
      //     checkoutUrl: response.data!.checkoutUrl,
      //   ));
      // } else if (response is DataFailed) {
      //   emit(UserFailed(error: response.error));
      // }
    });
  }

  Future<void> executeP2PPushTransaction(
      String recipientUniqueIdentifier, double amount) async {
    if (isBusy) return;

    await run(() async {
      emit(UserLoading());

      Future.delayed(const Duration(seconds: 1), () {
        emit(
          UserSuccess(eventCodes: EventCodes.TRANSFER_SUCCESSFUL),
        );
      });
      // TODO: uncomment in production
      // final response = await _apiRepository.executeP2PPushTransaction(
      //   request: ExecuteP2PPushTransactionRequest(
      //     recipientUniqueIdentifier: recipientUniqueIdentifier,
      //     amount: amount,
      //   ),
      // );

      // if (response is DataSuccess) {
      //   emit(UserSuccess(
      //     message: response.data!.message,
      //   ));
      // } else if (response is DataFailed) {
      //   emit(UserFailed(error: response.error));
      // }
    });
  }

  Future<void> createP2PPullTransaction(
    String senderUniqueIdentifier,
    double amount,
  ) async {
    if (isBusy) return;

    await run(() async {
      emit(UserLoading());

      Future.delayed(const Duration(seconds: 1), () {
        emit(
          UserSuccess(eventCodes: EventCodes.REQUEST_SUCCESSFUL),
        );
      });

      // TODO: uncomment in production
      // final response = await _apiRepository.createP2PPullTransaction(
      //   request: CreateP2PPullTransactionRequest(
      //     senderUniqueIdentifier: senderUniqueIdentifier,
      //     amount: amount,
      //   ),
      // );

      // if (response is DataSuccess) {
      //   emit(UserSuccess(message: response.data!.message));
      // } else if (response is DataFailed) {
      //   emit(UserFailed(error: response.error));
      // }
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
        print("Sign in was successful");
        emit(UserSuccess(
          message: "Sign in was successful",
          eventCodes: EventCodes.USER_AUTHENTICATED,
        ));
      } on firebase_auth.FirebaseAuthException catch (e) {
        print(e);
        emit(UserFailed(errorMessage: e.message ?? ''));
      }
    });
  }

  Future<void> initialize() async {
    if (isBusy) return;

    await run(() async {
      emit(UserInitial(user: data));
    });
  }
}

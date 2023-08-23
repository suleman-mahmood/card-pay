import 'package:cardpay/src/domain/models/closed_loop.dart';
import 'package:cardpay/src/domain/models/requests/change_pin_request.dart';
import 'package:cardpay/src/domain/models/requests/create_customer_request.dart';
import 'package:cardpay/src/domain/models/requests/create_deposit_request.dart';
import 'package:cardpay/src/domain/models/requests/create_p2p_pull_transaction_request.dart';
import 'package:cardpay/src/domain/models/requests/execute_p2p_push_transaction_request.dart';
import 'package:cardpay/src/domain/models/requests/register_closed_loop_request.dart';
import 'package:cardpay/src/domain/models/requests/verify_closed_loop_request.dart';
import 'package:cardpay/src/domain/models/requests/verify_phone_number_request.dart';
import 'package:cardpay/src/domain/models/responses/change_pin_response.dart';
import 'package:cardpay/src/domain/models/responses/create_customer_response.dart';
import 'package:cardpay/src/domain/models/responses/create_deposit_response.dart';
import 'package:cardpay/src/domain/models/responses/create_p2p_pull_transaction_response.dart';
import 'package:cardpay/src/domain/models/responses/execute_p2p_push_transaction_response.dart';
import 'package:cardpay/src/domain/models/responses/get_all_closed_loops_response.dart';
import 'package:cardpay/src/domain/models/responses/get_user_balance_response.dart';
import 'package:cardpay/src/domain/models/responses/get_user_recent_transactions_response.dart';
import 'package:cardpay/src/domain/models/responses/get_user_response.dart';
import 'package:cardpay/src/domain/models/responses/register_closed_loop_response.dart';
import 'package:cardpay/src/domain/models/responses/verify_closed_loop_response.dart';
import 'package:cardpay/src/domain/models/responses/verify_phone_number_response.dart';
import 'package:cardpay/src/domain/models/transaction.dart';
import 'package:cardpay/src/utils/constants/event_codes.dart';
import 'package:cardpay/src/utils/data_state.dart';

import '../../domain/repositories/api_repository.dart';
import 'base/base_api_repository.dart';

class FakeApiRepositoryImpl extends BaseApiRepository implements ApiRepository {
  FakeApiRepositoryImpl();

  @override
  Future<DataState<CreateCustomerResponse>> createCustomer({
    required CreateCustomerRequest request,
  }) {
    CreateCustomerResponse dummyUserData = CreateCustomerResponse(
      success: true,
      message: 'Customer created successfully',
      eventCode: EventCodes.OTP_SENT,
      userId: "123",
    );

    return Future.value(DataSuccess(dummyUserData));
  }

  @override
  Future<DataState<VerifyPhoneNumberResponse>> verifyPhoneNumber({
    required VerifyPhoneNumberRequest request,
  }) {
    VerifyPhoneNumberResponse verificationStatus = VerifyPhoneNumberResponse(
      success: true,
      message: 'Phone number verified successfully',
    );

    return Future.value(DataSuccess(verificationStatus));
  }

  @override
  Future<DataState<GetAllClosedLoopsResponse>> getAllClosedLoops() {
    return Future.value(DataSuccess(GetAllClosedLoopsResponse(
      success: true,
      message: 'Customer created successfully',
      closedLoops: [
        ClosedLoop(
          name: 'Nust',
          id: 'Nust-id',
        ),
        ClosedLoop(
          name: 'Fast',
          id: 'fast-id',
        ),
      ],
    )));
  }

  @override
  Future<DataState<RegisterClosedLoopResponse>> registerClosedLoop({
    required RegisterClosedLoopRequest request,
  }) {
    RegisterClosedLoopResponse registerClosedLoopResponse =
        RegisterClosedLoopResponse(
      success: true,
      message: 'close loop registered successfully',
    );

    return Future.value(DataSuccess(registerClosedLoopResponse));
  }

  @override
  Future<DataState<VerifyClosedLoopResponse>> verifyClosedLoop({
    required VerifyClosedLoopRequest request,
  }) {
    VerifyClosedLoopResponse VerifyClosedLoopRequest = VerifyClosedLoopResponse(
      success: true,
      message: 'close loop verified successfully',
    );

    return Future.value(DataSuccess(VerifyClosedLoopRequest));
  }

  @override
  Future<DataState<ChangePinResponse>> changePin({
    required ChangePinRequest request,
  }) {
    ChangePinResponse ChangePinRequest = ChangePinResponse(
      success: true,
      message: 'Pin changed successfully',
    );

    return Future.value(DataSuccess(ChangePinRequest));
  }

  Future<DataState<GetUserResponse>> getUser(String token) {
    return Future.value(
      DataSuccess(
        GetUserResponse(
          user: UserResponse(
            fullName: 'Suleman',
            id: '123',
          ),
          success: true,
          message: 'Customer created successfully',
        ),
      ),
    );
  }

  Future<DataState<GetUserBalanceResponse>> getUserBalance(String token) {
    return Future.value(
      DataSuccess(
        GetUserBalanceResponse(
          success: true,
          message: 'Customer created successfully',
          balance: 1000,
        ),
      ),
    );
  }

  Future<DataState<GetUserRecentTransactionsResponse>>
      getUserRecentTransactions(String token) {
    return Future.value(
      DataSuccess(
        GetUserRecentTransactionsResponse(
          success: true,
          message: 'Customer created successfully',
          recentTransactions: [
            TransactionResponse(
              id: 'transaction-1',
              amount: 251,
              mode: TransactionMode.APP_TRANSFER,
              transactionType: TransactionType.P2P_PUSH,
              status: TransactionStatus.SUCCESSFUL,
              createdAt: DateTime.now(),
              lastUpdated: DateTime.now(),
              senderName: 'Suleman',
              recipientName: 'Namelus',
            ),
            TransactionResponse(
              id: 'transaction-2',
              amount: 501,
              mode: TransactionMode.APP_TRANSFER,
              transactionType: TransactionType.P2P_PUSH,
              status: TransactionStatus.SUCCESSFUL,
              createdAt: DateTime.now(),
              lastUpdated: DateTime.now(),
              senderName: 'Suleman',
              recipientName: 'Namelus',
            )
          ],
        ),
      ),
    );
  }

  Future<DataState<CreateDepositResponse>> createDepositRequest({
    required CreateDepositRequest request,
    required String token,
  }) {
    CreateDepositResponse CreateDepositRequest = CreateDepositResponse(
        success: true,
        message: 'Customer created successfully',
        checkoutUrl:
            'https://marketplace.paypro.com.pk/pyb?bid=MTIzNTIzMjA3MDAwMDE%3d');

    return Future.value(DataSuccess(CreateDepositRequest));
  }

  Future<DataState<ExecuteP2PPushTransactionResponse>>
      executeP2PPushTransaction({
    required ExecuteP2PPushTransactionRequest request,
    required String token,
  }) {
    ExecuteP2PPushTransactionResponse ExecuteP2PPushTransactionRequest =
        ExecuteP2PPushTransactionResponse(
      success: true,
      message: 'Execute successfully',
    );

    return Future.value(DataSuccess(ExecuteP2PPushTransactionRequest));
  }

  Future<DataState<CreateP2PPullTransactionResponse>> createP2PPullTransaction({
    required CreateP2PPullTransactionRequest request,
    required String token,
  }) {
    CreateP2PPullTransactionResponse CreateP2PPullTransactionRequest =
        CreateP2PPullTransactionResponse(
      success: true,
      message: 'Transection is successfully',
    );

    return Future.value(DataSuccess(CreateP2PPullTransactionRequest));
  }
}

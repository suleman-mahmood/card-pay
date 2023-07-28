import 'package:cardpay/src/data/datasources/remote/python_api_service.dart';
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
import 'package:cardpay/src/utils/data_state.dart';

import '../../domain/repositories/api_repository.dart';
import 'base/base_api_repository.dart';

class ApiRepositoryImpl extends BaseApiRepository implements ApiRepository {
  final PythonApiService _pythonApiService;

  ApiRepositoryImpl(this._pythonApiService);

  @override
  Future<DataState<CreateCustomerResponse>> createCustomer({
    required CreateCustomerRequest request,
  }) {
    return getStateOf<CreateCustomerResponse>(
      request: () => _pythonApiService.createCustomer(
        createCustomerRequest: request,
      ),
    );
  }

  @override
  Future<DataState<VerifyPhoneNumberResponse>> verifyPhoneNumber({
    required VerifyPhoneNumberRequest request,
  }) {
    return getStateOf<VerifyPhoneNumberResponse>(
      request: () => _pythonApiService.verifyPhoneNumber(
        verifyPhoneNumberRequest: request,
      ),
    );
  }

  @override
  Future<DataState<GetAllClosedLoopsResponse>> getAllClosedLoops() {
    return getStateOf<GetAllClosedLoopsResponse>(
      request: () => _pythonApiService.getAllClosedLoops(),
    );
  }

  @override
  Future<DataState<RegisterClosedLoopResponse>> registerClosedLoop({
    required RegisterClosedLoopRequest request,
  }) {
    return getStateOf<RegisterClosedLoopResponse>(
      request: () => _pythonApiService.registerClosedLoop(
        registerClosedLoopRequest: request,
      ),
    );
  }

  @override
  Future<DataState<VerifyClosedLoopResponse>> verifyClosedLoop({
    required VerifyClosedLoopRequest request,
  }) {
    return getStateOf<VerifyClosedLoopResponse>(
      request: () => _pythonApiService.verifyClosedLoop(
        verifyClosedLoopRequest: request,
      ),
    );
  }

  @override
  Future<DataState<ChangePinResponse>> changePin({
    required ChangePinRequest request,
  }) {
    return getStateOf<ChangePinResponse>(
      request: () => _pythonApiService.changePin(
        changePinRequest: request,
      ),
    );
  }

  Future<DataState<GetUserResponse>> getUser(String token) {
    return getStateOf<GetUserResponse>(
      request: () => _pythonApiService.getUser(token: 'Bearer $token'),
    );
  }

  Future<DataState<GetUserBalanceResponse>> getUserBalance(String token) {
    return getStateOf<GetUserBalanceResponse>(
      request: () => _pythonApiService.getUserBalance(token: 'Bearer $token'),
    );
  }

  Future<DataState<GetUserRecentTransactionsResponse>>
      getUserRecentTransactions(String token) {
    return getStateOf<GetUserRecentTransactionsResponse>(
      request: () => _pythonApiService.getUserRecentTransactions(
        token: 'Bearer $token',
      ),
    );
  }

  Future<DataState<CreateDepositResponse>> createDepositRequest({
    required CreateDepositRequest request,
  }) {
    return getStateOf<CreateDepositResponse>(
      request: () => _pythonApiService.createDepositRequest(
        createDepositRequest: request,
      ),
    );
  }

  Future<DataState<ExecuteP2PPushTransactionResponse>>
      executeP2PPushTransaction({
    required ExecuteP2PPushTransactionRequest request,
  }) {
    return getStateOf<ExecuteP2PPushTransactionResponse>(
      request: () => _pythonApiService.executeP2PPushTransaction(
        executeP2PPushTransactionRequest: request,
      ),
    );
  }

  Future<DataState<CreateP2PPullTransactionResponse>> createP2PPullTransaction({
    required CreateP2PPullTransactionRequest request,
  }) {
    return getStateOf<CreateP2PPullTransactionResponse>(
      request: () => _pythonApiService.createP2PPullTransaction(
        createP2PPullTransactionRequest: request,
      ),
    );
  }
}
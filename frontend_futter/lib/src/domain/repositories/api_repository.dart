import 'package:cardpay/src/domain/models/requests/change_pin_request.dart';
import 'package:cardpay/src/domain/models/requests/create_customer_request.dart';
import 'package:cardpay/src/domain/models/requests/create_deposit_request.dart';
import 'package:cardpay/src/domain/models/requests/create_p2p_pull_transaction_request.dart';
import 'package:cardpay/src/domain/models/requests/execute_p2p_push_transaction_request.dart';
import 'package:cardpay/src/domain/models/requests/execute_qr_transaction_request.dart';
import 'package:cardpay/src/domain/models/requests/register_closed_loop_request.dart';
import 'package:cardpay/src/domain/models/requests/register_event_request.dart';
import 'package:cardpay/src/domain/models/requests/set_fcm_token_request.dart';
import 'package:cardpay/src/domain/models/requests/verify_closed_loop_request.dart';
import 'package:cardpay/src/domain/models/requests/verify_phone_number_request.dart';
import 'package:cardpay/src/domain/models/responses/change_pin_response.dart';
import 'package:cardpay/src/domain/models/responses/create_customer_response.dart';
import 'package:cardpay/src/domain/models/responses/create_deposit_response.dart';
import 'package:cardpay/src/domain/models/responses/create_p2p_pull_transaction_response.dart';
import 'package:cardpay/src/domain/models/responses/execute_p2p_push_transaction_response.dart';
import 'package:cardpay/src/domain/models/responses/execute_qr_transaction_response.dart';
import 'package:cardpay/src/domain/models/responses/get_all_closed_loops_response.dart';
import 'package:cardpay/src/domain/models/responses/get_checkpoint_response.dart';
import 'package:cardpay/src/domain/models/responses/get_events_response.dart';
import 'package:cardpay/src/domain/models/responses/get_frequent_users_response.dart';
import 'package:cardpay/src/domain/models/responses/get_user_balance_response.dart';
import 'package:cardpay/src/domain/models/responses/get_user_recent_transactions_response.dart';
import 'package:cardpay/src/domain/models/responses/get_user_response.dart';
import 'package:cardpay/src/domain/models/responses/register_closed_loop_response.dart';
import 'package:cardpay/src/domain/models/responses/register_event_response.dart';
import 'package:cardpay/src/domain/models/responses/set_fcm_token_response.dart';
import 'package:cardpay/src/domain/models/responses/verify_closed_loop_response.dart';
import 'package:cardpay/src/domain/models/responses/verify_phone_number_response.dart';
import 'package:cardpay/src/domain/models/responses/version_update_response.dart';
import 'package:cardpay/src/domain/models/responses/get_full_name_response.dart';
import 'package:cardpay/src/domain/models/user_info.dart';

import 'package:cardpay/src/utils/data_state.dart';

abstract class ApiRepository {
  Future<DataState<CreateCustomerResponse>> createCustomer({
    required CreateCustomerRequest request,
  });

  Future<DataState<VerifyPhoneNumberResponse>> verifyPhoneNumber({
    required VerifyPhoneNumberRequest request,
    required String token,
  });

  Future<DataState<GetAllClosedLoopsResponse>> getAllClosedLoops(String token);

  Future<DataState<RegisterClosedLoopResponse>> registerClosedLoop({
    required RegisterClosedLoopRequest request,
    required String token,
  });

  Future<DataState<VerifyClosedLoopResponse>> verifyClosedLoop({
    required VerifyClosedLoopRequest request,
    required String token,
  });

  Future<DataState<ChangePinResponse>> changePin({
    required ChangePinRequest request,
    required String token,
  });

  Future<DataState<GetUserResponse>> getUser(String token);

  Future<DataState<GetUserBalanceResponse>> getUserBalance(String token);

  Future<DataState<GetUserRecentTransactionsResponse>>
      getUserRecentTransactions(String token);

  Future<DataState<CreateDepositResponse>> createDepositRequest({
    required CreateDepositRequest request,
    required String token,
  });

  Future<DataState<ExecuteP2PPushTransactionResponse>>
      executeP2PPushTransaction({
    required ExecuteP2PPushTransactionRequest request,
    required String token,
  });

  Future<DataState<ExecuteQrTransactionResponse>> executeQrTransaction({
    required ExecuteQrTransactionRequest request,
    required String token,
  });

  Future<DataState<CreateP2PPullTransactionResponse>> createP2PPullTransaction({
    required CreateP2PPullTransactionRequest request,
    required String token,
  });
  Future<DataState<GetCheckpointsResponse>> getCheckpoints(
    String token,
  );
  Future<DataState<GetVersionsResponse>> getVersions();

  Future<DataState<GetFullNameResponse>> getFullName({
    required String uniqueIdentifier,
    required String closedLoopId,
    required String token,
  });

  Future<DataState<GetFrequentUsersResponse>> getFrequentUsers({
    required String closedLoopId,
    required String token,
  });

  Future<DataState<SetFcmTokenResponse>> setFcmToken({
    required SetFcmTokenRequest request,
    required String token,
  });

  // Events
  Future<DataState<GetEventsResponse>> getLiveEvents({
    required String token,
    required String closedLoopId,
  });

  Future<DataState<GetEventsResponse>> getRegisteredEvents({
    required String token,
  });

  Future<DataState<RegisterEventResponse>> registerEvent({
    required RegisterEventRequest registerEventRequest,
    required String token,
  });
}

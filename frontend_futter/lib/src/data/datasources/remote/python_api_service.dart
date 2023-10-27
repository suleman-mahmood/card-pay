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
import 'package:cardpay/src/domain/models/responses/get_user_balance_response.dart';
import 'package:cardpay/src/domain/models/responses/get_full_name_response.dart';
import 'package:cardpay/src/domain/models/responses/get_user_recent_transactions_response.dart';
import 'package:cardpay/src/domain/models/responses/get_user_response.dart';
import 'package:cardpay/src/domain/models/responses/register_closed_loop_response.dart';
import 'package:cardpay/src/domain/models/responses/register_event_response.dart';
import 'package:cardpay/src/domain/models/responses/set_fcm_token_response.dart';
import 'package:cardpay/src/domain/models/responses/verify_closed_loop_response.dart';
import 'package:cardpay/src/domain/models/responses/verify_phone_number_response.dart';
import 'package:cardpay/src/domain/models/responses/version_update_response.dart';
import 'package:dio/dio.dart';
import 'package:cardpay/src/utils/constants/strings.dart';
import 'package:retrofit/retrofit.dart';

part 'python_api_service.g.dart';

@RestApi(baseUrl: baseUrl, parser: Parser.MapSerializable)
abstract class PythonApiService {
  factory PythonApiService(Dio dio, {String baseUrl}) = _PythonApiService;

  @POST('/create-customer')
  Future<HttpResponse<CreateCustomerResponse>> createCustomer({
    @Body() CreateCustomerRequest? createCustomerRequest,
  });

  @POST('/verify-phone-number')
  Future<HttpResponse<VerifyPhoneNumberResponse>> verifyPhoneNumber({
    @Body() VerifyPhoneNumberRequest? verifyPhoneNumberRequest,
    @Header("Authorization") String? token,
  });

  @GET('/get-all-closed-loops')
  Future<HttpResponse<GetAllClosedLoopsResponse>> getAllClosedLoops({
    @Header("Authorization") String? token,
  });

  @POST('/register-closed-loop')
  Future<HttpResponse<RegisterClosedLoopResponse>> registerClosedLoop({
    @Body() RegisterClosedLoopRequest? registerClosedLoopRequest,
    @Header("Authorization") String? token,
  });

  @POST('/verify-closed-loop')
  Future<HttpResponse<VerifyClosedLoopResponse>> verifyClosedLoop({
    @Body() VerifyClosedLoopRequest? verifyClosedLoopRequest,
    @Header("Authorization") String? token,
  });

  @POST('/change-pin')
  Future<HttpResponse<ChangePinResponse>> changePin({
    @Body() ChangePinRequest? changePinRequest,
    @Header("Authorization") String? token,
  });

  @GET('/get-user')
  Future<HttpResponse<GetUserResponse>> getUser({
    @Header("Authorization") String? token,
  });

  @GET('/get-user-balance')
  Future<HttpResponse<GetUserBalanceResponse>> getUserBalance({
    @Header("Authorization") String? token,
  });

  @GET('/get-user-recent-transactions')
  Future<HttpResponse<GetUserRecentTransactionsResponse>>
      getUserRecentTransactions({
    @Header("Authorization") String? token,
  });

  @POST('/create-deposit-request')
  Future<HttpResponse<CreateDepositResponse>> createDepositRequest({
    @Body() CreateDepositRequest? createDepositRequest,
    @Header("Authorization") String? token,
  });

  @POST('/execute-p2p-push-transaction')
  Future<HttpResponse<ExecuteP2PPushTransactionResponse>>
      executeP2PPushTransaction({
    @Body() ExecuteP2PPushTransactionRequest? executeP2PPushTransactionRequest,
    @Header("Authorization") String? token,
  });

  @POST('/execute-qr-transaction')
  Future<HttpResponse<ExecuteQrTransactionResponse>> executeQrTransaction({
    @Body() ExecuteQrTransactionRequest? executeQrTransactionRequest,
    @Header("Authorization") String? token,
  });

  @POST('/create-p2p-pull-transaction')
  Future<HttpResponse<CreateP2PPullTransactionResponse>>
      createP2PPullTransaction({
    @Body() CreateP2PPullTransactionRequest? createP2PPullTransactionRequest,
    @Header("Authorization") String? token,
  });

  @GET('/get-user-checkpoints')
  Future<HttpResponse<GetCheckpointsResponse>> getCheckpoints({
    @Header("Authorization") String? token,
  });

  @GET('/get-latest-force-update-version')
  Future<HttpResponse<GetVersionsResponse>> getVersions();

  @GET('/get-name-from-unique-identifier-and-closed-loop')
  Future<HttpResponse<GetFullNameResponse>> getFullName({
    @Query("unique_identifier") required String uniqueIdentifier,
    @Query("closed_loop_id") required String closedLoopId,
    @Header("Authorization") required String token,
  });

  @POST('/set-fcm-token')
  Future<HttpResponse<SetFcmTokenResponse>> setFcmToken({
    @Body() SetFcmTokenRequest? request,
    @Header("Authorization") String? token,
  });

  // Events
  @GET("/get-live-events")
  Future<HttpResponse<GetEventsResponse>> getLiveEvents({
    @Query("closed_loop_id") required String closedLoopId,
    @Header("Authorization") required String token,
  });

  @GET("/get-registered-events")
  Future<HttpResponse<GetEventsResponse>> getRegisteredEvents({
    @Header("Authorization") required String token,
  });

  @POST('/register-event')
  Future<HttpResponse<RegisterEventResponse>> registerEvent({
    @Body() required RegisterEventRequest registerEventRequest,
    @Header("Authorization") required String token,
  });
}

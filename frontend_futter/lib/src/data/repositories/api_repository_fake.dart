import 'package:cardpay/src/domain/models/checkpoints.dart';
import 'package:cardpay/src/domain/models/closed_loop.dart';
import 'package:cardpay/src/domain/models/event.dart';
import 'package:cardpay/src/domain/models/p2p_request_info.dart';
import 'package:cardpay/src/domain/models/requests/accept_p2p_pull_transaction_request.dart';
import 'package:cardpay/src/domain/models/requests/change_pin_request.dart';
import 'package:cardpay/src/domain/models/requests/create_customer_request.dart';
import 'package:cardpay/src/domain/models/requests/create_deposit_request.dart';
import 'package:cardpay/src/domain/models/requests/create_p2p_pull_transaction_request.dart';
import 'package:cardpay/src/domain/models/requests/decline_p2p_pull_transaction_request.dart';
import 'package:cardpay/src/domain/models/requests/execute_p2p_push_transaction_request.dart';
import 'package:cardpay/src/domain/models/requests/execute_qr_transaction_request.dart';
import 'package:cardpay/src/domain/models/requests/register_closed_loop_request.dart';
import 'package:cardpay/src/domain/models/requests/register_event_request.dart';
import 'package:cardpay/src/domain/models/requests/set_fcm_token_request.dart';
import 'package:cardpay/src/domain/models/requests/verify_closed_loop_request.dart';
import 'package:cardpay/src/domain/models/requests/verify_phone_number_request.dart';
import 'package:cardpay/src/domain/models/responses/change_pin_response.dart';
import 'package:cardpay/src/domain/models/responses/common_response.dart';
import 'package:cardpay/src/domain/models/responses/create_customer_response.dart';
import 'package:cardpay/src/domain/models/responses/create_deposit_response.dart';
import 'package:cardpay/src/domain/models/responses/create_p2p_pull_transaction_response.dart';
import 'package:cardpay/src/domain/models/responses/execute_p2p_push_transaction_response.dart';
import 'package:cardpay/src/domain/models/responses/execute_qr_transaction_response.dart';
import 'package:cardpay/src/domain/models/responses/get_all_closed_loops_response.dart';
import 'package:cardpay/src/domain/models/responses/get_checkpoint_response.dart';
import 'package:cardpay/src/domain/models/responses/get_events_response.dart';
import 'package:cardpay/src/domain/models/responses/get_frequent_users_response.dart';
import 'package:cardpay/src/domain/models/responses/get_p2p_pull_requests_response.dart';
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
import 'package:cardpay/src/domain/models/transaction.dart';
import 'package:cardpay/src/domain/models/user_info.dart';
import 'package:cardpay/src/domain/models/version.dart';
import 'package:cardpay/src/domain/repositories/api_repository.dart';
import 'package:cardpay/src/utils/constants/event_codes.dart';
import 'package:cardpay/src/utils/data_state.dart';
import 'package:dio/dio.dart';
import 'base/base_api_repository.dart';

class FakeApiRepositoryImpl extends BaseApiRepository implements ApiRepository {
  FakeApiRepositoryImpl();

  @override
  Future<DataState<CreateCustomerResponse>> createCustomer({
    required CreateCustomerRequest request,
  }) {
    CreateCustomerResponse dummyUserData = CreateCustomerResponse(
      message: 'Customer created successfully',
      eventCode: EventCodes.OTP_SENT,
      userId: "123",
    );

    // return Future.delayed(
    //   const Duration(seconds: 1),
    //   () => DataFailed(
    //     DioError(
    //       requestOptions: RequestOptions(),
    //       response: Response(
    //         requestOptions: RequestOptions(),
    //         data: {"message": "Some error"},
    //       ),
    //       type: DioErrorType.badResponse,
    //       error: null,
    //     ),
    //   ),
    // );

    return Future.delayed(
      const Duration(seconds: 1),
      () => DataSuccess(dummyUserData),
    );
  }

  @override
  Future<DataState<VerifyPhoneNumberResponse>> verifyPhoneNumber({
    required VerifyPhoneNumberRequest request,
    required String token,
  }) {
    VerifyPhoneNumberResponse verificationStatus = VerifyPhoneNumberResponse(
      message: 'Phone number verified successfully',
    );

    // return Future.delayed(
    //   const Duration(seconds: 1),
    //   () => DataFailed(
    //     DioError(
    //       requestOptions: RequestOptions(),
    //       response: Response(
    //         requestOptions: RequestOptions(),
    //         data: {"message": "Some error"},
    //       ),
    //       type: DioErrorType.badResponse,
    //       error: null,
    //     ),
    //   ),
    // );

    return Future.delayed(
      const Duration(seconds: 1),
      () => DataSuccess(verificationStatus),
    );
  }

  @override
  Future<DataState<GetAllClosedLoopsResponse>> getAllClosedLoops(String token) {
    return Future.delayed(
      const Duration(seconds: 1),
      () => DataSuccess(GetAllClosedLoopsResponse(
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
      )),
    );
  }

  @override
  Future<DataState<RegisterClosedLoopResponse>> registerClosedLoop({
    required RegisterClosedLoopRequest request,
    required String token,
  }) {
    RegisterClosedLoopResponse registerClosedLoopResponse =
        RegisterClosedLoopResponse(
      message: 'close loop registered successfully',
    );

    // return Future.delayed(
    //   const Duration(seconds: 1),
    //   () => DataFailed(
    //     DioError(
    //       requestOptions: RequestOptions(),
    //       response: Response(
    //         requestOptions: RequestOptions(),
    //         data: {"message": "Some error"},
    //       ),
    //       type: DioErrorType.badResponse,
    //       error: null,
    //     ),
    //   ),
    // );

    return Future.delayed(
      const Duration(seconds: 1),
      () => DataSuccess(registerClosedLoopResponse),
    );
  }

  @override
  Future<DataState<VerifyClosedLoopResponse>> verifyClosedLoop({
    required VerifyClosedLoopRequest request,
    required String token,
  }) {
    VerifyClosedLoopResponse VerifyClosedLoopRequest = VerifyClosedLoopResponse(
      message: 'close loop verified successfully',
    );

    // return Future.delayed(
    //   const Duration(seconds: 1),
    //   () => DataFailed(
    //     DioError(
    //       requestOptions: RequestOptions(),
    //       response: Response(
    //         requestOptions: RequestOptions(),
    //         data: {"message": "Some error"},
    //       ),
    //       type: DioErrorType.badResponse,
    //       error: null,
    //     ),
    //   ),
    // );

    return Future.delayed(
      const Duration(seconds: 1),
      () => DataSuccess(VerifyClosedLoopRequest),
    );
  }

  @override
  Future<DataState<ChangePinResponse>> changePin({
    required ChangePinRequest request,
    required String token,
  }) {
    ChangePinResponse ChangePinRequest = ChangePinResponse(
      message: 'Pin changed successfully',
    );

    // return Future.delayed(
    //   const Duration(seconds: 1),
    //   () => DataFailed(
    //     DioError(
    //       requestOptions: RequestOptions(),
    //       response: Response(
    //         requestOptions: RequestOptions(),
    //         data: {"message": "Some error"},
    //       ),
    //       type: DioErrorType.badResponse,
    //       error: null,
    //     ),
    //   ),
    // );

    return Future.delayed(
      const Duration(seconds: 1),
      () => DataSuccess(ChangePinRequest),
    );
  }

  Future<DataState<GetUserResponse>> getUser(String token) {
    return Future.delayed(
      const Duration(seconds: 1),
      () => DataSuccess(GetUserResponse(
        user: UserResponse(
          fullName: 'Suleman',
          id: '123',
          closedLoops: [ClosedLoopUser(closedLoopId: "lums-id")],
        ),
        message: 'Customer created successfully',
      )),
    );
  }

  Future<DataState<GetUserBalanceResponse>> getUserBalance(String token) {
    return Future.delayed(
      const Duration(seconds: 1),
      () => DataSuccess(
        GetUserBalanceResponse(
          message: 'Customer created successfully',
          balance: 1000,
        ),
      ),
    );
  }

  Future<DataState<GetUserRecentTransactionsResponse>>
      getUserRecentTransactions(String token) {
    return Future.delayed(
      const Duration(seconds: 1),
      () => DataSuccess(
        GetUserRecentTransactionsResponse(
          message: 'Customer created successfully',
          // recentTransactions: [],
          recentTransactions: [
            Transaction(
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
            Transaction(
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
        message: 'Customer created successfully',
        checkoutUrl:
            'https://marketplace.paypro.com.pk/pyb?bid=MTIzNTIzMjA3MDAwMDE%3d');

    // return Future.delayed(
    //   const Duration(seconds: 1),
    //   () => DataFailed(
    //     DioError(
    //       requestOptions: RequestOptions(),
    //       response: Response(
    //         requestOptions: RequestOptions(),
    //         data: {"message": "Some error"},
    //       ),
    //       type: DioErrorType.badResponse,
    //       error: null,
    //     ),
    //   ),
    // );

    return Future.delayed(
      const Duration(seconds: 1),
      () => DataSuccess(CreateDepositRequest),
    );
  }

  Future<DataState<ExecuteP2PPushTransactionResponse>>
      executeP2PPushTransaction({
    required ExecuteP2PPushTransactionRequest request,
    required String token,
  }) {
    ExecuteP2PPushTransactionResponse ExecuteP2PPushTransactionRequest =
        ExecuteP2PPushTransactionResponse(
      message: 'Execute successfully',
    );

    // return Future.delayed(
    //   const Duration(seconds: 1),
    //   () => DataFailed(
    //     DioError(
    //       requestOptions: RequestOptions(),
    //       response: Response(
    //         requestOptions: RequestOptions(),
    //         data: {"message": "Some error"},
    //       ),
    //       type: DioErrorType.badResponse,
    //       error: null,
    //     ),
    //   ),
    // );

    return Future.delayed(
      const Duration(seconds: 1),
      () => DataSuccess(ExecuteP2PPushTransactionRequest),
    );
  }

  Future<DataState<ExecuteQrTransactionResponse>> executeQrTransaction({
    required ExecuteQrTransactionRequest request,
    required String token,
  }) {
    ExecuteQrTransactionResponse ExecuteP2PPushTransactionRequest =
        ExecuteQrTransactionResponse(
      message: 'Execute qr successfully',
    );

    // return Future.delayed(
    //   const Duration(seconds: 1),
    //   () => DataFailed(
    //     DioError(
    //       requestOptions: RequestOptions(),
    //       response: Response(
    //         requestOptions: RequestOptions(),
    //         data: {"message": "Some error"},
    //       ),
    //       type: DioErrorType.badResponse,
    //       error: null,
    //     ),
    //   ),
    // );

    return Future.delayed(
      const Duration(seconds: 1),
      () => DataSuccess(ExecuteP2PPushTransactionRequest),
    );
  }

  Future<DataState<GetCheckpointsResponse>> getCheckpoints(String user_id) {
    return Future.delayed(
      const Duration(seconds: 1),
      () => DataSuccess(
        GetCheckpointsResponse(
          checks: Checkpoints(
            verifiedPhoneOtp: true,
            verifiedClosedLoop: true,
            pinSetup: true,
          ),
          message: 'Customer verify successfully',
        ),
      ),
    );
  }

  Future<DataState<GetVersionsResponse>> getVersions() {
    return Future.delayed(
      const Duration(seconds: 1),
      () => DataSuccess(
        GetVersionsResponse(
          versions: Versions(
            forceUpdateVersion: '1.0.0',
            latestVersion: '1.5.0',
          ),
          message: 'Already updated version ',
        ),
      ),
    );
  }

  Future<DataState<GetFullNameResponse>> getFullName({
    required String uniqueIdentifier,
    required String closedLoopId,
    required String token,
  }) {
    GetFullNameResponse getFullNameRequest = const GetFullNameResponse(
      fullName: 'Schrodinger Catu',
      message: 'User name successfully',
    );

    return Future.delayed(
      const Duration(seconds: 1),
      () => DataSuccess(getFullNameRequest),
    );
  }

  Future<DataState<SetFcmTokenResponse>> setFcmToken({
    required SetFcmTokenRequest request,
    required String token,
  }) {
    SetFcmTokenResponse res = SetFcmTokenResponse(
      message: 'Fcm token set successfully',
    );

    // return Future.delayed(
    //   const Duration(seconds: 1),
    //   () => DataFailed(
    //     DioError(
    //       requestOptions: RequestOptions(),
    //       response: Response(
    //         requestOptions: RequestOptions(),
    //         data: {"message": "Some error"},
    //       ),
    //       type: DioErrorType.badResponse,
    //       error: null,
    //     ),
    //   ),
    // );

    return Future.delayed(const Duration(seconds: 1), () => DataSuccess(res));
  }

  // Payments
  Future<DataState<CreateP2PPullTransactionResponse>> createP2PPullTransaction({
    required CreateP2PPullTransactionRequest request,
    required String token,
  }) {
    CreateP2PPullTransactionResponse CreateP2PPullTransactionRequest =
        CreateP2PPullTransactionResponse(
      message: 'Transection is successfully',
    );

    // return Future.delayed(
    //   const Duration(seconds: 1),
    //   () => DataFailed(
    //     DioError(
    //       requestOptions: RequestOptions(),
    //       response: Response(
    //         requestOptions: RequestOptions(),
    //         data: {"message": "Some error"},
    //       ),
    //       type: DioErrorType.badResponse,
    //       error: null,
    //     ),
    //   ),
    // );

    return Future.delayed(
      const Duration(seconds: 1),
      () => DataSuccess(CreateP2PPullTransactionRequest),
    );
  }

  Future<DataState<CommonResponse>> acceptP2PPullTransaction({
    required AcceptP2PPullTransactionRequest request,
    required String token,
  }) {
    CommonResponse commonResponse = CommonResponse(
      message: 'Transection is successfully',
    );

    // return Future.delayed(
    //   const Duration(seconds: 1),
    //   () => DataFailed(
    //     DioError(
    //       requestOptions: RequestOptions(),
    //       response: Response(
    //         requestOptions: RequestOptions(),
    //         data: {"message": "Some error"},
    //       ),
    //       type: DioErrorType.badResponse,
    //       error: null,
    //     ),
    //   ),
    // );

    return Future.delayed(
      const Duration(seconds: 1),
      () => DataSuccess(commonResponse),
    );
  }

  Future<DataState<CommonResponse>> declineP2PPullTransaction({
    required DeclineP2PPullTransactionRequest request,
    required String token,
  }) {
    CommonResponse commonResponse = CommonResponse(
      message: 'Transection is successfully',
    );

    // return Future.delayed(
    //   const Duration(seconds: 1),
    //   () => DataFailed(
    //     DioError(
    //       requestOptions: RequestOptions(),
    //       response: Response(
    //         requestOptions: RequestOptions(),
    //         data: {"message": "Some error"},
    //       ),
    //       type: DioErrorType.badResponse,
    //       error: null,
    //     ),
    //   ),
    // );

    return Future.delayed(
      const Duration(seconds: 1),
      () => DataSuccess(commonResponse),
    );
  }

  Future<DataState<GetFrequentUsersResponse>> getFrequentUsers({
    required String closedLoopId,
    required String token,
  }) {
    GetFrequentUsersResponse getFrequentUsers = GetFrequentUsersResponse(
      // frequentUsers: [],
      frequentUsers: [
        UserInfo(fullName: 'Hamza BM', uniqueIdentifier: '26100353'),
        UserInfo(fullName: 'Shaheer', uniqueIdentifier: '26100240'),
      ],
      message: 'User name successfully',
    );

    return Future.delayed(
      const Duration(seconds: 1),
      () => DataSuccess(getFrequentUsers),
    );
  }

  Future<DataState<GetP2PPullRequestsResponse>> getP2PPullRequests({
    required String token,
  }) {
    GetP2PPullRequestsResponse res = GetP2PPullRequestsResponse(
      p2pRequestInfo: [
        P2PRequestInfo(fullName: 'Suleman', amount: 420),
        P2PRequestInfo(fullName: 'Khuzimi', amount: 169),
      ],
      message: 'User name successfully',
    );

    return Future.delayed(
      const Duration(seconds: 1),
      () => DataSuccess(res),
    );
  }

  // Events
  @override
  Future<DataState<GetEventsResponse>> getLiveEvents({
    required String closedLoopId,
    required String token,
  }) {
    return Future.delayed(
      const Duration(seconds: 1),
      () => DataSuccess(GetEventsResponse(
        message: 'Customer created successfully',
        events: [
          Event(
            name: "Cricket 007",
            description:
                "The best cricket screening evericket screening evericket screening evericket screening evericket screening eve ricket screening evericket screening evericket screening evericket screening evericket screening eve ricket screening evericket screening evericket screening evericket screening evericket screening eve ricket screening evericket screening evericket screening evericket screening eve ricket screening evericket screening evericket screening evericket screening eve ricket screening evericket screening evericket screening eve ricket screening evericket screening evericket screening evericket screening eve ricket screening evericket screening evericket screening ever, The best cricket screening ever The best cricket screening ever The best cricket screening ever The best cricket screening ever",
            imageUrl:
                "https://static.vecteezy.com/system/resources/previews/000/458/333/original/vector-cricket-background.jpg",
            registrationFee: 1500,
            organizerName: "Student Council",
            venue: "Sports Complex",
          ),
          Event(name: "FIFA", description: "OMG! FIFA screening!"),
        ],
      )),
    );
  }

  @override
  Future<DataState<GetEventsResponse>> getRegisteredEvents({
    required String token,
  }) {
    return Future.delayed(
      const Duration(seconds: 1),
      () => DataSuccess(GetEventsResponse(
        message: 'Customer created successfully',
        events: [
          Event(
            name: "Cricket 007",
            description:
                "The best cricket screeningscreeningscreeningscreeningscreeningscreeningscreeningscreeningscreeningscreening screeningscreeningscreeningscreeningscreeningscreeningscreeningscreening screeningscreeningscreeningscreeningscreening ever",
            imageUrl:
                "https://static.vecteezy.com/system/resources/previews/000/458/333/original/vector-cricket-background.jpg",
            registrationFee: 1500,
            organizerName: "Student Council",
            venue: "Sports Complex",
          ),
          Event(
            name: "FIFA 14",
            description: "OMG! FIFA screening!",
            venue: "Khokha Stall",
          ),
          Event(
            name: "FIFA 15",
            description: "OMG! FIFA screening!",
            venue: "Khokha Stall",
            imageUrl:
                "https://static.vecteezy.com/system/resources/previews/000/458/333/original/vector-cricket-background.jpg",
            registrationFee: 1500,
          ),
          Event(
            name: "FIFA 16",
            description: "OMG! FIFA screening!",
            venue: "Khokha Stall",
            imageUrl:
                "https://static.vecteezy.com/system/resources/previews/000/458/333/original/vector-cricket-background.jpg",
            registrationFee: 1500,
          ),
          Event(
            name: "FIFA 2062314123 version 20000.00123213",
            description: "OMG! FIFA screening!",
            venue: "Khokha Stall",
            imageUrl:
                "https://static.vecteezy.com/system/resources/previews/000/458/333/original/vector-cricket-background.jpg",
            registrationFee: 1500,
          ),
          Event(
            name: "FIFA 18",
            description: "OMG! FIFA screening!",
            venue: "Khokha Stall",
            imageUrl:
                "https://static.vecteezy.com/system/resources/previews/000/458/333/original/vector-cricket-background.jpg",
            registrationFee: 1500,
          ),
        ],
      )),
    );
  }

  @override
  Future<DataState<RegisterEventResponse>> registerEvent({
    required RegisterEventRequest registerEventRequest,
    required String token,
  }) {
    // return Future.delayed(
    //   const Duration(seconds: 1),
    //   () => DataFailed(
    //     DioError(
    //       requestOptions: RequestOptions(),
    //       response: Response(
    //         requestOptions: RequestOptions(),
    //         data: {"message": "Some error"},
    //       ),
    //       type: DioErrorType.badResponse,
    //       error: null,
    //     ),
    //   ),
    // );

    RegisterEventResponse registerEventRequest = RegisterEventResponse(
      message: 'Event registered successfully',
    );

    return Future.delayed(
      const Duration(seconds: 1),
      () => DataSuccess(registerEventRequest),
    );
  }
}

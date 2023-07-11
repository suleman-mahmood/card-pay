import 'package:cardpay/src/domain/models/requests/user_request.dart';
import 'package:cardpay/src/domain/models/responses/user_response.dart';
import 'package:cardpay/src/utils/data_state.dart';

abstract class ApiRepository {
  Future<DataState<UserResponse>> getUser({
    required UserRequest request,
  });
}

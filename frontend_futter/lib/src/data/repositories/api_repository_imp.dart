import 'package:frontend_futter/src/data/datasources/remote/python_api_service.dart';
import 'package:frontend_futter/src/domain/models/requests/user_request.dart';
import 'package:frontend_futter/src/domain/models/responses/user_response.dart';
import 'package:frontend_futter/src/utils/data_state.dart';

import '../../domain/repositories/api_repository.dart';
import 'base/base_api_repository.dart';

class ApiRepositoryImpl extends BaseApiRepository implements ApiRepository {
  final PythonApiService _pythonApiService;

  ApiRepositoryImpl(this._pythonApiService);

  @override
  Future<DataState<UserResponse>> getUser({
    required UserRequest request,
  }) {
    return getStateOf<UserResponse>(
      request: () => _pythonApiService.getUser(
        id: request.id,
      ),
    );
  }
}

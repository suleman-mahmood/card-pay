import 'package:dio/dio.dart';
import 'package:frontend_futter/src/domain/models/responses/user_response.dart';
import 'package:frontend_futter/src/utils/constants/strings.dart';
import 'package:retrofit/retrofit.dart';

part 'python_api_service.g.dart';

@RestApi(baseUrl: baseUrl, parser: Parser.MapSerializable)
abstract class PythonApiService {
  factory PythonApiService(Dio dio, {String baseUrl}) = _PythonApiService;

  @GET('/get-user')
  Future<HttpResponse<UserResponse>> getUser({
    @Query("id") String? id,
  });
}

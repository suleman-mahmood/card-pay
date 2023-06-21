import 'package:dio/dio.dart';
import 'package:equatable/equatable.dart';
import 'package:frontend_futter/src/domain/models/requests/user_request.dart';
import 'package:frontend_futter/src/domain/models/user.dart';
import 'package:frontend_futter/src/domain/repositories/api_repository.dart';
import 'package:frontend_futter/src/presentation/cubits/base/base_cubit.dart';
import 'package:frontend_futter/src/utils/data_state.dart';

part 'remote_user_state.dart';

class RemoteUserCubit extends BaseCubit<RemoteUserState, User> {
  final ApiRepository _apiRepository;

  RemoteUserCubit(this._apiRepository)
      : super(const RemoteUserLoading(), const User());

  Future<void> getUser() async {
    if (isBusy) return;

    await run(() async {
      final response = await _apiRepository.getUser(
        request: UserRequest(),
      );

      if (response is DataSuccess) {
        final user = response.data!.user;

        emit(RemoteUserSuccess(user: user));
      } else if (response is DataFailed) {
        emit(RemoteUserFailed(error: response.error));
      }
    });
  }
}

import 'package:cardpay/src/domain/models/closed_loop.dart';
import 'package:cardpay/src/domain/repositories/api_repository.dart';
import 'package:cardpay/src/presentation/cubits/base/base_cubit.dart';
import 'package:cardpay/src/utils/data_state.dart';
import 'package:dio/dio.dart';
import 'package:meta/meta.dart';

part 'closed_loop_state.dart';

class ClosedLoopCubit extends BaseCubit<ClosedLoopState, ClosedLoop> {
  final ApiRepository _apiRepository;

  ClosedLoopCubit(this._apiRepository)
      : super(
          ClosedLoopInitial(),
          ClosedLoop(),
        );

  Future<void> getAllClosedLoops() async {
    if (isBusy) return;

    await run(() async {
      emit(const ClosedLoopLoading());

      final response = await _apiRepository.getAllClosedLoops();

      if (response is DataSuccess) {
        emit(ClosedLoopSuccess(
          message: response.data!.message,
          closedLoops: response.data!.closedLoops,
        ));
      } else if (response is DataFailed) {
        emit(ClosedLoopFailed(error: response.error));
      }
    });
  }
}

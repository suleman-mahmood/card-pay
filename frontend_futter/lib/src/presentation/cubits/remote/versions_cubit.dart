import 'package:cardpay/src/domain/models/version.dart';
import 'package:cardpay/src/domain/repositories/api_repository.dart';
import 'package:cardpay/src/presentation/cubits/base/base_cubit.dart';
import 'package:cardpay/src/utils/data_state.dart';
import 'package:cardpay/src/utils/version_comparing_util.dart';
import 'package:package_info_plus/package_info_plus.dart';

import 'package:dio/dio.dart';
import 'package:meta/meta.dart';

part 'versions_state.dart';

class VersionsCubit extends BaseCubit<VersionsState, Versions> {
  final ApiRepository _apiRepository;

  VersionsCubit(this._apiRepository)
      : super(
          VersionsInitial(),
          Versions(),
        );

  Future<void> init() async {
    emit(VersionsInitial());
  }

  Future<void> getVersions() async {
    if (isBusy) return;

    await run(() async {
      emit(VersionsLoading());
      final response = await _apiRepository.getVersions();

      if (response is DataSuccess) {
        data.forceUpdateVersion = response.data!.versions.forceUpdateVersion;
        data.latestVersion = response.data!.versions.latestVersion;
        final PackageInfo packageInfo = await PackageInfo.fromPlatform();
        final appNormalUpdateState = isVersionGreaterThan(
          data.latestVersion,
          packageInfo.version,
        );
        final appForceUpdateState = isVersionGreaterThan(
          data.forceUpdateVersion,
          packageInfo.version,
        );

        emit(VersionsSuccess(
          message: response.data!.message,
          versions: data,
          forceUpdate: appForceUpdateState,
          normalUpdate: appNormalUpdateState,
        ));
      } else if (response is DataFailed) {
        if (response.error?.type.name == "unknown") {
          emit(VersionsUnknownFailure(
            errorMessage: "Unknown error, check internet connections",
          ));
        } else {
          emit(VersionsFailed(
            error: response.error,
            errorMessage: response.error?.response?.data["message"],
          ));
        }
      }
    });
  }
}

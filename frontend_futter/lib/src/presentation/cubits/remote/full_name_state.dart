part of 'full_name_cubit.dart';

@immutable
abstract class FullNameState {
  final String fullName;

  final String errorMessage;
  final DioError? error;

  FullNameState({
    this.fullName = '',
    this.errorMessage = '',
    this.error,
  });
}

class FullNameInitial extends FullNameState {
  FullNameInitial();
}

class FullNameLoading extends FullNameState {
  FullNameLoading();
}

class FullNameSuccess extends FullNameState {
  FullNameSuccess({super.fullName});
}

class FullNameFailed extends FullNameState {
  FullNameFailed({super.errorMessage, super.error});
}

class FullNameUnknownFailure extends FullNameState {
  FullNameUnknownFailure({super.errorMessage});
}

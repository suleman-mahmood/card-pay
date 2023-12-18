part of 'transfer_cubit.dart';

@immutable
abstract class TransferState {
  final String message;

  final String errorMessage;
  final DioError? error;

  TransferState({
    this.message = '',
    this.errorMessage = '',
    this.error,
  });
}

class TransferInitial extends TransferState {
  TransferInitial();
}

class TransferLoading extends TransferState {
  TransferLoading();
}

class TransferSuccess extends TransferState {
  TransferSuccess({super.message});
}

class TransferPullDeclined extends TransferState {
  TransferPullDeclined({super.message});
}

class TransferFailed extends TransferState {
  TransferFailed({super.error, super.errorMessage});
}

class TransferUnknownFailure extends TransferState {
  TransferUnknownFailure({super.errorMessage});
}

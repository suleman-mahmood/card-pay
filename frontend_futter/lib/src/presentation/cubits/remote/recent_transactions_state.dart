part of 'recent_transactions_cubit.dart';

@immutable
abstract class RecentTransactionsState {
  final String message;
  final List<Transaction> recentTransactions;

  final String errorMessage;
  final DioError? error;

  RecentTransactionsState({
    this.message = '',
    this.errorMessage = '',
    this.recentTransactions = const [],
    this.error,
  });
}

class RecentTransactionsInitial extends RecentTransactionsState {
  RecentTransactionsInitial();
}

class RecentTransactionsLoading extends RecentTransactionsState {
  RecentTransactionsLoading();
}

class RecentTransactionsSuccess extends RecentTransactionsState {
  RecentTransactionsSuccess({super.message, super.recentTransactions});
}

class RecentTransactionsFailed extends RecentTransactionsState {
  RecentTransactionsFailed({super.error, super.errorMessage});
}

class RecentTransactionsUnknownFailure extends RecentTransactionsState {
  RecentTransactionsUnknownFailure({super.errorMessage});
}

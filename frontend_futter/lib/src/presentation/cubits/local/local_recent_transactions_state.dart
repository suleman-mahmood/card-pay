part of 'local_recent_transactions_cubit.dart';

@immutable
abstract class LocalRecentTransactionsState {
  final List<Transaction> transactions;

  const LocalRecentTransactionsState({
    this.transactions = const [],
  });
}

class LocalRecentTransactionsInitial extends LocalRecentTransactionsState {
  const LocalRecentTransactionsInitial();
}

class LocalRecentTransactionsSuccess extends LocalRecentTransactionsState {
  const LocalRecentTransactionsSuccess({super.transactions});
}

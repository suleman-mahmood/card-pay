import 'package:bloc/bloc.dart';
import 'package:cardpay/src/domain/models/transaction.dart';
import 'package:cardpay/src/domain/repositories/database_repository.dart';
import 'package:meta/meta.dart';

part 'local_recent_transactions_state.dart';

class LocalRecentTransactionsCubit extends Cubit<LocalRecentTransactionsState> {
  final DatabaseRepository _databaseRepository;

  LocalRecentTransactionsCubit(this._databaseRepository)
      : super(const LocalRecentTransactionsInitial());

  Future<void> getRecentTransactions() async {
    final txs = await _databaseRepository.getRecentTransactions();
    emit(LocalRecentTransactionsSuccess(transactions: txs));
  }

  Future<void> updateRecentTransactions(List<Transaction> txs) async {
    await _databaseRepository.updateRecentTransactions(txs);
    emit(LocalRecentTransactionsSuccess(transactions: txs));
  }
}

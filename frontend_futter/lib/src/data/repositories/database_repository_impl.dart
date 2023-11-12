import 'package:cardpay/src/data/datasources/local/app_database.dart';
import 'package:cardpay/src/domain/models/balance.dart';
import 'package:cardpay/src/domain/models/transaction.dart';
import 'package:cardpay/src/domain/repositories/database_repository.dart';

class DatabaseRepositoryImpl implements DatabaseRepository {
  final AppDatabase _appDatabase;

  DatabaseRepositoryImpl(this._appDatabase);

  @override
  Future<Balance> getBalance() async {
    return await _appDatabase.balanceDao.getBalance() ?? Balance();
  }

  @override
  Future<void> updateBalance(Balance balance) async {
    return _appDatabase.balanceDao.updateBalance(balance);
  }

  @override
  Future<List<Transaction>> getRecentTransactions() async {
    return await _appDatabase.recentTransactions.getRecentTransactions();
  }

  @override
  Future<void> updateRecentTransactions(List<Transaction> txs) {
    return _appDatabase.recentTransactions.updateRecentTransactions(txs);
  }
}

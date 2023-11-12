import 'package:cardpay/src/domain/models/balance.dart';
import 'package:cardpay/src/domain/models/transaction.dart';

abstract class DatabaseRepository {
  Future<Balance> getBalance();

  Future<void> updateBalance(Balance balance);

  Future<List<Transaction>> getRecentTransactions();

  Future<void> updateRecentTransactions(List<Transaction> txs);
}

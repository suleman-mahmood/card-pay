import 'package:cardpay/src/domain/models/transaction.dart';
import 'package:floor/floor.dart';

@dao
abstract class RecentTransactionsDao {
  @Query('select * from transactions order by createdAt desc')
  Future<List<Transaction>> getRecentTransactions();

  @Insert(onConflict: OnConflictStrategy.replace)
  Future<void> updateRecentTransactions(List<Transaction> txs);
}

import 'package:cardpay/src/domain/models/balance.dart';
import 'package:floor/floor.dart';

@dao
abstract class BalanceDao {
  @Query('select * from balance where id = 0')
  Future<Balance?> getBalance();

  @Insert(onConflict: OnConflictStrategy.replace)
  Future<void> updateBalance(Balance balance);
}

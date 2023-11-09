import 'package:cardpay/src/domain/models/balance.dart';

abstract class DatabaseRepository {
  Future<Balance> getBalance();

  Future<void> updateBalance(Balance balance);
}

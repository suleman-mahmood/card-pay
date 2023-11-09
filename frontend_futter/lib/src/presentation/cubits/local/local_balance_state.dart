part of 'local_balance_cubit.dart';

@immutable
abstract class LocalBalanceState {
  final Balance balance;

  LocalBalanceState({
    Balance? balance,
  }) : balance = balance ?? Balance();
}

class LocalBalanceInitial extends LocalBalanceState {
  LocalBalanceInitial();
}

class LocalBalanceSuccess extends LocalBalanceState {
  LocalBalanceSuccess({super.balance});
}

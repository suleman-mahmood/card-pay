import 'package:bloc/bloc.dart';
import 'package:cardpay/src/domain/models/balance.dart';
import 'package:cardpay/src/domain/repositories/database_repository.dart';
import 'package:meta/meta.dart';

part 'local_balance_state.dart';

class LocalBalanceCubit extends Cubit<LocalBalanceState> {
  final DatabaseRepository _databaseRepository;

  LocalBalanceCubit(this._databaseRepository) : super(LocalBalanceInitial());

  Future<void> getBalance() async {
    final balance = await _databaseRepository.getBalance();
    emit(LocalBalanceSuccess(balance: balance));
  }

  Future<void> updateBalance(int amount) async {
    final balance = Balance(amount: amount);
    await _databaseRepository.updateBalance(balance);
    emit(LocalBalanceSuccess(balance: balance));
  }
}

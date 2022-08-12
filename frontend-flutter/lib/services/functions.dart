import 'package:cloud_functions/cloud_functions.dart';
import 'package:cardpay/services/models.dart' as mdl;

class FunctionsSevice {
  final FirebaseFunctions _functions = FirebaseFunctions.instance;

  Future<void> makeDeposit(mdl.DepositArguments args) async {
    await _functions.httpsCallable("deposit").call(args.toJson());
  }

  Future<void> createUser(mdl.CreateUserArguments args) async {
    await _functions.httpsCallable("createUser").call(args.toJson());
  }

  Future<void> makeTransfer(mdl.MakeTransferArguments args) async {
    await _functions.httpsCallable("transfer").call(args.toJson());
  }
}

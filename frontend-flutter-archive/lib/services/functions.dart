import 'package:cloud_functions/cloud_functions.dart';
import 'package:cardpay/services/models.dart' as mdl;

class FunctionsService {
  final FirebaseFunctions _functions = FirebaseFunctions.instance;

  Future<mdl.DepositReturnObject> makeDeposit(mdl.DepositArguments args) async {
    final res =
        await _functions.httpsCallable("addDepositRequest").call(args.toJson());
    return mdl.DepositReturnObject.fromJson(res.data);
  }

  Future<void> createUser(mdl.CreateUserArguments args) async {
    await _functions.httpsCallable("createUser").call(args.toJson());
  }

  Future<void> makeTransfer(mdl.MakeTransferArguments args) async {
    await _functions.httpsCallable("transfer").call(args.toJson());
  }

  Future<void> checkDepositStatus() async {
    await _functions.httpsCallable("handleDepositSuccess").call();
  }
}

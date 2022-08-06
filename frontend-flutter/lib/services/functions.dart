import 'package:cloud_functions/cloud_functions.dart';
import 'package:cardpay/services/models.dart' as mdl;

class FunctionsSevice {
  final FirebaseFunctions _functions = FirebaseFunctions.instance;

  // TODO: change the return type of function and handle the result
  Future<bool> makeDeposit(mdl.DepositArguments args) async {
    try {
      final result = await _functions.httpsCallable("deposit").call(
            args.toJson(),
          );
      print(result);
      return true;
    } on FirebaseFunctionsException catch (e) {
      // Handle error
      print(e.code);
      print(e.message);
      return false;
    }
  }

  // TODO: change the return type of function and handle the result
  Future<bool> createUser(mdl.CreateUserArguments args) async {
    try {
      final result = await _functions.httpsCallable("createUser").call(
            args.toJson(),
          );
      print(result);
      return true;
    } on FirebaseFunctionsException catch (e) {
      // Handle error
      print(e.code);
      print(e.message);
      return false;
    }
  }
}

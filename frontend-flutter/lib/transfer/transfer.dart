import 'package:cardpay/services/functions.dart';
import 'package:cardpay/services/models.dart' as model;
import 'package:cardpay/services/utils.dart';
import 'package:cardpay/shared/loading.dart';
import 'package:cloud_functions/cloud_functions.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class TransferScreen extends StatelessWidget {
  String rollNumber = '';
  int amount = 0;

  TransferScreen({Key? key}) : super(key: key);

  void _submit(BuildContext context) async {
    context.read<model.Loading>().showLoading();

    try {
      await FunctionsSevice().makeTransfer(
        model.MakeTransferArguments(
          amount: amount,
          recipientRollNumber: rollNumber,
        ),
      );
    } on FirebaseFunctionsException catch (e) {
      final String errorMessage;

      if (codeToMessage.containsKey(e.code)) {
        errorMessage = codeToMessage[e.code];
      } else {
        errorMessage = "Unknown exception thrown: ${e.code}";
      }

      printError(errorMessage);
      context.read<model.ErrorModel>().errorOcurred(
            e.code,
            errorMessage,
          );
      context.read<model.Loading>().hideLoading();
      return;
    }

    // Handle success
    context.read<model.ErrorModel>().errorResolved();
    context.read<model.Loading>().hideLoading();
    printInGreen("Transfer Success!");
  }

  @override
  Widget build(BuildContext context) {
    if (context.watch<model.Loading>().getLoading) {
      return const LoadingWidget();
    }

    return Scaffold(
      body: Center(
        child: Container(
          margin: EdgeInsets.only(top: 50),
          child: Column(
            children: [
              Text(
                'Instant Transfer',
                style: Theme.of(context).textTheme.headline5,
              ),
              Container(
                margin: EdgeInsets.only(top: 20),
                width: 250,
                child: Text(
                  'Enter details',
                  style: Theme.of(context).textTheme.headline5,
                ),
              ),
              Container(
                width: 250,
                margin: EdgeInsets.only(top: 15),
                padding: EdgeInsets.only(left: 20),
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.all(
                    Radius.circular(10),
                  ),
                  color: Colors.orange[700],
                ),
                child: TextField(
                  onChanged: (String rollNumberValue) {
                    rollNumber = rollNumberValue;
                  },
                  decoration: InputDecoration(
                    labelText: 'Roll Number',
                    border: InputBorder.none,
                  ),
                ),
              ),
              Container(
                width: 250,
                margin: EdgeInsets.only(top: 15),
                padding: EdgeInsets.only(left: 20),
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.all(
                    Radius.circular(10),
                  ),
                  color: Colors.orange[700],
                ),
                child: TextField(
                  onChanged: (String amountValue) {
                    amount = int.parse(amountValue);
                  },
                  decoration: InputDecoration(
                    labelText: 'Amount',
                    border: InputBorder.none,
                  ),
                ),
              ),
              Container(
                width: 200,
                margin: EdgeInsets.only(top: 30),
                child: MaterialButton(
                  color: Colors.orange[800],
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                  onPressed: () => _submit(context),
                  child: Text(
                    'Transfer Now!',
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

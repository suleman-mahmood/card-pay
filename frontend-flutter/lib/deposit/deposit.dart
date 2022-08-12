import 'package:cardpay/services/models.dart' as model;
import 'package:cardpay/services/utils.dart';
import 'package:cardpay/shared/loading.dart';
import 'package:cloud_functions/cloud_functions.dart';
import 'package:flutter/material.dart';
import 'package:cardpay/services/functions.dart';
import 'package:provider/provider.dart';

class DepositScreen extends StatelessWidget {
  int amount = 0;
  String cardNumber = '';
  String cvv = '';
  String expiryDate = '';

  DepositScreen({Key? key}) : super(key: key);

  void _submit(BuildContext context) async {
    context.read<model.Loading>().showLoading();

    try {
      await FunctionsSevice().makeDeposit(
        model.DepositArguments(
          amount: amount,
          cardNumber: cardNumber,
          cvv: cvv,
          expiryDate: expiryDate,
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
    Navigator.of(context).pushNamed('/dashboard');
  }

  @override
  Widget build(BuildContext context) {
    if (context.watch<model.Loading>().getLoading) {
      return LoadingWidget();
    }

    return Scaffold(
      body: Center(
        child: Container(
          margin: EdgeInsets.only(top: 50),
          child: Column(
            children: [
              Text(
                'Deposit Options',
                style: Theme.of(context).textTheme.headline5,
              ),
              Container(
                margin: EdgeInsets.only(top: 20),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Container(
                      margin: EdgeInsets.only(right: 20),
                      child: Column(
                        children: [
                          Container(
                            width: 100,
                            decoration: BoxDecoration(
                              borderRadius: BorderRadius.all(
                                Radius.circular(10),
                              ),
                              border: Border.all(
                                color: (Colors.orange[700])!,
                              ),
                            ),
                            child: ElevatedButton(
                              style: ButtonStyle(
                                backgroundColor: MaterialStateProperty.all(
                                    Colors.transparent),
                              ),
                              onPressed: () => {},
                              child: Icon(
                                Icons.arrow_upward,
                              ),
                            ),
                          ),
                          Container(
                            width: 100,
                            child: Text(
                              'Credit / Debit Card',
                              style: Theme.of(context).textTheme.bodyText2,
                              textAlign: TextAlign.center,
                            ),
                          )
                        ],
                      ),
                    ),
                    Container(
                      margin: EdgeInsets.only(right: 20),
                      child: Column(
                        children: [
                          Container(
                            width: 100,
                            decoration: BoxDecoration(
                              borderRadius: BorderRadius.all(
                                Radius.circular(10),
                              ),
                              border: Border.all(
                                color: (Colors.orange[700])!,
                              ),
                            ),
                            child: ElevatedButton(
                              style: ButtonStyle(
                                backgroundColor: MaterialStateProperty.all(
                                    Colors.transparent),
                              ),
                              onPressed: () => {},
                              child: Icon(
                                Icons.arrow_upward,
                              ),
                            ),
                          ),
                          Text(
                            'PayPro',
                            style: Theme.of(context).textTheme.bodyText2,
                          )
                        ],
                      ),
                    ),
                    Column(
                      children: [
                        Container(
                          width: 100,
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.all(
                              Radius.circular(10),
                            ),
                            border: Border.all(
                              color: (Colors.orange[700])!,
                            ),
                          ),
                          child: ElevatedButton(
                            style: ButtonStyle(
                              backgroundColor:
                                  MaterialStateProperty.all(Colors.transparent),
                            ),
                            onPressed: () => {},
                            child: Icon(
                              Icons.arrow_upward,
                            ),
                          ),
                        ),
                        Text(
                          'PayPak',
                          style: Theme.of(context).textTheme.bodyText2,
                        )
                      ],
                    ),
                  ],
                ),
              ),
              Container(
                margin: EdgeInsets.only(top: 20),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Container(
                      margin: EdgeInsets.only(right: 20),
                      child: Column(
                        children: [
                          Container(
                            width: 100,
                            decoration: BoxDecoration(
                              borderRadius: BorderRadius.all(
                                Radius.circular(10),
                              ),
                              border: Border.all(
                                color: (Colors.orange[700])!,
                              ),
                            ),
                            child: ElevatedButton(
                              style: ButtonStyle(
                                backgroundColor: MaterialStateProperty.all(
                                    Colors.transparent),
                              ),
                              onPressed: () => {},
                              child: Icon(
                                Icons.arrow_upward,
                              ),
                            ),
                          ),
                          Container(
                            width: 100,
                            child: Text(
                              'EasyPaisa',
                              style: Theme.of(context).textTheme.bodyText2,
                              textAlign: TextAlign.center,
                            ),
                          )
                        ],
                      ),
                    ),
                    Column(
                      children: [
                        Container(
                          width: 100,
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.all(
                              Radius.circular(10),
                            ),
                            border: Border.all(
                              color: (Colors.orange[700])!,
                            ),
                          ),
                          child: ElevatedButton(
                            style: ButtonStyle(
                              backgroundColor:
                                  MaterialStateProperty.all(Colors.transparent),
                            ),
                            onPressed: () => {},
                            child: Icon(
                              Icons.arrow_upward,
                            ),
                          ),
                        ),
                        Text(
                          'JazzCash',
                          style: Theme.of(context).textTheme.bodyText2,
                        )
                      ],
                    ),
                  ],
                ),
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
                  decoration: InputDecoration(
                    labelText: 'Full Name (as written on card)',
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
                  onChanged: (String cardNumberValue) {
                    cardNumber = cardNumberValue;
                  },
                  decoration: InputDecoration(
                    labelText: 'Card Number',
                    border: InputBorder.none,
                  ),
                ),
              ),
              Container(
                width: 250,
                child: Row(
                  children: [
                    Flexible(
                      flex: 1,
                      child: Container(
                        margin: EdgeInsets.only(top: 15),
                        padding: EdgeInsets.only(left: 20),
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.all(
                            Radius.circular(10),
                          ),
                          color: Colors.orange[700],
                        ),
                        child: TextField(
                          onChanged: (String expiryDateValue) {
                            expiryDate = expiryDateValue;
                          },
                          decoration: InputDecoration(
                            labelText: 'Expiry date',
                            border: InputBorder.none,
                          ),
                        ),
                      ),
                    ),
                    SizedBox(
                      width: 20,
                    ),
                    Flexible(
                      flex: 1,
                      child: Container(
                        width: 125,
                        margin: EdgeInsets.only(top: 15),
                        padding: EdgeInsets.only(left: 20),
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.all(
                            Radius.circular(10),
                          ),
                          color: Colors.orange[700],
                        ),
                        child: TextField(
                          onChanged: (String cvvValue) {
                            cvv = cvvValue;
                          },
                          decoration: InputDecoration(
                            labelText: 'CVV',
                            border: InputBorder.none,
                          ),
                        ),
                      ),
                    ),
                  ],
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
                margin: EdgeInsets.only(top: 10),
                width: 250,
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.start,
                  children: [
                    Checkbox(value: false, onChanged: (e) => true),
                    Container(
                      width: 200,
                      child: Text(
                        'I agree to the Terms and Conditions',
                        style: Theme.of(context).textTheme.bodyText2,
                      ),
                    ),
                  ],
                ),
              ),
              Container(
                width: 250,
                margin: EdgeInsets.only(top: 10),
                child: MaterialButton(
                  color: Colors.orange[800],
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                  onPressed: () => _submit(context),
                  child: Text(
                    'Deposit Now!',
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

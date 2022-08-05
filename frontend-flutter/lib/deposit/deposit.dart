import 'package:cardpay/services/models.dart';
import 'package:flutter/material.dart';
import 'package:flutter/src/foundation/key.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:cardpay/services/functions.dart';

class DepositScreen extends StatelessWidget {
  int amount = 0;
  String cardNumber = '';
  String cvv = '';
  String expiryDate = '';

  DepositScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
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
                  onPressed: () => {
                    FunctionsSevice().makeDeposit(
                      DepositArguments(
                        amount: amount,
                        cardNumber: cardNumber,
                        cvv: cvv,
                        expiryDate: expiryDate,
                      ),
                    )
                  },
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

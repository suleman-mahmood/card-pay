import 'package:flutter/material.dart';
import 'package:flutter/src/foundation/key.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:cardpay/services/models.dart' as model;
import 'package:provider/provider.dart';

class TransactionsScreen extends StatelessWidget {
  const TransactionsScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    var user = context.read<model.User>();
    var transactions = user.transactions;

    Widget getTransactions() {
      return Column(
        children: transactions.map((t) {
          return TransactionWidget(transactionData: t);
        }).toList(),
      );
    }

    return Scaffold(
      body: Center(
        child: Container(
          margin: EdgeInsets.only(top: 50),
          child: Column(
            children: [
              Text(
                'Transactions',
                style: Theme.of(context).textTheme.headline5,
              ),
              SizedBox(
                height: 20,
              ),
              getTransactions(),
            ],
          ),
        ),
      ),
    );
  }
}

class TransactionWidget extends StatelessWidget {
  model.UserTransaction transactionData;

  TransactionWidget({
    required this.transactionData,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 300,
      padding: EdgeInsets.symmetric(vertical: 10, horizontal: 15),
      margin: EdgeInsets.only(top: 10),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.all(
          Radius.circular(10),
        ),
        color: Colors.orange[700],
      ),
      child: Row(
        children: [
          Flexible(
            flex: 2,
            fit: FlexFit.tight,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  transactionData.senderName,
                  style: Theme.of(context).textTheme.bodyText2,
                ),
                Text(
                  'Card',
                  style: Theme.of(context).textTheme.bodyText2,
                ),
              ],
            ),
          ),
          Spacer(flex: 1),
          Flexible(
            flex: 2,
            fit: FlexFit.tight,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                Text(
                  transactionData.amount.toString(),
                  style: Theme.of(context).textTheme.bodyText2,
                ),
                Text(
                  transactionData.timestamp,
                  style: Theme.of(context).textTheme.bodyText2,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

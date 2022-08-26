import 'package:cardpay/shared/shared.dart';
import 'package:flutter/material.dart';
import 'package:cardpay/services/models.dart' as model;
import 'package:provider/provider.dart';

class TransactionsScreen extends StatelessWidget {
  const TransactionsScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final user = context.watch<model.User>();
    final transactions = user.transactions;

    return WalletLayoutCustomWidget(
      children: transactions
          .map(
            (t) {
              return Column(
                children: [
                  TransactionCardCustomWidget(
                    transactionData: t,
                    isDebit: user.fullName == t.senderName,
                  ),
                  SizedBox(height: 10),
                ],
              );
            },
          )
          .toList()
          .reversed
          .toList(),
    );
  }
}

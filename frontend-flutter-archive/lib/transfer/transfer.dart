import 'package:cardpay/services/functions.dart';
import 'package:cardpay/services/models.dart' as model;
import 'package:cardpay/services/utils.dart';
import 'package:cardpay/shared/shared.dart';
import 'package:cloud_functions/cloud_functions.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class TransferScreen extends StatefulWidget {
  TransferScreen({Key? key}) : super(key: key);

  @override
  State<TransferScreen> createState() => _TransferScreenState();
}

class _TransferScreenState extends State<TransferScreen> {
  final List<int> denominations = [10, 50, 100, 500, 1000, 5000];

  String rollNumber = '';
  int amount = 0;

  void _submit(BuildContext context) async {
    context.read<model.Loading>().showLoading();

    try {
      await FunctionsService().makeTransfer(
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
    return MultiProvider(
      providers: [
        ChangeNotifierProvider<model.ErrorModel>(
          create: (_) => model.ErrorModel(),
        ),
      ],
      builder: (context, child) {
        if (context.watch<model.Loading>().getLoading) {
          return ScreenTransitionLoaderCustomWidget();
        }

        return WalletLayoutCustomWidget(
          children: [
            PlaceholderInputCustomWidget(
              labelText: "Roll Number",
              hintText: "23100011",
              onChanged: (String rollNumberValue) {
                rollNumber = rollNumberValue;
              },
              invertColors: true,
            ),
            SizedBox(height: 10),
            GridView(
              shrinkWrap: true,
              padding: EdgeInsets.symmetric(vertical: 20),
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 3,
                mainAxisSpacing: 20,
                crossAxisSpacing: 30,
                childAspectRatio: 5 / 3,
              ),
              children: denominations.map<Widget>((d) {
                return NumberButtonCustomWidget(
                  number: d,
                  onPressed: () {
                    setState(() {
                      amount += d;
                    });
                  },
                  invertColors: true,
                );
              }).toList(),
            ),
            SizedBox(height: 10),
            TextPlaceholderInputCustomWidget(
              onChanged: (v) {
                setState(() {
                  amount = int.parse(v);
                });
              },
              prefixText: "Custom Amount: ",
              hintText: "xxxxx",
            ),
            SizedBox(height: 50),
            Row(
              children: [
                MediumBodyTypographyCustomWidget(
                    content: "Total Amount\nPKR. $amount/-"),
                SizedBox(width: 20),
                Expanded(
                  child: TextButtonCustomWidget(
                    content: "Confirm Transfer",
                    onPressed: () => _submit(context),
                  ),
                ),
              ],
            ),
            const ErrorTypographyCustomWidget(),
          ],
        );
      },
    );
  }
}

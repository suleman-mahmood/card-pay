import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'dart:convert';
import 'package:frontend_futter/src/config/themes/colors.dart';
import 'package:flutter/services.dart';
import 'package:frontend_futter/src/presentation/widgets/containment/cards/transaction_history_card.dart';

class TransactionList extends HookWidget {
  final List<Color> colors = [
    AppColors.blackColor,
    AppColors.greenColor,
    AppColors.redColor,
  ];

  const TransactionList({super.key});

  Future<List<dynamic>> loadTransactions() async {
    try {
      String jsonString =
          await rootBundle.loadString('assets/files/catalog.json');
      return jsonDecode(jsonString);
    } catch (e) {
      print("Error loading transactions: $e");
      return [];
    }
  }

  @override
  Widget build(BuildContext context) {
    final transactions = useState(<dynamic>[]);

    useEffect(() {
      loadTransactions().then((value) => transactions.value = value);
      return () {};
    }, []);

    return ListView.builder(
      itemCount: transactions.value.length,
      itemBuilder: (context, index) {
        Map<String, dynamic> transaction = transactions.value[index];
        Color color = colors[transaction['colorIndex']];

        return Padding(
          padding: EdgeInsets.symmetric(
              horizontal: MediaQuery.of(context).size.width * 0.04),
          child: TransactionContainer(
            icon: Icons.send,
            firstText: transaction['id'],
            secondText: transaction['amount'],
            firstTextColor: color,
            secondTextColor: color,
            iconColor: color,
          ),
        );
      },
    );
  }
}

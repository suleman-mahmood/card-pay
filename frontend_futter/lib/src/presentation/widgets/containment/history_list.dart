import 'package:cardpay/src/presentation/widgets/boxes/padding_box.dart';
import 'dart:math';

import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'dart:convert';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:flutter/services.dart';
import 'package:cardpay/src/presentation/widgets/containment/cards/transaction_history_card.dart';

class TransactionList extends HookWidget {
  final List<Color> colors = [
    AppColors.blackColor,
    AppColors.greenColor,
    AppColors.redColor,
  ];

  TransactionList({super.key});

  // Future<List<dynamic>> loadTransactions() async {
  //   try {
  //     String jsonString =
  //         await rootBundle.loadString('assets/files/catalog.json');
  //     return jsonDecode(jsonString);
  //   } catch (e) {
  //     print("Error loading transactions: $e");
  //     return [];
  //   }
  // }

  @override
  Widget build(BuildContext context) {
    // final transactions = useState(<dynamic>[]);

    // useEffect(() {
    //   loadTransactions().then((value) => transactions.value = value);
    //   return () {};
    // }, []);

    final userCubit = BlocProvider.of<UserCubit>(context);

    useEffect(() {
      // userCubit.getUserRecentTransactions();
    }, []);

    return BlocBuilder<UserCubit, UserState>(
      builder: (_, state) {
        switch (state.runtimeType) {
          case UserSuccess:
            return ListView.builder(
              itemCount: state.transactions.length,
              itemBuilder: (context, index) {
                final transaction = state.transactions[index];
                // generate a random number between 0 and 2
                final randomNumber = Random().nextInt(3);
                Color color = colors[randomNumber];

                return PaddingHorizontal(
                  slab: 1,
                  child: TransactionContainer(
                    icon: Icons.send,
                    firstText: transaction.id,
                    secondText: transaction.amount.toString(),
                    firstTextColor: color,
                    secondTextColor: color,
                    iconColor: color,
                  ),
                );
              },
            );
          default:
            return const SizedBox.shrink();
        }
      },
    );
  }
}

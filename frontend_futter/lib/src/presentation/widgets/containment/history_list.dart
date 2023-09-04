import 'dart:math';
import 'package:cardpay/src/presentation/widgets/boxes/horizontal_padding.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/containment/cards/transaction_history_card.dart';

class TransactionList extends HookWidget {
  final List<Color> colors = [
    AppColors.blackColor,
    AppColors.greenColor,
    AppColors.redColor,
  ];

  TransactionList({super.key});

  @override
  Widget build(BuildContext context) {
    final userCubit = BlocProvider.of<UserCubit>(context);

    // useEffect(() {
    //   userCubit.getUserRecentTransactions();
    // }, []);

    return BlocBuilder<UserCubit, UserState>(
      builder: (_, state) {
        switch (state.runtimeType) {
          case UserLoading:
            return const Center(child: CircularProgressIndicator());
          case UserSuccess:
            return ListView.builder(
              itemCount: state.user.recentTransactions.length,
              itemBuilder: (context, index) {
                final transaction = state.user.recentTransactions[index];
                // generate a random number between 0 and 2
                final randomNumber = Random().nextInt(3);
                Color color = colors[randomNumber];

                return PaddingHorizontal(
                  slab: 1,
                  child: TransactionContainer(
                    amount: transaction.amount.toString(),
                    senderName: transaction.senderName,
                    recipientName: transaction.recipientName,
                    currentUserName: state.user.fullName,
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

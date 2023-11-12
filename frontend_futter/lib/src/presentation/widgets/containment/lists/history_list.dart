import 'dart:math';
import 'package:cardpay/src/presentation/cubits/local/local_recent_transactions_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/balance_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/recent_transactions_cubit.dart';
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
    final balanceCubit = BlocProvider.of<BalanceCubit>(context);
    final recentTransactionsCubit =
        BlocProvider.of<RecentTransactionsCubit>(context);

    return BlocBuilder<RecentTransactionsCubit, RecentTransactionsState>(
      builder: (_, state) {
        switch (state.runtimeType) {
          case RecentTransactionsLoading:
            return BlocBuilder<LocalRecentTransactionsCubit,
                LocalRecentTransactionsState>(
              builder: (_, state) {
                switch (state.runtimeType) {
                  case LocalRecentTransactionsSuccess:
                    return ListView.builder(
                      itemCount: state.transactions.length,
                      itemBuilder: (context, index) {
                        final transaction = state.transactions[index];
                        return PaddingHorizontal(
                          slab: 3,
                          child: TransactionContainer(
                            loading: true,
                            amount: transaction.amount.toString(),
                            senderName: transaction.senderName,
                            recipientName: transaction.recipientName,
                            currentUserName: userCubit.state.user.fullName,
                            timeOfTransaction:
                                transaction.createdAt ?? DateTime.now(),
                          ),
                        );
                      },
                    );
                  default:
                    return const SizedBox.shrink();
                }
              },
            );
          case RecentTransactionsSuccess:
            return RefreshIndicator(
              backgroundColor: AppColors.secondaryColor,
              onRefresh: () async {
                balanceCubit.getUserBalance();
                recentTransactionsCubit.getUserRecentTransactions();

                // We are much faster than one sec :P
                return Future<void>.delayed(const Duration(seconds: 1));
              },
              child: ListView.builder(
                itemCount: state.recentTransactions.length,
                itemBuilder: (context, index) {
                  final transaction = state.recentTransactions[index];
                  return PaddingHorizontal(
                    slab: 3,
                    child: TransactionContainer(
                      amount: transaction.amount.toString(),
                      senderName: transaction.senderName,
                      recipientName: transaction.recipientName,
                      currentUserName: userCubit.state.user.fullName,
                      timeOfTransaction:
                          transaction.createdAt ?? DateTime.now(),
                    ),
                  );
                },
              ),
            );
          default:
            return const SizedBox.shrink();
        }
      },
    );
  }
}

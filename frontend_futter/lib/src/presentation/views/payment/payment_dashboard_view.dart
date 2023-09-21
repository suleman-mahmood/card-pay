import 'dart:math';
import 'package:cardpay/src/presentation/cubits/remote/balance_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/recent_transactions_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/all_padding.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/loadings/circle_list_item_loading.dart';
import 'package:cardpay/src/presentation/widgets/loadings/inputfield_shimmer_loading.dart';
import 'package:cardpay/src/presentation/widgets/loadings/shimmer_loading.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/containment/cards/balance_card.dart';
import 'package:cardpay/src/presentation/widgets/containment/cards/transaction_history_card.dart';
import 'package:cardpay/src/presentation/widgets/containment/cards/greeting_card.dart';
import 'package:cardpay/src/presentation/widgets/containment/cards/services_card.dart';
import 'package:cardpay/src/utils/constants/payment_strings.dart';

@RoutePage()
class PaymentDashboardView extends HookWidget {
  final GlobalKey<ScaffoldState>? scaffoldKey;

  PaymentDashboardView({
    Key? key,
    this.scaffoldKey,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final userCubit = BlocProvider.of<UserCubit>(context);
    final balanceCubit = BlocProvider.of<BalanceCubit>(context);
    final recentTransactionsCubit =
        BlocProvider.of<RecentTransactionsCubit>(context);

    String displayName(String fullName) {
      final words = fullName.split(" ");

      if (words.isEmpty) {
        return "";
      }
      return words[0];
    }

    return PaddingAll(
      slab: 1,
      child: SingleChildScrollView(
        child: Column(
          children: [
            // Full name and avatar wala section
            const HeightBox(slab: 4),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                BlocBuilder<UserCubit, UserState>(
                  builder: (_, state) {
                    switch (state.runtimeType) {
                      case UserLoading:
                        return const ShimmerLoading(
                          child: CircleListItemLoading(),
                        );
                      case UserSuccess || UserInitial:
                        return GreetingRow(
                          greeting: PaymentStrings.greet,
                          name: displayName(state.user.fullName),
                          imagePath: 'assets/images/talha.jpg',
                        );
                      default:
                        return const SizedBox.shrink();
                    }
                  },
                ),
                Transform.scale(
                  scale: 1.75,
                  child: IconButton(
                    icon: const Icon(Icons.menu),
                    color: AppColors.greyColor,
                    onPressed: () {
                      scaffoldKey?.currentState!.openEndDrawer();
                    },
                  ),
                ),
              ],
            ),

            // Balance wala section
            const HeightBox(slab: 3),
            BlocBuilder<BalanceCubit, BalanceState>(
              builder: (_, state) {
                switch (state.runtimeType) {
                  case BalanceLoading:
                    return const CircularProgressIndicator();
                  // return Positioned.fill(
                  //   child: FieldShimmer(
                  //     height: 170,
                  //     width: 330,
                  //   ),
                  // );
                  case BalanceSuccess:
                    return BalanceCard(
                      balance: 'Rs. ${state.balance.amount.toString()}',
                      topRightImage: 'assets/images/balance_corner.png',
                      bottomLeftImage: 'assets/images/balance_corner2.png',
                    );
                  default:
                    return const SizedBox.shrink();
                }
              },
            ),

            // Transactions wala section
            BlocBuilder<RecentTransactionsCubit, RecentTransactionsState>(
              builder: (_, state) {
                switch (state.runtimeType) {
                  case RecentTransactionsLoading:
                    return const CircularProgressIndicator();
                  case RecentTransactionsSuccess:
                    if (state.recentTransactions.isEmpty) {
                      return const SizedBox.shrink();
                    }
                    return Column(
                      children: [
                        const HeightBox(slab: 2),
                        Align(
                          alignment: Alignment.centerLeft,
                          child: Text(
                            PaymentStrings.recentTransactions,
                            style: AppTypography.bodyTextBold,
                          ),
                        ),
                        const HeightBox(slab: 1),
                        SizedBox(
                          height: 100,
                          child: RefreshIndicator(
                            onRefresh: () async {
                              balanceCubit.getUserBalance();
                              recentTransactionsCubit
                                  .getUserRecentTransactions();

                              // We are much faster than one sec :P
                              return Future<void>.delayed(
                                  const Duration(seconds: 1));
                            },
                            child: ListView.builder(
                              itemCount: min(
                                2,
                                state.recentTransactions.length,
                              ),
                              itemBuilder: (_, index) {
                                return TransactionContainer(
                                  senderName: state
                                      .recentTransactions[index].senderName,
                                  recipientName: state
                                      .recentTransactions[index].recipientName,
                                  amount: state.recentTransactions[index].amount
                                      .toString(),
                                  currentUserName:
                                      userCubit.state.user.fullName,
                                );
                              },
                            ),
                          ),
                        ),
                      ],
                    );
                  default:
                    return const SizedBox.shrink();
                }
              },
            ),

            const HeightBox(slab: 3),
            const Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                CustomBox(
                  imagePath: 'assets/images/Upwork-3.png',
                  text: PaymentStrings.deposit,
                  route: DepositAmountRoute(),
                ),
                CustomBox(
                  imagePath: 'assets/images/Upwork.png',
                  text: PaymentStrings.transfer,
                  route: TransferRecipientRoute(),
                )
              ],
            ),
            const HeightBox(slab: 1),
            const Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                CustomBox(
                  imagePath: 'assets/images/request-disabled.png',
                  text: PaymentStrings.request,
                  isDisabled: true,
                ),
                CustomBox(
                  imagePath: 'assets/images/faq.png',
                  text: PaymentStrings.faq,
                  route: FaqsRoute(),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

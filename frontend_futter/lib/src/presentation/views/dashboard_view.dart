import 'dart:math';
import 'package:cardpay/src/presentation/cubits/remote/balance_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/deposit_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/recent_transactions_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/transfer_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/all_padding.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/loadings/card_list_item_loading.dart';
import 'package:cardpay/src/presentation/widgets/loadings/circle_list_item_loading.dart';
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
import 'package:cardpay/src/utils/constants/payment_string.dart';

@RoutePage()
class DashboardView extends HookWidget {
  final GlobalKey<ScaffoldState>? scaffoldKey;

  DashboardView({
    Key? key,
    this.scaffoldKey,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final transferCubit = BlocProvider.of<TransferCubit>(context);
    final depositCubit = BlocProvider.of<DepositCubit>(context);

    final userFullName = useState<String>('');

    useEffect(() {
      transferCubit.init();
      depositCubit.init();
    }, []);

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
                          isLoading: true,
                          child: CircleListItemLoading(),
                        );
                      case UserSuccess || UserInitial:
                        WidgetsBinding.instance.addPostFrameCallback((_) {
                          userFullName.value = state.user.fullName;
                        });

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
                    return const ShimmerLoading(
                      isLoading: true,
                      child: CardListItemLoading(),
                    );
                  case BalanceSuccess:
                    return BalanceCard(
                      balance: state.balance.amount.toString(),
                      topRightImage: 'assets/images/balance_corner.png',
                      bottomLeftImage: 'assets/images/balance_corner2.png',
                    );
                  default:
                    return const SizedBox.shrink();
                }
              },
            ),

            // Transactions wala section
            HeightBox(slab: 2),
            Align(
              alignment: Alignment.centerLeft,
              child: Text(
                PaymentStrings.recentTransactions,
                style: AppTypography.bodyTextBold,
              ),
            ),
            HeightBox(slab: 1),
            BlocBuilder<RecentTransactionsCubit, RecentTransactionsState>(
              builder: (_, state) {
                switch (state.runtimeType) {
                  case RecentTransactionsLoading:
                    return const CircularProgressIndicator();
                  case RecentTransactionsSuccess:
                    return SizedBox(
                      height: 100,
                      child: ListView.builder(
                        itemCount: min(
                          2,
                          state.recentTransactions.length,
                        ),
                        itemBuilder: (_, index) {
                          return TransactionContainer(
                            senderName:
                                state.recentTransactions[index].senderName,
                            recipientName:
                                state.recentTransactions[index].recipientName,
                            amount: state.recentTransactions[index].amount
                                .toString(),
                            currentUserName: userFullName.value,
                          );
                        },
                      ),
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
                  text: PaymentStrings.deposite,
                  route: DepositRoute(),
                ),
                CustomBox(
                  imagePath: 'assets/images/Upwork.png',
                  text: PaymentStrings.transfer,
                  route: TransferRoute(),
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
                  imagePath: 'assets/images/faqs-disabled.png',
                  text: PaymentStrings.faq,
                  route: FaqsRoute(),
                  isDisabled: true,
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

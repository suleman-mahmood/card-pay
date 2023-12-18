import 'package:cardpay/src/config/firebase/analytics_service.dart';
import 'package:cardpay/src/locator.dart';
import 'package:cardpay/src/presentation/cubits/local/local_recent_transactions_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/all_requests_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/balance_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/frequent_users_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/recent_transactions_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
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
import 'package:cardpay/src/utils/constants/payment_strings.dart';
import 'package:skeleton_loader/skeleton_loader.dart';

import 'request_amount_view.dart';

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
    final localRecentTransactionsCubit =
        BlocProvider.of<LocalRecentTransactionsCubit>(context);
    final frequentUsersCubit = BlocProvider.of<FrequentUsersCubit>(context);
    final allRequestsCubit = BlocProvider.of<AllRequestsCubit>(context);

    final deviceHeight = MediaQuery.of(context).size.height;

    Widget buildTransactions() {
      return BlocBuilder<RecentTransactionsCubit, RecentTransactionsState>(
        builder: (_, state) {
          switch (state.runtimeType) {
            case RecentTransactionsLoading:
              return BlocBuilder<LocalRecentTransactionsCubit,
                  LocalRecentTransactionsState>(
                builder: (_, state) {
                  switch (state.runtimeType) {
                    case LocalRecentTransactionsSuccess:
                      if (state.transactions.isEmpty) {
                        // a no transaction found widget
                        return SkeletonLoader(
                          builder: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              SizedBox(height: deviceHeight * 0.007),
                              Align(
                                alignment: Alignment.centerLeft,
                                child: Text(
                                  PaymentStrings.recentTransactions,
                                  style: AppTypography.bodyTextBold,
                                ),
                              ),
                              SizedBox(
                                height:
                                    MediaQuery.sizeOf(context).height * 0.13,
                                child: const Row(
                                  mainAxisAlignment: MainAxisAlignment.center,
                                  children: [
                                    Column(
                                      mainAxisSize: MainAxisSize.min,
                                      mainAxisAlignment:
                                          MainAxisAlignment.center,
                                      crossAxisAlignment:
                                          CrossAxisAlignment.center,
                                      children: [
                                        Text(
                                          'No Recent Transactions Found!',
                                          style: TextStyle(
                                            color: Colors.black54,
                                            fontSize: 16,
                                            fontWeight: FontWeight.bold,
                                          ),
                                        ),
                                        Text(
                                          'Make a Deposit or Transfer',
                                          style: TextStyle(
                                            color: AppColors.greyColor,
                                            fontSize: 14,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          ),
                        );
                      }
                      return SkeletonLoader(
                        builder: Column(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            SizedBox(height: deviceHeight * 0.007),
                            Align(
                              alignment: Alignment.centerLeft,
                              child: Text(
                                PaymentStrings.recentTransactions,
                                style: AppTypography.bodyTextBold,
                              ),
                            ),
                            SizedBox(height: deviceHeight * 0.007),
                            // using a column instead of list to display the entire container
                            Column(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                TransactionContainer(
                                  senderName: state.transactions[0].senderName,
                                  recipientName:
                                      state.transactions[0].recipientName,
                                  amount:
                                      state.transactions[0].amount.toString(),
                                  currentUserName:
                                      userCubit.state.user.fullName,
                                  timeOfTransaction:
                                      state.transactions[0].createdAt ??
                                          DateTime.now(),
                                ),
                                if (deviceHeight > 750 &&
                                    state.transactions.length > 1)
                                  TransactionContainer(
                                    senderName:
                                        state.transactions[1].senderName,
                                    recipientName:
                                        state.transactions[1].recipientName,
                                    amount:
                                        state.transactions[1].amount.toString(),
                                    currentUserName:
                                        userCubit.state.user.fullName,
                                    timeOfTransaction:
                                        state.transactions[1].createdAt ??
                                            DateTime.now(),
                                  ),
                              ],
                            ),
                          ],
                        ),
                      );
                    default:
                      return const SizedBox.shrink();
                  }
                },
              );

            case RecentTransactionsSuccess:
              localRecentTransactionsCubit
                  .updateRecentTransactions(state.recentTransactions);
              if (state.recentTransactions.isEmpty) {
                // a no transaction found widget
                return Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    SizedBox(height: deviceHeight * 0.007),
                    Align(
                      alignment: Alignment.centerLeft,
                      child: Text(
                        PaymentStrings.recentTransactions,
                        style: AppTypography.bodyTextBold,
                      ),
                    ),
                    SizedBox(
                      height: MediaQuery.sizeOf(context).height * 0.13,
                      child: const Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Column(
                            mainAxisSize: MainAxisSize.min,
                            mainAxisAlignment: MainAxisAlignment.center,
                            crossAxisAlignment: CrossAxisAlignment.center,
                            children: [
                              Text(
                                'No Recent Transactions Found!',
                                style: TextStyle(
                                  color: Colors.black54,
                                  fontSize: 16,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              Text(
                                'Make a Deposit or Transfer',
                                style: TextStyle(
                                  color: AppColors.greyColor,
                                  fontSize: 14,
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ],
                );
              }
              return Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  SizedBox(height: deviceHeight * 0.007),
                  Align(
                    alignment: Alignment.centerLeft,
                    child: Text(
                      PaymentStrings.recentTransactions,
                      style: AppTypography.bodyTextBold,
                    ),
                  ),
                  SizedBox(height: deviceHeight * 0.007),
                  // using a column instead of list to display the entire container
                  Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      TransactionContainer(
                        senderName: state.recentTransactions[0].senderName,
                        recipientName:
                            state.recentTransactions[0].recipientName,
                        amount: state.recentTransactions[0].amount.toString(),
                        currentUserName: userCubit.state.user.fullName,
                        timeOfTransaction:
                            state.recentTransactions[0].createdAt ??
                                DateTime.now(),
                      ),
                      if (deviceHeight > 750 &&
                          state.recentTransactions.length > 1)
                        TransactionContainer(
                          senderName: state.recentTransactions[1].senderName,
                          recipientName:
                              state.recentTransactions[1].recipientName,
                          amount: state.recentTransactions[1].amount.toString(),
                          currentUserName: userCubit.state.user.fullName,
                          timeOfTransaction:
                              state.recentTransactions[1].createdAt ??
                                  DateTime.now(),
                        ),
                    ],
                  ),
                ],
              );
            default:
              return const SizedBox.shrink();
          }
        },
      );
    }

    String displayName(String fullName) {
      final words = fullName.split(" ");

      if (words.isEmpty) {
        return "";
      }
      return words[0];
    }

    return GestureDetector(
      // reload when gesture scroll downn
      onVerticalDragEnd: (details) {
        if (details.primaryVelocity! > 100) {
          balanceCubit.getUserBalance();
          recentTransactionsCubit.getUserRecentTransactions();

          locator<AnalyticsService>().logMotion(
            'VerticalDrag',
            "Dashboard",
          );
        }
      },
      child: Container(
        constraints: BoxConstraints.loose(
          Size.fromHeight(deviceHeight),
        ),
        decoration: const BoxDecoration(
          color: Colors.transparent,
        ),
        // height - safe area height
        //height: double.infinity,
        margin: const EdgeInsets.only(
          // bottom padding to accomodate the bottom navigation bar = qr code button height + bottom navigation bar height + some extra padding
          bottom: 36 + 10,
          top: 10,
          left: 5,
          right: 5,
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            // Full name and avatar wala section
            SizedBox(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const HeightBox(slab: 1),
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
                  const SizedBox(height: 4),
                  const BalanceCard(),
                ],
              ),
            ),

            // Transactions wala section
            buildTransactions(),

            // TODO: Do the figma design magic
            MaterialButton(
              child: Text("View all requests mate"),
              onPressed: () {
                allRequestsCubit.getP2PPullRequests();
                context.router.push(const AllRequestsRoute());
              },
            ),

            // Reason? Wrapping it with Column prevents any unnecessary distance between the two rows,
            // due to the parent column with space between property
            Column(
              children: [
                const Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    CustomBox(
                      imagePath: 'assets/icon/deposit.svg',
                      text: PaymentStrings.deposit,
                      route: DepositAmountRoute(),
                      cardColor: Color.fromRGBO(6, 127, 205, 1),
                      splashColor: Color.fromRGBO(3, 83, 136, 1),
                    ),
                    CustomBox(
                      imagePath: 'assets/icon/transfer.svg',
                      text: PaymentStrings.transfer,
                      route: TransferRecipientRoute(),
                      cardColor: Color.fromRGBO(1, 204, 136, 1),
                      splashColor: Color.fromRGBO(1, 96, 64, 1),
                    )
                  ],
                ),
                SizedBox(height: deviceHeight * 0.01),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const CustomBox(
                      imagePath: 'assets/icon/faqs.svg',
                      text: PaymentStrings.events,
                      route: EventSelectorRoute(),
                      cardColor: Color.fromRGBO(1, 204, 192, 1),
                      splashColor: Color.fromRGBO(1, 84, 79, 1),
                    ),
                    CustomBox(
                      imagePath: 'assets/icon/faqs.svg',
                      text: PaymentStrings.request,
                      route: RequestSenderRoute(),
                      cardColor: Color.fromRGBO(1, 204, 192, 1),
                      splashColor: Color.fromRGBO(1, 84, 79, 1),
                      onTap: () {
                        frequentUsersCubit.getFrequentUsers(
                          closedLoopId:
                              userCubit.data.closedLoops[0].closedLoopId,
                        );
                      },
                    ),
                  ],
                ),
              ],
            ),

            // // // // // //// // // // // // // // // //
            // The two rows and scroll left right thingy //
            // // // // // //// // // // // // // // // //

            // const HeightBox(slab: 3),
            // const SingleChildScrollView(
            //   scrollDirection: Axis.horizontal,
            //   child: Row(
            //     children: [
            //       CustomBox(
            //         imagePath: 'assets/images/Upwork-3.png',
            //         text: PaymentStrings.deposit,
            //         route: DepositAmountRoute(),
            //       ),
            //       WidthBetween(),
            //       CustomBox(
            //         imagePath: 'assets/images/Upwork.png',
            //         text: PaymentStrings.transfer,
            //         route: TransferRecipientRoute(),
            //       ),
            //       WidthBetween(),
            //       CustomBox(
            //         imagePath: 'assets/images/faq.png',
            //         text: PaymentStrings.faq,
            //         route: FaqsRoute(),
            //       ),
            //       WidthBetween(),
            //       CustomBox(
            //         imagePath: 'assets/images/request-disabled.png',
            //         text: PaymentStrings.request,
            //         isDisabled: true,
            //       ),
            //     ],
            //   ),
            // ),
            // const HeightBox(slab: 3),
            // const Row(
            //   children: [
            //     CustomBox(
            //       imagePath: 'assets/images/faq.png',
            //       text: PaymentStrings.events,
            //       route: EventSelectorRoute(),
            //     ),
            //   ],
            // ),
          ],
        ),
      ),
    );
  }
}

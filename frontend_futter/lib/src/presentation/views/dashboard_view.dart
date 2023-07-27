import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/views/payment_dashboard_view.dart';
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
import 'package:cardpay/src/presentation/widgets/navigations/drawer_navigation.dart';
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
    final userCubit = BlocProvider.of<UserCubit>(context);
    final isLoading = true;

    // TODO: Have separte loading for full name, balance and recent transactions
    useEffect(() {
      // userCubit.getUser();
      // userCubit.getUserBalance();
      // userCubit.getUserRecentTransactions();

      // This definitely works
      someFunction() async {
        await userCubit.getUser();
        await userCubit.getUserBalance();
        // await userCubit.getUserRecentTransactions();
      }

      someFunction();
    }, []);

    return Column(
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
                    return ShimmerLoading(
                      isLoading: isLoading,
                      child: CircleListItemLoading(),
                    );
                  case UserSuccess || UserInitial:
                    return GreetingRow(
                      greeting: PaymentStrings.greet,
                      name: state.user.fullName,
                      imagePath: 'assets/images/talha.jpg',
                    );
                  case UserFailed:
                    return Text(
                      state.error!.response!.data['message'],
                      style: const TextStyle(color: Colors.red),
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
                  // Scaffold.of(context).openEndDrawer();
                },
              ),
            ),
          ],
        ),

        // Balance wala section
        const HeightBox(slab: 3),
        BlocBuilder<UserCubit, UserState>(
          builder: (_, state) {
            switch (state.runtimeType) {
              case UserLoading:
                return ShimmerLoading(
                  isLoading: isLoading,
                  child: CardListItemLoading(),
                );
              case UserSuccess || UserInitial:
                return BalanceCard(
                  balance: state.user.balance.toString(),
                  topRightImage: 'assets/images/balance_corner.png',
                  bottomLeftImage: 'assets/images/balance_corner2.png',
                );
              case UserFailed:
                return Text(
                  state.error!.response!.data['message'],
                  style: const TextStyle(color: Colors.red),
                );
              default:
                return const SizedBox.shrink();
            }
          },
        ),

        // Transactions wala section
        // HeightBox(slab: 2),
        // Align(
        //   alignment: Alignment.centerLeft,
        //   child: Text(
        //     PaymentStrings.recentTransactions,
        //     style: AppTypography.bodyTextBold,
        //   ),
        // ),
        // TransactionContainer(
        //   icon: Icons.send,
        //   firstText: PaymentStrings.rollNumber,
        //   secondText: PaymentStrings.pAmount,
        //   firstTextColor: AppColors.blackColor,
        //   secondTextColor: AppColors.redColor,
        //   iconColor: AppColors.primaryColor,
        // ),
        // TransactionContainer(
        //   icon: Icons.money,
        //   firstText: PaymentStrings.rollNumber,
        //   secondText: PaymentStrings.nAmount,
        //   firstTextColor: AppColors.blackColor,
        //   secondTextColor: AppColors.greenColor,
        //   iconColor: AppColors.primaryColor,
        // ),

        // BlocBuilder<UserCubit, UserState>(
        //   builder: (_, state) {
        //     switch (state.runtimeType) {
        //       case UserLoading:
        //         return const CircularProgressIndicator();
        //       case UserSuccess:
        //         return ListView.builder(
        //           itemCount:
        //               min(2, state.transactions.length),
        //           itemBuilder: (_, index) {
        //             return TransactionContainer(
        //               icon: Icons.send,
        //               firstText:
        //                   PaymentStrings.rollNumber,
        //               secondText: state
        //                   .transactions[index].amount
        //                   .toString(),
        //               firstTextColor:
        //                   AppColors.blackColor,
        //               secondTextColor: AppColors.redColor,
        //               iconColor: AppColors.primaryColor,
        //             );
        //           },
        //         );
        //       case UserFailed:
        //         return Text(
        //           state.error!.response!.data['message'],
        //           style:
        //               const TextStyle(color: Colors.red),
        //         );
        //       default:
        //         return const SizedBox.shrink();
        //     }
        //   },
        // ),

        HeightBox(slab: 3),
        Row(
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
        HeightBox(slab: 3),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            CustomBox(
              imagePath: 'assets/images/Upwork-1.png',
              text: PaymentStrings.request,
              route: RequestRoute(),
            ),
            // CustomBox(
            //   imagePath: 'assets/images/Upwork-2.png',
            //   text: PaymentStrings.faq,
            //   route: FaqsRoute(),
            // )
          ],
        ),
      ],
    );
  }
}

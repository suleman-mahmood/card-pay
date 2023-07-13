import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/layout/payment_layouts.dart';
import 'package:flutter/material.dart';
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
  const DashboardView({Key? key}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: false,
      body: Builder(
        builder: (BuildContext scaffoldContext) {
          return PaymentLayout(
            child: Column(
              children: [
                const HeightBox(slab: 4),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const GreetingRow(
                      greeting: PaymentStrings.greet,
                      name: PaymentStrings.name,
                      imagePath: 'assets/images/talha.jpg',
                    ),
                    Transform.scale(
                      scale: 1.75,
                      child: IconButton(
                        icon: const Icon(Icons.menu),
                        color: AppColors.greyColor,
                        onPressed: () {
                          Scaffold.of(scaffoldContext).openEndDrawer();
                        },
                      ),
                    ),
                  ],
                ),
                const HeightBox(slab: 3),
                BalanceCard(
                  balance: PaymentStrings.balance,
                  topRightImage: 'assets/images/balance_corner.png',
                  bottomLeftImage: 'assets/images/balance_corner2.png',
                ),
                HeightBox(slab: 2),
                Align(
                  alignment: Alignment.centerLeft,
                  child: Text(PaymentStrings.recentTransactions,
                      style: AppTypography.bodyTextBold),
                ),
                const TransactionContainer(
                  icon: Icons.send,
                  firstText: PaymentStrings.rollNumber,
                  secondText: PaymentStrings.pAmount,
                  firstTextColor: AppColors.blackColor,
                  secondTextColor: AppColors.redColor,
                  iconColor: AppColors.primaryColor,
                ),
                const TransactionContainer(
                  icon: Icons.money,
                  firstText: PaymentStrings.rollNumber,
                  secondText: PaymentStrings.nAmount,
                  firstTextColor: AppColors.blackColor,
                  secondTextColor: AppColors.greenColor,
                  iconColor: AppColors.primaryColor,
                ),
                HeightBox(slab: 3),
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
                HeightBox(slab: 3),
                const Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    CustomBox(
                      imagePath: 'assets/images/Upwork-1.png',
                      text: PaymentStrings.request,
                      route: RequestRoute(),
                    ),
                    CustomBox(
                      imagePath: 'assets/images/Upwork-2.png',
                      text: PaymentStrings.faq,
                      route: DashboardRoute(),
                    )
                  ],
                ),
              ],
            ),
          );
        },
      ),
      endDrawer: MyDrawer(),
    );
  }
}

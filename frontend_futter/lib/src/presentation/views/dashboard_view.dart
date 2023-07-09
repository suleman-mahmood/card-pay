import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:auto_route/auto_route.dart';
import 'package:frontend_futter/src/config/router/app_router.dart';
import 'package:frontend_futter/src/presentation/widgets/layout/auth_layout.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';
import 'package:frontend_futter/src/config/screen_utills/screen_util.dart';
import 'package:frontend_futter/src/presentation/widgets/containment/cards/balance_card.dart';
import 'package:frontend_futter/src/presentation/widgets/containment/cards/transaction_history_card.dart';
import 'package:frontend_futter/src/presentation/widgets/containment/cards/greeting_card.dart';
import 'package:frontend_futter/src/presentation/widgets/containment/cards/services_card.dart';
import 'package:frontend_futter/src/presentation/widgets/navigations/bottom_bar.dart';
import 'package:frontend_futter/src/presentation/widgets/navigations/drawer_navigation.dart';
import 'package:frontend_futter/src/utils/constants/payment_string.dart';

final pages = [
  const DashboardRoute(),
  const ConfirmationRoute(),
  const FilterHistoryRoute(),
  const HistroyRoute(),
];

@RoutePage()
class DashboardView extends HookWidget {
  const DashboardView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final selectedIndex = useState(0);
    return Scaffold(
      body: Builder(
        builder: (BuildContext scaffoldContext) {
          return AuthLayout(
            child: Padding(
              padding: EdgeInsets.symmetric(
                horizontal: ScreenUtil.widthMultiplier(context) * 2,
              ),
              child: Column(
                children: [
                  Padding(
                    padding: const EdgeInsets.only(top: 8.0),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const GreetingRow(
                          greeting: PaymentStrings.greet,
                          name: PaymentStrings.name,
                          imagePath: 'assets/images/talha.jpg',
                        ),
                        IconButton(
                          icon: const Icon(Icons.menu),
                          onPressed: () {
                            Scaffold.of(scaffoldContext).openEndDrawer();
                          },
                        ),
                      ],
                    ),
                  ),
                  const VerticalSpace(3),
                  BalanceCard(
                    balance: PaymentStrings.balance,
                    topRightImage: 'assets/images/balance_corner.png',
                    bottomLeftImage: 'assets/images/balance_corner2.png',
                  ),
                  const VerticalSpace(1),
                  const RecentTransactionsTitle(),
                  const VerticalSpace(1),
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
                  SizedBox(height: ScreenUtil.heightMultiplier(context) * 2),
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
                  SizedBox(height: ScreenUtil.heightMultiplier(context) * 2),
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
            ),
          );
        },
      ),
      endDrawer: MyDrawer(),
      bottomNavigationBar: CustomCurvedBottomBar(
        selectedIndex: selectedIndex.value,
        onItemTapped: (index) {
          selectedIndex.value = index;
          context.router.push(pages[index]);
        },
      ),
    );
  }
}

class VerticalSpace extends HookWidget {
  final double multiplier;

  const VerticalSpace(this.multiplier, {Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return SizedBox(height: ScreenUtil.heightMultiplier(context) * multiplier);
  }
}

class RecentTransactionsTitle extends HookWidget {
  const RecentTransactionsTitle({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Text(
      PaymentStrings.recentTransactions,
      style: AppTypography.headingFont.copyWith(
        fontSize: ScreenUtil.textMultiplier(context) * 2,
      ),
    );
  }
}

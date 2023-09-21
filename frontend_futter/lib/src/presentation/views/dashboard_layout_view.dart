import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/views/payment/payment_dashboard_view.dart';
import 'package:cardpay/src/presentation/views/profile/profile_view.dart';
import 'package:cardpay/src/presentation/widgets/navigations/animated_bottom_bar.dart';
import 'package:cardpay/src/presentation/widgets/navigations/drawer_navigation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/router/app_router.dart';

import 'payment/transactions_view.dart';

@RoutePage()
class DashboardLayoutView extends HookWidget {
  final bool showBottomBar;
  final Color? backgroundColor;
  final bool useHorizontalPadding;

  const DashboardLayoutView({
    Key? key,
    this.backgroundColor,
    this.showBottomBar = true,
    this.useHorizontalPadding = true,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final GlobalKey<ScaffoldState> scaffoldKey = GlobalKey();
    final backgroundColor = useState(AppColors.secondaryColor);
    final horizontalPadding = useState(true);
    final selectedIndex = useState(0);

    List<Widget> pageList = [
      PaymentDashboardView(scaffoldKey: scaffoldKey),
      const TransactionsView(),
      const TransactionsView(),
      ProfileView(),
    ];

    useEffect(() {
      switch (selectedIndex.value) {
        case 1 || 2:
          backgroundColor.value = AppColors.purpleColor;
          horizontalPadding.value = false;
        case 3:
          horizontalPadding.value = true;
          backgroundColor.value = AppColors.secondaryColor;
        default:
          backgroundColor.value = AppColors.secondaryColor;
          horizontalPadding.value = true;
      }
    }, [selectedIndex.value]);

    return Scaffold(
      key: scaffoldKey,
      resizeToAvoidBottomInset: true,
      backgroundColor: backgroundColor.value,
      body: SafeArea(
        child: Padding(
          padding: horizontalPadding.value
              ? const EdgeInsets.symmetric(horizontal: 18)
              : EdgeInsets.zero,
          child: pageList.elementAt(selectedIndex.value),
        ),
      ),
      floatingActionButton: Transform.translate(
        offset: const Offset(0, -8),
        child: SizedBox(
          width: 72,
          height: 72,
          child: FloatingActionButton(
            shape: const CircleBorder(),
            onPressed: () {
              context.router.push(QrRoute());
            },
            child: Image.asset(
              'assets/images/qrCode.png',
              width: 48,
            ),
          ),
        ),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerDocked,
      bottomNavigationBar: showBottomBar
          ? AnimatedBottomBar(selectedIndex: selectedIndex)
          : null,
      endDrawer: MyDrawer(),
    );
  }
}

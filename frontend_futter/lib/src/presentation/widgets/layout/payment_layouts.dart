import 'package:auto_route/auto_route.dart';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/presentation/widgets/navigations/bottom_bar.dart';

final pages = [
  const DashboardRoute(),
  const ConfirmationRoute(),
  const FilterHistoryRoute(),
  const HistroyRoute(),
];

class PaymentLayout extends HookWidget {
  final Widget child;
  final bool showBottomBar;
  final Color? backgroundColor;
  final bool useHorizontalPadding;

  const PaymentLayout({
    Key? key,
    required this.child,
    this.showBottomBar = true,
    this.backgroundColor,
    this.useHorizontalPadding = true,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final selectedIndex = useState(0);

    return Scaffold(
      resizeToAvoidBottomInset: true,
      backgroundColor: backgroundColor ?? Colors.white,
      body: SafeArea(
        child: Padding(
          padding: useHorizontalPadding
              ? const EdgeInsets.symmetric(horizontal: 24)
              : EdgeInsets.zero,
          child: SingleChildScrollView(
            child: SizedBox(
              height: MediaQuery.of(context).size.height -
                  MediaQuery.of(context).padding.top,
              child: child,
            ),
          ),
        ),
      ),
      bottomNavigationBar: showBottomBar
          ? CustomCurvedBottomBar(
              selectedIndex: selectedIndex.value,
              onItemTapped: (index) {
                selectedIndex.value = index;
                context.router.push(pages[index]);
              },
            )
          : null,
    );
  }
}

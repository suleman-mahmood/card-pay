import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/views/transaction_service/payment_dashboard_view.dart';
import 'package:cardpay/src/utils/constants/signUp_string.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:cardpay/src/presentation/widgets/containment/confirmation_dialog.dart';
import 'package:cardpay/src/presentation/widgets/navigations/top_navigation.dart';
import 'package:cardpay/src/utils/constants/payment_string.dart';

@RoutePage()
class ConfirmationView extends HookWidget {
  const ConfirmationView({super.key});

  Widget buildConfirmationViewContent(BuildContext context) {
    return Column(
      children: [
        buildHeader(),
        const HeightBox(slab: 3),
        buildSuccessImage(),
        const HeightBox(slab: 3),
        buildSuccessLabel(),
        const HeightBox(slab: 2),
        buildBalanceLabel(),
        const HeightBox(slab: 2),
        buildConfirmationContainer(),
        PrimaryButton(
          text: PaymentStrings.done,
          color: AppColors.parrotColor,
          onPressed: () => context.router.push(PaymentDashboardRoute()),
        ),
        const HeightBox(slab: 5),
      ],
    );
  }

  Widget buildHeader() {
    return const Header(
      title: PaymentStrings.receipt,
      color: Colors.black,
      showMainHeading: true,
    );
  }

  Widget buildSuccessImage() {
    return Image.asset('assets/images/tickbox.png');
  }

  Widget buildSuccessLabel() {
    return Text(PaymentStrings.successful,
        style: AppTypography.mainHeading.copyWith(
          color: AppColors.parrotColor,
        ));
  }

  Widget buildBalanceLabel() {
    return Text(
      PaymentStrings.balanceRupee,
      style: AppTypography.introHeading,
    );
  }

  Widget buildConfirmationContainer() {
    return Expanded(
      child: ConfirmationContainer(
        title1: PaymentStrings.send,
        text1: PaymentStrings.rollNumber,
        title2: AppStrings.date,
        text2: AppStrings.dateToday,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    // return PaymentLayout(
    //   showBottomBar: false,
    return Scaffold(
      body: buildConfirmationViewContent(context),
    );
  }
}

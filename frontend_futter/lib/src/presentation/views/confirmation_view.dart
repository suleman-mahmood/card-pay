import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';
import 'package:frontend_futter/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:frontend_futter/src/presentation/widgets/containment/confirmation_dialog.dart';
import 'package:frontend_futter/src/presentation/widgets/layout/auth_layout.dart';
import 'package:frontend_futter/src/presentation/widgets/navigations/top_navigation.dart';
import 'package:frontend_futter/src/utils/constants/payment_string.dart';
import 'package:frontend_futter/src/config/screen_utills/screen_util.dart';

@RoutePage()
class ConfirmationView extends HookWidget {
  const ConfirmationView({super.key});

  @override
  Widget build(BuildContext context) {
    return AuthLayout(
      child: _buildConfirmationViewContent(context),
    );
  }

  Widget _buildConfirmationViewContent(BuildContext context) {
    return Column(
      children: [_buildHeader(), _buildConfirmationContent(context)],
    );
  }

  Widget _buildHeader() {
    return Header(
      title: PaymentStrings.receipt,
      color: Colors.black,
      showMainHeading: true,
    );
  }

  Widget _buildConfirmationContent(BuildContext context) {
    return Container(
      child: Column(children: [
        _buildSuccessImage(context),
        _buildSuccessLabel(context),
        _buildBalanceLabel(context),
        _buildConfirmationContainer(),
        _buildSpacing(context),
        _buildActionButton(context)
      ]),
    );
  }

  Widget _buildSuccessImage(BuildContext context) {
    return Image.asset(
      'assets/images/tickbox.png',
      width: ScreenUtil.blockSizeHorizontal(context) * 20,
      height: ScreenUtil.blockSizeVertical(context) * 20,
    );
  }

  Widget _buildSuccessLabel(BuildContext context) {
    return Text(
      PaymentStrings.successful,
      style: AppTypography.inputFont.copyWith(
          color: AppColors.primaryColor,
          fontSize: ScreenUtil.textMultiplier(context) * 2.5,
          fontWeight: FontWeight.bold),
    );
  }

  Widget _buildBalanceLabel(BuildContext context) {
    return Text(
      PaymentStrings.balance,
      style: AppTypography.mainHeading
          .copyWith(color: AppColors.blackColor, fontWeight: FontWeight.bold),
    );
  }

  Widget _buildConfirmationContainer() {
    return ConfirmationContainer(
      title1: PaymentStrings.send,
      text1: PaymentStrings.rollNumber,
      title2: PaymentStrings.send,
      text2: PaymentStrings.rollNumber,
    );
  }

  Widget _buildSpacing(BuildContext context) {
    return SizedBox(height: ScreenUtil.blockSizeVertical(context) * 5);
  }

  Widget _buildActionButton(BuildContext context) {
    return CustomButton(
      text: PaymentStrings.done,
      onPressed: () => context.router.pop(),
    );
  }
}

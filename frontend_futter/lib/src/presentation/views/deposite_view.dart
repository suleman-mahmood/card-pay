import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
// import 'package:cardpay/src/presentation/widgets/transection_layout/transection_common_layout.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/themes/colors.dart';

import 'package:cardpay/src/presentation/widgets/layout/transaction_common_layout.dart';
import 'package:cardpay/src/utils/constants/payment_string.dart';

// DepositView Constants
class DepositViewConstants {
  static const title = PaymentStrings.deposite;
  static const buttonText = PaymentStrings.continu;
}

@RoutePage()
class DepositView extends HookWidget {
  const DepositView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return TransactionView(
      title: DepositViewConstants.title,
      buttonText: DepositViewConstants.buttonText,
      backgroundColor: AppColors.mediumBlueColor,
      onButtonPressed: () => context.router.push(const DashboardRoute()),
    );
  }
}

import 'package:cardpay/src/utils/constants/payment_string.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/presentation/widgets/layout/transaction_common_layout.dart';

// import '../widgets/layout/transection_common_layout.dart';

class RequestAmountViewConstants {
  static const title = 'Request Money';
  static const buttonText = 'Continue';
}

@RoutePage()
class RequestAmountView extends HookWidget {
  final String rollNumber;
  const RequestAmountView({Key? key, required this.rollNumber})
      : super(key: key);
  @override
  Widget build(BuildContext context) {
    final rollNumberController = useState<String>(rollNumber);
    return TransactionView(
      title: PaymentStrings.requestMoney,
      buttonText: PaymentStrings.continu,
      rollNumber: rollNumberController.value,
      backgroundColor: AppColors.purpleColor,
      onButtonPressed: () => context.router.push(const DashboardRoute()),
    );
  }
}

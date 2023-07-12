import 'package:cardpay/src/utils/constants/payment_string.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
// import 'package:cardpay/src/presentation/widgets/transection_layout/transection_common_layout.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/presentation/widgets/layout/transaction_common_layout.dart';

// import '../widgets/layout/transection_common_layout.dart';

// SendView Constants
class SendViewConstants {
  static const title = 'Send Money';
  static const buttonText = 'Continue';
}

@RoutePage()
class SendView extends HookWidget {
  final String rollNumber;
  const SendView({Key? key, required this.rollNumber}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    final rollNumberController = useState<String>(rollNumber);
    return TransactionView(
      title: PaymentStrings.depositMoney,
      buttonText: PaymentStrings.continu,
      rollNumber: rollNumberController.value,
      backgroundColor: AppColors.parrotColor,
      onButtonPressed: () => context.router.push(const DashboardRoute()),
    );
  }
}

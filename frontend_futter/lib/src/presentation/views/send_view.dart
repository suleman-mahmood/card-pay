import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
// import 'package:frontend_futter/src/presentation/widgets/transection_layout/transection_common_layout.dart';
import 'package:frontend_futter/src/config/router/app_router.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/presentation/widgets/layout/transaction_common_layout.dart';

// import '../widgets/layout/transection_common_layout.dart';

// SendView Constants
class SendViewConstants {
  static const title = 'Send Money';
  static const buttonText = 'Continue';
}

@RoutePage()
class SendView extends HookWidget {
  final String rollNumber;

  const SendView({super.key, required this.rollNumber});

  @override
  Widget build(BuildContext context) {
    final rollNumberController = useRollNumberController(rollNumber);

    return TransactionView(
      title: SendViewConstants.title,
      buttonText: SendViewConstants.buttonText,
      rollNumber: rollNumberController.rollNumber,
      backgroundColor: AppColors.parrotColor,
      onButtonPressed: () => context.router.push(const DashboardRoute()),
    );
  }
}

RollNumberController useRollNumberController(String rollNumber) {
  final rollNumberController =
      useState<RollNumberController>(RollNumberController(rollNumber));
  return rollNumberController.value;
}

class RollNumberController {
  String rollNumber;

  RollNumberController(this.rollNumber);
}

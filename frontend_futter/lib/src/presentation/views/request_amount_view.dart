import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:frontend_futter/src/config/router/app_router.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/presentation/widgets/layout/transaction_common_layout.dart';

// import '../widgets/layout/transection_common_layout.dart';

class RequestAmountViewConstants {
  static const title = 'Request Money';
  static const buttonText = 'Continue';
}

@RoutePage()
class RequestAmountView extends HookWidget {
  final String rollNumber;

  const RequestAmountView({required this.rollNumber}) : super();

  @override
  Widget build(BuildContext context) {
    final rollNumberController = useRollNumberController(rollNumber);

    return TransactionView(
      title: RequestAmountViewConstants.title,
      buttonText: RequestAmountViewConstants.buttonText,
      rollNumber: rollNumberController.rollNumber,
      backgroundColor: AppColors.purpleColor,
      onButtonPressed: () => context.router.push(DashboardRoute()),
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

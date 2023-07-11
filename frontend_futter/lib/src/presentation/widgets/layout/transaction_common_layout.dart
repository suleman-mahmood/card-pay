import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/screen_utills/screen_util.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/payment_input_buttons.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:cardpay/src/presentation/widgets/navigations/top_navigation.dart';

class TransactionView extends HookWidget {
  final String title;
  final String buttonText;
  final String? rollNumber;
  final Color backgroundColor;
  final VoidCallback onButtonPressed;

  const TransactionView({
    super.key,
    required this.title,
    required this.buttonText,
    this.rollNumber,
    required this.backgroundColor,
    required this.onButtonPressed,
  });

  @override
  Widget build(BuildContext context) {
    final paymentController = useTextEditingController();

    // Whole transaction view with background color
    return Scaffold(
      backgroundColor: backgroundColor,
      body: Stack(
        children: [
          // Align payment info container to bottom of the screen
          Align(
            alignment: Alignment.bottomCenter,
            child: Container(
              margin: EdgeInsets.only(
                bottom: ScreenUtil.blockSizeVertical(context) * 0.025,
              ),
              decoration: BoxDecoration(
                color: AppColors.secondaryColor,
                borderRadius: const BorderRadius.only(
                  topLeft: Radius.circular(30),
                  topRight: Radius.circular(30),
                ),
                boxShadow: [
                  BoxShadow(
                    color: AppColors.greyColor.withOpacity(0.5),
                    spreadRadius: 5,
                    blurRadius: 7,
                    offset: const Offset(0, 3),
                  ),
                ],
              ),
              // Column for payment info
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  SizedBox(
                    height: ScreenUtil.blockSizeVertical(context) * 2,
                  ),
                  if (rollNumber != null)
                    Container(
                      width: MediaQuery.of(context).size.width * 0.9,
                      padding: const EdgeInsets.all(8),
                      decoration: BoxDecoration(
                        color: AppColors.secondaryColor,
                        border: Border.all(
                          color: AppColors.greyColor,
                          width: 2,
                        ),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Text(
                        '$rollNumber',
                        style: AppTypography.mainHeading,
                        textAlign: TextAlign.center,
                      ),
                    ),
                  PaymentEntry(controller: paymentController),
                  PrimaryButton(
                    color: backgroundColor,
                    text: buttonText,
                    onPressed: onButtonPressed,
                  ),
                  SizedBox(
                    height: ScreenUtil.blockSizeVertical(context) * 2,
                  ),
                ],
              ),
            ),
          ),
          // Header component with passed title
          Header(title: title),
        ],
      ),
    );
  }
}

import 'package:cardpay/src/config/screen_utills/box_shadow.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
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

    return Scaffold(
      backgroundColor: backgroundColor,
      body: Stack(
        children: [
          Align(
            alignment: Alignment.bottomCenter,
            child: Container(
              decoration: CustomBoxDecoration.getDecoration(),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  HeightBox(slab: 3),
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
                  HeightBox(slab: 3),
                  PrimaryButton(
                    color: backgroundColor,
                    text: buttonText,
                    onPressed: onButtonPressed,
                  ),
                  HeightBox(slab: 5)
                ],
              ),
            ),
          ),
          Header(title: title),
        ],
      ),
    );
  }
}

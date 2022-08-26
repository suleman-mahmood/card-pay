import 'package:cardpay/theme/colors.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:lottie/lottie.dart';

class ScreenTransitionLoaderCustomWidget extends StatelessWidget {
  const ScreenTransitionLoaderCustomWidget({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        backgroundColor: AppColors().secondaryColor,
        body: Center(
          child: Lottie.asset('assets/animations/loading-payment.json'),
        ),
      ),
    );
  }
}

import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/headings/main_heading.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:cardpay/src/presentation/widgets/text_inputs/otp_input_field.dart';
import 'package:cardpay/src/utils/constants/signUp_string.dart';
import 'package:flutter/material.dart';
import 'package:cardpay/src/presentation/widgets/boxes/width_between.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

class BottomSheetOTP extends HookWidget {
  final String deviceCheckHeading;
  final String otpDeviceText;
  final PageRouteInfo route;

  const BottomSheetOTP({
    required this.deviceCheckHeading,
    required this.otpDeviceText,
    required this.route,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(24),
      child: Container(
        color: AppColors.secondaryColor,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            MainHeading(
              accountTitle: deviceCheckHeading,
              accountDescription: otpDeviceText,
            ),
            const HeightBox(slab: 2),
            OTPInput(
              digitCount: 4,
              onCompleted: (String otp) {},
            ),
            const HeightBox(slab: 2),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Text(
                  AppStrings.noOtp,
                  style: AppTypography.bodyText,
                ),
                const WidthBetween(),
                GestureDetector(
                  onTap: () {
                    context.router.push(const LoginRoute());
                  },
                  child: const Text(
                    AppStrings.resendCode,
                    style: AppTypography.bodyTextBold,
                  ),
                ),
              ],
            ),
            const HeightBox(slab: 4),
            PrimaryButton(
              text: AppStrings.verify,
              onPressed: () {
                context.router.push(route);
              },
            ),
            const HeightBox(slab: 4),
          ],
        ),
      ),
    );
  }
}

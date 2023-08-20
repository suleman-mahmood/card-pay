import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/boxes/all_padding.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/headings/main_heading.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:cardpay/src/presentation/widgets/text_inputs/otp_input_field.dart';
import 'package:cardpay/src/utils/constants/signUp_string.dart';
import 'package:flutter/material.dart';
import 'package:cardpay/src/presentation/widgets/boxes/width_between.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

class BottomSheetOTP extends HookWidget {
  final String deviceCheckHeading;
  final String otpDeviceText;
  final void Function() onAction;
  final ValueChanged<String> onChanged;

  const BottomSheetOTP({
    super.key,
    required this.deviceCheckHeading,
    required this.otpDeviceText,
    required this.onAction,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return PaddingAll(
      slab: 3,
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
              onCompleted: (otp) => {onChanged(otp)},
            ),
            const HeightBox(slab: 2),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  AppStrings.noOtp,
                  style: AppTypography.bodyText,
                ),
                const WidthBetween(),
                GestureDetector(
                  onTap: () {
                    context.router.push(const LoginRoute());
                  },
                  child: Text(
                    AppStrings.resendCode,
                    style: AppTypography.bodyTextBold,
                  ),
                ),
              ],
            ),
            const HeightBox(slab: 4),
            BlocBuilder<UserCubit, UserState>(builder: (_, state) {
              switch (state.runtimeType) {
                case UserFailed:
                  return Column(
                    children: [
                      Text(
                        state.error!.response!.data['message'],
                        style: TextStyle(color: Colors.red),
                      ),
                      const HeightBox(slab: 4),
                    ],
                  );
                default:
                  return const SizedBox.shrink();
              }
            }),
            PrimaryButton(
              text: AppStrings.verify,
              onPressed: onAction,
            ),
            const HeightBox(slab: 5),
          ],
        ),
      ),
    );
  }
}

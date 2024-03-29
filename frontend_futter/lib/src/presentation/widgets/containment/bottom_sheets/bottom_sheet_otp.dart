import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/cubits/remote/closed_loop_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/signup_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/all_padding.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/headings/main_heading.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:cardpay/src/presentation/widgets/text_inputs/otp_input_field.dart';
import 'package:cardpay/src/utils/constants/auth_strings.dart';
import 'package:flutter/material.dart';
import 'package:cardpay/src/presentation/widgets/boxes/width_between.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

class BottomSheetOTP extends HookWidget {
  final String deviceCheckHeading;
  final String otpDeviceText;
  final void Function(String) onAction;

  const BottomSheetOTP({
    super.key,
    required this.deviceCheckHeading,
    required this.otpDeviceText,
    required this.onAction,
  });

  @override
  Widget build(BuildContext context) {
    final otp = useState<String>('');

    return Padding(
      padding: EdgeInsets.only(
        bottom: MediaQuery.of(context).viewInsets.bottom,
      ),
      child: PaddingAll(
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
                onCompleted: (o) => otp.value = o,
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
                    onTap: () {},
                    child: Text(
                      AppStrings.resendCode,
                      style: AppTypography.bodyTextBold,
                    ),
                  ),
                ],
              ),
              const HeightBox(slab: 4),
              BlocBuilder<SignupCubit, SignupState>(builder: (_, state) {
                switch (state.runtimeType) {
                  case SignupFailed:
                    return Column(
                      children: [
                        Text(
                          state.errorMessage,
                          style: const TextStyle(color: Colors.red),
                          textAlign: TextAlign.center,
                        ),
                        const HeightBox(slab: 4),
                      ],
                    );
                  default:
                    return const SizedBox.shrink();
                }
              }),
              BlocBuilder<ClosedLoopCubit, ClosedLoopState>(
                  builder: (_, state) {
                switch (state.runtimeType) {
                  case ClosedLoopFailed:
                    return Column(
                      children: [
                        Text(
                          state.errorMessage,
                          style: const TextStyle(color: Colors.red),
                          textAlign: TextAlign.center,
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
                onPressed: () => onAction(otp.value),
              ),
              const HeightBox(slab: 5),
            ],
          ),
        ),
      ),
    );
  }
}

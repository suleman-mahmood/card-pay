import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/screen_utills/screen_util.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/containment/bottom_sheet_otp.dart';
import 'package:cardpay/src/presentation/widgets/headings/main_heading.dart';
import 'package:cardpay/src/presentation/widgets/layout/auth_layout.dart';
import 'package:cardpay/src/presentation/widgets/selections/organization_drop_down.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:cardpay/src/presentation/widgets/communication/progress_bar/progress_bar.dart';
import 'package:cardpay/src/presentation/widgets/text_inputs/input_field.dart';
import 'package:cardpay/src/utils/constants/signUp_string.dart';

@RoutePage()
class RegisterView extends HookWidget {
  const RegisterView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final progress = useState<double>(1);
    final showRollNumberField = useState<bool>(false);

    Widget OTPBottomSheet() {
      return Container(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const MainHeading(
              accountTitle: AppStrings.check,
              accountDescription: AppStrings.otpText,
            ),
            const HeightBox(slab: 1),
            OTPInput(
              digitCount: 4,
              onCompleted: (String otp) {},
            ),
            const HeightBox(slab: 1),
            Text(
              AppStrings.noOtp,
              style: AppTypography.headingFont.copyWith(
                color: AppColors.primaryColor,
                fontSize: ScreenUtil.textMultiplier(context) * 2,
              ),
            ),
            const HeightBox(slab: 1),
            PrimaryButton(
              text: AppStrings.verify,
              onPressed: () {
                context.router.push(const AuthRoute());
              },
            ),
          ],
        ),
      );
    }

    void _showOTPBottomSheet() {
      showModalBottomSheet(
        context: context,
        isScrollControlled: true,
        builder: (BuildContext context) {
          return Padding(
            padding: MediaQuery.of(context).viewInsets,
            child: SingleChildScrollView(
              child: OTPBottomSheet(),
            ),
          );
        },
      );
    }

    return AuthLayout(
      child: Column(
        children: [
          const HeightBox(slab: 3),
          CustomProgressBar(progress: progress.value),
          const HeightBox(slab: 1),
          const MainHeading(
            accountTitle: AppStrings.register,
            accountDescription: AppStrings.sign,
          ),
          const HeightBox(slab: 1),
          DropDown(
            onChanged: (String? value) {
              showRollNumberField.value = value != null;
            },
          ),
          const HeightBox(slab: 1),
          const CustomInputField(
            label: AppStrings.rollNumber,
            hint: AppStrings.enterRollNumber,
          ),
          const HeightBox(slab: 1),
          PrimaryButton(
            text: AppStrings.create,
            onPressed: () => _showOTPBottomSheet(),
          ),
        ],
      ),
    );
  }
}

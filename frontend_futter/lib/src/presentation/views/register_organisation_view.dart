import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/screen_utills/screen_util.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';
import 'package:frontend_futter/src/config/router/app_router.dart';
import 'package:frontend_futter/src/presentation/widgets/containment/bottom_sheet_otp.dart';
import 'package:frontend_futter/src/presentation/widgets/headings/main_heading.dart';
import 'package:frontend_futter/src/presentation/widgets/layout/auth_layout.dart';
import 'package:frontend_futter/src/presentation/widgets/selections/organization_drop_down.dart';
import 'package:frontend_futter/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:frontend_futter/src/presentation/widgets/communication/progress_bar/progress_bar.dart';
import 'package:frontend_futter/src/presentation/widgets/text_inputs/input_field.dart';
import 'package:frontend_futter/src/utils/constants/signUp_string.dart';

@RoutePage()
class RegisterView extends HookWidget {
  const RegisterView({Key? key}) : super(key: key);

  void _showOTPBottomSheet(BuildContext context) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      builder: (BuildContext context) {
        return Padding(
          padding: MediaQuery.of(context).viewInsets,
          child: SingleChildScrollView(
            child: OTPBottomSheet(context),
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final progress = useState<double>(1);
    final showRollNumberField = useState<bool>(false);

    return AuthLayout(
      child: Column(
        children: [
          SizedBox(
              height: ScreenUtil.heightMultiplier(context) *
                  1), // Leverage ScreenUtil
          CustomProgressBar(progress: progress.value),
          SizedBox(
              height: ScreenUtil.heightMultiplier(context) *
                  1), // Leverage ScreenUtil
          const MainHeading(
            accountTitle: AppStrings.register,
            accountDescription: AppStrings.sign,
          ),
          SizedBox(
              height: ScreenUtil.heightMultiplier(context) *
                  0.5), // Leverage ScreenUtil
          DropDown(
            onChanged: (String? value) {
              showRollNumberField.value = value != null;
            },
          ),
          if (showRollNumberField.value)
            SizedBox(
                height: ScreenUtil.heightMultiplier(context) *
                    0.5), // Leverage ScreenUtil
          const CustomInputField(
            label: AppStrings.rollNumber,
            hint: AppStrings.enterRollNumber,
          ),
          SizedBox(
              height: ScreenUtil.heightMultiplier(context) *
                  1), // Leverage ScreenUtil
          PrimaryButton(
            text: AppStrings.create,
            onPressed: () => _showOTPBottomSheet(context),
          ),
        ],
      ),
    );
  }

  Widget OTPBottomSheet(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(20),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const MainHeading(
            accountTitle: AppStrings.check,
            accountDescription: AppStrings.otpText,
          ),
          SizedBox(
              height: ScreenUtil.heightMultiplier(context) *
                  1), // Leverage ScreenUtil
          OTPInput(
            digitCount: 4,
            onCompleted: (String otp) {},
          ),
          SizedBox(
              height: ScreenUtil.heightMultiplier(context) *
                  1), // Leverage ScreenUtil
          Text(
            AppStrings.noOtp,
            style: AppTypography.headingFont.copyWith(
              color: AppColors.primaryColor,
              fontSize:
                  ScreenUtil.textMultiplier(context) * 2, // Leverage ScreenUtil
            ),
          ),
          SizedBox(
              height: ScreenUtil.heightMultiplier(context) *
                  0.2), // Leverage ScreenUtil
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
}

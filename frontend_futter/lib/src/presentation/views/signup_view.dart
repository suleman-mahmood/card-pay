import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:auto_route/auto_route.dart';
import 'package:frontend_futter/src/config/router/app_router.dart';
import 'package:frontend_futter/src/config/screen_utills/screen_util.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';
import 'package:frontend_futter/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:frontend_futter/src/presentation/widgets/communication/progress_bar/progress_bar.dart';
import 'package:frontend_futter/src/presentation/widgets/containment/bottom_sheet_otp.dart';
import 'package:frontend_futter/src/presentation/widgets/selections/check_box.dart';
import 'package:frontend_futter/src/presentation/widgets/selections/phonenumber_drop_down.dart';
import 'package:frontend_futter/src/presentation/widgets/layout/auth_layout.dart';
import 'package:frontend_futter/src/presentation/widgets/headings/main_heading.dart';
import 'package:frontend_futter/src/presentation/widgets/text_inputs/input_field.dart';
import 'package:frontend_futter/src/utils/constants/signUp_string.dart';

@RoutePage()
class SignupView extends HookWidget {
  const SignupView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final acceptPrivacyTerms = useState<bool>(false);
    final phoneNumberController = useTextEditingController();
    final dropdownValue =
        useState<String>(AppStrings.defaultCountryCode); // from strings.dart
    void _showOTPBottomSheet() {
      showModalBottomSheet(
        context: context,
        isScrollControlled: true,
        builder: (BuildContext context) {
          return Padding(
            padding: MediaQuery.of(context).viewInsets,
            child: SingleChildScrollView(
              child: OTPBottomSheet(context), // extracted widget
            ),
          );
        },
      );
    }

    return AuthLayout(
      child: Column(
        children: [
          _buildSizedBox(ScreenUtil.screenHeight(context), 0.01),
          CustomProgressBar(
            progress: 0.5,
          ),
          _buildSizedBox(ScreenUtil.screenHeight(context), 0.01),

          MainHeading(
            accountTitle: AppStrings.createAccount, // from strings.dart
            accountDescription:
                AppStrings.createAccountDesc, // from strings.dart
          ),
          _buildSizedBox(ScreenUtil.screenHeight(context), 0.005),
          _buildCustomInputField(AppStrings.username,
              AppStrings.enterUsername), // from strings.dart
          _buildSizedBox(ScreenUtil.screenHeight(context), 0.01),

          _buildCustomInputField(AppStrings.email, AppStrings.enterEmail,
              obscureText: false), // from strings.dart
          _buildSizedBox(ScreenUtil.screenHeight(context), 0.01),

          _buildCustomInputField(AppStrings.password, AppStrings.enterPassword,
              obscureText: true), // from strings.dart
          _buildSizedBox(ScreenUtil.screenHeight(context), 0.01),

          _buildCustomInputField(
              AppStrings.confirmPassword, AppStrings.reEnterPassword,
              obscureText: true), // from strings.dart
          _buildSizedBox(ScreenUtil.screenHeight(context), 0.015),
          PhoneNumberInput(
            controller: phoneNumberController,
            dropdownItems: AppStrings.phoneCountryCodes, // from strings.dart
            dropdownValue: dropdownValue.value,
            onChanged: (String? newValue) {
              if (newValue != null) {
                dropdownValue.value = newValue;
              }
            },
          ),
          _buildSizedBox(ScreenUtil.screenHeight(context), 0.02),
          CheckBox(
            onChanged: (bool value) {
              acceptPrivacyTerms.value = value;
            },
            text: AppStrings.acceptPrivacyTerms, // from strings.dart
          ),
          _buildSizedBox(ScreenUtil.screenHeight(context), 0.01),

          CustomButton(
            text: AppStrings.createAccount, // from strings.dart
            onPressed: _showOTPBottomSheet,
          ),
          _buildSizedBox(ScreenUtil.screenHeight(context), 0.02),
          _buildLoginText(context),
        ],
      ),
    );
  }

  // extracted widgets
  Widget _buildSizedBox(double screenHeight, double multiplier) {
    return SizedBox(height: screenHeight * multiplier);
  }

  Widget _buildCustomInputField(String label, String hint,
      {bool obscureText = false}) {
    return CustomInputField(
      label: label,
      hint: hint,
      obscureText: obscureText,
    );
  }

  Widget OTPBottomSheet(BuildContext context) {
    return Container(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          MainHeading(
            accountTitle: AppStrings.check,
            accountDescription: AppStrings.otpText,
          ),
          SizedBox(height: 10),
          OTPInput(
            digitCount: 4,
            onCompleted: (String otp) {},
          ),
          SizedBox(height: 10),
          Text(
            AppStrings.confirmCode,
            style: AppTypography.headingFont.copyWith(
              color: AppColors.primaryColor,
              fontSize: ScreenUtil.textMultiplier(context) * 2,
            ),
          ),
          SizedBox(height: 2),
          CustomButton(
            text: AppStrings.verify,
            onPressed: () {
              context.router.push(RegisterRoute());
            },
          ),
        ],
      ),
    );
  }

  Widget _buildLoginText(BuildContext context) {
    return GestureDetector(
      onTap: () {
        context.router.push(LoginRoute());
      },
      child: RichText(
        text: TextSpan(
          text: AppStrings.alreadyHaveAccount, // from strings.dart
          style: TextStyle(
            color: AppColors.blackColor,
          ),
          children: [
            TextSpan(
              text: AppStrings.logIn, // from strings.dart
              style: TextStyle(
                color: AppColors.primaryColor,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

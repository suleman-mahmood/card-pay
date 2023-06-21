import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:auto_route/auto_route.dart';
import 'package:frontend_futter/src/config/router/app_router.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';
import 'package:frontend_futter/src/presentation/Widgets/layout/auth_layout.dart';
import 'package:frontend_futter/src/presentation/Widgets/input_fields/input_field.dart';
import 'package:frontend_futter/src/presentation/Widgets/button/primary_button.dart';
import 'package:frontend_futter/src/presentation/Widgets/headings/main_heading.dart';
import 'package:frontend_futter/src/presentation/Widgets/check_box/check_box.dart';
import 'package:frontend_futter/src/presentation/Widgets/progress_bar/progress_bar.dart';
import 'package:frontend_futter/src/presentation/Widgets/bottom_sheet/bottom_sheet_otp.dart';
import 'package:frontend_futter/src/presentation/Widgets/drop_down/phone_input.dart';

@RoutePage()
class SignupView extends HookWidget {
  const SignupView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final screenHeight = MediaQuery.of(context).size.height;
    final acceptPrivacyTerms = useState<bool>(false);

    final phoneNumberController = useTextEditingController();
    final dropdownValue = useState<String>("+92");

    void _showOTPBottomSheet() {
      showModalBottomSheet(
        context: context,
        isScrollControlled: true,
        builder: (BuildContext context) {
          return Padding(
            padding: MediaQuery.of(context).viewInsets,
            child: SingleChildScrollView(
              child: Container(
                padding: EdgeInsets.all(20),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    MainHeading(
                      accountTitle: 'Please check your mobile',
                      accountDescription:
                          'We send an otp at your number +923*****786',
                    ),
                    SizedBox(height: screenHeight * 0.01),
                    OTPInput(
                      digitCount: 4,
                      onCompleted: (String otp) {
                        // Handle completed OTP here
                      },
                    ),
                    SizedBox(height: screenHeight * 0.01),
                    Text(
                      'Didn\'t receive the code? Resend',
                      style: AppTypography.headingFont.copyWith(
                        color: AppColors.primaryColor,
                        fontSize: 16,
                      ),
                    ),
                    SizedBox(height: screenHeight * 0.002),
                    CustomButton(
                      text: 'Verify',
                      onPressed: () {
                        context.router.push(RegisterRoute());
                      },
                    ),
                  ],
                ),
              ),
            ),
          );
        },
      );
    }

    return AuthLayout(
      child: Column(
        children: [
          SizedBox(height: screenHeight * 0.01),
          CustomProgressBar(
            progress: 0.5,
          ),
          SizedBox(height: screenHeight * 0.01),
          MainHeading(
            accountTitle: 'Create Your Account',
            accountDescription:
                'Let\'s get you started. Help us create your account',
          ),
          SizedBox(height: screenHeight * 0.005),
          CustomInputField(
            label: 'Username',
            hint: 'Enter your username',
          ),
          SizedBox(height: screenHeight * 0.01),
          CustomInputField(
            label: 'Email',
            hint: 'Enter your email',
          ),
          SizedBox(height: screenHeight * 0.01),
          CustomInputField(
            label: 'Password',
            hint: 'Enter your password',
            obscureText: true,
          ),
          SizedBox(height: screenHeight * 0.01),
          CustomInputField(
            label: 'Password',
            hint: 'Please re-enter your password',
            obscureText: true,
          ),
          SizedBox(height: screenHeight * 0.015),
          PhoneNumberInput(
            controller: phoneNumberController,
            dropdownItems: ['+92', '+91', '+7'],
            dropdownValue: dropdownValue.value,
            onChanged: (String? newValue) {
              if (newValue != null) {
                dropdownValue.value = newValue;
              }
            },
          ),
          SizedBox(height: screenHeight * 0.02),
          CheckBox(
            onChanged: (bool value) {
              acceptPrivacyTerms.value = value;
            },
            text: 'I accept the privacy terms and conditions. ',
          ),
          SizedBox(height: screenHeight * 0.01),
          CustomButton(
            text: 'Create Account',
            onPressed: _showOTPBottomSheet,
          ),
          SizedBox(height: screenHeight * 0.02),
          GestureDetector(
            onTap: () {
              context.router.push(LoginRoute());
            },
            child: RichText(
              text: TextSpan(
                text: 'Already have an account? ',
                style: TextStyle(
                  color: AppColors.blackColor,
                ),
                children: [
                  TextSpan(
                    text: 'Log In',
                    style: TextStyle(
                      color: AppColors.primaryColor,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

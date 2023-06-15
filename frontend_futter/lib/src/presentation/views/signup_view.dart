import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/presentation/Widgets/input_fields/input_field.dart';
import 'package:frontend_futter/src/presentation/Widgets/button/primary_button.dart';
import 'package:frontend_futter/src/presentation/Widgets/headings/main_heading.dart';
import 'package:frontend_futter/src/presentation/Widgets/check_box/check_box.dart';
import 'package:frontend_futter/src/presentation/Widgets/progress_bar/progress_bar.dart';
import 'package:frontend_futter/src/presentation/Widgets/bottom_sheet/bottom_sheet.dart';
import 'package:frontend_futter/src/config/router/app_router.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';
import 'package:auto_route/auto_route.dart';
import 'package:frontend_futter/src/presentation/Widgets/layout/common_app_layout.dart';

@RoutePage()
class SignupView extends HookWidget {
  const SignupView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final acceptPrivacyTerms = useState<bool>(false);

    void _showOTPBottomSheet() {
      showModalBottomSheet(
        context: context,
        builder: (BuildContext context) {
          return SingleChildScrollView(
            // Make the content scrollable
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
                  SizedBox(height: 10),
                  OTPInput(
                    digitCount: 4,
                    onCompleted: (String otp) {
                      // Handle completed OTP here
                    },
                  ),
                  SizedBox(height: 10),
                  Text(
                    'Didn\'t receive the code? Resend',
                    style: AppColors().headingFont.copyWith(
                          fontSize: 16,
                          color: AppColors().primaryColor,
                        ),
                  ),
                  SizedBox(height: 2),
                  CustomButton(
                    text: 'Verify',
                    onPressed: () {
                      context.router.push(RegisterRoute());
                    },
                  ),
                ],
              ),
            ),
          );
        },
      );
    }

    return AppLayout(
      child: Column(
        children: [
          SizedBox(height: 10),
          CustomProgressBar(
            progress: 0.5,
          ), // Use the custom progress bar widget here

          SizedBox(height: 10),
          MainHeading(
            accountTitle: 'Create Your Account',
            accountDescription:
                'Let\'s get you started. Help us create your account',
          ),
          SizedBox(height: 5),
          CustomInputField(
            label: 'Username',
            hint: 'Enter your username',
          ),
          SizedBox(height: 10),
          CustomInputField(
            label: 'Email',
            hint: 'Enter your email',
          ),
          SizedBox(height: 10),
          CustomInputField(
            label: 'Password',
            hint: 'Enter your password',
            obscureText: true,
          ),
          SizedBox(height: 10),
          CustomInputField(
            label: 'Password',
            hint: 'Please re-enter your password',
            obscureText: true,
          ),
          SizedBox(height: 10),
          CustomInputField(
            label: "Phone",
            hint: "Please Enter you phone  number",
            dropdownItems: ['+92', ' 2', ' 3'],
            obscureText: false, // Optional
            // validator: (value) {
            //   // Optional
            //   if (value == null || value.isEmpty) {
            //     return 'Please enter some text';
            //   }
            // return null;
            // },
          ),

          SizedBox(height: 15),
          CheckBox(
            onChanged: (bool value) {
              acceptPrivacyTerms.value = value; // Assign value to the hook
            },
            text:
                'I accept the privacy terms and conditions. By creating an account, you agree to our terms and conditions.',
          ),
          CustomButton(
            text: 'Create Account',
            onPressed: _showOTPBottomSheet,
          ),
          SizedBox(height: 5),
          GestureDetector(
            onTap: () {
              // Handle "Already have an account" press
            },
            child: Text(
              'Already have an account?',
              style: AppColors().headingFont.copyWith(
                    fontSize: 16,
                    color: AppColors().primaryColor,
                  ),
            ),
          ),
        ],
      ),
    );
  }
}

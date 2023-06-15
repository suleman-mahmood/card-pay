import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/presentation/Widgets/headings/main_heading.dart';
import 'package:frontend_futter/src/presentation/Widgets/input_fields/input_field.dart';
import 'package:frontend_futter/src/presentation/Widgets/progress_bar/progress_bar.dart';
import 'package:frontend_futter/src/presentation/Widgets/button/primary_button.dart';
import 'package:frontend_futter/src/presentation/Widgets/bottom_sheet/bottom_sheet.dart';
import 'package:frontend_futter/src/config/router/app_router.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';
import 'package:frontend_futter/src/presentation/Widgets/layout/common_app_layout.dart';

@RoutePage()
class RegisterView extends HookWidget {
  const RegisterView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final progress = useState<double>(1);
    final showRollNumberField = useState<bool>(false);
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
                  Text('Didn\'t receive the code? Resend',
                      style: AppColors().headingFont.copyWith(
                            color: AppColors().primaryColor,
                            fontSize: 16,
                          )),
                  SizedBox(height: 2),
                  CustomButton(
                    text: 'Verify',
                    onPressed: () {
                      context.router.push(SplashRoute());
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
          CustomProgressBar(progress: progress.value),
          SizedBox(height: 10),
          MainHeading(
            accountTitle: 'Register your Organization',
            accountDescription:
                'Sign in to your organization account to get started',
          ),
          SizedBox(height: 5),
          CustomInputField(
            label: "Organization",
            hint: "Enter your organization name",
            dropdownItems: ['LUMS', ' MIT', ' IBA'],
            dropdownAlignment: Alignment.centerRight,
            obscureText: false,
            onChanged: (value) {
              showRollNumberField.value = value != null;
            },
          ),
          if (showRollNumberField.value)
            CustomInputField(
              label: "Roll Number",
              hint: "Enter your roll number",
            ),
          CustomButton(
            text: 'Create Account',
            onPressed:
                _showOTPBottomSheet, // Call the function instead of assigning it
          ),
        ],
      ),
    );
  }
}

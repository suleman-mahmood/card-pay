import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/presentation/Widgets/headings/main_heading.dart';
import 'package:frontend_futter/src/presentation/Widgets/input_fields/input_field.dart';
import 'package:frontend_futter/src/presentation/Widgets/progress_bar/progress_bar.dart';
import 'package:frontend_futter/src/presentation/Widgets/button/primary_button.dart';
import 'package:frontend_futter/src/presentation/Widgets/bottom_sheet/bottom_sheet_otp.dart';
import 'package:frontend_futter/src/config/router/app_router.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';
import 'package:frontend_futter/src/presentation/Widgets/layout/auth_layout.dart';
import 'package:frontend_futter/src/presentation/Widgets/drop_down/drop_down_org.dart';

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
        isScrollControlled: true, // add this line
        builder: (BuildContext context) {
          return Padding(
            padding: MediaQuery.of(context).viewInsets, // Compute padding
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
                    SizedBox(height: 10),
                    OTPInput(
                      digitCount: 4,
                      onCompleted: (String otp) {
                        // Handle completed OTP here
                      },
                    ),
                    SizedBox(height: 10),
                    Text('Didn\'t receive the code? Resend',
                        style: AppTypography.headingFont.copyWith(
                          color: AppColors.primaryColor,
                          fontSize: 16,
                        )),
                    SizedBox(height: 2),
                    CustomButton(
                      text: 'Verify',
                      onPressed: () {
                        context.router.push(AuthRoute());
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
          CustomProgressBar(progress: progress.value),
          SizedBox(height: 10),
          MainHeading(
            accountTitle: 'Register your Organization',
            accountDescription: 'Sign in to your organization to get started',
          ),
          SizedBox(height: 5),
          Container(
            width: 420,
            height: 50, // Set the desired width
            child: DropDown(
              onChanged: (String? value) {
                Align:
                Alignment.center;
                showRollNumberField.value = value != null;
              },
            ),
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

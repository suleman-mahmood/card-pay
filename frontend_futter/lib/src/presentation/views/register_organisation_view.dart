import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:auto_route/auto_route.dart';
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
    final screenHeight = MediaQuery.of(context).size.height;
    final screenWidth = MediaQuery.of(context).size.width;

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
                      accountTitle: 'Please check your Email',
                      accountDescription:
                          'We send an otp at tal******@youremail.com',
                    ),
                    SizedBox(height: screenHeight * 0.01),
                    OTPInput(
                      digitCount: 4,
                      onCompleted: (String otp) {},
                    ),
                    SizedBox(height: screenHeight * 0.01),
                    Text(
                      'Didn\'t receive the code? Resend',
                      style: AppTypography.headingFont.copyWith(
                        color: AppColors.primaryColor,
                        fontSize: screenWidth * 0.04,
                      ),
                    ),
                    SizedBox(height: screenHeight * 0.002),
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
          SizedBox(height: screenHeight * 0.01),
          CustomProgressBar(progress: progress.value),
          SizedBox(height: screenHeight * 0.01),
          MainHeading(
            accountTitle: 'Register your Organization',
            accountDescription: 'Sign in to your organization to get started',
          ),
          SizedBox(height: screenHeight * 0.005),
          DropDown(
            onChanged: (String? value) {
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
            onPressed: _showOTPBottomSheet,
          ),
        ],
      ),
    );
  }
}

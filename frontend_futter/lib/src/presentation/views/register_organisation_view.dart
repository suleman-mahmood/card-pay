import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/presentation/Widgets/headings/main_heading.dart';
import 'package:frontend_futter/src/presentation/Widgets/input_fields/input_field.dart';
import 'package:frontend_futter/src/presentation/Widgets/progress_bar/progress_bar.dart';
import 'package:frontend_futter/src/presentation/Widgets/button/primary_button.dart';
import 'package:frontend_futter/src/config/router/app_router.dart';
import 'package:frontend_futter/src/presentation/Widgets/layout/common_app_layout.dart';

@RoutePage()
class RegisterView extends HookWidget {
  const RegisterView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final progress = useState<double>(1);
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
          Center(
            child: CustomInputField(
              label: "Organization",
              dropdownItems: ['LUMS', ' MIT', ' IBA'],
              obscureText: false, // Optional
              // validator: (value) {
              //   // Optional
              //   if (value == null || value.isEmpty) {
              //     return 'Please enter some text';
              //   }
              // return null;
              // },
            ),
          ),
          CustomButton(
            text: 'Create Account',
            onPressed: () {
              context.router.replace(RegisterrollRoute());
            },
          ),
        ],
      ),
    );
  }
}

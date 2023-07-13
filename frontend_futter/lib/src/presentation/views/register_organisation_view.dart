import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
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

    void _showOTPBottomSheet() {
      showModalBottomSheet(
        context: context,
        builder: (BuildContext context) {
          return SingleChildScrollView(
            child: BottomSheetOTP(
              deviceCheckHeading: AppStrings.checkEmail,
              otpDeviceText: AppStrings.otpEmailText,
              route: const AuthRoute(),
            ),
          );
        },
      );
    }

    return AuthLayout(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const HeightBox(slab: 4),
          CustomProgressBar(progress: progress.value),
          const HeightBox(slab: 4),
          const MainHeading(
            accountTitle: AppStrings.register,
            accountDescription: AppStrings.sign,
          ),
          const HeightBox(slab: 4),
          DropDown(
            onChanged: (String? value) {
              showRollNumberField.value = value != null;
            },
          ),
          Visibility(
            visible: showRollNumberField.value,
            maintainSize: false,
            child: const HeightBox(slab: 2),
          ),
          Visibility(
            visible: showRollNumberField.value,
            maintainSize: false,
            child: const CustomInputField(
              label: AppStrings.rollNumber,
              hint: AppStrings.enterRollNumber,
            ),
          ),
          const HeightBox(slab: 4),
          Center(
            child: PrimaryButton(
              text: AppStrings.create,
              onPressed: () => _showOTPBottomSheet(),
            ),
          )
        ],
      ),
    );
  }
}

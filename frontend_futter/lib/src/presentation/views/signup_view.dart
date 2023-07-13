import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/boxes/width_between.dart';
import 'package:cardpay/src/presentation/widgets/communication/progress_bar/progress_bar.dart';
import 'package:cardpay/src/presentation/widgets/containment/bottom_sheet_otp.dart';
import 'package:cardpay/src/presentation/widgets/selections/check_box.dart';
import 'package:cardpay/src/presentation/widgets/selections/phonenumber_drop_down.dart';
import 'package:cardpay/src/presentation/widgets/layout/auth_layout.dart';
import 'package:cardpay/src/presentation/widgets/headings/main_heading.dart';
import 'package:cardpay/src/presentation/widgets/text_inputs/input_field.dart';
import 'package:cardpay/src/utils/constants/signUp_string.dart';

@RoutePage()
class SignupView extends HookWidget {
  const SignupView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final acceptPrivacyTerms = useState<bool>(false);
    final phoneNumberController = useTextEditingController();
    final dropdownValue = useState<String>(AppStrings.defaultCountryCode);
    final formKey =
        useMemoized(() => GlobalKey<FormState>()); // 1. create a key for form

    void onPhoneNumberChanged(String newValue) {
      dropdownValue.value = newValue;
    }

    Widget _buildCustomInputField(String label, String hint,
        {bool obscureText = false}) {
      return CustomInputField(
        label: label,
        hint: hint,
        obscureText: obscureText,
      );
    }

    void _showOTPBottomSheet() {
      showModalBottomSheet(
        context: context,
        builder: (BuildContext context) {
          return SingleChildScrollView(
            child: BottomSheetOTP(
              deviceCheckHeading: AppStrings.checkMobile,
              otpDeviceText: AppStrings.otpMobileText,
              route: const RegisterRoute(),
            ),
          );
        },
      );
    }

    Widget _buildLoginText() {
      return Row(
        mainAxisAlignment: MainAxisAlignment.start,
        children: [
          const Text(
            AppStrings.alreadyHaveAccount,
            style: AppTypography.bodyText,
          ),
          const WidthBetween(),
          GestureDetector(
            onTap: () {
              context.router.push(const LoginRoute());
            },
            child: const Text(
              AppStrings.logIn,
              style: AppTypography.linkText,
            ),
          ),
        ],
      );
    }

    return AuthLayout(
      child: Form(
        key: formKey,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const HeightBox(slab: 4),
            const CustomProgressBar(
              progress: 0.5,
            ),
            const HeightBox(slab: 4),
            const MainHeading(
              accountTitle: AppStrings.createAccount,
              accountDescription: AppStrings.createAccountDesc,
            ),
            const HeightBox(slab: 1),
            _buildLoginText(),
            const HeightBox(slab: 4),
            _buildCustomInputField(
                AppStrings.username, AppStrings.enterUsername),
            const HeightBox(slab: 1),
            _buildCustomInputField(
              AppStrings.email,
              AppStrings.enterEmail,
              obscureText: false,
            ),
            const HeightBox(slab: 1),
            _buildCustomInputField(
              AppStrings.password,
              AppStrings.enterPassword,
              obscureText: true,
            ),
            const HeightBox(slab: 1),
            _buildCustomInputField(
              AppStrings.confirmPassword,
              AppStrings.reEnterPassword,
              obscureText: true,
            ),
            const HeightBox(slab: 1),
            PhoneNumberInput(
              controller: phoneNumberController,
              dropdownItems: AppStrings.phoneCountryCodes,
              dropdownValue: dropdownValue.value,
              onChanged: onPhoneNumberChanged,
            ),
            const HeightBox(slab: 3),
            CheckBox(
              onChanged: (bool value) {
                acceptPrivacyTerms.value = value;
              },
              text: AppStrings.acceptPrivacyTerms,
            ),
            const HeightBox(slab: 3),
            Center(
              child: PrimaryButton(
                text: AppStrings.createAccount,
                onPressed: () {
                  if (formKey.currentState!.validate()) {
                    _showOTPBottomSheet();
                  }
                },
              ),
            ),
            const HeightBox(slab: 1),
          ],
        ),
      ),
    );
  }
}

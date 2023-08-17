import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/headings/main_heading.dart';
import 'package:cardpay/src/presentation/views/transaction_service/payment_dashboard_view.dart';
import 'package:cardpay/src/presentation/widgets/selections/phonenumber_drop_down.dart';
import 'package:cardpay/src/utils/constants/event_codes.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:local_auth/local_auth.dart';
import 'package:flutter/services.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:cardpay/src/presentation/widgets/layout/auth_layout.dart';
import 'package:cardpay/src/presentation/widgets/text_inputs/input_field.dart';
import 'package:cardpay/src/utils/constants/signUp_string.dart';
import 'package:cardpay/src/config/extensions/validation.dart';

@RoutePage()
class LoginView extends HookWidget {
  const LoginView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final phoneNumberController = useTextEditingController();
    final dropdownValue = useState<String>(AppStrings.defaultCountryCode);
    final formKey = useMemoized(() => GlobalKey<FormState>());

    final phoneNumber = useState<String>('3333462677');
    final password = useState<String>('abcd1234');

    final userCubit = BlocProvider.of<UserCubit>(context);

    void onPhoneNumberChanged(String newValue) {
      dropdownValue.value = newValue;
    }

    void handleLogin() async {
      // if (!formKey.currentState!.validate()) {
      //   return;
      // }

      await userCubit.login(phoneNumber.value, password.value);
    }

    Future<bool> authenticateWithBiometrics() async {
      print("Hello! We are triggering");
      final LocalAuthentication auth = LocalAuthentication();
      bool didAuthenticate = false;

      try {
        didAuthenticate = await auth.authenticate(
          localizedReason: 'Please authenticate to show account balance',
          options: const AuthenticationOptions(biometricOnly: true),
        );
      } on PlatformException catch (e) {
        print(e);
        return false;
      }

      // Handle after biometric authentication flow
      if (!didAuthenticate) {
        return false;
      }

      // Handle successful biometric authentication
      return true;
    }

    return AuthLayout(
      child: SingleChildScrollView(
        physics: const AlwaysScrollableScrollPhysics(),
        child: Form(
          key: formKey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              FutureBuilder(
                future: authenticateWithBiometrics(),
                builder: (context, snapshot) {
                  if (snapshot.connectionState == ConnectionState.done) {
                    if (snapshot.data == true) {
                      context.router.push(PaymentDashboardRoute());
                    }
                  }
                  return const SizedBox.shrink();
                },
              ),
              HeightBox(slab: 4),
              Align(
                alignment: Alignment.centerLeft,
                child: const MainHeading(
                  accountTitle: AppStrings.logIn,
                  accountDescription: AppStrings.logInDescription,
                ),
              ),
              HeightBox(slab: 4),
              PhoneNumberInput(
                controller: phoneNumberController,
                dropdownItems: AppStrings.phoneCountryCodes,
                dropdownValue: dropdownValue.value,
                onChanged: onPhoneNumberChanged,
                onPhoneNumberChanged: (v) => phoneNumber.value = v,
                validator: (fullNameValue) {
                  if (fullNameValue == null) {
                    return "Please enter your phone number";
                  }
                  if (!fullNameValue.isValidPhoneNumber) {
                    return "Invalid phone number";
                  }
                  return null;
                },
              ),
              HeightBox(slab: 2),
              CustomInputField(
                label: AppStrings.password,
                hint: AppStrings.enterPassword,
                obscureText: true,
                onChanged: (v) => password.value = v,
              ),
              HeightBox(slab: 1),
              // TODO: handle it later
              // Align(
              //   alignment: Alignment.centerRight,
              //   child: Text(AppStrings.forgot,
              //       style: AppTypography.subHeadingBold),
              // ),
              HeightBox(slab: 3),
              PrimaryButton(
                text: AppStrings.logIn,
                onPressed: handleLogin,
              ),
              BlocBuilder<UserCubit, UserState>(builder: (_, state) {
                switch (state.runtimeType) {
                  case UserSuccess:
                    if (state.eventCodes == EventCodes.USER_AUTHENTICATED) {
                      context.router.push(PaymentDashboardRoute());
                    }
                    return const SizedBox.shrink();
                  default:
                    return const SizedBox.shrink();
                }
              }),
            ],
          ),
        ),
      ),
    );
  }
}

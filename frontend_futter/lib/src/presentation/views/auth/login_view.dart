import 'package:cardpay/src/presentation/cubits/remote/login_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/headings/main_heading.dart';
import 'package:cardpay/src/presentation/widgets/selections/phonenumber_drop_down.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:cardpay/src/presentation/widgets/layout/auth_layout.dart';
import 'package:cardpay/src/presentation/widgets/text_inputs/input_field.dart';
import 'package:cardpay/src/utils/constants/auth_strings.dart';
import 'package:cardpay/src/config/extensions/validation.dart';

@RoutePage()
class LoginView extends HookWidget {
  const LoginView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final loginCubit = BlocProvider.of<LoginCubit>(context);

    final phoneNumberController = useTextEditingController();

    final formKey = useMemoized(() => GlobalKey<FormState>());
    final dropdownValue = useState<String>(AppStrings.defaultCountryCode);
    final phoneNumber = useState<String>('');
    final password = useState<String>('');

    void onPhoneNumberChanged(String newValue) {
      dropdownValue.value = newValue.trim();
    }

    void handleLogin() {
      if (!formKey.currentState!.validate()) {
        return;
      }

      loginCubit.login(phoneNumber.value, password.value);
    }

    return AuthLayout(
      child: SingleChildScrollView(
        physics: const AlwaysScrollableScrollPhysics(),
        child: Form(
          key: formKey,
          child: Column(
            children: [
              const HeightBox(slab: 6),
              const HeightBox(slab: 2),
              const Align(
                alignment: Alignment.centerLeft,
                child: MainHeading(
                  accountTitle: AppStrings.logIn,
                  accountDescription: AppStrings.logInDescription,
                ),
              ),
              const HeightBox(slab: 2),
              PhoneNumberInput(
                controller: phoneNumberController,
                dropdownItems: AppStrings.phoneCountryCodes,
                dropdownValue: dropdownValue.value,
                onChanged: onPhoneNumberChanged,
                onPhoneNumberChanged: (v) => phoneNumber.value = v,
                validator: (fullNameValue) {
                  if (fullNameValue == null) {
                    return AppStrings.nullPhoneNumber;
                  }
                  if (!fullNameValue.isValidPhoneNumber) {
                    return AppStrings.invalidPhone;
                  }
                  return null;
                },
              ),
              HeightBox(slab: 2),
              CustomInputField(
                label: AppStrings.password,
                hint: AppStrings.enterPassword,
                obscureText: true,
                onChanged: (v) => password.value = v.trim(),
              ),
              const HeightBox(slab: 1),
              // TODO: handle it later
              // Align(
              //   alignment: Alignment.centerRight,
              //   child: Text(AppStrings.forgot,
              //       style: AppTypography.subHeadingBold),
              // ),
              const HeightBox(slab: 3),
              PrimaryButton(
                text: AppStrings.logIn,
                onPressed: handleLogin,
              ),
              const HeightBox(slab: 2),
              BlocConsumer<LoginCubit, LoginState>(
                listener: (context, state) {
                  switch (state.runtimeType) {
                    case BiometricLoginSuccess:
                      loginCubit.login(
                        state.login.phoneNumber,
                        state.login.password,
                      );
                      break;
                  }
                },
                builder: (_, state) {
                  switch (state.runtimeType) {
                    case LoginFailed:
                      return Text(
                        state.errorMessage,
                        style: const TextStyle(color: Colors.red),
                        textAlign: TextAlign.center,
                      );
                    default:
                      return const SizedBox.shrink();
                  }
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}

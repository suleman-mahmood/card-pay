import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/headings/main_heading.dart';
import 'package:cardpay/src/presentation/widgets/selections/phonenumber_drop_down.dart';
import 'package:cardpay/src/utils/constants/event_codes.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
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

    useEffect(() {
      someFunction() async {
        await userCubit.loginWithBiometric();
      }

      someFunction();
      return () {
        phoneNumberController.dispose();
        userCubit.close();
      };
    }, []);
    return AuthLayout(
      child: SingleChildScrollView(
        physics: const AlwaysScrollableScrollPhysics(),
        child: Form(
          key: formKey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
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
              const HeightBox(slab: 2),
              BlocBuilder<UserCubit, UserState>(builder: (_, state) {
                switch (state.runtimeType) {
                  case UserSuccess:
                    if (state.eventCodes == EventCodes.USER_AUTHENTICATED) {
                      context.router.push(PaymentDashboardRoute());
                    } else if (state.eventCodes ==
                        EventCodes.USER_AUTHENTICATED_WITH_BIOMETRIC) {
                      userCubit.login(state.phoneNumber, state.password);
                    }
                    return const SizedBox.shrink();
                  case UserFailed:
                    return Text(
                      state.errorMessage,
                      style: const TextStyle(color: Colors.red),
                      textAlign: TextAlign.center,
                    );
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

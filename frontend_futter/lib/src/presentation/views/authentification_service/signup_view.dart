import 'dart:io';

import 'package:cardpay/src/config/screen_utills/box_shadow.dart';
import 'package:cardpay/src/presentation/cubits/remote/closed_loop_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/login_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/versions_cubit.dart';
import 'package:cardpay/src/presentation/widgets/communication/progress_bar/divder.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/utils/constants/event_codes.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/boxes/width_between.dart';
import 'package:cardpay/src/presentation/widgets/containment/bottom_sheet_otp.dart';
import 'package:cardpay/src/presentation/widgets/selections/check_box.dart';
import 'package:cardpay/src/presentation/widgets/selections/phonenumber_drop_down.dart';
import 'package:cardpay/src/presentation/widgets/layout/auth_layout.dart';
import 'package:cardpay/src/presentation/widgets/headings/main_heading.dart';
import 'package:cardpay/src/presentation/widgets/text_inputs/input_field.dart';
import 'package:cardpay/src/utils/constants/signUp_string.dart';
import 'package:cardpay/src/config/extensions/validation.dart';
import 'package:url_launcher/url_launcher.dart';

@RoutePage()
class SignupView extends HookWidget {
  const SignupView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final acceptPrivacyTerms = useState<bool>(false);
    final phoneNumberController = useTextEditingController();
    final dropdownValue = useState<String>(AppStrings.defaultCountryCode);
    final formKey = useMemoized(() => GlobalKey<FormState>());
    final personalEmail = useState<String>('');
    final phoneNumber = useState<String>('');
    final fullName = useState<String>('');
    final password = useState<String>('');
    final confirmPassword = useState<String>('');

    final userCubit = BlocProvider.of<UserCubit>(context);
    final loginCubit = BlocProvider.of<LoginCubit>(context);
    final closedLoopCubit = BlocProvider.of<ClosedLoopCubit>(context);

    void onPhoneNumberChanged(String newValue) {
      dropdownValue.value = newValue;
    }

    void _showOTPBottomSheet() {
      showModalBottomSheet(
        context: context,
        builder: (BuildContext context) {
          return SingleChildScrollView(
            child: Container(
              decoration: CustomBoxDecoration.getDecoration(),
              child: BottomSheetOTP(
                deviceCheckHeading: AppStrings.checkMobile,
                otpDeviceText: AppStrings.otpMobileText,
                onAction: (otp) => userCubit.verifyPhoneNumber(otp),
              ),
            ),
          );
        },
      );
    }

    Widget _buildLoginText() {
      return Row(
        mainAxisAlignment: MainAxisAlignment.start,
        children: [
          Text(
            AppStrings.alreadyHaveAccount,
            style: AppTypography.bodyText,
          ),
          const WidthBetween(),
          GestureDetector(
            onTap: () {
              context.router.push(const LoginRoute());
            },
            child: Text(
              AppStrings.logIn,
              style: AppTypography.linkText,
            ),
          ),
        ],
      );
    }

    void handleCreateAccount() async {
      if (!formKey.currentState!.validate()) {
        return;
      }

      if (!acceptPrivacyTerms.value) {
        userCubit.termsDenied();
        return;
      }

      await userCubit.createCustomer(
        personalEmail.value,
        phoneNumber.value,
        fullName.value,
        password.value,
      );
    }

    useEffect(() {
      return () {
        phoneNumberController.dispose();
        // userCubit.close();
      };
    }, []);

    void _showDialog(bool showMaybeLaterButton) {
      showDialog(
        context: context,
        barrierDismissible: false,
        builder: (BuildContext context) => AlertDialog(
          backgroundColor: Colors.white,
          title: const Text('Update your app'),
          content: Text(Platform.isIOS
              ? AppStrings.updateMessageIOS
              : AppStrings.updateMessageAndroid),
          actions: <Widget>[
            if (showMaybeLaterButton)
              TextButton(
                onPressed: () {
                  Navigator.pop(context, 'Cancel');
                },
                child: const Text('Maybe later'),
              ),
            TextButton(
              onPressed: () async {
                final url = Platform.isIOS
                    ? 'https://apps.apple.com/app/1644127078'
                    : 'https://play.google.com/store/apps/details?id=io.payment.cardpay';

                await launchUrl(Uri.parse(url));
              },
              child: const Text('Update Now'),
            ),
          ],
        ),
      );
    }

    return AuthLayout(
      child: SingleChildScrollView(
        child: Form(
          key: formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const HeightBox(slab: 5),
              // Half progress bar
              Row(
                children: [
                  Expanded(
                    flex: 2,
                    child: CustomDivider(
                      thickness: 3,
                      indent: 70,
                      color: AppColors.primaryColor,
                      endIndent: 5,
                    ),
                  ),
                  Expanded(
                    flex: 2,
                    child: CustomDivider(
                      thickness: 3,
                      indent: 5,
                      color: AppColors.lightGreyColor,
                      endIndent: 70,
                    ),
                  ),
                ],
              ),
              const HeightBox(slab: 2),
              const MainHeading(
                accountTitle: AppStrings.createAccount,
                accountDescription: AppStrings.createAccountDesc,
              ),
              const HeightBox(slab: 1),
              BlocConsumer<UserCubit, UserState>(
                listener: (_, state) {
                  switch (state.runtimeType) {
                    case UserSuccess:
                      if (state.eventCodes == EventCodes.OTP_SENT) {
                        // Login the user after a successful sign up
                        loginCubit.login(phoneNumber.value, password.value);

                        WidgetsBinding.instance.addPostFrameCallback((_) {
                          _showOTPBottomSheet();
                        });
                      } else if (state.eventCodes == EventCodes.USER_VERIFIED) {
                        context.router.push(const LoginRoute());
                      } else if (state.eventCodes == EventCodes.OTP_VERIFIED) {
                        closedLoopCubit.getAllClosedLoops();
                        context.router.push(const RegisterOrganizationRoute());
                      }
                      break;
                  }
                },
                builder: (_, state) {
                  switch (state.runtimeType) {
                    case UserSuccess:
                      if (state.eventCodes == EventCodes.OTP_INCORRECT) {
                        return const Text(
                          AppStrings.incorrectOtp,
                          style: TextStyle(color: Colors.red),
                        );
                      }
                      return const SizedBox.shrink();
                    default:
                      return const SizedBox.shrink();
                  }
                },
              ),
              _buildLoginText(),
              const HeightBox(slab: 4),
              CustomInputField(
                label: AppStrings.username,
                hint: AppStrings.enterUsername,
                obscureText: false,
                onChanged: (v) => fullName.value = v,
                validator: (fullNameValue) {
                  if (fullNameValue == null) {
                    return AppStrings.nullName;
                  }
                  if (!fullNameValue.isValidFullName) {
                    return AppStrings.invalidName;
                  }
                  return null;
                },
              ),
              const HeightBox(slab: 1),
              CustomInputField(
                label: AppStrings.email,
                hint: AppStrings.enterEmail,
                obscureText: false,
                onChanged: (v) => personalEmail.value = v,
                validator: (EmailValue) {
                  if (EmailValue == null) {
                    return AppStrings.nullEmail;
                  }
                  if (!EmailValue.isValidEmail) {
                    return AppStrings.invalidEmail;
                  }
                  return null;
                },
              ),
              const HeightBox(slab: 1),
              CustomInputField(
                label: AppStrings.password,
                hint: AppStrings.enterPassword,
                obscureText: true,
                onChanged: (v) => password.value = v,
                validator: (passwordValue) {
                  if (passwordValue == null) {
                    return AppStrings.nullPassword;
                  }
                  if (!passwordValue.isValidPassword) {
                    return AppStrings.invalidPassword;
                  }
                  return null;
                },
              ),
              const HeightBox(slab: 1),
              CustomInputField(
                label: AppStrings.confirmPassword,
                hint: AppStrings.reEnterPassword,
                obscureText: true,
                onChanged: (v) => confirmPassword.value = v,
                validator: (confirmPasswordValue) {
                  if (confirmPasswordValue == null) {
                    return AppStrings.nullConfirmPassword;
                  }
                  if (!confirmPasswordValue.isValidPassword) {
                    return AppStrings.invalidConfirmPassword;
                  }
                  if (confirmPasswordValue != password.value) {
                    return AppStrings.wrongPassword;
                  }
                  return null;
                },
              ),
              const HeightBox(slab: 1),
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
              const HeightBox(slab: 3),
              CheckBox(
                onChanged: (bool value) {
                  acceptPrivacyTerms.value = value;
                },
                text: AppStrings.acceptPrivacyTerms,
                onTap: () => launchUrl(
                  Uri.parse('https://pages.flycricket.io/cardpay/privacy.html'),
                ),
              ),
              const HeightBox(slab: 3),
              BlocBuilder<UserCubit, UserState>(builder: (_, state) {
                switch (state.runtimeType) {
                  case UserSuccess:
                    if (state.eventCodes == EventCodes.TERMS_DENIED) {
                      return Column(
                        children: [
                          Text(
                            state.message,
                            style: TextStyle(color: Colors.red),
                          ),
                          const HeightBox(slab: 3),
                        ],
                      );
                    }
                    return const SizedBox.shrink();
                  default:
                    return const SizedBox.shrink();
                }
              }),
              Center(
                child: PrimaryButton(
                  text: AppStrings.createAccount,
                  onPressed: handleCreateAccount,
                ),
              ),
              const HeightBox(slab: 3),
              BlocListener<VersionsCubit, VersionsState>(
                listener: (_, state) {
                  switch (state.runtimeType) {
                    case VersionsSuccess:
                      if (state.forceUpdate) {
                        WidgetsBinding.instance.addPostFrameCallback((_) {
                          _showDialog(false);
                        });
                        return;
                      }
                      if (state.normalUpdate) {
                        WidgetsBinding.instance.addPostFrameCallback((_) {
                          _showDialog(true);
                        });
                        return;
                      }
                      break;
                  }
                },
                child: const SizedBox.shrink(),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

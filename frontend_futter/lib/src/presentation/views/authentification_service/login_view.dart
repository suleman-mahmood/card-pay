import 'dart:io';

import 'package:cardpay/src/presentation/cubits/remote/balance_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/checkpoints_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/closed_loop_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/login_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/recent_transactions_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/versions_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/headings/main_heading.dart';
import 'package:cardpay/src/presentation/widgets/selections/phonenumber_drop_down.dart';
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
import 'package:url_launcher/url_launcher.dart';

@RoutePage()
class LoginView extends HookWidget {
  const LoginView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final userCubit = BlocProvider.of<UserCubit>(context);
    final closedLoopCubit = BlocProvider.of<ClosedLoopCubit>(context);

    final phoneNumberController = useTextEditingController();
    final dropdownValue = useState<String>(AppStrings.defaultCountryCode);
    final formKey = useMemoized(() => GlobalKey<FormState>());

    final phoneNumber = useState<String>('');
    final password = useState<String>('');

    final loginCubit = BlocProvider.of<LoginCubit>(context);
    final balanceCubit = BlocProvider.of<BalanceCubit>(context);
    final recentTransactionsCubit =
        BlocProvider.of<RecentTransactionsCubit>(context);
    final checkPointsCubit = BlocProvider.of<CheckpointsCubit>(context);

    void navigateToNextScreen(CheckpointsState state) {
      PageRouteInfo route = SignupRoute();

      if (state.checkPoints.verifiedPhoneOtp &&
          state.checkPoints.verifiedClosedLoop &&
          state.checkPoints.pinSetup) {
        route = PaymentDashboardRoute();
      } else if (state.checkPoints.verifiedPhoneOtp &&
          state.checkPoints.verifiedClosedLoop &&
          state.checkPoints.pinSetup == false) {
        route = PinRoute();
      } else if (state.checkPoints.verifiedPhoneOtp &&
          state.checkPoints.verifiedClosedLoop == false) {
        route = RegisterOrganizationRoute();
      }

      WidgetsBinding.instance.addPostFrameCallback(
        (_) {
          context.router.push(route);
        },
      );
    }

    void onPhoneNumberChanged(String newValue) {
      dropdownValue.value = newValue;
    }

    void handleLogin() async {
      if (!formKey.currentState!.validate()) {
        return;
      }

      await loginCubit.login(phoneNumber.value, password.value);
    }

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
                  loginCubit.loginWithBiometric();
                  Navigator.pop(context, 'Cancel');
                },
                child: const Text('Maybe later'),
              ),
            TextButton(
              onPressed: () async {
                final appId =
                    Platform.isAndroid ? 'io.payment.cardpay' : '1644127078';
                final url = Uri.parse(
                  Platform.isAndroid
                      ? "market://details?id=$appId"
                      : "https://apps.apple.com/app/id$appId",
                );
                launchUrl(
                  url,
                  mode: LaunchMode.externalApplication,
                );
              },
              child: const Text('Update Now'),
            ),
          ],
        ),
      );
    }

    useEffect(() {
      return () {
        phoneNumberController.dispose();
      };
    }, []);

    return AuthLayout(
      child: SingleChildScrollView(
        physics: const AlwaysScrollableScrollPhysics(),
        child: Form(
          key: formKey,
          child: Column(
            children: [
              HeightBox(slab: 6),
              HeightBox(slab: 2),
              Align(
                alignment: Alignment.centerLeft,
                child: const MainHeading(
                  accountTitle: AppStrings.logIn,
                  accountDescription: AppStrings.logInDescription,
                ),
              ),
              HeightBox(slab: 2),
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
              BlocConsumer<LoginCubit, LoginState>(
                listener: (context, state) {
                  switch (state.runtimeType) {
                    case ManualLoginSuccess:
                      checkPointsCubit.getCheckpoints();
                      break;
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
              BlocListener<CheckpointsCubit, CheckpointsState>(
                listener: (_, state) {
                  switch (state.runtimeType) {
                    case CheckpointsSuccess:
                      userCubit.getUser();
                      balanceCubit.getUserBalance();
                      recentTransactionsCubit.getUserRecentTransactions();
                      closedLoopCubit.getAllClosedLoops();

                      navigateToNextScreen(state);
                      break;
                    case CheckpointsFailed:
                      context.router.push(const SignupRoute());
                      break;
                  }
                },
                child: const SizedBox.shrink(),
              ),
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
                      loginCubit.loginWithBiometric();
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

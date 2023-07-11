import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/screen_utills/screen_util.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/utils/constants/signUp_string.dart';
import '../widgets/layout/pin_numpad_layout.dart';

@RoutePage()
class AuthView extends HookWidget {
  const AuthView({super.key});

  @override
  Widget build(BuildContext context) {
    final pinController = useMemoized(() => TextEditingController(), []);
    final showErrorMessage = useState(false);

    void handleLogin() {
      if (pinController.text.length == 4) {
        context.router.push(const DashboardRoute());
      } else {
        showErrorMessage.value = true;
      }
    }

    useEffect(() {
      return () {
        pinController.dispose();
      };
    }, []);

    return Scaffold(
      body: Container(
        color: AppColors.darkVlueColor,
        child: Column(
          children: [
            SizedBox(
                height: ScreenUtil.heightMultiplier(context) *
                    15), // Leverage ScreenUtil
            Text(
              AppStrings.enterPin, // from strings.dart
              style: AppTypography.mainHeading.copyWith(
                color: AppColors.secondaryColor,
                fontSize: ScreenUtil.textMultiplier(context) * 3.0,
              ),
            ),
            SizedBox(
                height: ScreenUtil.heightMultiplier(context) *
                    15), // Leverage ScreenUtil
            Expanded(
              child: SingleChildScrollView(
                child: PinEntry(
                  controller: pinController,
                  onPinEntered: handleLogin,
                ),
              ),
            ),
            if (showErrorMessage.value)
              Padding(
                padding: EdgeInsets.symmetric(
                  vertical: ScreenUtil.heightMultiplier(context) *
                      2, // Leverage ScreenUtil
                  horizontal: ScreenUtil.widthMultiplier(context) *
                      4, // Leverage ScreenUtil
                ),
                child: const Text(
                  AppStrings.enterPin, // from strings.dart
                  style: TextStyle(
                    color: AppColors.orangeColor,
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}

import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/router/app_router.dart';
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
        color: AppColors.darkBlueColor,
        child: Flex(
          direction: Axis.vertical,
          children: [
            Expanded(flex: 2, child: Container()),
            Text(AppStrings.enterPin, style: AppTypography.mainHeadingWhite),
            Expanded(flex: 2, child: Container()),
            PinEntry(
              controller: pinController,
              onPinEntered: handleLogin,
            ),
            if (showErrorMessage.value)
              Text(
                AppStrings.enterPin,
                style: AppTypography.inputFont,
              ),
            Expanded(flex: 1, child: Container()),
          ],
        ),
      ),
    );
  }
}

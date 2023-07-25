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
    final pinController = useTextEditingController();
    final showErrorMessage = useState(false);
    final isPinConfirmed = useState(false);
    String enteredPin = '';

    void handleLogin() {
      if (isPinConfirmed.value) {
        String confirmPin = pinController.text;

        if (confirmPin.length == 4 && confirmPin == enteredPin) {
          context.router.push(const DashboardRoute());
        } else {
          showErrorMessage.value = true;
          isPinConfirmed.value = false;
          enteredPin = '';
          pinController.clear();
        }
      } else {
        String entered = pinController.text;
        if (entered.length == 4) {
          isPinConfirmed.value = true;
          enteredPin = entered;
          pinController.clear();
        } else {
          showErrorMessage.value = true;
          pinController.clear();
        }
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
            Text(
              isPinConfirmed.value
                  ? AppStrings.confirmPin
                  : AppStrings.enterPin,
              style: AppTypography.mainHeadingWhite,
            ),
            Expanded(flex: 1, child: Container()),
            if (showErrorMessage.value)
              Text(
                AppStrings.error,
                style: AppTypography.errorText,
              ),
            Expanded(flex: 2, child: Container()),
            PinEntry(
              controller: pinController,
              onPinEntered: handleLogin,
            ),
            Expanded(flex: 1, child: Container()),
          ],
        ),
      ),
    );
  }
}

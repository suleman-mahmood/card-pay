import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:auto_route/auto_route.dart';
import 'package:frontend_futter/src/config/router/app_router.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';
import 'package:frontend_futter/src/presentation/Widgets/radio_box/radio_input.dart';
import 'package:frontend_futter/src/presentation/Widgets/layout/common_app_layout.dart';

@RoutePage()
class AuthView extends HookWidget {
  @override
  Widget build(BuildContext context) {
    final pinController = useTextEditingController();
    final showErrorMessage = useState(false);

    void handleLogin() {
      if (pinController.text.length == 4) {
        context.router.push(SplashRoute());
      } else {
        showErrorMessage.value = true;
      }
    }

    useEffect(() {
      return () {
        pinController.dispose();
      };
    }, []);

    return AppLayout(
      child: Container(
        color: AppColors.blueColor, // Set the desired blue color here
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            SizedBox(height: 20),
            Text(
              'Enter your PIN',
              style: AppTypography.headingFont.copyWith(
                color: AppColors.secondaryColor,
                fontSize: 34,
              ),
            ),
            SizedBox(height: 80),
            RadioView(controller: pinController, onPinEntered: handleLogin),
            if (showErrorMessage.value)
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 10),
                child: Text(
                  'Please enter a 4-digit PIN.',
                  style: AppTypography.headingFont.copyWith(
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

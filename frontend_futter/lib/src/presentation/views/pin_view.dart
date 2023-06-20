import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:auto_route/auto_route.dart';
import 'package:frontend_futter/src/config/router/app_router.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';
import 'package:frontend_futter/src/presentation/Widgets/radio_box/radio_view.dart';

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

    return Scaffold(
      body: Container(
        color: AppColors.blueColor,
        child: Column(
          children: [
            SizedBox(height: 70),
            Text(
              'Enter your PIN',
              style: AppTypography.mainHeading.copyWith(
                color: AppColors.secondaryColor,
              ),
            ),
            SizedBox(height: 120),
            Expanded(
              child: SingleChildScrollView(
                child: RadioView(
                  controller: pinController,
                  onPinEntered: handleLogin,
                ),
              ),
            ),
            if (showErrorMessage.value)
              Padding(
                padding: const EdgeInsets.symmetric(
                  vertical: 10,
                  horizontal: 20,
                ),
                child: Text(
                  'Please enter a 4-digit PIN.',
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

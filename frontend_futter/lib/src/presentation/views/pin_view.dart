import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:auto_route/auto_route.dart';
import 'package:frontend_futter/src/config/router/app_router.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';
import 'package:frontend_futter/src/presentation/Widgets/radio_box/radio_input.dart';
import 'package:frontend_futter/src/presentation/Widgets/number_pad/num_pad.dart';

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
              style: TextStyle(
                color: AppColors.secondaryColor,
                fontSize: 34,
              ),
            ),
            SizedBox(height: 120),
            Expanded(
              child: SingleChildScrollView(
                child: RadioView(
                    controller: pinController, onPinEntered: handleLogin),
              ),
            ),
            if (showErrorMessage.value)
              Padding(
                padding:
                    const EdgeInsets.symmetric(vertical: 10, horizontal: 20),
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

class RadioView extends HookWidget {
  final TextEditingController controller;
  final int pinLength;
  final VoidCallback onPinEntered;

  const RadioView({
    required this.controller,
    this.pinLength = 4,
    required this.onPinEntered,
  });

  @override
  Widget build(BuildContext context) {
    final enteredDigits = useState<int>(0);

    void updateEnteredDigits() {
      final enteredPin = controller.text;
      enteredDigits.value = enteredPin.length;

      if (enteredDigits.value == pinLength) {
        onPinEntered();
      }
    }

    useEffect(() {
      controller.addListener(updateEnteredDigits);
      return () {
        controller.removeListener(updateEnteredDigits);
      };
    }, []);

    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: List.generate(
            pinLength,
            (index) => Padding(
              padding: const EdgeInsets.symmetric(horizontal: 32.0),
              child: RadioButton(filled: index < enteredDigits.value),
            ),
          ),
        ),
        SizedBox(height: 30),
        NumPad(controller: controller),
      ],
    );
  }
}

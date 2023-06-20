import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
// import 'package:frontend_futter/src/config/themes/colors.dart';
import 'package:frontend_futter/src/presentation/Widgets/radio_box/radio_input.dart';
import 'package:frontend_futter/src/presentation/Widgets/number_pad/num_pad.dart';

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

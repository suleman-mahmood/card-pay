import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';
// import 'number_pad.dart';
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
              padding: const EdgeInsets.symmetric(
                  horizontal: 39.0), // Increase the horizontal spacing
              child: PinRadioButton(filled: index < enteredDigits.value),
            ),
          ),
        ),
        SizedBox(height: 124), // Increase the height for spacing
        NumberPad(controller: controller),
      ],
    );
  }
}

class PinRadioButton extends StatelessWidget {
  final bool filled;

  const PinRadioButton({required this.filled});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 16,
      height: 16,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        color: filled ? AppColors().secondaryColor : Colors.transparent,
        border: Border.all(
          color: AppColors().secondaryColor,
          width: 1.0,
        ),
      ),
      transform: Matrix4.diagonal3Values(1.9, 1.9, 1.4), // Increase the scale
    );
  }
}

import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/presentation/widgets/selections/radio_input_button.dart';
import 'package:frontend_futter/src/presentation/widgets/number_pad/numpad.dart';
import 'package:frontend_futter/src/config/screen_utills/screen_util.dart';

class PinEntry extends HookWidget {
  final TextEditingController controller;
  final int pinLength;
  final VoidCallback onPinEntered;

  const PinEntry(
      {super.key, required this.controller,
      this.pinLength = 4,
      required this.onPinEntered});

  @override
  Widget build(BuildContext context) {
    final enteredDigits = useState<int>(0);
    final paddingSize = ScreenUtil.blockSizeHorizontal(context) * 3.4;

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

    return NumpadWithDisplay(
        display: _buildDisplay(context, paddingSize, enteredDigits.value),
        controller: controller);
  }

  Widget _buildDisplay(BuildContext context, double paddingSize, int digits) {
    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: _buildRadioButtons(paddingSize, digits),
        ),
        SizedBox(height: ScreenUtil.blockSizeVertical(context) * 15),
      ],
    );
  }

  List<Widget> _buildRadioButtons(double paddingSize, int digits) {
    return List.generate(
      pinLength,
      (index) => Padding(
        padding: EdgeInsets.symmetric(horizontal: paddingSize),
        child: RadioButton(filled: index < digits),
      ),
    );
  }
}

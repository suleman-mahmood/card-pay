import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/selections/radio_input_button.dart';
import 'package:cardpay/src/presentation/widgets/number_pad/numpad.dart';

class PinEntry extends HookWidget {
  final TextEditingController controller;
  final int pinLength;
  final VoidCallback onPinEntered;

  const PinEntry({
    Key? key,
    required this.controller,
    this.pinLength = 4,
    required this.onPinEntered,
  }) : super(key: key);

  Widget _buildDisplay(BuildContext context, double paddingSize, int digits) {
    return Column(
      children: [_radioButtonRow(paddingSize, digits), HeightBox(slab: 3)],
    );
  }

  Widget _radioButtonRow(double paddingSize, int digits) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: _buildRadioButtons(paddingSize, digits),
    );
  }

  List<Widget> _buildRadioButtons(double paddingSize, int digits) {
    return List.generate(
      pinLength,
      (index) => Padding(
        padding: EdgeInsets.symmetric(horizontal: 5),
        child: RadioButton(filled: index < digits),
      ),
    );
  }

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

    return NumpadWithDisplay(
        display: _buildDisplay(context, 2, enteredDigits.value),
        controller: controller);
  }
}

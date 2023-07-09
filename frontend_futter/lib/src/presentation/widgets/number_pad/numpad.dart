/// The NumpadWithDisplay class is a Flutter widget that displays a number pad and a display widget.
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/presentation/widgets/actions/button/numpad_buttons.dart';

class NumpadWithDisplay extends HookWidget {
  final Widget display;
  final TextEditingController controller;
  const NumpadWithDisplay({super.key, required this.display, required this.controller});
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        display,
        NumPad(controller: controller),
      ],
    );
  }
}

// class RadioView extends HookWidget {
//   final TextEditingController controller;
//   final int pinLength;
//   final VoidCallback onPinEntered;

//   const RadioView({
//     required this.controller,
//     this.pinLength = 4,
//     required this.onPinEntered,
//   });

//   @override
//   Widget build(BuildContext context) {
//     final enteredDigits = useState<int>(0);

//     void updateEnteredDigits() {
//       final enteredPin = controller.text;
//       enteredDigits.value = enteredPin.length;

//       if (enteredDigits.value == pinLength) {
//         onPinEntered();
//       }
//     }

//     useEffect(() {
//       controller.addListener(updateEnteredDigits);
//       return () {
//         controller.removeListener(updateEnteredDigits);
//       };
//     }, []);

//     final screenWidth = MediaQuery.of(context).size.width;

//     return Column(
//       children: [
//         Row(
//           mainAxisAlignment: MainAxisAlignment.center,
//           children: List.generate(
//             pinLength,
//             (index) => Padding(
//               padding: EdgeInsets.symmetric(horizontal: screenWidth * 0.04),
//               child: RadioButton(filled: index < enteredDigits.value),
//             ),
//           ),
//         ),
//         NumPad(controller: controller),
//       ],
//     );
//   }
// }

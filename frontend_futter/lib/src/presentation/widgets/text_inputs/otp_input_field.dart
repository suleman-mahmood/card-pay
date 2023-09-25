import 'package:cardpay/src/presentation/widgets/boxes/horizontal_padding.dart';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';

class OTPInput extends HookWidget {
  final int digitCount;
  final ValueChanged<String> onCompleted;

  const OTPInput({
    super.key,
    required this.digitCount,
    required this.onCompleted,
  });

  bool _isInputComplete(List<TextEditingController> controllers) {
    for (var controller in controllers) {
      if (controller.text.isEmpty) {
        return false;
      }
    }
    return true;
  }

  void _moveFocusForward(
    BuildContext context,
    List<FocusNode> focusNodes,
    int index,
  ) {
    final newIndex = index + 1;
    focusNodes[index].unfocus(); // Un focus the current textfield

    if (newIndex < digitCount) {
      FocusScope.of(context).requestFocus(focusNodes[newIndex]);
    }
  }

  void _moveFocusBackward(
    BuildContext context,
    List<FocusNode> focusNodes,
    int index,
  ) {
    final newIndex = index - 1;
    focusNodes[index].unfocus(); // Un focus the current textfield

    if (newIndex >= 0) {
      FocusScope.of(context).requestFocus(focusNodes[newIndex]);
    }
  }

  void _checkOtpCompleted(List<TextEditingController> controllers) {
    if (_isInputComplete(controllers)) {
      String otp = '';
      for (var controller in controllers) {
        otp += controller.text;
      }
      onCompleted(otp);
    }
  }

  @override
  Widget build(BuildContext context) {
    final focusNodes = List.generate(digitCount, (index) => useFocusNode());
    final controllers = List.generate(
      digitCount,
      (index) => useTextEditingController(),
    );

    return PaddingHorizontal(
      slab: 1,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: List.generate(digitCount, (index) {
          return SizedBox(
            width: 64,
            height: 40,
            child: PaddingHorizontal(
              slab: 1,
              child: TextField(
                controller: controllers[index],
                focusNode: focusNodes[index],
                keyboardType: TextInputType.number,
                maxLength: 1,
                textAlign: TextAlign.center,
                style: AppTypography.inputFont,
                decoration: InputDecoration(
                  counterText: '',
                  contentPadding: EdgeInsets.all(3),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                    borderSide: BorderSide(
                      color: AppColors.greyColor,
                      width: 1.0,
                    ),
                  ),
                  fillColor: AppColors.secondaryColor,
                  filled: true,
                ),
                onChanged: (value) {
                  if (value.length == 1) {
                    _moveFocusForward(context, focusNodes, index);
                  } else if (value.isEmpty) {
                    _moveFocusBackward(context, focusNodes, index);
                  }
                  _checkOtpCompleted(controllers);
                },
              ),
            ),
          );

          // TODO(suleman): Implement this later on since it's not working but is the right way to do things
          // Using raw keyboard listener
          // return RawKeyboardListener(
          //   focusNode: focusNodes[index],
          //   child: SizedBox(
          //     width: 64,
          //     height: 40,
          //     child: PaddingHorizontal(
          //       slab: 1,
          //       child: TextField(
          //         controller: controllers[index],
          //         // focusNode: focusNodes[index],
          //         keyboardType: TextInputType.number,
          //         maxLength: 1,
          //         textAlign: TextAlign.center,
          //         style: AppTypography.inputFont,
          //         decoration: InputDecoration(
          //           counterText: '',
          //           contentPadding: EdgeInsets.all(3),
          //           border: OutlineInputBorder(
          //             borderRadius: BorderRadius.circular(8),
          //             borderSide: BorderSide(
          //               color: AppColors.greyColor,
          //               width: 1.0,
          //             ),
          //           ),
          //           fillColor: AppColors.secondaryColor,
          //           filled: true,
          //         ),
          //       ),
          //     ),
          //   ),
          //   onKey: (keyEvent) {
          //     final value = keyEvent.data.logicalKey.keyLabel;
          //     printWarning(
          //       "Key event called ${value}",
          //     );

          //     if (value == "Backspace") {
          //       _moveFocusBackward(context, focusNodes, index);
          //     } else if (digits.contains(int.parse(value))) {
          //       _moveFocusForward(context, focusNodes, index);
          //     }
          //     _checkAndCallOnCompleted(controllers);
          //   },
          // );
        }),
      ),
    );
  }
}

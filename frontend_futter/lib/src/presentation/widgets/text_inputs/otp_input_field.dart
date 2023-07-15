import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';

class OTPInput extends HookWidget {
  final int digitCount;
  final ValueChanged<String>? onCompleted;

  const OTPInput({
    super.key,
    required this.digitCount,
    this.onCompleted,
  });

  bool _isInputComplete(List<TextEditingController> controllers) {
    for (var controller in controllers) {
      if (controller.text.isEmpty) {
        return false;
      }
    }
    return true;
  }

  void _moveFocus(BuildContext context, List<FocusNode> focusNodes, int index) {
    focusNodes[index].unfocus();
    if (index != digitCount - 1) {
      FocusScope.of(context).requestFocus(focusNodes[index + 1]);
    }
  }

  void _checkAndCallOnCompleted(List<TextEditingController> controllers) {
    if (_isInputComplete(controllers)) {
      String otp = '';
      for (var controller in controllers) {
        otp += controller.text;
      }
      onCompleted?.call(otp);
    }
  }

  @override
  Widget build(BuildContext context) {
    final focusNodes = List.generate(digitCount, (index) => useFocusNode());
    final controllers = List.generate(
      digitCount,
      (index) => useTextEditingController(),
    );

    useEffect(() {
      return () {
        for (var controller in controllers) {
          controller.dispose();
        }
      };
    }, []);

    return Padding(
      padding: EdgeInsets.symmetric(horizontal: 5),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: List.generate(digitCount, (index) {
          return SizedBox(
            width: 64,
            height: 40,
            child: Padding(
              padding: EdgeInsets.symmetric(horizontal: 5),
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
                    _moveFocus(context, focusNodes, index);
                  }
                  _checkAndCallOnCompleted(controllers);
                },
              ),
            ),
          );
        }),
      ),
    );
  }
}

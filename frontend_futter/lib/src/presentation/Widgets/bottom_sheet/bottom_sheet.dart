import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class OTPInput extends HookWidget {
  final int digitCount;
  final ValueChanged<String>? onCompleted;
  final double boxWidth;
  final double boxHeight;

  OTPInput({
    required this.digitCount,
    this.onCompleted,
    this.boxWidth = 48.0,
    this.boxHeight = 30.0,
  });

  bool _isInputComplete(List<TextEditingController> controllers) {
    for (var controller in controllers) {
      if (controller.text.isEmpty) {
        return false;
      }
    }
    return true;
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

    return Center(
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: List.generate(digitCount, (index) {
          return SizedBox(
            width: boxWidth,
            height: boxHeight,
            child: Padding(
              padding: EdgeInsets.symmetric(horizontal: 8.0),
              child: TextField(
                controller: controllers[index],
                focusNode: focusNodes[index],
                keyboardType: TextInputType.number,
                maxLength: 1,
                textAlign: TextAlign.center,
                style: AppColors().inputFont.copyWith(),
                decoration: InputDecoration(
                  counterText: '',
                  contentPadding: EdgeInsets.all(8.0),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(6.0),
                    borderSide: BorderSide(
                      color: AppColors().secondaryColor,
                      width: 1.0,
                    ),
                  ),
                  fillColor: AppColors().secondaryColor,
                  filled: true,
                ),
                onChanged: (value) {
                  if (value.length == 1 && index != digitCount - 1) {
                    focusNodes[index].unfocus();
                    FocusScope.of(context).requestFocus(focusNodes[index + 1]);
                  }
                  if (_isInputComplete(controllers)) {
                    String otp = '';
                    for (var controller in controllers) {
                      otp += controller.text;
                    }
                    onCompleted?.call(otp);
                  }
                },
              ),
            ),
          );
        }),
      ),
    );
  }
}

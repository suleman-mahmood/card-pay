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
    this.boxWidth = 60.0,
    this.boxHeight = 37.0,
  });

  bool _isInputComplete(List<TextEditingController> controllers) {
    for (var controller in controllers) {
      if (controller.text.isEmpty) {
        return false;
      }
    }
    return true;
  }

  void _onTextChanged(
      List<TextEditingController> controllers,
      List<FocusNode> focusNodes,
      int index,
      String value,
      BuildContext context) {
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

    final double screenWidth = MediaQuery.of(context).size.width;
    final double screenHeight = MediaQuery.of(context).size.height;
    final double scaledBoxWidth = boxWidth * screenWidth / 375.0;
    final double scaledBoxHeight = boxHeight * screenHeight / 812.0;
    final double fontSize = 20.0 * screenWidth / 375.0;

    return Center(
      child: Align(
        alignment: Alignment.center,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: List.generate(digitCount, (index) {
            return SizedBox(
              width: scaledBoxWidth,
              height: scaledBoxHeight,
              child: Padding(
                padding:
                    EdgeInsets.symmetric(horizontal: scaledBoxWidth * 0.05),
                child: TextField(
                  controller: controllers[index],
                  focusNode: focusNodes[index],
                  keyboardType: TextInputType.number,
                  maxLength: 1,
                  textAlign: TextAlign.center,
                  style: AppTypography.inputFont.copyWith(
                    fontSize: fontSize,
                    color: AppColors.blackColor,
                  ),
                  decoration: InputDecoration(
                    counterText: '',
                    contentPadding: EdgeInsets.all(scaledBoxWidth * 0.05),
                    border: OutlineInputBorder(
                      borderRadius:
                          BorderRadius.circular(scaledBoxWidth * 0.16),
                      borderSide: BorderSide(
                        color: Theme.of(context).primaryColor,
                        width: 1.0,
                      ),
                    ),
                    fillColor: AppColors.secondaryColor,
                    filled: true,
                  ),
                  onChanged: (value) {
                    _onTextChanged(
                      controllers,
                      focusNodes,
                      index,
                      value,
                      context,
                    );
                  },
                ),
              ),
            );
          }),
        ),
      ),
    );
  }
}

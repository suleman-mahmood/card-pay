import 'package:flutter/material.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class OTPInput extends StatefulWidget {
  final int digitCount;
  final ValueChanged<String>? onCompleted;

  OTPInput({required this.digitCount, this.onCompleted});

  @override
  _OTPInputState createState() => _OTPInputState();
}

class _OTPInputState extends State<OTPInput> {
  late List<FocusNode> _focusNodes;
  late List<TextEditingController> _controllers;

  @override
  void initState() {
    super.initState();
    _focusNodes = List.generate(widget.digitCount, (index) => FocusNode());
    _controllers =
        List.generate(widget.digitCount, (index) => TextEditingController());
  }

  @override
  void dispose() {
    for (var controller in _controllers) {
      controller.dispose();
    }
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      children: List.generate(widget.digitCount, (index) {
        return Expanded(
          child: Padding(
            padding: EdgeInsets.symmetric(horizontal: 8.0),
            child: TextField(
              controller: _controllers[index],
              focusNode: _focusNodes[index],
              keyboardType: TextInputType.number,
              maxLength: 1,
              textAlign: TextAlign.center,
              style: AppColors().inputFont,
              decoration: InputDecoration(
                counterText: '',
                contentPadding: EdgeInsets.all(8.0),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12.0),
                  borderSide: BorderSide(
                    color:
                        AppColors().secondaryColor, // Set the border color here
                    width: 1.0, // Set the border width here
                  ),
                ),
                fillColor:
                    AppColors().secondaryColor, // Set the fill color here
                filled: true, // Enable filling
              ),
              onChanged: (value) {
                if (value.length == 1 && index != widget.digitCount - 1) {
                  _focusNodes[index].unfocus();
                  FocusScope.of(context).requestFocus(_focusNodes[index + 1]);
                }
                if (_isInputComplete()) {
                  String otp = '';
                  for (var controller in _controllers) {
                    otp += controller.text;
                  }
                  widget.onCompleted?.call(otp);
                }
              },
            ),
          ),
        );
      }),
    );
  }

  bool _isInputComplete() {
    for (var controller in _controllers) {
      if (controller.text.isEmpty) {
        return false;
      }
    }
    return true;
  }
}

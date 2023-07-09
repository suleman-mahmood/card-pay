import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/screen_utills/screen_util.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class CustomInputField extends HookWidget {
  final String label;
  final String? hint;
  final bool obscureText;
  final FormFieldValidator<String>? validator;
  final ValueChanged<String?>? onChanged;
  final TextInputType? keyboardType;
  final Color textcolor;
  final Color color;
  final TextEditingController? controller;

  const CustomInputField({
    required this.label,
    this.hint,
    this.obscureText = false,
    this.validator,
    this.onChanged,
    this.keyboardType,
    this.textcolor = AppColors.blackColor,
    this.color = AppColors.greyColor,
    this.controller,
  });

  @override
  Widget build(BuildContext context) {
    final passwordVisible = useState<bool>(false);
    final padding = ScreenUtil.blockSizeHorizontal(context) * 2;
    final verticalPadding = ScreenUtil.blockSizeVertical(context) * 2.0;

    void togglePasswordVisibility() {
      passwordVisible.value = !passwordVisible.value;
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: TextStyle(
            color: textcolor,
            fontSize: ScreenUtil.blockSizeHorizontal(context) * 4,
          ),
        ),
        SizedBox(height: ScreenUtil.blockSizeVertical(context) * 0.5),
        Container(
          width: double.infinity,
          decoration: BoxDecoration(
            color: color.withOpacity(0.5),
            borderRadius: BorderRadius.circular(19),
          ),
          child: Row(
            children: [
              Expanded(
                child: Padding(
                  padding: EdgeInsets.symmetric(
                      horizontal: padding, vertical: verticalPadding),
                  child: TextFormField(
                    obscureText: obscureText && !passwordVisible.value,
                    controller: controller,
                    validator: validator,
                    keyboardType: keyboardType,
                    onChanged: onChanged,
                    decoration: InputDecoration(
                      border: InputBorder.none,
                      hintText: hint,
                      isCollapsed: true,
                      contentPadding: EdgeInsets.zero,
                    ),
                  ),
                ),
              ),
              if (obscureText)
                Padding(
                  padding: EdgeInsets.only(right: padding),
                  child: InkWell(
                    onTap: togglePasswordVisibility,
                    child: Icon(
                      passwordVisible.value
                          ? Icons.visibility
                          : Icons.visibility_off,
                      color: AppColors.greyColor,
                    ),
                  ),
                ),
            ],
          ),
        ),
      ],
    );
  }
}

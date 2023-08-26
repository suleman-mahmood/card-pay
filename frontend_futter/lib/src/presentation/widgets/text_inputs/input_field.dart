import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';

class CustomInputField extends HookWidget {
  final String label;
  final String? hint;
  final bool obscureText;
  final FormFieldValidator<String>? validator;
  final ValueChanged<String>? onChanged;
  final TextInputType? keyboardType;
  final Color textcolor;
  final Color color;
  final TextEditingController? controller;
  final Color hintColor;
  final Color labelColor;

  const CustomInputField({
    Key? key,
    required this.label,
    this.hint,
    this.obscureText = false,
    this.validator,
    this.onChanged,
    this.keyboardType,
    this.textcolor = AppColors.blackColor,
    this.color = AppColors.lightGreyColor,
    this.controller,
    this.hintColor = AppColors.greyColor,
    this.labelColor = AppColors.blackColor,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final passwordVisible = useState<bool>(false);

    void togglePasswordVisibility() {
      passwordVisible.value = !passwordVisible.value;
    }

    useEffect(() {
      return () {
        controller?.dispose();
      };
    }, [controller]);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: AppTypography.bodyText.copyWith(color: labelColor)),
        const HeightBox(slab: 1),
        Container(
          decoration: BoxDecoration(
            color: color,
            borderRadius: BorderRadius.circular(10),
          ),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 18),
            child: Row(
              children: [
                Expanded(
                  child: TextFormField(
                    obscureText: obscureText && !passwordVisible.value,
                    controller: controller,
                    validator: validator,
                    keyboardType: keyboardType,
                    onChanged: onChanged,
                    decoration: InputDecoration(
                      border: InputBorder.none,
                      hintText: hint,
                      hintStyle: TextStyle(color: hintColor),
                      isCollapsed: true,
                      contentPadding: EdgeInsets.zero,
                    ),
                  ),
                ),
                if (obscureText)
                  InkWell(
                    onTap: togglePasswordVisibility,
                    child: Icon(
                      passwordVisible.value
                          ? Icons.visibility
                          : Icons.visibility_off,
                      color: AppColors.greyColor,
                    ),
                  ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}

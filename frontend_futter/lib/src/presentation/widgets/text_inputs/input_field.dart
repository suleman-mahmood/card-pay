import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';

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
    super.key,
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

    void togglePasswordVisibility() {
      passwordVisible.value = !passwordVisible.value;
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: AppTypography.bodyText),
        const HeightBox(slab: 1),
        Container(
          decoration: BoxDecoration(
            color: color.withOpacity(0.25),
            borderRadius: BorderRadius.circular(16),
          ),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
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

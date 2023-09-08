import 'package:cardpay/src/presentation/widgets/boxes/width_between.dart';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';

class CheckBoxFormField extends HookWidget {
  final ValueNotifier<bool> isChecked;
  final String text;
  final FormFieldValidator<bool> validator;
  final Function()? onTap;

  CheckBoxFormField({
    required this.isChecked,
    required this.text,
    required this.validator,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return FormField<bool>(
      validator: validator,
      builder: (FormFieldState<bool> field) {
        return InkWell(
          onTap: () => toggleCheckbox(isChecked),
          child: buildContainer(context, isChecked),
        );
      },
    );
  }

  void toggleCheckbox(ValueNotifier<bool> isChecked) {
    isChecked.value = !isChecked.value;
  }

  Widget buildContainer(BuildContext context, ValueNotifier<bool> isChecked) {
    return Row(
      children: [
        buildCheckbox(isChecked),
        const WidthBetween(),
        GestureDetector(
          onTap: onTap,
          child: Text(text, style: AppTypography.linkText),
        ),
      ],
    );
  }

  Widget buildCheckbox(ValueNotifier<bool> isChecked) {
    return Container(
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        color: isChecked.value ? AppColors.primaryColor : AppColors.greyColor,
        border: !isChecked.value
            ? Border.all(color: AppColors.greyColor, width: 12.0)
            : null,
      ),
      child: isChecked.value
          ? Icon(Icons.check, color: AppColors.secondaryColor)
          : null,
    );
  }
}

import 'package:cardpay/src/presentation/widgets/boxes/width_between.dart';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';

class CheckBox extends HookWidget {
  final Function(bool value)? onChanged;
  final Function()? onTap;
  final String text;

  const CheckBox({
    super.key,
    required this.text,
    this.onChanged,
    this.onTap,
  }) : super();

  @override
  Widget build(BuildContext context) {
    final isChecked = useState(false);

    return InkWell(
      onTap: () => toggleCheckbox(isChecked),
      child: buildContainer(context, isChecked),
    );
  }

  void toggleCheckbox(ValueNotifier<bool> isChecked) {
    isChecked.value = !isChecked.value;
    onChanged?.call(isChecked.value);
  }

  Widget buildContainer(BuildContext context, ValueNotifier<bool> isChecked) {
    return Row(
      children: [
        buildCheckbox(isChecked),
        WidthBetween(),
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

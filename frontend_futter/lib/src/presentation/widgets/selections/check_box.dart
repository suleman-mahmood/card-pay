import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';

class CheckBox extends HookWidget {
  final Function(bool value)? onChanged;
  final String text;

  const CheckBox({
    super.key,
    required this.text,
    this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    final isChecked = useState(false);
    final screenHeight = MediaQuery.of(context).size.height;
    final screenWidth = MediaQuery.of(context).size.width;

    return InkWell(
      onTap: () => toggleCheckbox(isChecked),
      child: buildContainer(context, isChecked, screenHeight, screenWidth),
    );
  }

  void toggleCheckbox(ValueNotifier<bool> isChecked) {
    isChecked.value = !isChecked.value;
    onChanged?.call(isChecked.value);
  }

  Widget buildContainer(BuildContext context, ValueNotifier<bool> isChecked,
      double screenHeight, double screenWidth) {
    return Container(
      width: double.infinity,
      padding: EdgeInsets.symmetric(
          vertical: screenHeight * 0.01, horizontal: screenWidth * 0.05),
      decoration: BoxDecoration(
        color: AppColors.greyColor.withOpacity(0.5),
        borderRadius: BorderRadius.circular(20),
      ),
      child: buildRow(context, isChecked, screenWidth),
    );
  }

  Row buildRow(
      BuildContext context, ValueNotifier<bool> isChecked, double screenWidth) {
    return Row(
      children: [
        buildCheckbox(isChecked, screenWidth),
        SizedBox(width: screenWidth * 0.02),
        buildText(context, screenWidth),
      ],
    );
  }

  Widget buildCheckbox(ValueNotifier<bool> isChecked, double screenWidth) {
    return Container(
      width: screenWidth * 0.06,
      height: screenWidth * 0.06,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        color: isChecked.value ? AppColors.primaryColor : AppColors.greyColor,
      ),
      child: isChecked.value
          ? Icon(
              Icons.check,
              color: AppColors.greyColor,
              size: screenWidth * 0.04,
            )
          : null,
    );
  }

  Expanded buildText(BuildContext context, double screenWidth) {
    return Expanded(
      child: Text(
        text,
        style: Theme.of(context).textTheme.titleMedium!.copyWith(
              color: AppColors.blackColor.withOpacity(0.8),
              fontSize: screenWidth * 0.045,
            ),
      ),
    );
  }
}

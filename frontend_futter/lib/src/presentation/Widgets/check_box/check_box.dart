import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class CheckBox extends HookWidget {
  final Function(bool value)? onChanged;
  final String text;

  const CheckBox({
    required this.text,
    this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    final isChecked = useState(false);
    final screenHeight = MediaQuery.of(context).size.height;
    final screenWidth = MediaQuery.of(context).size.width;

    return InkWell(
      onTap: () {
        isChecked.value = !isChecked.value;
        onChanged?.call(isChecked.value);
      },
      child: Container(
        width: screenWidth * 0.9,
        padding: EdgeInsets.symmetric(
            vertical: screenHeight * 0.01, horizontal: screenWidth * 0.05),
        decoration: BoxDecoration(
          color: AppColors.greyColor.withOpacity(0.5),
          borderRadius: BorderRadius.circular(20),
        ),
        child: Row(
          children: [
            Container(
              width: screenWidth * 0.06,
              height: screenWidth * 0.06,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: isChecked.value
                    ? AppColors.primaryColor
                    : const Color.fromARGB(255, 34, 31, 208),
              ),
              child: isChecked.value
                  ? Icon(
                      Icons.check,
                      color: AppColors.greyColor,
                      size: screenWidth * 0.04,
                    )
                  : null,
            ),
            SizedBox(width: screenWidth * 0.02),
            Expanded(
              child: Text(
                text,
                style: Theme.of(context).textTheme.subtitle1!.copyWith(
                      color: AppColors.blackColor,
                      fontSize: screenWidth * 0.045,
                    ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

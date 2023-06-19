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

    return InkWell(
      onTap: () {
        isChecked.value = !isChecked.value;
        onChanged?.call(isChecked.value);
      },
      child: Container(
        width: double.infinity,
        padding: EdgeInsets.symmetric(vertical: 10, horizontal: 20),
        decoration: BoxDecoration(
          color: AppColors.greyColor,
          borderRadius: BorderRadius.circular(20),
        ),
        child: Row(
          children: [
            Container(
              width: 24,
              height: 24,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: isChecked.value
                    ? AppColors.primaryColor
                    : AppColors.blueColor,
              ),
              child: isChecked.value
                  ? Icon(
                      Icons.check,
                      color: AppColors.greyColor,
                      size: 16,
                    )
                  : null,
            ),
            SizedBox(width: 10),
            Expanded(
              child: Text(
                text,
                style: AppTypography.inputFont.copyWith(
                  color: AppColors.blueColor,
                  fontSize: 16,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

import 'package:flutter/material.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class CheckBox extends StatefulWidget {
  final Function(bool value)? onChanged;
  final String text;

  const CheckBox({
    required this.text,
    this.onChanged,
  });

  @override
  _AcceptTermsCheckboxState createState() => _AcceptTermsCheckboxState();
}

class _AcceptTermsCheckboxState extends State<CheckBox> {
  bool isChecked = false;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: () {
        setState(() {
          isChecked = !isChecked;
          widget.onChanged?.call(isChecked);
        });
      },
      child: Container(
        width: double.infinity,
        padding: EdgeInsets.symmetric(vertical: 10, horizontal: 20),
        decoration: BoxDecoration(
          color: AppColors().greyColor,
          borderRadius: BorderRadius.circular(20),
        ),
        child: Row(
          children: [
            Container(
              width: 24,
              height: 24,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: isChecked
                    ? AppColors().primaryColor
                    : AppColors().blueColor,
              ),
              child: isChecked
                  ? Icon(
                      Icons.check,
                      color: AppColors().greyColor,
                      size: 16,
                    )
                  : null,
            ),
            SizedBox(width: 10),
            Expanded(
              child: Text(widget.text,
                  style: AppColors().inputFont.copyWith(
                        color: AppColors().blueColor,
                        fontSize: 16,
                      )),
            ),
          ],
        ),
      ),
    );
  }
}

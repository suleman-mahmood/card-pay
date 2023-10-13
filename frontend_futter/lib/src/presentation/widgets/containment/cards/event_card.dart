import 'package:cardpay/src/config/themes/colors.dart';
import 'package:flutter/material.dart';

class EventCard extends StatelessWidget {
  final IconData? icon;
  final String text;
  final String? subText;
  final IconData? iconEnd;
  final IconData? secondLastIcon;
  final Color suffixIconColor;
  final Function()? onEndIconTap;
  final Function()? onSecondLastIconTap;
  final bool selected;

  final Color iconColor;
  final Color textColor;
  final Color backgroundColor;
  final Color subTextColor;

  const EventCard({
    Key? key,
    this.icon,
    required this.text,
    this.iconEnd,
    this.secondLastIcon,
    this.onSecondLastIconTap,
    this.subText,
    this.onEndIconTap,
    this.selected = false,
    this.iconColor = AppColors.greyColor,
    this.textColor = AppColors.greyColor,
    this.backgroundColor = AppColors.secondaryColor,
    this.subTextColor = AppColors.greyColor,
    this.suffixIconColor = AppColors.greyColor,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final Color finalBackgroundColor = selected ? Colors.blue : backgroundColor;
    final Color finalTextColor = selected ? Colors.white : textColor;
    return InkWell(
      child: Container(
        decoration: BoxDecoration(
          color: finalBackgroundColor,
          borderRadius: BorderRadius.circular(16),
        ),
        padding: EdgeInsets.all(8.0),
        child: ListTile(
          leading: icon != null
              ? CircleAvatar(
                  backgroundColor:
                      selected ? Colors.transparent : AppColors.lightGreyColor,
                  child: Icon(
                    icon,
                    color: selected ? AppColors.secondaryColor : iconColor,
                  ),
                )
              : null,
          title: Text(
            text,
            style: AppTypography.mainHeading.copyWith(
              fontSize: 20,
              color: finalTextColor,
            ),
          ),
          subtitle: subText != null
              ? Text(
                  subText!,
                  style: TextStyle(
                      color:
                          selected ? AppColors.secondaryColor : subTextColor),
                )
              : null,
          trailing: iconEnd != null
              ? SizedBox(
                  width: 100,
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      GestureDetector(
                        onTap: onSecondLastIconTap,
                        child: Icon(
                          secondLastIcon,
                          color: selected
                              ? AppColors.secondaryColor
                              : suffixIconColor,
                        ),
                      ),
                      GestureDetector(
                        onTap: onEndIconTap,
                        child: Icon(
                          iconEnd,
                          color: selected
                              ? AppColors.secondaryColor
                              : suffixIconColor,
                        ),
                      ),
                    ],
                  ),
                )
              : null,
        ),
      ),
    );
  }
}

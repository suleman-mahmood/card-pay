import 'package:cardpay/shared/typography/sub_heading.dart';
import 'package:cardpay/theme/colors.dart';
import 'package:flutter/material.dart';

class DashboardCardCustomWidget extends StatelessWidget {
  final bool invertColors;

  const DashboardCardCustomWidget({
    Key? key,
    this.invertColors = false,
  }) : super(key: key);

  Color primaryColorDisplay() {
    return invertColors ? AppColors().secondaryColor : AppColors().primaryColor;
  }

  Color secondaryColorDisplay() {
    return invertColors ? AppColors().primaryColor : AppColors().secondaryColor;
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 10,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.all(
          Radius.circular(20),
        ),
      ),
      color: primaryColorDisplay(),
      child: Container(
        decoration: BoxDecoration(
          gradient: AppColors().dashboardCardGradient,
          borderRadius: BorderRadius.all(Radius.circular(20)),
        ),
        child: Padding(
          padding: const EdgeInsets.symmetric(
            horizontal: 15,
            vertical: 20,
          ),
          child: Column(
            children: [
              // Upper content
              Row(
                children: [
                  SubHeadingTypographyCustomWidget(
                    content: "Monthly",
                    invertColors: true,
                  ),
                  Spacer(),
                  Column(
                    children: [
                      Text(
                        "Spent",
                        style: TextStyle(
                          color: secondaryColorDisplay(),
                        ),
                      ),
                      Text(
                        "300",
                        style: TextStyle(
                          color: secondaryColorDisplay(),
                        ),
                      ),
                    ],
                  ),
                  SizedBox(width: 10),
                  Column(
                    children: [
                      Text(
                        "Income",
                        style: TextStyle(
                          color: secondaryColorDisplay(),
                        ),
                      ),
                      Text(
                        "300",
                        style: TextStyle(
                          color: secondaryColorDisplay(),
                        ),
                      ),
                    ],
                  ),
                ],
              ),

              SizedBox(height: 10),

              // Slider
              SliderTheme(
                child: Slider(
                  thumbColor: secondaryColorDisplay(),
                  activeColor: AppColors().redColor,
                  inactiveColor: secondaryColorDisplay(),
                  value: 10,
                  max: 100,
                  label: "200",
                  onChanged: (_) {},
                ),
                data: SliderTheme.of(context).copyWith(
                  trackHeight: 5,
                  thumbShape: RoundSliderThumbShape(enabledThumbRadius: 0.0),
                  overlayShape: SliderComponentShape.noOverlay,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

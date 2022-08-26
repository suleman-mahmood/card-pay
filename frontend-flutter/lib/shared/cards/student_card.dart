import 'package:cardpay/shared/typography/caption.dart';
import 'package:cardpay/shared/typography/sub_heading.dart';
import 'package:cardpay/theme/colors.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:cardpay/services/models.dart' as model;

class StudentCardCustomWidget extends StatelessWidget {
  const StudentCardCustomWidget({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    // Listen to changes to the user model
    final userData = context.watch<model.User>();

    return Card(
      elevation: 10,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.all(
          Radius.circular(20),
        ),
      ),
      child: Padding(
        padding: const EdgeInsets.symmetric(
          horizontal: 0,
          vertical: 20,
        ),
        child: Row(
          children: [
            // Left padding
            const SizedBox(width: 10),

            // Aesthetic card image
            Stack(
              alignment: AlignmentDirectional.topStart,
              clipBehavior: Clip.none,
              children: [
                const SizedBox(
                  width: 100,
                  height: 150,
                ),
                Positioned(
                  top: -40,
                  child: ClipRRect(
                    borderRadius: BorderRadius.circular(20),
                    child: Image.asset("assets/images/student_card.png"),
                  ),
                ),
              ],
            ),

            const SizedBox(width: 10),

            // Right half of the card

            // Strip of name and roll number
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Container(
                    padding: EdgeInsets.all(10),
                    color: AppColors().primaryColor,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        SubHeadingTypographyCustomWidget(
                          content: userData.fullName,
                          invertColors: true,
                          textAlign: TextAlign.left,
                        ),
                        SizedBox(height: 10),
                        SubHeadingTypographyCustomWidget(
                          content: userData.rollNumber,
                          invertColors: true,
                          textAlign: TextAlign.left,
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 20),
                  SubHeadingTypographyCustomWidget(
                    content: "PKR. ${userData.balance.toString()}/-",
                    textAlign: TextAlign.left,
                  ),
                  const CaptionTypographyCustomWidget(
                      content: "Available Balance"),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

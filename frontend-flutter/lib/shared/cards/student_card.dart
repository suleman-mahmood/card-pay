import 'dart:async';

import 'package:cardpay/services/functions.dart';
import 'package:cardpay/shared/typography/caption.dart';
import 'package:cardpay/shared/typography/small_body.dart';
import 'package:cardpay/shared/typography/sub_heading.dart';
import 'package:cardpay/shared/utils/utils.dart';
import 'package:cardpay/theme/colors.dart';
import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:provider/provider.dart';
import 'package:cardpay/services/models.dart' as model;

class StudentCardCustomWidget extends StatefulWidget {
  const StudentCardCustomWidget({Key? key}) : super(key: key);

  @override
  State<StudentCardCustomWidget> createState() =>
      _StudentCardCustomWidgetState();
}

class _StudentCardCustomWidgetState extends State<StudentCardCustomWidget> {
  int secondsRemaining = 30;
  bool enableResend = false;
  late Timer timer;

  @override
  initState() {
    super.initState();
    timer = Timer.periodic(Duration(seconds: 1), (_) {
      if (secondsRemaining != 0) {
        setState(() {
          secondsRemaining--;
        });
      } else {
        setState(() {
          enableResend = true;
        });
      }
    });
  }

  @override
  dispose() {
    timer.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    // Listen to changes to the user model
    final userData = context.watch<model.User>();

    return Card(
      elevation: 15,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.all(
          Radius.circular(20),
        ),
      ),
      child: Padding(
        padding: const EdgeInsets.symmetric(
          horizontal: 0,
          vertical: 15,
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
                  top: -50,
                  child: ClipRRect(
                    borderRadius: BorderRadius.horizontal(
                        left: Radius.circular(20), right: Radius.circular(10)),
                    child: Image.asset(
                      "assets/images/student_card.png",
                    ),
                  ),
                ),
              ],
            ),

            const SizedBox(width: 10),

            // Right half of the card

            // Strip of name and roll number
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Container(
                    padding: EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      gradient: AppColors().dashboardCardGradient,
                      borderRadius: BorderRadius.horizontal(
                        left: Radius.circular(10),
                      ),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        SubHeadingTypographyCustomWidget(
                          content: userData.fullName.split(' ')[0] +
                              ' ' +
                              userData.fullName.split(' ')[1][0] +
                              '.',
                          invertColors: true,
                          textAlign: TextAlign.left,
                        ),
                        const SizedBox(height: 10),
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
                  const SizedBox(height: 10),
                  const CaptionTypographyCustomWidget(
                    content: "Available Balance",
                  ),
                  userData.pendingDeposits
                      ? Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                const SmallBodyTypographyCustomWidget(
                                  content: "Refresh balance",
                                ),
                                IconButton(
                                  icon: Icon(
                                    FontAwesomeIcons.arrowsRotate,
                                    size: 20,
                                    color: AppColors().primaryColor,
                                  ),
                                  onPressed: () async {
                                    if (!enableResend) return;
                                    await FunctionsService()
                                        .checkDepositStatus();
                                    setState(() {
                                      secondsRemaining = 30;
                                      enableResend = false;
                                    });
                                  },
                                  tooltip: "Refresh balance",
                                ),
                              ],
                            ),
                            SmallBodyTypographyCustomWidget(
                              content: "after $secondsRemaining seconds",
                            ),
                          ],
                        )
                      : const EmptyCustomWidget(),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

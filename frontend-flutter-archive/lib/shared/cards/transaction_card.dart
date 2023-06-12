import 'package:cardpay/shared/typography/medium_body.dart';
import 'package:cardpay/shared/typography/Sub_heading2.dart';
import 'package:cardpay/theme/colors.dart';
import 'package:flutter/material.dart';
import 'package:cardpay/services/models.dart' as model;
import 'package:intl/intl.dart';

class TransactionCardCustomWidget extends StatelessWidget {
  model.UserTransaction transactionData;
  final bool invertColors;
  final bool isDebit;

  TransactionCardCustomWidget({
    Key? key,
    this.invertColors = false,
    required this.transactionData,
    required this.isDebit,
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
      elevation: 5,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.all(
          Radius.circular(20),
        ),
      ),
      color: primaryColorDisplay(),
      child: Container(
        decoration: BoxDecoration(
            gradient: AppColors().dashboardCardGradient,
            borderRadius: BorderRadius.all(Radius.circular(20))),
        child: Padding(
          padding: const EdgeInsets.symmetric(
            horizontal: 15,
            vertical: 15,
          ),
          child: Row(
            children: [
              Expanded(
                // flex: 3,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    SubHeading2TypographyCustomWidget(
                      content:
                          "${isDebit ? 'To: ' + transactionData.recipientName : 'From: ' + transactionData.senderName}",
                      invertColors: true,
                      textAlign: TextAlign.start,
                    ),
                    SizedBox(height: 5),
                    MediumBodyTypographyCustomWidget(
                      content: DateFormat('kk:mm dd MMM yyyy').format(
                          DateTime.parse(transactionData.timestamp).toLocal()),
                      invertColors: true,
                    ),
                  ],
                ),
              ),
              SizedBox(width: 5),
              SubHeading2TypographyCustomWidget(
                content:
                    "${isDebit ? '-' : '+'}${transactionData.amount.toString()}",
                invertColors: true,
                isDebit: isDebit,
              ),
            ],
          ),
        ),
      ),
    );
  }
}

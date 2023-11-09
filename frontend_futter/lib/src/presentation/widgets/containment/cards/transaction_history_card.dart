import 'package:cardpay/src/presentation/widgets/boxes/all_padding.dart';
import 'package:cardpay/src/utils/constants/payment_strings.dart';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:intl/intl.dart';
import 'package:skeleton_loader/skeleton_loader.dart';
import 'package:flutter_svg/svg.dart';

class TransactionContainer extends HookWidget {
  final IconData icon = Icons.send;
  final Color iconColor = AppColors.primaryColor;

  final String senderName;
  final String recipientName;
  final String amount;
  final String currentUserName;
  final DateTime timeOfTransaction;

  final bool display;

  final bool loading;

  const TransactionContainer({
    super.key,
    required this.senderName,
    required this.recipientName,
    required this.amount,
    required this.currentUserName,
    required this.timeOfTransaction,
    this.loading = false,
    this.display = false,
  });

  @override
  Widget build(BuildContext context) {
    final inflow = useState<bool>(true);
    String formattedDate =
        DateFormat('hh:mm a - MMM d, y').format(timeOfTransaction);

    useEffect(() {
      if (currentUserName == senderName) {
        inflow.value = false;
      }
    }, []);

    Widget buildIcon() {
      return senderName != currentUserName
          ? SvgPicture.asset(
              "assets/icon/ReceivedTransaction.svg",
            )
          : SvgPicture.asset(
              "assets/icon/sentTransaction.svg",
            );
    }

    Widget buildFirstText() {
      return Padding(
        padding: const EdgeInsets.all(10),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              inflow.value ? senderName : recipientName,
              style: AppTypography.bodyText,
            ),
            if (display)
              Text(PaymentStrings.send, style: AppTypography.subHeadingBold),
            const SizedBox(width: 5),
            Text(
              formattedDate,
              style: AppTypography.bodyText.copyWith(
                color: AppColors.greyColor,
                fontSize: 12,
              ),
            ),
          ],
        ),
      );
    }

    Widget buildSecondText() {
      String _amount =
          senderName != currentUserName ? "+$amount.00" : "-$amount.00";
      return PaddingAll(
        slab: 1,
        child: Text(
          _amount,
          style: inflow.value
              ? AppTypography.transactionAmountInflow
              : AppTypography.transactionAmountOutflow,
        ),
      );
    }

    return Align(
      alignment: Alignment.center,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 3),
        padding: const EdgeInsets.symmetric(vertical: 2, horizontal: 5),
        decoration: BoxDecoration(
          //color: AppColors.secondaryColor,
          borderRadius: BorderRadius.circular(10),
          boxShadow: [
            BoxShadow(
              color: AppColors.greyColor.withOpacity(0.05),
              spreadRadius: 2,
              blurRadius: 5,
              offset: Offset(0, 4),
            ),
          ],
        ),
        child: loading
            ? SkeletonLoader(
                builder: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    buildIcon(),
                    buildFirstText(),
                    const Spacer(),
                    buildSecondText(),
                  ],
                ),
                items: 1,
                period: const Duration(seconds: 2),
                highlightColor: AppColors.greyColor,
                direction: SkeletonDirection.ltr,
              )
            : Row(
                mainAxisAlignment: MainAxisAlignment.center,
                mainAxisSize: MainAxisSize.min,
                children: [
                  buildIcon(),
                  buildFirstText(),
                  const Spacer(),
                  buildSecondText(),
                ],
              ),
      ),
    );
  }
}

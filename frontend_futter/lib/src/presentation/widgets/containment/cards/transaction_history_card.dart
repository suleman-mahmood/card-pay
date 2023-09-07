import 'package:cardpay/src/presentation/widgets/boxes/all_padding.dart';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';

class TransactionContainer extends HookWidget {
  final IconData icon = Icons.send;
  final Color inflowAmountColor = AppColors.greenColor;
  final Color outflowAmountColor = AppColors.redColor;
  final Color iconColor = AppColors.primaryColor;

  final String senderName;
  final String recipientName;
  final String amount;
  final String currentUserName;

  final bool display;

  const TransactionContainer({
    super.key,
    required this.senderName,
    required this.recipientName,
    required this.amount,
    required this.currentUserName,
    this.display = false,
  });

  @override
  Widget build(BuildContext context) {
    final inflow = useState<bool>(true);

    useEffect(() {
      if (currentUserName == senderName) {
        inflow.value = false;
      }
    }, []);

    Icon buildIcon() {
      return Icon(
        icon,
        color: iconColor,
      );
    }

    Widget buildFirstText() {
      return Padding(
        padding: const EdgeInsets.all(10),
        child: Column(
          children: [
            Text(
              inflow.value ? senderName : recipientName,
              style: AppTypography.bodyText,
            ),
            if (display) Text('send', style: AppTypography.subHeadingBold),
          ],
        ),
      );
    }

    Widget buildSecondText() {
      return PaddingAll(
        slab: 1,
        child: Text(
          amount,
          style: AppTypography.bodyText.copyWith(
            color: inflow.value ? inflowAmountColor : outflowAmountColor,
          ),
        ),
      );
    }

    return Align(
      alignment: Alignment.center,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 4),
        padding: const EdgeInsets.symmetric(vertical: 3, horizontal: 5),
        decoration: BoxDecoration(
          color: AppColors.secondaryColor,
          borderRadius: BorderRadius.circular(10),
          boxShadow: [
            BoxShadow(
              color: AppColors.greyColor.withOpacity(0.2),
              spreadRadius: 2,
              blurRadius: 5,
              offset: Offset(0, 4),
            ),
          ],
        ),
        child: Row(
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

import 'package:cardpay/src/presentation/widgets/boxes/all_padding.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/numpad_buttons.dart';

class PaymentEntry extends HookWidget {
  final TextEditingController controller;
  final List<String> buttons = ['1500', '3000', '1500', '1000', '7000', '5000'];

  PaymentEntry({super.key, required this.controller});

  @override
  Widget build(BuildContext context) {
    final selectedButton = useState<String?>(null);

    Widget PaymentButton(String amount) {
      return OutlinedButton(
        style: OutlinedButton.styleFrom(
          side: BorderSide(color: AppColors.greyColor),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(10),
          ),
        ),
        onPressed: () {
          selectedButton.value = amount;
          controller.text = amount;
        },
        child: Padding(
          padding: EdgeInsets.fromLTRB(8, 8, 8, 8),
          child: Text(amount, style: AppTypography.bodyText),
        ),
      );
    }

    Widget PaymentValueListenableBuilder() {
      useEffect(() {
        return () {
          controller.dispose();
        };
      }, []);
      return PaddingAll(
        slab: 1,
        child: ValueListenableBuilder(
          valueListenable: controller,
          builder: (context, value, child) {
            final text = controller.text.isEmpty ? '_ _ _ _' : controller.text;

            return SizedBox(
              height: 48,
              child: ListView.separated(
                shrinkWrap: true,
                itemCount: text.length,
                separatorBuilder: (context, index) => HeightBox(slab: 2),
                scrollDirection: Axis.horizontal,
                itemBuilder: (context, index) {
                  return Text(text[index],
                      style: AppTypography.mainHeadingGrey);
                },
              ),
            );
          },
        ),
      );
    }

    return Column(
      children: [
        PaymentValueListenableBuilder(),
        HeightBox(slab: 3),
        Wrap(
          spacing: 9,
          runSpacing: 9,
          alignment: WrapAlignment.spaceEvenly,
          crossAxisAlignment: WrapCrossAlignment.center,
          children: buttons.map((amount) => PaymentButton(amount)).toList(),
        ),
        HeightBox(slab: 2),
        NumPad(
          controller: controller,
          buttonColor: AppColors.greyColor,
        ),
      ],
    );
  }
}

class PaymentValueListenableBuilder extends HookWidget {
  final TextEditingController controller;

  const PaymentValueListenableBuilder({
    super.key,
    required this.controller,
  });

  @override
  Widget build(BuildContext context) {
    return PaymentValueListenableBuilder(
      controller: controller,
    );
  }
}

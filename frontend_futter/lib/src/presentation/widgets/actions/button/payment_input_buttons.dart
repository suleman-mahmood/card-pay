import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/screen_utills/screen_util.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/numpad_buttons.dart';

class PaymentEntry extends HookWidget {
  final TextEditingController controller;
  final List<String> buttons = [
    '100',
    '10000',
    '1500',
    '50000',
    '1000',
    '15000',
    '30000',
    '5000'
  ];

  PaymentEntry({super.key, required this.controller});

  @override
  Widget build(BuildContext context) {
    final selectedButton = useState<String?>(null);

    // Local PaymentButton widget
    Widget PaymentButton(String amount) {
      final isSelected = selectedButton.value == amount;
      final buttonColor =
          isSelected ? AppColors.primaryColor : AppColors.bluishColor;
      final textColor =
          isSelected ? AppColors.secondaryColor : AppColors.primaryColor;

      return ElevatedButton(
        onPressed: () {
          selectedButton.value = amount;
          controller.text = amount;
        },
        style: ButtonStyle(
          backgroundColor: MaterialStateProperty.all<Color>(buttonColor),
        ),
        child: Text(
          amount,
          style: TextStyle(color: textColor),
        ),
      );
    }

    // Local PaymentValueListenableBuilder widget
    Widget PaymentValueListenableBuilder() {
      return Padding(
        padding: EdgeInsets.all(10),
        child: ValueListenableBuilder(
          valueListenable: controller,
          builder: (context, value, child) {
            final text = controller.text.isEmpty ? '____' : controller.text;
            return SizedBox(
              height: ScreenUtil.blockSizeVertical(context) * 5,
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
          spacing: 6,
          runSpacing: 6,
          alignment: WrapAlignment.spaceEvenly,
          crossAxisAlignment: WrapCrossAlignment.center,
          children: buttons.map((amount) => PaymentButton(amount)).toList(),
        ),
        HeightBox(slab: 2), // NumPad
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
    return Padding(
      padding: EdgeInsets.all(ScreenUtil.blockSizeHorizontal(context) * 2),
      child: ValueListenableBuilder(
        valueListenable: controller,
        builder: (context, value, child) {
          final text = controller.text.isEmpty ? '____' : controller.text;
          return SizedBox(
            height: ScreenUtil.blockSizeVertical(context) * 5,
            child: ListView.separated(
              shrinkWrap: true,
              itemCount: text.length,
              separatorBuilder: (context, index) =>
                  SizedBox(width: ScreenUtil.blockSizeHorizontal(context) * 2),
              scrollDirection: Axis.horizontal,
              itemBuilder: (context, index) {
                return Text(text[index],
                    style: TextStyle(
                        fontSize: ScreenUtil.blockSizeHorizontal(context) * 10,
                        fontWeight: FontWeight.bold,
                        fontFamily: 'popins'));
              },
            ),
          );
        },
      ),
    );
  }
}

class PaymentButton extends StatelessWidget {
  final BuildContext context;
  final String amount;
  final ValueNotifier<String?> selectedButton;
  final TextEditingController controller;

  const PaymentButton(
      this.context, this.amount, this.selectedButton, this.controller,
      {super.key});

  @override
  Widget build(BuildContext context) {
    final isSelected = selectedButton.value == amount;
    final buttonColor = isSelected
        ? AppColors.primaryColor
        : const Color.fromARGB(255, 224, 234, 246);
    final textColor =
        isSelected ? AppColors.secondaryColor : AppColors.primaryColor;

    return ElevatedButton(
      onPressed: () {
        selectedButton.value = amount;
        controller.text = amount;
      },
      style: ButtonStyle(
        backgroundColor: MaterialStateProperty.all<Color>(buttonColor),
      ),
      child: Text(
        amount,
        style: TextStyle(color: textColor),
      ),
    );
  }
}

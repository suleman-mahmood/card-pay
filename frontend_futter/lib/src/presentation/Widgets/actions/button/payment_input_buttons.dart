import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/screen_utills/screen_util.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';
import 'package:frontend_futter/src/presentation/widgets/actions/button/numpad_buttons.dart';

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

  PaymentEntry({required this.controller});

  @override
  Widget build(BuildContext context) {
    final selectedButton = useState<String?>(null);

    return Column(
      children: [
        PaymentValueListenableBuilder(
          controller: controller,
        ),
        SizedBox(height: ScreenUtil.blockSizeVertical(context) * 3),
        Wrap(
          spacing: ScreenUtil.blockSizeHorizontal(context) * 2,
          runSpacing: ScreenUtil.blockSizeVertical(context) * 2,
          alignment: WrapAlignment.spaceEvenly,
          crossAxisAlignment: WrapCrossAlignment.center,
          children: buttons
              .map((amount) =>
                  PaymentButton(context, amount, selectedButton, controller))
              .toList(),
        ),
        SizedBox(height: ScreenUtil.blockSizeVertical(context) * 2),
        // NumPad
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

  PaymentValueListenableBuilder({
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
          return Container(
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

  PaymentButton(
      this.context, this.amount, this.selectedButton, this.controller);

  @override
  Widget build(BuildContext context) {
    final isSelected = selectedButton.value == amount;
    final buttonColor = isSelected
        ? AppColors.primaryColor
        : Color.fromARGB(255, 224, 234, 246);
    final textColor =
        isSelected ? AppColors.secondaryColor : AppColors.primaryColor;

    return ElevatedButton(
      onPressed: () {
        selectedButton.value = amount;
        controller.text = amount;
      },
      child: Text(
        amount,
        style: TextStyle(color: textColor),
      ),
      style: ButtonStyle(
        backgroundColor: MaterialStateProperty.all<Color>(buttonColor),
      ),
    );
  }
}

import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/screen_utills/screen_util.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';

class CustomBottomSheet extends HookWidget {
  const CustomBottomSheet({
    Key? key,
    required this.checked1,
    required this.checked2,
    required this.checked3,
    required this.checked4,
  }) : super(key: key);

  final ValueNotifier<bool> checked1;
  final ValueNotifier<bool> checked2;
  final ValueNotifier<bool> checked3;
  final ValueNotifier<bool> checked4;

  @override
  Widget build(BuildContext context) {
    return Material(
      elevation: 8,
      borderRadius: BorderRadius.only(
        topLeft: Radius.circular(ScreenUtil.blockSizeHorizontal(context) * 6),
        topRight: Radius.circular(ScreenUtil.blockSizeHorizontal(context) * 6),
      ),
      child: Container(
        height: ScreenUtil.blockSizeVertical(context) * 40,
        color: Theme.of(context).colorScheme.background,
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: <Widget>[
              buildTitle(context),
              buildCheckBoxes(context),
              buildButton(context),
              SizedBox(
                height: ScreenUtil.blockSizeVertical(context) * 2,
              )
            ],
          ),
        ),
      ),
    );
  }

  Text buildTitle(BuildContext context) {
    return Text(
      'BottomSheet',
      style: Theme.of(context).textTheme.titleLarge,
    );
  }

  Column buildCheckBoxes(BuildContext context) {
    return Column(
      children: [
        _buildCheckboxListTile(
            context, "Checkbox 1", Icons.accessibility, checked1),
        _buildCheckboxListTile(context, "Checkbox 2", Icons.alarm, checked2),
        _buildCheckboxListTile(
            context, "Checkbox 3", Icons.battery_alert, checked3),
        _buildCheckboxListTile(context, "Checkbox 4", Icons.cake, checked4),
      ],
    );
  }

  PrimaryButton buildButton(BuildContext context) {
    return PrimaryButton(
      color: Theme.of(context).primaryColor,
      text: 'Done',
      onPressed: () {
        Navigator.pop(context);
      },
    );
  }

  CheckboxListTile _buildCheckboxListTile(BuildContext context, String title,
      IconData icon, ValueNotifier<bool> checked) {
    return CheckboxListTile(
      title: Text(title,
          style: TextStyle(fontSize: ScreenUtil.textMultiplier(context) * 2)),
      value: checked.value,
      onChanged: (bool? value) {
        checked.value = value ?? false;
      },
      secondary: Icon(icon, size: ScreenUtil.blockSizeHorizontal(context) * 6),
    );
  }
}

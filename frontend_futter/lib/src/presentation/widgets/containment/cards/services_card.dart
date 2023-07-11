import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/screen_utills/screen_util.dart';

class CustomBox extends StatelessWidget {
  final String imagePath;
  final String text;
  final PageRouteInfo route;

  const CustomBox({
    Key? key,
    required this.imagePath,
    required this.text,
    required this.route,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Material(
      elevation: 8.0,
      borderRadius: BorderRadius.circular(10),
      child: InkWell(
        onTap: () => context.router.push(route),
        child: buildStack(context),
      ),
    );
  }

  Stack buildStack(BuildContext context) {
    return Stack(
      alignment: Alignment.bottomLeft,
      children: <Widget>[
        buildClipRRect(context),
        buildTextPadding(context),
      ],
    );
  }

  ClipRRect buildClipRRect(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(15),
      child: Container(
        color: Colors.transparent,
        height: ScreenUtil.blockSizeVertical(context) * 16.25,
        width: ScreenUtil.blockSizeHorizontal(context) * 36.5,
        child: Image.asset(
          imagePath,
          fit: BoxFit.cover,
        ),
      ),
    );
  }

  Padding buildTextPadding(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(ScreenUtil.blockSizeVertical(context) * 1),
      child: Text(
        text,
        style: TextStyle(
          fontSize: ScreenUtil.textMultiplier(context) * 2.5,
          fontWeight: FontWeight.bold,
          color: Colors.white,
        ),
      ),
    );
  }
}

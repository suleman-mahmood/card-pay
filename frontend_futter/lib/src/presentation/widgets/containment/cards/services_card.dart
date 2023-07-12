import 'package:cardpay/src/config/themes/colors.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';

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
    final deviceHeight = MediaQuery.of(context).size.height;
    final deviceWidth = MediaQuery.of(context).size.width;

    ClipRRect buildClipRRect() {
      return ClipRRect(
        borderRadius: BorderRadius.circular(15),
        child: Container(
          color: Colors.transparent,
          height: deviceHeight * 0.165,
          width: deviceWidth * 0.41,
          child: Image.asset(
            imagePath,
            fit: BoxFit.cover,
          ),
        ),
      );
    }

    Padding buildTextPadding() {
      return Padding(
        padding: EdgeInsets.all(8),
        child: Text(text, style: AppTypography.mainHeadingWhite),
      );
    }

    Stack buildStack() {
      return Stack(
        alignment: Alignment.bottomLeft,
        children: <Widget>[
          buildClipRRect(),
          buildTextPadding(),
        ],
      );
    }

    return Material(
      elevation: 8.0,
      borderRadius: BorderRadius.circular(10),
      child: InkWell(
        onTap: () => context.router.push(route),
        child: buildStack(),
      ),
    );
  }
}

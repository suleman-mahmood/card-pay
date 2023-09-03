import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/boxes/all_padding.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class CustomBox extends StatelessWidget {
  final String imagePath;
  final String text;
  final PageRouteInfo? route;
  final bool isDisabled;
  final String disabledMessage;

  const CustomBox({
    Key? key,
    required this.imagePath,
    required this.text,
    this.route,
    this.isDisabled = false,
    this.disabledMessage = "Coming Soon",
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final deviceHeight = MediaQuery.of(context).size.height;
    final deviceWidth = MediaQuery.of(context).size.width;

    final userCubit = BlocProvider.of<UserCubit>(context);

    ClipRRect buildClipRRect() {
      return ClipRRect(
        borderRadius: BorderRadius.circular(15),
        child: Container(
          color: Colors.transparent,
          height: deviceHeight * 0.165,
          width: deviceWidth * 0.42,
          child: Image.asset(
            imagePath,
            fit: BoxFit.cover,
          ),
        ),
      );
    }

    Widget buildTextPadding() {
      return PaddingAll(
        slab: 1,
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

    onTap() async {
      if (!isDisabled) {
        userCubit.initialize();
        context.router.push(route!);
      }
      // else {
      //   ScaffoldMessenger.of(context).showSnackBar(
      //     SnackBar(content: Text(disabledMessage)),
      //   );
      // }
    }

    return Material(
      elevation: 8.0,
      borderRadius: BorderRadius.circular(10),
      child: InkWell(
        onTap: onTap,
        child: buildStack(),
      ),
    );
  }
}

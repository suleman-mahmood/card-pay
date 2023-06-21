// import 'package:auto_route/auto_route.dart';
// import 'package:flutter/material.dart';
// import 'package:flutter_hooks/flutter_hooks.dart';
// import 'package:frontend_futter/src/config/router/app_router.dart';

// import 'dart:math';

// import 'package:frontend_futter/src/config/themes/colors.dart';

// @RoutePage()
// class SplashView extends HookWidget {
//   const SplashView({Key? key}) : super(key: key);

//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       body: SafeArea(
//         child: GradientPage(),
//       ),
//     );
//   }
// }

// class GradientPage extends StatefulWidget {
//   @override
//   _GradientPageState createState() => _GradientPageState();
// }

// class _GradientPageState extends State<GradientPage>
//     with TickerProviderStateMixin {
//   late final AnimationController _controller;
//   late final Animation<double> _frontAnimation;
//   late final Animation<double> _backAnimation;

//   @override
//   void initState() {
//     super.initState();

//     _controller = AnimationController(
//       duration: const Duration(seconds: 5),
//       vsync: this,
//     );

//     _frontAnimation = TweenSequence<double>([
//       TweenSequenceItem(
//         tween: Tween(begin: 0.0, end: pi / 2)
//             .chain(CurveTween(curve: Curves.easeIn)),
//         weight: 0.5,
//       ),
//     ]).animate(_controller);

//     _backAnimation = TweenSequence<double>([
//       TweenSequenceItem(
//         tween: ConstantTween<double>(pi / 2),
//         weight: 0.5,
//       ),
//       TweenSequenceItem(
//         tween: Tween(begin: pi / 2, end: 0.0)
//             .chain(CurveTween(curve: Curves.easeOut)),
//         weight: 0.5,
//       ),
//     ]).animate(_controller);

//     _controller.repeat();

//     // Navigate to the next page after 5 to 7 seconds
//     Future.delayed(Duration(seconds: 8), () {
//       context.router.push(IntroRoute());
//     });
//   }

//   @override
//   Widget build(BuildContext context) {
//     return Container(
//       decoration: BoxDecoration(
//         gradient: LinearGradient(
//           colors: [
//             AppColors.animationHomeGradient.colors[0],
//             AppColors.animationHomeGradient.colors[1],
//             AppColors.animationHomeGradient.colors[2],
//           ],
//           begin: Alignment.topCenter,
//           end: Alignment.bottomCenter,
//           stops: [0.0417, 1.0, 1.0],
//         ),
//       ),
//       child: Center(
//         child: Stack(
//           alignment: Alignment.center,
//           children: [
//             AnimatedBuilder(
//               animation: _backAnimation,
//               child: Container(
//                 child: Image.asset('assets/images/logo.png'),
//               ),
//               builder: (context, child) {
//                 return Transform(
//                   alignment: FractionalOffset.center,
//                   transform: Matrix4.identity()
//                     ..setEntry(3, 2, 0.002)
//                     ..rotateY(_backAnimation.value),
//                   child: child,
//                 );
//               },
//             ),
//             AnimatedBuilder(
//               animation: _frontAnimation,
//               child: Container(
//                 child: Image.asset('assets/images/logo.png'),
//               ),
//               builder: (context, child) {
//                 return Transform(
//                   alignment: FractionalOffset.center,
//                   transform: Matrix4.identity()
//                     ..setEntry(3, 2, 0.002)
//                     ..rotateY(_frontAnimation.value),
//                   child: child,
//                 );
//               },
//             ),
//           ],
//         ),
//       ),
//     );
//   }

//   @override
//   void dispose() {
//     _controller.dispose();
//     super.dispose();
//   }
// }

import 'package:auto_route/auto_route.dart';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/router/app_router.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';
import 'package:frontend_futter/src/config/themes/screen_util.dart';

@RoutePage()
class SplashView extends HookWidget {
  const SplashView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: GestureDetector(
          onTap: () {
            context.router.push(IntroRoute());
          },
          child: Container(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [
                  AppColors.animationHomeGradient.colors[0],
                  AppColors.animationHomeGradient.colors[1],
                  AppColors.animationHomeGradient.colors[2],
                ],
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                stops: [0.0417, 1.0, 1.0],
              ),
            ),
            child: Center(
              child: LayoutBuilder(
                builder: (ctx, constraints) {
                  return Image.asset(
                    'assets/images/logo.png',
                    height: constraints.maxHeight * 0.5,
                    width: constraints.maxWidth * 0.5,
                  );
                },
              ),
            ),
          ),
        ),
      ),
    );
  }
}

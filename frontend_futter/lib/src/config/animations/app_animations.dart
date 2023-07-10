import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

Animation<Offset> useSlideAnimation(
    {required Offset begin, required Offset end, required Duration duration}) {
  final controller = useAnimationController(duration: duration)..forward();

  return Tween<Offset>(
    begin: begin,
    end: end,
  ).animate(
    CurvedAnimation(
      parent: controller,
      curve: Curves.easeInOut,
    ),
  );
}

Animation<double> useFadeAnimation(
    {required double begin, required double end, required Duration duration}) {
  final controller = useAnimationController(duration: duration)..forward();

  return Tween<double>(
    begin: begin,
    end: end,
  ).animate(
    CurvedAnimation(
      parent: controller,
      curve: Curves.easeInOut,
    ),
  );
}

Animation<double> useRotationAnimation(
    {required double begin, required double end, required Duration duration}) {
  final controller = useAnimationController(duration: duration)..forward();

  return Tween<double>(
    begin: begin,
    end: end,
  ).animate(
    CurvedAnimation(
      parent: controller,
      curve: Curves.easeInOut,
    ),
  );
}

Animation<double> useScaleAnimation(
    {required double begin, required double end, required Duration duration}) {
  final controller = useAnimationController(duration: duration)..forward();

  return Tween<double>(
    begin: begin,
    end: end,
  ).animate(
    CurvedAnimation(
      parent: controller,
      curve: Curves.easeInOut,
    ),
  );
}


// SlideTransition(
//   position: _imageAnimationOffset,
//   child: Image.asset('assets/images/transection.png'),
// ),

// FadeTransition(
//   opacity: _fadeAnimation,
//   child: YourWidget(),
// ),

// RotationTransition(
//   turns: _rotationAnimation,
//   child: YourWidget(),
// ),

// ScaleTransition(
//   scale: _scaleAnimation,
//   child: YourWidget(),
// ),
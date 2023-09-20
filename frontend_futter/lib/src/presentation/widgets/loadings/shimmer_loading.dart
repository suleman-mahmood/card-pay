import 'package:cardpay/src/config/themes/colors.dart';
import 'package:flutter/material.dart';

class ShimmerLoading extends StatefulWidget {
  final Widget child;

  const ShimmerLoading({
    Key? key,
    required this.child,
  });

  @override
  State<ShimmerLoading> createState() => _ShimmerLoadingState();
}

class _ShimmerLoadingState extends State<ShimmerLoading>
    with SingleTickerProviderStateMixin {
  late AnimationController _shimmerController;

  @override
  void initState() {
    super.initState();
    _shimmerController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1000),
    )..repeat();
  }

  @override
  void dispose() {
    _shimmerController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _shimmerController,
      builder: (context, child) {
        final progress = _shimmerController.value;
        return ShaderMask(
          blendMode: BlendMode.srcATop,
          shaderCallback: (bounds) {
            return LinearGradient(
              colors: [
                AppColors.lightGreyColor,
                Color.fromARGB(255, 213, 212, 212),
                AppColors.lightGreyColor,
              ],
              stops: [-0.2, 0.5 + progress * 0.2, 0.5 + progress * 0.2],
              begin: Alignment(0.5 - progress * 2.0, -0.3),
              end: Alignment(1.0, 0.3),
              tileMode: TileMode.clamp,
            ).createShader(bounds);
          },
          child: child,
        );
      },
      child: widget.child,
    );
  }
}

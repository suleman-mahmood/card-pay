import 'package:flutter/material.dart';
import 'package:shimmer/shimmer.dart';

class FieldShimmer extends StatelessWidget {
  final double width;
  final double height;

  FieldShimmer({this.width = double.infinity, this.height = 24.0});

  @override
  Widget build(BuildContext context) {
    return Shimmer.fromColors(
      baseColor: Colors.grey[300]!,
      highlightColor: Colors.grey[100]!,
      child: Container(
        width: width,
        height: height,
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(12),
        ),
      ),
    );
  }
}

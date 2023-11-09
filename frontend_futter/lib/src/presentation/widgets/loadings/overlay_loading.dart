import 'package:flutter/material.dart';

class OverlayLoading extends StatelessWidget {
  final bool inSafeArea;

  const OverlayLoading({super.key, this.inSafeArea = true});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: MediaQuery.of(context).size.height,
      width: MediaQuery.of(context).size.width,
      child: Stack(
        children: [
          Container(
            color: Colors.grey.withOpacity(0.6),
          ),
          const Center(
            child: CircularProgressIndicator(),
          ),
        ],
      ),
    );
  }
}

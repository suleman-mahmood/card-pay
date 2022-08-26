import 'package:flutter/widgets.dart';

class EmptyCustomWidget extends StatelessWidget {
  const EmptyCustomWidget({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return const SizedBox.shrink();
  }
}

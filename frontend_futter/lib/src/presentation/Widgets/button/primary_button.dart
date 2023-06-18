import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class CustomButton extends HookWidget {
  final String text;
  final VoidCallback onPressed;
  final double width;
  final double height;

  const CustomButton({
    required this.text,
    required this.onPressed,
    this.width = 272,
    this.height = 48,
  });

  EdgeInsets calculateMargin(BuildContext context) {
    return EdgeInsets.only(
      top: 0.03 * MediaQuery.of(context).size.height,
      left: 0.05 * MediaQuery.of(context).size.width,
    );
  }

  @override
  Widget build(BuildContext context) {
    final margin = useMemoized(() => calculateMargin(context));
    final isHovered = useState(false);

    return Container(
      width: width,
      height: height,
      margin: margin,
      child: MouseRegion(
        onEnter: (_) => isHovered.value = true,
        onExit: (_) => isHovered.value = false,
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 200),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(10),
            color: isHovered.value
                ? AppColors().primaryColor.withOpacity(0.2)
                : AppColors().primaryColor,
          ),
          child: ElevatedButton(
            onPressed: onPressed,
            child: Container(
              constraints: BoxConstraints.expand(),
              alignment: Alignment.center,
              padding: EdgeInsets.symmetric(vertical: 8, horizontal: 16),
              child: Text(
                text,
                style: AppColors().headingFont.copyWith(
                      color: AppColors().secondaryColor,
                    ),
              ),
            ),
            style: ButtonStyle(
              padding: MaterialStateProperty.all<EdgeInsets>(EdgeInsets.zero),
              backgroundColor:
                  MaterialStateProperty.all<Color>(Colors.transparent),
              shape: MaterialStateProperty.all<RoundedRectangleBorder>(
                RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}

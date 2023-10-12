import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/screen_utills/screen_util.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/domain/models/event.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/layout/basic_view_layout.dart';
import 'package:flutter/material.dart';
import 'package:qr_flutter/qr_flutter.dart';

@RoutePage()
class EventAttendanceQrView extends StatelessWidget {
  final Event event;

  const EventAttendanceQrView({
    super.key,
    required this.event,
  });

  @override
  Widget build(BuildContext context) {
    return BasicViewLayout(
      headerTitle: "Attendance QR",
      backgroundColor: AppColors.teal,
      children: [
        Align(
          child: Text(
            event.name,
            style: AppTypography.mainHeadingWhite,
          ),
        ),
        const HeightBox(slab: 2),
        Align(
          child: QrImageView(
            backgroundColor: AppColors.secondaryColor,
            data: event.attendanceQr ?? '',
            version: QrVersions.auto,
            size: ScreenUtil.screenWidth(context) * (3 / 4),
          ),
        ),
      ],
    );
  }
}

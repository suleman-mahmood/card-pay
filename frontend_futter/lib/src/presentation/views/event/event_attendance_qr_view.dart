import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/screen_utills/screen_util.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/domain/models/event.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/layout/basic_view_layout.dart';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
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
      headerTitle: "",
      headerColor: AppColors.blackColor,
      backgroundColor: AppColors.secondaryColor,
      centered: true,
      children: [
        Container(
          alignment: Alignment.center,
          width: ScreenUtil.screenWidth(context) * 0.9,
          decoration: BoxDecoration(
            color: AppColors.secondaryColor,
            borderRadius: BorderRadius.circular(16),
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Stack(
                children: [
                  Column(
                    children: [
                      Stack(
                        children: [
                          Container(
                            height: ScreenUtil.screenHeight(context) * 0.25,
                            decoration: BoxDecoration(
                              color: AppColors.secondaryColor,
                              borderRadius: BorderRadius.only(
                                topLeft: Radius.circular(16),
                                topRight: Radius.circular(16),
                              ),
                              border: // give it a dashed border throughout
                                  Border.all(
                                color: AppColors.blackColor.withOpacity(0.5),
                                width: 1,
                                style: BorderStyle.solid,
                              ),
                              image: DecorationImage(
                                image: NetworkImage(event.imageUrl),
                                fit: BoxFit.cover,
                              ),
                            ),
                          ),
                          Container(
                            height: ScreenUtil.screenHeight(context) * 0.25,
                            width: ScreenUtil.screenWidth(context) * 0.9,
                            padding: EdgeInsets.fromLTRB(16, 20, 16, 30),
                            decoration: BoxDecoration(
                              color: AppColors.blackColor.withOpacity(0.5),
                              borderRadius: BorderRadius.only(
                                topLeft: Radius.circular(16),
                                topRight: Radius.circular(16),
                              ),
                            ),
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.start,
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  event.name,
                                  maxLines: 1,
                                  overflow: TextOverflow.ellipsis,
                                  style: TextStyle(
                                    color: AppColors.secondaryColor,
                                    fontSize: 26,
                                    fontWeight: FontWeight.w800,
                                  ),
                                ),
                                const HeightBox(slab: 2),
                                Row(
                                  mainAxisAlignment:
                                      MainAxisAlignment.spaceBetween,
                                  crossAxisAlignment: CrossAxisAlignment.center,
                                  children: [
                                    Column(
                                      crossAxisAlignment:
                                          CrossAxisAlignment.start,
                                      children: [
                                        Text(
                                          'Location\n${event.venue}',
                                          style: TextStyle(
                                            color: AppColors.secondaryColor,
                                            fontSize: 14,
                                            fontWeight: FontWeight.w800,
                                          ),
                                        ),
                                        const HeightBox(slab: 4),
                                        Text(
                                          'Rs.${event.registrationFee}',
                                          style: TextStyle(
                                            color: AppColors.secondaryColor,
                                            fontSize: 24,
                                            fontWeight: FontWeight.w300,
                                          ),
                                        ),
                                      ],
                                    ),
                                    Column(
                                      crossAxisAlignment:
                                          CrossAxisAlignment.start,
                                      children: [
                                        const HeightBox(slab: 4),
                                        Text(
                                          'Date \n${DateFormat.yMMMd().format(event.eventStartTimestamp)}',
                                          style: TextStyle(
                                            color: AppColors.secondaryColor,
                                            fontSize: 14,
                                            fontWeight: FontWeight.w400,
                                          ),
                                        ),
                                        const HeightBox(slab: 1),
                                        Text(
                                          'Time\n${event.eventStartTimestamp.hour}:${event.eventStartTimestamp.minute}',
                                          style: TextStyle(
                                            color: AppColors.secondaryColor,
                                            fontSize: 14,
                                            fontWeight: FontWeight.w400,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ],
                                )
                              ],
                            ),
                          )
                        ],
                      ),
                      Container(
                        padding: EdgeInsets.fromLTRB(16, 30, 16, 30),
                        decoration: BoxDecoration(
                          color: AppColors.secondaryColor,
                          borderRadius: BorderRadius.only(
                            bottomLeft: Radius.circular(16),
                            bottomRight: Radius.circular(16),
                          ),
                          boxShadow: [
                            BoxShadow(
                              color: Colors.black.withOpacity(0.05),
                              spreadRadius: 5,
                              blurRadius: 5,
                              offset:
                                  Offset(0, 2), // changes position of shadow
                            ),
                          ],
                          border: // give it a dashed border throughout
                              Border.all(
                            color: AppColors.blackColor.withOpacity(0.5),
                            width: 1,
                            style: BorderStyle.solid,
                          ),
                        ),
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          crossAxisAlignment: CrossAxisAlignment.center,
                          children: [
                            Text(
                              "Scan this QR",
                              style: TextStyle(
                                color: AppColors.blackColor,
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            Text(
                              "to check in",
                              style: TextStyle(
                                color: AppColors.blackColor,
                                fontSize: 16,
                                fontWeight: FontWeight.w300,
                              ),
                            ),
                            const HeightBox(slab: 2),
                            Align(
                              child: QrImageView(
                                backgroundColor: AppColors.secondaryColor,
                                data: event.attendanceQr ?? '',
                                version: QrVersions.auto,
                                size: ScreenUtil.screenWidth(context) * (3 / 8),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                  Positioned(
                    // a circle in the left centre
                    left: -ScreenUtil.screenWidth(context) * 0.1,
                    top: ScreenUtil.screenHeight(context) * 0.2,
                    child: Container(
                      height: ScreenUtil.screenHeight(context) * 0.1,
                      width: ScreenUtil.screenHeight(context) * 0.1,
                      decoration: BoxDecoration(
                        color: AppColors.secondaryColor,
                        borderRadius: BorderRadius.circular(1000),
                        border: Border.all(
                          color: AppColors.blackColor.withOpacity(0.5),
                          width: 1,
                          style: BorderStyle.solid,
                        ),
                      ),
                    ),
                  ),
                  Positioned(
                    // a circle in the left centre
                    right: -ScreenUtil.screenWidth(context) * 0.1,
                    top: ScreenUtil.screenHeight(context) * 0.2,
                    child: Container(
                      height: ScreenUtil.screenHeight(context) * 0.1,
                      width: ScreenUtil.screenHeight(context) * 0.1,
                      decoration: BoxDecoration(
                        color: AppColors.secondaryColor,
                        borderRadius: BorderRadius.circular(1000),
                        border: Border.all(
                          color: AppColors.blackColor.withOpacity(0.5),
                          width: 1,
                          style: BorderStyle.solid,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
              const HeightBox(slab: 4),
            ],
          ),
        ),
        Container(
          height: ScreenUtil.screenHeight(context) * 0.2,
          child: SingleChildScrollView(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  "Event Details",
                  style: TextStyle(
                    color: AppColors.blackColor,
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                const HeightBox(slab: 1),
                Text(
                  event.description,
                  style: TextStyle(
                    color: AppColors.blackColor,
                    fontSize: 16,
                    fontWeight: FontWeight.w300,
                  ),
                ),
              ],
            ),
          ),
        )
      ],
    );
  }
}

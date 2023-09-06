import 'dart:convert';

import 'package:camera/camera.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/all_padding.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/boxes/horizontal_padding.dart';
import 'package:cardpay/src/presentation/widgets/loadings/overlay_loading.dart';
import 'package:cardpay/src/presentation/widgets/navigations/top_navigation.dart';
import 'package:cardpay/src/utils/constants/event_codes.dart';
import 'package:cardpay/src/utils/pretty_logs.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:qr_code_dart_scan/qr_code_dart_scan.dart';

@RoutePage()
class QrView extends HookWidget {
  const QrView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final controller = QRCodeDartScanController();

    final qrValue = useState<String>("");
    final cameraAspectRatio = useState<double>(9 / 16);

    useEffect(() {
      initializeCameras() async {
        final cameras = await availableCameras();
        if (cameras.isEmpty) {
          return;
        }

        final camera = cameras.first;

        final controller = CameraController(
          camera,
          ResolutionPreset.high,
        );

        await controller.initialize();

        printWarning(controller.value.aspectRatio.toString());

        cameraAspectRatio.value = controller.value.aspectRatio;
      }

      // initializeCameras();
    }, []);

    return SafeArea(
      child: Scaffold(
        body: Stack(
          children: [
            AspectRatio(
              aspectRatio: cameraAspectRatio.value,
              child: QRCodeDartScanView(
                scanInvertedQRCode: true,
                typeScan: TypeScan.live,
                controller: controller,
                onCapture: (Result result) {
                  qrValue.value = result.text;
                  Map<String, dynamic> jsonMap = {};
                  try {
                    jsonMap = json.decode(result.text);
                  } on FormatException catch (e) {
                    jsonMap["name"] = "Unknown QR";
                    jsonMap["qr_id"] = '';
                  }

                  if (controller.scanEnabled) {
                    controller.setScanEnabled(false);
                    context.router
                        .push(SendRoute(
                      uniqueIdentifier: jsonMap["name"],
                      qrId: jsonMap["qr_id"],
                    ))
                        .then(
                      (_) {
                        controller.setScanEnabled(true);
                      },
                    );
                  }
                },
              ),
            ),
            PaddingAll(
              slab: 5,
              child: Align(
                alignment: Alignment.bottomCenter,
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: [
                    Text('Scan QR', style: AppTypography.mainHeadingWhite),
                    HeightBox(slab: 1),
                    Text(
                      'Place the QR code close to your phone',
                      style: AppTypography.headingFont,
                      textAlign: TextAlign.center,
                    ),
                  ],
                ),
              ),
            ),
            PaddingHorizontal(slab: 2, child: Header(title: '')),
          ],
        ),
      ),
    );
  }
}

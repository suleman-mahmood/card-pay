import 'dart:convert';

import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/boxes/all_padding.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/boxes/horizontal_padding.dart';
import 'package:cardpay/src/presentation/widgets/navigations/top_navigation.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:qr_code_scanner/qr_code_scanner.dart';

@RoutePage()
class QrView extends HookWidget {
  QrView({Key? key}) : super(key: key);

  final GlobalKey qrKey = GlobalKey(debugLabel: 'QR');
  QRViewController? controller;

  @override
  Widget build(BuildContext context) {
    final cameraAspectRatio = useState<double>(9 / 16);

    void _onQRViewCreated(QRViewController controller) {
      this.controller = controller;
      controller.scannedDataStream.listen((scanData) {
        final qrValue = scanData.code ?? '';

        Map<String, dynamic> jsonMap = {};
        try {
          jsonMap = json.decode(qrValue);
        } on FormatException catch (_) {
          jsonMap["name"] = "Unknown QR";
          jsonMap["qr_id"] = '';
          jsonMap["v"] = 0;
        } on TypeError catch (_) {
          jsonMap["name"] = "Unknown QR";
          jsonMap["qr_id"] = '';
          jsonMap["v"] = 0;
        }

        if (jsonMap["v"] != 1) {
          jsonMap["name"] = "Unknown QR";
          jsonMap["qr_id"] = '';
          jsonMap["v"] = 0;
        }

        controller.pauseCamera();
        context.router
            .push(SendRoute(
          uniqueIdentifier: jsonMap["name"],
          qrId: jsonMap["qr_id"],
          v: jsonMap["v"],
          isQr: true,
        ))
            .then(
          (_) {
            controller.resumeCamera();
          },
        );
      });
    }

    return SafeArea(
      child: Scaffold(
        body: AspectRatio(
          aspectRatio: cameraAspectRatio.value,
          child: Stack(
            children: [
              QRView(
                key: qrKey,
                onQRViewCreated: _onQRViewCreated,
              ),
              PaddingAll(
                slab: 5,
                child: Align(
                  alignment: Alignment.bottomCenter,
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.end,
                    children: [
                      Text('Scan QR', style: AppTypography.mainHeadingWhite),
                      const HeightBox(slab: 1),
                      Text(
                        'Place the QR code close to your phone',
                        style: AppTypography.headingFont,
                        textAlign: TextAlign.center,
                      ),
                    ],
                  ),
                ),
              ),
              const PaddingHorizontal(slab: 2, child: Header(title: '')),
            ],
          ),
        ),
      ),
    );
  }
}

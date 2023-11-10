import 'dart:io';

import 'package:cardpay/src/presentation/cubits/remote/versions_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/all_padding.dart';
import 'package:cardpay/src/presentation/widgets/boxes/horizontal_padding.dart';
import 'package:cardpay/src/utils/constants/auth_strings.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:url_launcher/url_launcher.dart';

class UpdateModal extends StatelessWidget {
  final bool showMaybeLaterButton;

  const UpdateModal({super.key, required this.showMaybeLaterButton});

  @override
  Widget build(BuildContext context) {
    final versionCubit = BlocProvider.of<VersionsCubit>(context);

    return SizedBox(
      height: MediaQuery.of(context).size.height,
      width: MediaQuery.of(context).size.width,
      child: Stack(
        children: [
          Container(
            color: Colors.grey.withOpacity(0.6),
          ),
          PaddingHorizontal(
            slab: 2,
            child: Center(
              child: Card(
                child: PaddingAll(
                  slab: 1,
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: <Widget>[
                      ListTile(
                        leading: const Icon(Icons.update_outlined),
                        title: const Text('Update your app'),
                        subtitle: Text(Platform.isIOS
                            ? AppStrings.updateMessageIOS
                            : AppStrings.updateMessageAndroid),
                      ),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.end,
                        children: [
                          if (showMaybeLaterButton)
                            TextButton(
                              onPressed: versionCubit.skipDialog,
                              child: const Text('Maybe later'),
                            ),
                          TextButton(
                            onPressed: () async {
                              final appId = Platform.isAndroid
                                  ? 'io.payment.cardpay'
                                  : '1644127078';
                              final url = Uri.parse(
                                Platform.isAndroid
                                    ? "market://details?id=$appId"
                                    : "https://apps.apple.com/app/id$appId",
                              );
                              launchUrl(
                                url,
                                mode: LaunchMode.externalApplication,
                              );
                            },
                            child: const Text('Update Now'),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

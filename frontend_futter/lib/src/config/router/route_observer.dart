import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/firebase/analytics_service.dart';
import 'package:cardpay/src/locator.dart';
import 'package:flutter/material.dart';

class MyObserver extends AutoRouterObserver {
  @override
  void didPush(Route route, Route? previousRoute) {
    locator<AnalyticsService>().logScreenView(route.data?.name ?? '');
  }
}

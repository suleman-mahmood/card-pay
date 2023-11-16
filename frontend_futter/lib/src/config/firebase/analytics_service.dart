// import 'package:flutter/material.dart';
// import 'package:firebase_analytics/firebase_analytics.dart';
// import 'package:firebase_analytics/observer.dart';
// import 'package:firebase_analytics/firebase_analytics.dart';

// class AnalyticsService {
//   final FirebaseAnalytics _analytics = FirebaseAnalytics();

// class _MainActivityState extends State<MainActivity>
//     with MaxAdRevenueListener, ImpressionDataListener {
//   late FirebaseAnalytics firebaseAnalytics;

//   @override
//   void initState() {
//     super.initState();
//     firebaseAnalytics = FirebaseAnalytics();
//     enhancedEcommerce();
//     setUserFavoriteFood("pizza");
//     recordImageView();
//     logCustomEvent();
//   }

//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       appBar: AppBar(title: Text('Firebase Analytics Example')),
//       body: Center(child: Text('Analytics events will be logged')),
//     );
//   }

//   void enhancedEcommerce() {
//     // ... Add your enhancedEcommerce event logging methods here ...
//   }

//   void setUserFavoriteFood(String food) {
//     firebaseAnalytics.setUserProperty("favorite_food", food);
//   }

//   void recordImageView() {
//     String id = "imageId";
//     String name = "imageTitle";

//     firebaseAnalytics.logEvent(
//       name: FirebaseAnalytics.Event.SELECT_ITEM,
//       parameters: {
//         FirebaseAnalytics.Param.ITEM_ID: id,
//         FirebaseAnalytics.Param.ITEM_NAME: name,
//         FirebaseAnalytics.Param.CONTENT_TYPE: "image",
//       },
//     );
//   }

//   void logCustomEvent() {
//     String name = "customImage";
//     String text = "I'd love to hear more about $name";

//     firebaseAnalytics.logEvent(
//       name: "share_image",
//       parameters: {
//         "image_name": name,
//         "full_text": text,
//       },
//     );
//   }

//   @override
//   void onAdRevenuePaid(MaxAd? impressionData) {
//     if (impressionData != null) {
//       firebaseAnalytics.logEvent(
//         name: FirebaseAnalytics.Event.AD_IMPRESSION,
//         parameters: {
//           FirebaseAnalytics.Param.AD_PLATFORM: "appLovin",
//           FirebaseAnalytics.Param.AD_UNIT_NAME: impressionData.adUnitId,
//           FirebaseAnalytics.Param.AD_FORMAT: impressionData.format.label,
//           FirebaseAnalytics.Param.AD_SOURCE: impressionData.networkName,
//           FirebaseAnalytics.Param.VALUE: impressionData.revenue,
//           FirebaseAnalytics.Param.CURRENCY: "USD",
//         },
//       );
//     }
//   }

//   @override
//   void onImpressionSuccess(ImpressionData impressionData) {
//     firebaseAnalytics.logEvent(
//       name: FirebaseAnalytics.Event.AD_IMPRESSION,
//       parameters: {
//         FirebaseAnalytics.Param.AD_PLATFORM: "ironSource",
//         FirebaseAnalytics.Param.AD_SOURCE: impressionData.adNetwork,
//         FirebaseAnalytics.Param.AD_FORMAT: impressionData.adUnit,
//         FirebaseAnalytics.Param.AD_UNIT_NAME: impressionData.instanceName,
//         FirebaseAnalytics.Param.CURRENCY: "USD",
//         FirebaseAnalytics.Param.VALUE: impressionData.revenue,
//       },
//     );
//   }
// }

import 'package:firebase_analytics/firebase_analytics.dart';

class AnalyticsService {
  final FirebaseAnalytics _analytics = FirebaseAnalytics.instance;

  // For route navigation
  Future<void> logScreenView(String screenName) async {
    await _analytics.logScreenView(screenName: screenName);
  }

  // For clicks!
  Future<void> logSelectContent(String contentType, String itemId) async {
    await _analytics.logSelectContent(contentType: contentType, itemId: itemId);
  }

  // For gestures!
  Future<void> logMotion(String contentType, String itemId) async {
    await _analytics.logEvent(
      name: "Swipe",
      parameters: {"contentType": contentType, "itemId": itemId},
    );
  }
}

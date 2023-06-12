import 'dart:async';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:rxdart/rxdart.dart';
import 'package:cardpay/services/auth.dart';
import 'package:cardpay/services/models.dart' as model;

class FirestoreService {
  final FirebaseFirestore _db = FirebaseFirestore.instance;

  Future<model.User> getUser() async {
    final uid = AuthService().user!.uid;
    final ref = _db.collection('users').doc(uid);
    var snapshot = await ref.get();
    var data = snapshot.data();
    var user = model.User.fromJson(data ?? {});

    return user;
  }

  // Listens to current user's document in Firestore
  Stream<model.User> streamUser() {
    return AuthService().userStream.switchMap((user) {
      if (user != null) {
        final ref = _db.collection('users').doc(user.uid);
        return ref.snapshots().map((doc) {
          if (doc.exists) {
            return model.User.fromJson(doc.data()!);
          }
          return model.User();
        });
      } else {
        return Stream.fromIterable([model.User()]);
      }
    });
  }

  Future<model.AppVersionInfo> getAppVersionInfo() async {
    final ref = _db.collection('appInfo').doc("versionInfo");
    var snapshot = await ref.get();
    var data = snapshot.data();
    var info = model.AppVersionInfo.fromJson(data ?? {});

    return info;
  }
}

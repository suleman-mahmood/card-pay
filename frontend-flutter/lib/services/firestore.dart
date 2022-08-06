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

  // Future<List<model.Transaction>> getTransactions() async {
  //   final uid = AuthService().user!.uid;

  //   final ref = _db.collection('transactions');

  //   final q1 = ref.where('sender', isEqualTo: uid);
  //   final q2 = ref.where('recipient', isEqualTo: uid);

  //   var snapshot = await q1.get();
  //   var data = snapshot.docs.map((s) => s.data());
  //   var transactions = data.map((d) => model.Transaction.fromJson(d));

  //   var snapshot2 = await q2.get();
  //   var data2 = snapshot2.docs.map((s) => s.data());
  //   var transactions2 = data2.map((d) => model.Transaction.fromJson(d));

  //   return transactions.toList() + transactions2.toList();
  // }
}

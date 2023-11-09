import 'dart:async';

import 'package:cardpay/src/data/datasources/local/dao/balance_dao.dart';
import 'package:cardpay/src/domain/models/balance.dart';
import 'package:floor/floor.dart';

import 'package:sqflite/sqflite.dart' as sqflite;

part 'app_database.g.dart';

@Database(version: 1, entities: [Balance])
abstract class AppDatabase extends FloorDatabase {
  BalanceDao get balanceDao;
}

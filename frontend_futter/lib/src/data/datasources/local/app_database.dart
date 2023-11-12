import 'dart:async';

import 'package:cardpay/src/data/datasources/local/converters/datetime_type_converter.dart';
import 'package:cardpay/src/data/datasources/local/dao/balance_dao.dart';
import 'package:cardpay/src/data/datasources/local/dao/recent_transactions_dao.dart';
import 'package:cardpay/src/domain/models/balance.dart';
import 'package:cardpay/src/domain/models/transaction.dart';
import 'package:floor/floor.dart';

import 'package:sqflite/sqflite.dart' as sqflite;

part 'app_database.g.dart';

@TypeConverters([DatetimeTypeConverter])
@Database(version: 1, entities: [Balance, Transaction])
abstract class AppDatabase extends FloorDatabase {
  BalanceDao get balanceDao;

  RecentTransactionsDao get recentTransactions;
}

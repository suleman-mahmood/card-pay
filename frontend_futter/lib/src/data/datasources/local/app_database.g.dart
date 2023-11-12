// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'app_database.dart';

// **************************************************************************
// FloorGenerator
// **************************************************************************

// ignore: avoid_classes_with_only_static_members
class $FloorAppDatabase {
  /// Creates a database builder for a persistent database.
  /// Once a database is built, you should keep a reference to it and re-use it.
  static _$AppDatabaseBuilder databaseBuilder(String name) =>
      _$AppDatabaseBuilder(name);

  /// Creates a database builder for an in memory database.
  /// Information stored in an in memory database disappears when the process is killed.
  /// Once a database is built, you should keep a reference to it and re-use it.
  static _$AppDatabaseBuilder inMemoryDatabaseBuilder() =>
      _$AppDatabaseBuilder(null);
}

class _$AppDatabaseBuilder {
  _$AppDatabaseBuilder(this.name);

  final String? name;

  final List<Migration> _migrations = [];

  Callback? _callback;

  /// Adds migrations to the builder.
  _$AppDatabaseBuilder addMigrations(List<Migration> migrations) {
    _migrations.addAll(migrations);
    return this;
  }

  /// Adds a database [Callback] to the builder.
  _$AppDatabaseBuilder addCallback(Callback callback) {
    _callback = callback;
    return this;
  }

  /// Creates the database and initializes it.
  Future<AppDatabase> build() async {
    final path = name != null
        ? await sqfliteDatabaseFactory.getDatabasePath(name!)
        : ':memory:';
    final database = _$AppDatabase();
    database.database = await database.open(
      path,
      _migrations,
      _callback,
    );
    return database;
  }
}

class _$AppDatabase extends AppDatabase {
  _$AppDatabase([StreamController<String>? listener]) {
    changeListener = listener ?? StreamController<String>.broadcast();
  }

  BalanceDao? _balanceDaoInstance;

  RecentTransactionsDao? _recentTransactionsInstance;

  Future<sqflite.Database> open(
    String path,
    List<Migration> migrations, [
    Callback? callback,
  ]) async {
    final databaseOptions = sqflite.OpenDatabaseOptions(
      version: 1,
      onConfigure: (database) async {
        await database.execute('PRAGMA foreign_keys = ON');
        await callback?.onConfigure?.call(database);
      },
      onOpen: (database) async {
        await callback?.onOpen?.call(database);
      },
      onUpgrade: (database, startVersion, endVersion) async {
        await MigrationAdapter.runMigrations(
            database, startVersion, endVersion, migrations);

        await callback?.onUpgrade?.call(database, startVersion, endVersion);
      },
      onCreate: (database, version) async {
        await database.execute(
            'CREATE TABLE IF NOT EXISTS `balance` (`id` INTEGER NOT NULL, `amount` INTEGER NOT NULL, PRIMARY KEY (`id`))');
        await database.execute(
            'CREATE TABLE IF NOT EXISTS `transactions` (`id` TEXT NOT NULL, `amount` INTEGER NOT NULL, `mode` INTEGER NOT NULL, `transactionType` INTEGER NOT NULL, `status` INTEGER NOT NULL, `createdAt` TEXT, `lastUpdated` TEXT, `senderName` TEXT NOT NULL, `recipientName` TEXT NOT NULL, PRIMARY KEY (`id`))');

        await callback?.onCreate?.call(database, version);
      },
    );
    return sqfliteDatabaseFactory.openDatabase(path, options: databaseOptions);
  }

  @override
  BalanceDao get balanceDao {
    return _balanceDaoInstance ??= _$BalanceDao(database, changeListener);
  }

  @override
  RecentTransactionsDao get recentTransactions {
    return _recentTransactionsInstance ??=
        _$RecentTransactionsDao(database, changeListener);
  }
}

class _$BalanceDao extends BalanceDao {
  _$BalanceDao(
    this.database,
    this.changeListener,
  )   : _queryAdapter = QueryAdapter(database),
        _balanceInsertionAdapter = InsertionAdapter(
            database,
            'balance',
            (Balance item) =>
                <String, Object?>{'id': item.id, 'amount': item.amount});

  final sqflite.DatabaseExecutor database;

  final StreamController<String> changeListener;

  final QueryAdapter _queryAdapter;

  final InsertionAdapter<Balance> _balanceInsertionAdapter;

  @override
  Future<Balance?> getBalance() async {
    return _queryAdapter.query('select * from balance where id = 0',
        mapper: (Map<String, Object?> row) =>
            Balance(id: row['id'] as int, amount: row['amount'] as int));
  }

  @override
  Future<void> updateBalance(Balance balance) async {
    await _balanceInsertionAdapter.insert(balance, OnConflictStrategy.replace);
  }
}

class _$RecentTransactionsDao extends RecentTransactionsDao {
  _$RecentTransactionsDao(
    this.database,
    this.changeListener,
  )   : _queryAdapter = QueryAdapter(database),
        _transactionInsertionAdapter = InsertionAdapter(
            database,
            'transactions',
            (Transaction item) => <String, Object?>{
                  'id': item.id,
                  'amount': item.amount,
                  'mode': item.mode.index,
                  'transactionType': item.transactionType.index,
                  'status': item.status.index,
                  'createdAt': _datetimeTypeConverter.encode(item.createdAt),
                  'lastUpdated':
                      _datetimeTypeConverter.encode(item.lastUpdated),
                  'senderName': item.senderName,
                  'recipientName': item.recipientName
                });

  final sqflite.DatabaseExecutor database;

  final StreamController<String> changeListener;

  final QueryAdapter _queryAdapter;

  final InsertionAdapter<Transaction> _transactionInsertionAdapter;

  @override
  Future<List<Transaction>> getRecentTransactions() async {
    return _queryAdapter.queryList(
        'select * from transactions order by createdAt desc',
        mapper: (Map<String, Object?> row) => Transaction(
            createdAt:
                _datetimeTypeConverter.decode(row['createdAt'] as String),
            lastUpdated:
                _datetimeTypeConverter.decode(row['lastUpdated'] as String),
            id: row['id'] as String,
            amount: row['amount'] as int,
            mode: TransactionMode.values[row['mode'] as int],
            transactionType:
                TransactionType.values[row['transactionType'] as int],
            status: TransactionStatus.values[row['status'] as int],
            senderName: row['senderName'] as String,
            recipientName: row['recipientName'] as String));
  }

  @override
  Future<void> updateRecentTransactions(List<Transaction> txs) async {
    await _transactionInsertionAdapter.insertList(
        txs, OnConflictStrategy.replace);
  }
}

// ignore_for_file: unused_element
final _datetimeTypeConverter = DatetimeTypeConverter();

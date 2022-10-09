"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __asyncValues = (this && this.__asyncValues) || function (o) {
    if (!Symbol.asyncIterator) throw new TypeError("Symbol.asyncIterator is not defined.");
    var m = o[Symbol.asyncIterator], i;
    return m ? m.call(o) : (o = typeof __values === "function" ? __values(o) : o[Symbol.iterator](), i = {}, verb("next"), verb("throw"), verb("return"), i[Symbol.asyncIterator] = function () { return this; }, i);
    function verb(n) { i[n] = o[n] && function (v) { return new Promise(function (resolve, reject) { v = o[n](v), settle(resolve, reject, v.done, v.value); }); }; }
    function settle(resolve, reject, d, v) { Promise.resolve(v).then(function(v) { resolve({ value: v, done: d }); }, reject); }
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const app_1 = require("firebase-admin/app");
const auth_1 = require("firebase-admin/auth");
const firestore_1 = require("firebase-admin/firestore");
const functions_1 = require("firebase-admin/functions");
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
const app = (0, app_1.initializeApp)({
    credential: (0, app_1.applicationDefault)(),
});
// Initialize Auth
const auth = (0, auth_1.getAuth)(app);
// Initialize Firestore
const db = (0, firestore_1.getFirestore)(app);
// Initialize functions with emulator
const functions = (0, functions_1.getFunctions)(app);
const reversingTransactions = () => __awaiter(void 0, void 0, void 0, function* () {
    var e_1, _a, e_2, _b, e_3, _c, e_4, _d;
    const ref = db.collection('users');
    const q = ref.where('fullName', '==', 'The Bunker');
    const querySnapshot = yield q.get();
    const deleteTrans = [];
    try {
        for (var _e = __asyncValues(querySnapshot.docs), _f; _f = yield _e.next(), !_f.done;) {
            const v = _f.value;
            const data = v.data();
            const BunkerId = v.id;
            let sumTill = 0;
            data.transactions.forEach(v => {
                sumTill += v.amount;
                if (sumTill <= 1335) {
                    deleteTrans.push(v);
                }
            });
            const userTrans = {};
            deleteTrans.forEach(trans => {
                if (trans.senderName in userTrans) {
                    userTrans[trans.senderName].push(trans);
                }
                else {
                    userTrans[trans.senderName] = [trans];
                }
            });
            const userBalances = {};
            Object.keys(userTrans).map(senderName => {
                userBalances[senderName] = 0;
                userTrans[senderName].map(v => {
                    userBalances[senderName] += v.amount;
                });
            });
            try {
                for (var _g = (e_2 = void 0, __asyncValues(Object.keys(userTrans))), _h; _h = yield _g.next(), !_h.done;) {
                    const senderName = _h.value;
                    const ref = db.collection('users');
                    const q = ref.where('fullName', '==', senderName);
                    const querySnapshot = yield q.get();
                    try {
                        for (var _j = (e_3 = void 0, __asyncValues(querySnapshot.docs)), _k; _k = yield _j.next(), !_k.done;) {
                            const u = _k.value;
                            const id = u.id;
                            const docData = u.data();
                            const oldTrans = docData.transactions;
                            const oldBalance = docData.balance;
                            const tranIdsToDelete = userTrans[senderName].map(v => v.id);
                            const newTrans = oldTrans.filter(v => !tranIdsToDelete.includes(v.id));
                            const newBalance = oldBalance + userBalances[senderName];
                            console.log('New Users Transactions:', newTrans.length);
                            console.log('New Users Balance:', newBalance);
                            let sum = 0;
                            newTrans.forEach(t => {
                                if (t.senderName === senderName)
                                    sum -= t.amount;
                                else
                                    sum += t.amount;
                            });
                            console.log('Trans sum', sum);
                            yield db.collection('users').doc(id).update({
                                balance: newBalance,
                                transactions: newTrans,
                            });
                        }
                    }
                    catch (e_3_1) { e_3 = { error: e_3_1 }; }
                    finally {
                        try {
                            if (_k && !_k.done && (_c = _j.return)) yield _c.call(_j);
                        }
                        finally { if (e_3) throw e_3.error; }
                    }
                }
            }
            catch (e_2_1) { e_2 = { error: e_2_1 }; }
            finally {
                try {
                    if (_h && !_h.done && (_b = _g.return)) yield _b.call(_g);
                }
                finally { if (e_2) throw e_2.error; }
            }
            const docSnapshot = yield db.collection('users').doc(BunkerId).get();
            const docData = docSnapshot.data();
            const oldTrans = docData.transactions;
            const oldBalance = docData.balance;
            const tranIdsToDelete = deleteTrans.map(d => d.id);
            const newTrans = oldTrans.filter(v => !tranIdsToDelete.includes(v.id));
            const newBalance = oldBalance - 1335;
            console.log('ID:', BunkerId);
            console.log('New Bunkers Transactions:', newTrans.length);
            console.log('New Bunkers Balance:', newBalance);
            let sum = 0;
            newTrans.forEach(t => {
                if (t.senderName === 'The Bunker')
                    sum -= t.amount;
                else
                    sum += t.amount;
            });
            console.log('Trans sum', sum);
            yield db.collection('users').doc(BunkerId).update({
                balance: newBalance,
                transactions: newTrans,
            });
            const transactionsDeleteRef = db.collection('transactions');
            try {
                for (var tranIdsToDelete_1 = (e_4 = void 0, __asyncValues(tranIdsToDelete)), tranIdsToDelete_1_1; tranIdsToDelete_1_1 = yield tranIdsToDelete_1.next(), !tranIdsToDelete_1_1.done;) {
                    const id = tranIdsToDelete_1_1.value;
                    yield transactionsDeleteRef.doc(id).delete();
                }
            }
            catch (e_4_1) { e_4 = { error: e_4_1 }; }
            finally {
                try {
                    if (tranIdsToDelete_1_1 && !tranIdsToDelete_1_1.done && (_d = tranIdsToDelete_1.return)) yield _d.call(tranIdsToDelete_1);
                }
                finally { if (e_4) throw e_4.error; }
            }
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (_f && !_f.done && (_a = _e.return)) yield _a.call(_e);
        }
        finally { if (e_1) throw e_1.error; }
    }
});
const saveFirestoreState = () => __awaiter(void 0, void 0, void 0, function* () {
    var e_5, _l;
    const database = {};
    const ref = yield db.listCollections();
    try {
        for (var ref_1 = __asyncValues(ref), ref_1_1; ref_1_1 = yield ref_1.next(), !ref_1_1.done;) {
            const col = ref_1_1.value;
            const docs = yield col.get();
            const collectionName = col.path;
            database[collectionName] = {};
            docs.forEach(d => {
                database[collectionName][d.id] = d.data();
            });
        }
    }
    catch (e_5_1) { e_5 = { error: e_5_1 }; }
    finally {
        try {
            if (ref_1_1 && !ref_1_1.done && (_l = ref_1.return)) yield _l.call(ref_1);
        }
        finally { if (e_5) throw e_5.error; }
    }
    const now = new Date().toISOString().replace(/T/, ' ').replace(/\..+/, '');
    const fileName = `${now}_DBState.json`;
    writeToLocalStorage(database, fileName);
});
const deleteFirestore = () => __awaiter(void 0, void 0, void 0, function* () {
    var e_6, _m;
    const database = {};
    const ref = yield db.listCollections();
    try {
        for (var ref_2 = __asyncValues(ref), ref_2_1; ref_2_1 = yield ref_2.next(), !ref_2_1.done;) {
            const col = ref_2_1.value;
            const docs = yield col.get();
            const collectionName = col.path;
            database[collectionName] = [];
            docs.forEach(d => {
                database[collectionName].push(d.id);
            });
        }
    }
    catch (e_6_1) { e_6 = { error: e_6_1 }; }
    finally {
        try {
            if (ref_2_1 && !ref_2_1.done && (_m = ref_2.return)) yield _m.call(ref_2);
        }
        finally { if (e_6) throw e_6.error; }
    }
    Object.keys(database).map((colName) => __awaiter(void 0, void 0, void 0, function* () {
        var e_7, _o;
        const ref = db.collection(colName);
        try {
            for (var _p = __asyncValues(database[colName]), _q; _q = yield _p.next(), !_q.done;) {
                const id = _q.value;
                yield ref.doc(id).delete();
            }
        }
        catch (e_7_1) { e_7 = { error: e_7_1 }; }
        finally {
            try {
                if (_q && !_q.done && (_o = _p.return)) yield _o.call(_p);
            }
            finally { if (e_7) throw e_7.error; }
        }
    }));
});
const writeToLocalStorage = (data, fileName) => {
    fs_1.default.writeFile(fileName, JSON.stringify(data), err => {
        if (err)
            return console.log(err);
        console.log('Data written to file system');
    });
};
const restoreDbFromFile = () => __awaiter(void 0, void 0, void 0, function* () {
    const filePath = path_1.default.join('/home/soul/Projects/card-pay/temp/', '2022-10-08 01:00:05_DBState.json');
    fs_1.default.readFile(filePath, { encoding: 'utf-8' }, (err, data) => __awaiter(void 0, void 0, void 0, function* () {
        var e_8, _r, e_9, _s;
        if (err)
            console.log(err);
        else {
            const dbData = JSON.parse(data);
            try {
                for (var _t = __asyncValues(Object.keys(dbData)), _u; _u = yield _t.next(), !_u.done;) {
                    const collectionName = _u.value;
                    const colRef = db.collection(collectionName);
                    try {
                        for (var _v = (e_9 = void 0, __asyncValues(Object.keys(dbData[collectionName]))), _w; _w = yield _v.next(), !_w.done;) {
                            const docId = _w.value;
                            yield colRef
                                .doc(docId)
                                .create(dbData[collectionName][docId]);
                        }
                    }
                    catch (e_9_1) { e_9 = { error: e_9_1 }; }
                    finally {
                        try {
                            if (_w && !_w.done && (_s = _v.return)) yield _s.call(_v);
                        }
                        finally { if (e_9) throw e_9.error; }
                    }
                }
            }
            catch (e_8_1) { e_8 = { error: e_8_1 }; }
            finally {
                try {
                    if (_u && !_u.done && (_r = _t.return)) yield _r.call(_t);
                }
                finally { if (e_8) throw e_8.error; }
            }
        }
    }));
});
const topUp = () => __awaiter(void 0, void 0, void 0, function* () {
    // Configuration parameters
    const rollNumber = '00000000';
    const topUpAmount = 0;
    const ref = db.collection('users');
    const q = ref.where('rollNumber', '==', rollNumber);
    const querySnapshot = yield q.get();
    if (querySnapshot.size !== 1) {
        throw new Error(`Multiple people with the same roll number: ${querySnapshot.size}`);
    }
    querySnapshot.forEach((doc) => __awaiter(void 0, void 0, void 0, function* () {
        const id = doc.id;
        const docData = doc.data();
        const newBalance = docData.balance + topUpAmount;
        yield db.collection('users').doc(id).update({
            balance: newBalance,
        });
    }));
});
const getUserDoc = () => __awaiter(void 0, void 0, void 0, function* () {
    // Configuration parameters
    const rollNumber = '';
    const ref = db.collection('users');
    const q = ref.where('rollNumber', '==', rollNumber);
    const querySnapshot = yield q.get();
    if (querySnapshot.size !== 1) {
        throw new Error(`Multiple people with the same roll number: ${querySnapshot.size}`);
    }
    querySnapshot.forEach((doc) => __awaiter(void 0, void 0, void 0, function* () {
        const docData = doc.data();
        Object.keys(docData).map(k => {
            if (k === 'transactions') {
                console.log(k, ':', docData[k].length);
            }
            else {
                console.log(k, ':', docData[k]);
            }
        });
    }));
});
// restoreDbFromFile();
// reversingTransactions();
// deleteFirestore();
// saveFirestoreState();
// topUp();
getUserDoc();

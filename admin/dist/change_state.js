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
Object.defineProperty(exports, "__esModule", { value: true });
exports.makeVendorAccount = exports.forceTransaction = exports.TrimSpacesInFullNameOfAllUsers = exports.topUp = exports.reversingTransactions = void 0;
const init_firebase_1 = require("./init_firebase");
const reversingTransactions = () => __awaiter(void 0, void 0, void 0, function* () {
    var e_1, _a, e_2, _b, e_3, _c, e_4, _d;
    const ref = init_firebase_1.db.collection('users');
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
                    const ref = init_firebase_1.db.collection('users');
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
                            yield init_firebase_1.db.collection('users').doc(id).update({
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
            const docSnapshot = yield init_firebase_1.db.collection('users').doc(BunkerId).get();
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
            yield init_firebase_1.db.collection('users').doc(BunkerId).update({
                balance: newBalance,
                transactions: newTrans,
            });
            const transactionsDeleteRef = init_firebase_1.db.collection('transactions');
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
exports.reversingTransactions = reversingTransactions;
const topUp = () => __awaiter(void 0, void 0, void 0, function* () {
    // Configuration parameters
    const rollNumber = '23110240';
    const topUpAmount = 50000;
    const ref = init_firebase_1.db.collection('users');
    const q = ref.where('rollNumber', '==', rollNumber);
    const querySnapshot = yield q.get();
    if (querySnapshot.size !== 1) {
        throw new Error(`Multiple people with the same roll number: ${querySnapshot.size}`);
    }
    const doc = querySnapshot.docs[0];
    const id = doc.id;
    const docData = doc.data();
    const newBalance = docData.balance + topUpAmount;
    yield init_firebase_1.db.collection('users').doc(id).update({
        balance: newBalance,
    });
    console.log('Deposited', topUpAmount, 'into', docData.fullName, docData.rollNumber);
});
exports.topUp = topUp;
const TrimSpacesInFullNameOfAllUsers = () => __awaiter(void 0, void 0, void 0, function* () {
    const querySnapshot = yield init_firebase_1.db.collection('users').get();
    const promiseList = [];
    querySnapshot.forEach(doc => {
        const id = doc.id;
        const data = doc.data();
        if (data.fullName) {
            console.log(data.fullName.trim(), data.fullName.trim().length);
            console.log(data.fullName, data.fullName.length);
            console.log('');
            const pr = init_firebase_1.db.collection('users').doc(id).update({
                fullName: data.fullName.trim(),
            });
            promiseList.push(pr);
        }
    });
    yield Promise.all(promiseList);
});
exports.TrimSpacesInFullNameOfAllUsers = TrimSpacesInFullNameOfAllUsers;
const forceTransaction = () => __awaiter(void 0, void 0, void 0, function* () {
    const amount = 0;
    const senderRollNumber = '';
    const recipientRollNumber = '';
    // Get the recipient details from Firestore
    const recipientsQueryRef = init_firebase_1.db.collection("users")
        .where("rollNumber", "==", recipientRollNumber);
    const recipientSnapshot = yield recipientsQueryRef.get();
    const recipientDoc = recipientSnapshot.docs[0].data();
    const recipientUid = recipientSnapshot.docs[0].id;
    // Get the sender details from Firestore
    const sendersQueryRef = init_firebase_1.db.collection("users")
        .where("rollNumber", "==", senderRollNumber);
    const senderSnapshot = yield sendersQueryRef.get();
    const senderDoc = senderSnapshot.docs[0].data();
    const senderUid = senderSnapshot.docs[0].id;
    /*
    Handle transaction success!
    */
    // Add the transaction to the transactions collection
    const transactionsRef = init_firebase_1.db.collection("transactions").doc();
    const transaction = {
        id: transactionsRef.id,
        timestamp: new Date().toISOString(),
        senderId: senderUid,
        senderName: senderDoc.fullName,
        recipientId: recipientUid,
        recipientName: recipientDoc.fullName,
        amount: amount,
        status: "successful",
    };
    yield transactionsRef.create(transaction);
    const userTransaction = {
        id: transaction.id,
        timestamp: transaction.timestamp,
        senderName: transaction.senderName,
        recipientName: transaction.recipientName,
        amount: transaction.amount,
        status: transaction.status,
    };
    // Add the transaction to the sender's transaction history
    // Decrement the balance by the amount for the sender
    const sendersDocRef = init_firebase_1.db.collection("users").doc(senderUid);
    const newSenderTrans = senderDoc.transactions;
    newSenderTrans.push(userTransaction);
    yield sendersDocRef.update({
        transactions: newSenderTrans,
        balance: senderDoc.balance - amount // admin.firestore.FieldValue.increment(-1 * amount),
    });
    // Add the transaction to the recipient's transaction history
    // Increment the balance by the amount for the recipient
    const recipientsDocRef = init_firebase_1.db.collection("users").doc(recipientUid);
    const newRecipientTrans = recipientDoc.transactions;
    newRecipientTrans.push(userTransaction);
    yield recipientsDocRef.update({
        transactions: newRecipientTrans,
        balance: recipientDoc.balance + amount // admin.firestore.FieldValue.increment(amount),
    });
    console.log("Transaction was successfull");
});
exports.forceTransaction = forceTransaction;
const makeVendorAccount = () => __awaiter(void 0, void 0, void 0, function* () {
    const docId = '';
    const userData = {
        id: docId,
        fullName: '',
        personalEmail: '',
        email: '',
        pendingDeposits: false,
        pin: '',
        phoneNumber: '',
        rollNumber: '',
        verified: false,
        role: 'vendor',
        balance: 0,
        transactions: [],
    };
    const ref = init_firebase_1.db.collection('users').doc(docId);
    yield ref.create(userData);
});
exports.makeVendorAccount = makeVendorAccount;

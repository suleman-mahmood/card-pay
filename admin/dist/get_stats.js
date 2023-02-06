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
Object.defineProperty(exports, "__esModule", { value: true });
exports.getUserDoc = exports.getAllBalances = exports.getBalanceTillTime = exports.getTransactionsSum = void 0;
const init_firebase_1 = require("./init_firebase");
const getTransactionsSum = () => __awaiter(void 0, void 0, void 0, function* () {
    const ref = init_firebase_1.db.collection('users');
    const querySnapshot = yield ref.get();
    let totalSum = 0;
    let ppSum = 0;
    let balancesSum = 0;
    querySnapshot.forEach((doc) => __awaiter(void 0, void 0, void 0, function* () {
        const docData = doc.data();
        let sum = 0;
        let currPpSum = 0;
        docData.transactions.map(t => {
            if (t.senderName !== t.recipientName) {
                if (t.senderName === docData.fullName) {
                    sum -= t.amount;
                }
                else if (t.senderName === 'PayPro Payment Gateway') {
                    currPpSum += t.amount;
                }
                else {
                    sum += t.amount;
                }
            }
        });
        if (sum !== 0 || currPpSum !== 0) {
            console.log(docData.fullName, docData.email, sum, currPpSum, docData.balance);
        }
        ppSum += currPpSum;
        totalSum += sum;
        balancesSum += docData.balance;
    }));
    console.log('');
    console.log('Total Transactions Sum:', totalSum);
    console.log('Total PayPro Sum:', ppSum);
    console.log('Total Balance Sum:', balancesSum);
});
exports.getTransactionsSum = getTransactionsSum;
const getBalanceTillTime = (rollNumber, isoDate) => __awaiter(void 0, void 0, void 0, function* () {
    // Configuration parameters
    // const isoDate = new Date('2022-10-10T22:30:00.000Z'); // Enter time in PKT
    // Go transactions from last five hours
    isoDate.setHours(isoDate.getHours() - 5);
    const ref = init_firebase_1.db.collection('users');
    const q = ref.where('rollNumber', '==', rollNumber);
    const querySnapshot = yield q.get();
    if (querySnapshot.size !== 1) {
        throw new Error(`Multiple people with the same roll number: ${querySnapshot.size}`);
    }
    querySnapshot.forEach((doc) => __awaiter(void 0, void 0, void 0, function* () {
        const docData = doc.data();
        Object.keys(docData).map(k => {
            if (k === 'transactions') {
                const trans = docData[k];
                let sum = 0;
                trans.forEach(t => {
                    const nowDate = new Date(t.timestamp);
                    if (nowDate >= isoDate) {
                        console.log(t.timestamp, t.amount);
                        sum += t.amount;
                    }
                });
                console.log('Transactions then to now:', sum);
                console.log('Previous balance at the given timestamp', docData.balance - sum);
            }
        });
    }));
});
exports.getBalanceTillTime = getBalanceTillTime;
const getAllBalances = () => __awaiter(void 0, void 0, void 0, function* () {
    const ref = init_firebase_1.db.collection('users');
    const querySnapshot = yield ref.get();
    querySnapshot.forEach((doc) => __awaiter(void 0, void 0, void 0, function* () {
        const docData = doc.data();
        if (docData.balance !== 0) {
            console.log('Transactions count: ', docData.transactions.length);
            console.log(docData.fullName, docData.rollNumber, docData.balance);
            console.log('');
        }
    }));
});
exports.getAllBalances = getAllBalances;
const getUserDoc = (rollNumber) => __awaiter(void 0, void 0, void 0, function* () {
    const ref = init_firebase_1.db.collection('users');
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
                console.log('Last transaction:');
                console.log(docData[k][docData[k].length - 1]);
            }
            else {
                console.log(k, ':', docData[k]);
            }
        });
    }));
});
exports.getUserDoc = getUserDoc;

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
exports.getUserDoc = exports.getAllBalances = exports.getAllVendors = void 0;
const init_firebase_1 = require("../init_firebase");
const getAllVendors = () => __awaiter(void 0, void 0, void 0, function* () {
    const ref = init_firebase_1.db.collection('users').where('role', '==', 'vendor');
    const querySnapshot = yield ref.get();
    const vendors = [];
    querySnapshot.forEach(doc => {
        const docData = doc.data();
        vendors.push(docData);
    });
    return vendors;
});
exports.getAllVendors = getAllVendors;
const getAllBalances = () => __awaiter(void 0, void 0, void 0, function* () {
    const ref = init_firebase_1.db.collection('users');
    const querySnapshot = yield ref.get();
    querySnapshot.forEach(doc => {
        const docData = doc.data();
        if (docData.balance !== 0) {
            console.log('Transactions count: ', docData.transactions.length);
            console.log(docData.fullName, docData.rollNumber, docData.balance);
            console.log('');
        }
    });
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

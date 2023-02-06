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
exports.makeVendorAccount = exports.getAllVendors = void 0;
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
const makeVendorAccount = () => __awaiter(void 0, void 0, void 0, function* () {
    const docId = 'j4lFpFk51rgQcipHvss8GucqzPV2';
    const userData = {
        id: docId,
        fullName: 'JJ Kitchen',
        personalEmail: '',
        email: 'fkabli@gmail.com',
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

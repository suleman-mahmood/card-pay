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
exports.restoreDbFromFile = exports.deleteFirestore = exports.saveFirestoreState = void 0;
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
const init_firebase_1 = require("./init_firebase");
const utils_1 = require("./utils");
const saveFirestoreState = () => __awaiter(void 0, void 0, void 0, function* () {
    var e_1, _a;
    const database = {};
    const ref = yield init_firebase_1.db.listCollections();
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
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (ref_1_1 && !ref_1_1.done && (_a = ref_1.return)) yield _a.call(ref_1);
        }
        finally { if (e_1) throw e_1.error; }
    }
    const now = new Date().toISOString().replace(/T/, ' ').replace(/\..+/, '');
    const fileName = `${now}_DBState.json`;
    (0, utils_1.writeToLocalStorage)(database, fileName);
});
exports.saveFirestoreState = saveFirestoreState;
const deleteFirestore = () => __awaiter(void 0, void 0, void 0, function* () {
    var e_2, _b;
    const database = {};
    const ref = yield init_firebase_1.db.listCollections();
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
    catch (e_2_1) { e_2 = { error: e_2_1 }; }
    finally {
        try {
            if (ref_2_1 && !ref_2_1.done && (_b = ref_2.return)) yield _b.call(ref_2);
        }
        finally { if (e_2) throw e_2.error; }
    }
    Object.keys(database).map((colName) => __awaiter(void 0, void 0, void 0, function* () {
        var e_3, _c;
        const ref = init_firebase_1.db.collection(colName);
        try {
            for (var _d = __asyncValues(database[colName]), _e; _e = yield _d.next(), !_e.done;) {
                const id = _e.value;
                yield ref.doc(id).delete();
            }
        }
        catch (e_3_1) { e_3 = { error: e_3_1 }; }
        finally {
            try {
                if (_e && !_e.done && (_c = _d.return)) yield _c.call(_d);
            }
            finally { if (e_3) throw e_3.error; }
        }
    }));
});
exports.deleteFirestore = deleteFirestore;
const restoreDbFromFile = () => __awaiter(void 0, void 0, void 0, function* () {
    const filePath = path_1.default.join('/home/soul/Projects/card-pay/temp/', '2022-10-08 01:00:05_DBState.json');
    fs_1.default.readFile(filePath, { encoding: 'utf-8' }, (err, data) => __awaiter(void 0, void 0, void 0, function* () {
        var e_4, _f, e_5, _g;
        if (err)
            console.log(err);
        else {
            const dbData = JSON.parse(data);
            try {
                for (var _h = __asyncValues(Object.keys(dbData)), _j; _j = yield _h.next(), !_j.done;) {
                    const collectionName = _j.value;
                    const colRef = init_firebase_1.db.collection(collectionName);
                    try {
                        for (var _k = (e_5 = void 0, __asyncValues(Object.keys(dbData[collectionName]))), _l; _l = yield _k.next(), !_l.done;) {
                            const docId = _l.value;
                            yield colRef
                                .doc(docId)
                                .create(dbData[collectionName][docId]);
                        }
                    }
                    catch (e_5_1) { e_5 = { error: e_5_1 }; }
                    finally {
                        try {
                            if (_l && !_l.done && (_g = _k.return)) yield _g.call(_k);
                        }
                        finally { if (e_5) throw e_5.error; }
                    }
                }
            }
            catch (e_4_1) { e_4 = { error: e_4_1 }; }
            finally {
                try {
                    if (_j && !_j.done && (_f = _h.return)) yield _f.call(_h);
                }
                finally { if (e_4) throw e_4.error; }
            }
        }
    }));
});
exports.restoreDbFromFile = restoreDbFromFile;

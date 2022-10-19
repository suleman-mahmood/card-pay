"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.writeToLocalStorage = void 0;
const fs_1 = __importDefault(require("fs"));
const writeToLocalStorage = (data, fileName) => {
    fs_1.default.writeFile(fileName, JSON.stringify(data), err => {
        if (err)
            return console.log(err);
        console.log('Data written to file system');
    });
};
exports.writeToLocalStorage = writeToLocalStorage;

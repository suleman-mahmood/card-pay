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
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.sendEmail = exports.writeToLocalStorage = void 0;
const fs_1 = __importDefault(require("fs"));
const nodemailer = require('nodemailer');
const writeToLocalStorage = (data, fileName) => {
    fs_1.default.writeFile(fileName, JSON.stringify(data), err => {
        if (err)
            return console.log(err);
        console.log('Data written to file system');
    });
};
exports.writeToLocalStorage = writeToLocalStorage;
const sendEmail = () => __awaiter(void 0, void 0, void 0, function* () {
    const transporter = nodemailer.createTransport({
        host: 'email-smtp.ap-south-1.amazonaws.com',
        port: 465,
        secure: true,
        auth: {
            user: 'AKIAWLUTTIWJPJPQFIES',
            pass: 'BIelL3t+5wt+4G7N4ZgQS6zS1jkg+HYZA+9qYAoe2En1',
        },
    });
    // send mail with defined transport object
    let info = yield transporter.sendMail({
        from: 'cardpayteam@gmail.com',
        to: '23100011@lums.edu.pk',
        subject: 'Hello ✔',
        // text: "Hello world?", // plain text body
        html: '<b>Email from cardpay test server!</b>', // html body
    });
    console.log('Message sent: %s', info.messageId);
});
exports.sendEmail = sendEmail;

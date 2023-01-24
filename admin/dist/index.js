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
const nodemailer = require('nodemailer');
const sendEmail = () => __awaiter(void 0, void 0, void 0, function* () {
    const transporter = nodemailer.createTransport({
        host: 'email-smtp.ap-northeast-1.amazonaws.com',
        port: 465,
        secure: true,
        auth: {
            user: 'AKIAWLUTTIWJKEYHBQYL',
            pass: 'BBHsVss9Vg6PNPBREKXw1ikZcN3usOY3QnVSIpmdjQkp',
        },
    });
    // send mail with defined transport object
    let info = yield transporter.sendMail({
        from: 'sulemanmahmood99@gmail.com',
        to: '23100011@lums.edu.pk',
        subject: 'Hello ✔',
        // text: "Hello world?", // plain text body
        html: '<b>Email from cardpay test server!</b>', // html body
    });
    console.log('Message sent: %s', info.messageId);
});
// sendEmail();

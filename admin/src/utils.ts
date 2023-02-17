import fs from 'fs';
const nodemailer = require('nodemailer');

export const writeToLocalStorage = (data: Object, fileName: string) => {
	fs.writeFile(fileName, JSON.stringify(data), err => {
		if (err) return console.log(err);
		console.log('Data written to file system');
	});
};

export const sendEmail = async () => {
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
	let info = await transporter.sendMail({
		from: 'cardpayteam@gmail.com', // sender address
		to: '23100011@lums.edu.pk', // list of receivers
		subject: 'Hello ✔', // Subject line
		// text: "Hello world?", // plain text body
		html: '<b>Email from cardpay test server!</b>', // html body
	});

	console.log('Message sent: %s', info.messageId);
};
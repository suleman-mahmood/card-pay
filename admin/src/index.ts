import { getAllVendors } from './admin/vendors';
import { forceTransaction } from './change_state';
import { getAllBalances, getTransactionsSum, getUserDoc } from './get_stats';
import { saveFirestoreState } from './db_restore';

const nodemailer = require('nodemailer');

const sendEmail = async () => {
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

// getTransactionsSum();
// forceTransaction('sulemanmahmood', '23100011', 230);
// saveFirestoreState();
// getAllBalances();
// sendEmail();
// getUserDoc('sulemanmahmood');
// getUserDoc('thebunker');

/*
qpL3Er4w7LZZfiUBz6Ie
D1hM1H6qI1qEzlPjog3S
YN83EwcsnEUz1Ivo93of

*/

// import nodemailer = require('nodemailer');
import { createTransport } from 'nodemailer';

export const getTimestamp = (): string => {
	return new Date().toISOString();
};

export const generateRandom4DigitPin = (): string => {
	return (Math.floor(Math.random() * 10000) + 10000).toString().substring(1);
};

export const sendEmail = async (
	to: string,
	subject: string,
	text: string,
	html: string
) => {
	const transporter = createTransport({
		// host: 'email-smtp.ap-northeast-1.amazonaws.com',
		host: 'email-smtp.ap-south-1.amazonaws.com',
		port: 465,
		secure: true,
		auth: {
			// user: 'AKIAWLUTTIWJKEYHBQYL',
			// pass: 'BBHsVss9Vg6PNPBREKXw1ikZcN3usOY3QnVSIpmdjQkp',
			user: 'AKIAWLUTTIWJPJPQFIES',
			pass: 'BIelL3t+5wt+4G7N4ZgQS6zS1jkg+HYZA+9qYAoe2En1',
		},
	});

	// send mail with defined transport object
	await transporter.sendMail({
		from: 'cardpayteam@gmail.com', // sender address
		to: to,
		subject: subject,
		text: text,
		html: html,
	});
};

export const oneHourInMs = 60 * 60 * 1000;

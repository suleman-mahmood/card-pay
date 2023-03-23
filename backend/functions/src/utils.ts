import * as functions from 'firebase-functions';
import { createTransport } from 'nodemailer';

export const getTimestamp = (): string => {
	return new Date().toISOString();
};

export const getTimestampMilliseconds = (): number => {
	return new Date().getTime();
};

export const generateRandom4DigitPin = (): string => {
	return (Math.floor(Math.random() * 10000) + 10000).toString().substring(1);
};

export const oneHourInMs = 60 * 60 * 1000;

export const sendEmail = async (
	to: string,
	subject: string,
	text: string,
	html: string
) => {
	const transporter = createTransport({
		host: 'email-smtp.ap-south-1.amazonaws.com',
		port: 465,
		secure: true,
		auth: {
			user: 'AKIAWLUTTIWJPJPQFIES',
			pass: 'BIelL3t+5wt+4G7N4ZgQS6zS1jkg+HYZA+9qYAoe2En1',
		},
	});

	await transporter.sendMail({
		from: 'cardpayteam@gmail.com',
		to: to,
		subject: subject,
		text: text,
		html: html,
	});
};

export const throwError = (
	code: functions.https.FunctionsErrorCode,
	message: string,
	data?: any
) => {
	functions.logger.info(code, message, data);
	throw new functions.https.HttpsError(code, message);
};

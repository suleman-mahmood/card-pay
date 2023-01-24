const nodemailer = require('nodemailer');

const sendEmail = async () => {
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
	let info = await transporter.sendMail({
		from: 'sulemanmahmood99@gmail.com', // sender address
		to: '23100011@lums.edu.pk', // list of receivers
		subject: 'Hello ✔', // Subject line
		// text: "Hello world?", // plain text body
		html: '<b>Email from cardpay test server!</b>', // html body
	});

	console.log('Message sent: %s', info.messageId);
};

// sendEmail();

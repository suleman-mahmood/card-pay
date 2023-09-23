interface FAQ {
	question: string;
	answer: string;
}

export const faqs: FAQ[] = [
	{
		question: 'What is CardPay?',
		answer: 'CardPay converts your LUMS Student card into your Digital Wallet to enable cashless transactions via your LUMS Student Card.',
	},
	{
		question: 'How to pay with CardPay?',
		answer: 'You simply go to one of our registered vendors and place your order. Ask to pay by CardPay and wait for the vendor to enter the amount. Scan your university card and enter pin. Press enter and all done.',
	},
	{
		question: 'How to put money in account?',
		answer: "In Dashboard, tap on 'Deposit'. Copy the PayPro voucher number. Pay via online banking, mobile banking, or debit/credit card. Further instructions for each method is provided with pictures in Deposit section.",
	},
	{
		question: 'Can we take money out once put into card?',
		answer: 'Yes, but you can not directly withdraw the money. But, you can always transfer the money from your CardPay account to any other person with the CardPay account and get cash in return from them.',
	},
	{
		question: "Can Alumni's use this?",
		answer: "Yes, but you need to have your LUMS Outlook email access. That's because during sign up, the OTP code is sent your LUMS Outlook email.",
	},
	{
		question: 'Is my money secured if I put it in CardPay?',
		answer: 'Yes, your money is completely secured with CardPay. CardPay is powered by Amazon AWS security and uses PayPro as a payment gateway.',
	},
	{
		question: 'Where can I use CardPay?',
		answer: 'Currently, CardPay is live within LUMS at Bunker, Jammin Java, Baradari, Delish, Frooti, Juice Zone, Subway, and Chop Chop. Soon, it will be live at Zakir and Zaan. CardPay is also in talks with LUMS admin regarding availability at PDC and other inter-related eateries.',
	},
];

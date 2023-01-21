/** @type {import('tailwindcss').Config} */
module.exports = {
	content: [
		'./pages/**/*.{js,ts,jsx,tsx}',
		'./components/**/*.{js,ts,jsx,tsx}',
	],
	theme: {
		extend: {
			colors: {
				"primary": "#0084bfff",
				"primarydark": "#004c8bf5",
				"primarylight": "#3ba1c5",
				"btncolor": "#2587be",
			}
		},
	},
	plugins: [require('daisyui')],
	daisyui: {
		themes: ['winter'],
	},
};

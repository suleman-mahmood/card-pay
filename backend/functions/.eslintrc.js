module.exports = {
	root: true,
	env: {
		es6: true,
		node: true,
	},
	extends: [
		'eslint:recommended',
		'plugin:import/errors',
		'plugin:import/warnings',
		'plugin:import/typescript',
		'google',
		'plugin:@typescript-eslint/recommended',
	],
	parser: '@typescript-eslint/parser',
	parserOptions: {
		project: ['tsconfig.json', 'tsconfig.dev.json'],
		tsconfigRootDir: __dirname,
		sourceType: 'module',
	},
	ignorePatterns: [
		'/lib/**/*', // Ignore built files.
	],
	plugins: ['@typescript-eslint', 'import'],
	rules: {
		quotes: ['error', 'single'],
		'import/no-unresolved': 0,
		indent: [0, 'tab'],
		'no-tabs': 0,
		'object-curly-spacing': [2, 'always'],
		'arrow-parens': 0,
		'max-len': 0,
		'quote-props': 0,
	},
};

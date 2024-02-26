require('@rushstack/eslint-patch/modern-module-resolution')

module.exports = {
	root: true,
	parserOptions: {
		ecmaVersion: 'latest',
		sourceType: 'module',
	},
	extends: [
		'eslint:recommended',
		'plugin:vue/vue3-recommended',
		'@vue/eslint-config-typescript'
	],
	rules: {
		'camelcase': 'warn',
		'max-len': ['error', {
			'code': 150,
			'tabWidth': 4,
		}],

		'vue/camelcase': 'warn',
		'vue/max-len': ['error', {
			'code': 150,
			'template': 150,
			'tabWidth': 4,
		}],

		'semi': ["error", "never"],

		"vue/max-attributes-per-line": ["error", {
			"singleline": {
				"max": 4
			},
			"multiline": {
				"max": 1
			}
		}],

		'vue/html-indent': ['error', "tab"],

		"vue/block-lang": ["error", {
			"script": {
				"lang": "ts"
			}
		}]

	}
}
require('@rushstack/eslint-patch/modern-module-resolution')

// eslint-disable-next-line no-undef
module.exports = {
	root: true,
	parserOptions: {
		ecmaVersion: 'latest',
		sourceType: 'module',
	},
	extends: [
		// add more generic rulesets here, such as:
		'eslint:recommended',
		'plugin:vue/vue3-recommended',
		'@vue/eslint-config-typescript'
	],
	rules: {
		// override/add rules settings here, such as:
		// 'vue/no-unused-vars': 'error'
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

		"vue/max-attributes-per-line": ["error", {
			"singleline": {
				"max": 4
			},
			"multiline": {
				"max": 1
			}
		}],

		'vue/html-indent': ['error', "tab"],
	}
}
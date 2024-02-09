// eslint-disable-next-line no-undef
module.exports = {
    extends: [
        // add more generic rulesets here, such as:
        'eslint:recommended',
        'plugin:vue/vue3-recommended',
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
        }]
    }
}
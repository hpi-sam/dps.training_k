describe('pass-through tests', () => {
	beforeEach(() => {
		cy.visit('http://localhost:5173/')
	})

	it('trainer failed login test', () => {
		cy.get('#trainer-login-username').type('test')
		cy.get('#trainer-login-password').type('passwort')
		cy.get('#trainer-login').click()
		cy.get('.Vue-Toastification__toast-body').should('contain', 'Fehler: Falsches Passwort')
	})

	it('trainer login & passthrough test', () => {
		cy.get('#trainer-login-username').type('test')
		cy.get('#trainer-login-password').type('password')
		cy.get('#trainer-login').click()
		cy.get('#ps-test').should('be.visible').click()
		cy.get('.Vue-Toastification__toast-body').should('contain', 'received test event')
	})

	it('trainer create patient instance', () => {
		cy.get('#trainer-login-username').type('test')
		cy.get('#trainer-login-password').type('password')
		cy.get('#trainer-login').click()

		cy.get('#add-area-button').click()
		cy.get('.list-item').first().find('.list-item-button').click()
		cy.get('#create-patient-button').click()
		cy.contains('.available-patient-button', '1001').click()
		cy.get('#save-button').click()
		cy.get('.close-button').click()
		cy.contains('.list-item-button', '1001').should('be.visible')

		cy.get('#nav-exercise-code').invoke('text').then((exerciseId) => {
			Cypress.env('exercise-id', exerciseId.trim())
		})
		cy.contains('.list-item-button', '1001').find('.list-item-left').invoke('text').then((patientId) => {
			Cypress.env('patient-id', patientId.trim())
		})
	})

	it('patient login & passthrough test', () => {
		cy.get('#patient-login-exercise-id').type(Cypress.env('exercise-id'))
		cy.get('#patient-login-patient-id').type(Cypress.env('patient-id'))
		cy.get('#patient-login').click()
		cy.get('#ps-test').should('be.visible').click()
		cy.get('.Vue-Toastification__toast-body').should('contain', 'received test event')
	})
})
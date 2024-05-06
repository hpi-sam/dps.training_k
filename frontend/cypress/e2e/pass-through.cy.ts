describe('pass-through tests', () => {
	beforeEach(() => {
		cy.visit('http://localhost:5173/')
	})

	it('trainer route passthrough test', () => {
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

		cy.get('#create-exercise-button').click()
		cy.get('#add-area-button').click()
		cy.get('.listItem').first().find('.listItemButton').click()
		cy.get('#create-patient-button').click()
		cy.contains('.availablePatientButton', '1001').click()
		cy.get('#saveButton').click()
		cy.get('.close-button').click()
		cy.contains('.listItemButton', '1001').should('be.visible')

		cy.get('#nav-exercise-code').invoke('text').then((exerciseId) => {
			Cypress.env('exerciseId', exerciseId.trim())
		})
		cy.contains('.listItemButton', '1001').find('.listItemId').invoke('text').then((patientId) => {
			Cypress.env('patientId', patientId.trim())
		})
	})

	it('patient route passthrough test', () => {
		cy.get('#patient-login-exercise-id').type(Cypress.env('exerciseId'))
		cy.get('#patient-login-patient-id').type(Cypress.env('patientId'))
		cy.get('#patient-login').click()
		cy.get('#ps-test').should('be.visible').click()
		cy.get('.Vue-Toastification__toast-body').should('contain', 'received test event')
	})
})
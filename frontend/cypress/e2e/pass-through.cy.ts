describe('pass-through tests', () => {
	it('trainer route passthrough test', () => {
		cy.visit('http://localhost:5173/')
		cy.get('#trainer-login-username').type('test')
		cy.get('#trainer-login-password').type('password')
		cy.get('#trainer-login').click()
		cy.get('#ps-test').should('be.visible').click()
		cy.get('.Vue-Toastification__toast-body').should('contain', 'received test event')
	})

	it('patient route passthrough test', () => {
		cy.visit('http://localhost:5173/')
		cy.get('#patient-login-exercise-id').type('123456')
		cy.get('#patient-login-patient-id').type('6')
		cy.get('#patient-login').click()
		cy.get('#ps-test').should('be.visible').click()
		cy.get('.Vue-Toastification__toast-body').should('contain', 'received test event')
	})
})
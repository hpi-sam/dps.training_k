describe('pass-through tests', () => {
	it('trainer route passthrough test', () => {
		cy.visit('http://localhost:5173/')
		cy.get('#trainer-module-button').click()
		cy.get('#ps-test').should('be.visible').click()
		cy.get('.Vue-Toastification__toast-body').should('contain', 'received test event')
	})

	/*it('patient route passthrough test', () => {
		cy.visit('http://localhost:5173/')
		cy.get('#patient-module-button').click()
		cy.get('#ps-test').should('be.visible').click()
		cy.get('.Vue-Toastification__toast-body').should('contain', 'received test event')
	})*/
})
import {SignInPage} from "../../app/pages/sign-in-page.js";
import {AuthenticationModule} from "../../app/modules/authentication.module.js";


describe(SignInPage, () => {
    describe('signing in', () => {
        it.skip('signs in at authentication module', () => {
            let authenticationModule = new class extends AuthenticationModule {
                signIn = jest.fn(() => {})
            }
            SignInPage(authenticationModule);

            let sip = document.createElement('sign-in-page');
            document.body.appendChild(sip);
            console.log(sip._shadowRoot);
            expect(document.querySelector("#kookkie-signin").textContent).toContain("Please sign in");

        });
    });
});
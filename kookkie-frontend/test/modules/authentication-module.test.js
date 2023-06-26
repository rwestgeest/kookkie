import {AuthenticationModule} from "../../app/modules/authentication.module.js";
import {Authenticator} from "../../app/domain/authenticator.js";
import {UserProfileModule} from "../../app/modules/user-profile-module.js";


describe(AuthenticationModule, () => {
    describe('signing in', () => {
        let userProfileModule;
        let authenticator;
        let authenticationModule;

        beforeEach(() => {
            userProfileModule = new class extends UserProfileModule {
                onSignIn = jest.fn(() => {})
            }();
            authenticator = new class extends Authenticator {
                authenticate = jest.fn((username, password) => Promise.resolve())
            }();
            authenticationModule = new AuthenticationModule(userProfileModule, authenticator);
        });

        it('authenticates at the authenticator', async () => {
            await authenticationModule.signIn("harry", "verysecret");
            expect(authenticator.authenticate).toHaveBeenCalledWith("harry", "verysecret");
        });

        it('updates the profile when sign in is successful', async () => {
            await authenticationModule.signIn("harry", "verysecret");
            expect(userProfileModule.onSignIn).toHaveBeenCalled();
        });

        describe('when it fails', () => {
            it('does not update the profile', async () => {
                authenticator.authenticate = jest.fn(() => Promise.reject({messageId: "error while signing in"}));
                await authenticationModule.signIn("harry", "verysecret");
                expect(userProfileModule.onSignIn).not.toHaveBeenCalled();
            });

            it('prepares an error message', async () => {
                authenticator.authenticate = jest.fn(() => Promise.reject({messageId: "error while signing in"}));
                await authenticationModule.signIn("harry", "verysecret");
                expect(authenticationModule.errorMessage).toEqual("error while signing in");
            });

        });
    });
});
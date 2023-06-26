export class AuthenticationModule {
    constructor(userProfileModule, authenticator) {
        this._userProfileModule = userProfileModule;
        this._authenticator = authenticator;
    }

    get errorMessage() {
        return this._errorMessage;
    }

    async signIn(username, password) {
        await this._authenticator.authenticate(username, password)
            .then(() => {
                this._userProfileModule.onSignIn();
            })
            .catch(() => {
                this._errorMessage = "error while signing in";
            });
    }
}
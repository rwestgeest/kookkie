import { Component } from '../components/component.js'

export function SignInPage(userProfileModule) {
    return Component.define('sign-in-page', class extends Component {
        constructor() {
            super();
            this.userProfileModule = userProfileModule;
        }

        html() {
            return /*html*/ `
            <div class="kookkie">
              <h2>Please sign in with your username and password</h2>
              <form @submit.prevent>
                  Username:
                  <input
                  id="sign-in-username"
                  placeholder="username (email address)"/>

                 Password: <input
                  id="sign-in-password"
                  type="password"
                  placeholder="password"/>
                 
                <div class="buttons">
                  <button id="sign-in-button" class="button" type="submit">Sign in</button>
                </div>
              </form>
            </div>
        `
        }

        onInit() {
            this._shadowRoot.getElementById('sign-in-button').addEventListener('click', e => this.login());
        }

        login() {
            let username = this.elementById('sign-in-username').value;
            let password = this.elementById('sign-in-password').value;
            fetch('/api/login', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({username: username, password: password})
            })
                .then((response) => {
                    if (response.ok) {
                        this.userProfileModule.onSignIn();
                    }
                });
        }

    });
}
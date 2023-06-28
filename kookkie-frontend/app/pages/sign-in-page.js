import { Component } from '../components/component.js'

export function SignInPage(authenticationModule) {
    return Component.define('sign-in-page', class extends Component {
        constructor() {
            super();
            this._authenticationModule = authenticationModule;
        }

        html() {
            return /*html*/ `
            <div id="kookkie-signin">
              <h2>Please sign in with your username and password</h2>
              <form>
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

        whenRendered() {
            this._shadowRoot.getElementById('sign-in-button').addEventListener('click', e => this.login());
        }

        login() {
            let username = this.elementById('sign-in-username').value;
            let password = this.elementById('sign-in-password').value;
            this._authenticationModule.signIn(username, password);
        }

    });
}
import {GetPeople, HttpBasedPersonRepository} from "./get-people.js";
import {PageThatRenders, Router} from "./router.js";
import { Component } from './components/component.js';

export class UserProfileModule  {
    constructor() {
        this.userProfile = {}
    }
    onSignIn() {
        this.getUserProfile().then(() => {
            window.location.hash = "#/sessions";
        });
    }

    async getUserProfile() {
        self = this;
        await fetch('/api/profile', {
            headers: {
                "Content-Type": "application/json",
            }}).then(r => {
                if (r.ok) {
                    r.json().then(userProfile => {
                        self.userProfile = userProfile;
                        console.log(userProfile);
                    });
                }
            });
    }

}
export function SessionsPage(userProfileModule) {
    return class extends Component {
        constructor() {
            super();
            this.userProfileModule = userProfileModule;
            this.kookkies = [{ name: 'lekker eten met antond'} ];
        }
        html() {
            let profile = this.userProfileModule.userProfile
            return `<p class="profile-header"> ${profile.name} </p>
            <h1>Sessions</h1>
            <ul class="Kookkies">
                 ${ this.kookkies.map(k => { `<li>k.name</li>` }).join('\n') }
                
            </ul>`
        }
        onInit() {

        }
    }

}
export function SignInPage(userProfileModule)
{
    return class extends Component {
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

    }
}
customElements.define('get-people', GetPeople(new HttpBasedPersonRepository()));
let userProfileModule = new UserProfileModule();
customElements.define('sign-in-page', SignInPage(userProfileModule));
customElements.define('sessions-page', SessionsPage(userProfileModule));

const router = new Router(window)
    .addRoute('#/', new PageThatRenders('root-content'))
    .addRoute('#/sessions', new PageThatRenders('<sessions-page></sessions-page>'))
    .addRoute('#/signin', new PageThatRenders('<sign-in-page></sign-in-page>'))
    .default('#/signin')
    .start();


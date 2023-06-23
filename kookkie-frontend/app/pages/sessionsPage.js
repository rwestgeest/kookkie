import {Component} from '../components/component.js';

export function SessionsPage(userProfileModule) {
    return Component.define('sessions-page', class extends Component {
        constructor() {
            super();
            this.userProfileModule = userProfileModule;
            this.kookkies = [{name: 'lekker eten met anton'}];
        }

        html() {
            let profile = this.userProfileModule.userProfile
            return `
                <p class="profile-header"> ${profile.name} </p>
                <h1>Sessions</h1>
                <ul id="kookkies-list">
                     ${this.kookkies.map(k => {
                return `<li onclick="">${k.name}</li>`
            }).join('\n')}
                </ul>
                `
        }

        onInit() {
            this.elementById('kookkies-list').addEventListener('click', e => {
                console.log('click', e.target.dataset);
            })
        }
    });
}
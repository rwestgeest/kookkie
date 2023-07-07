import {Component} from '../components/component.js';

export function SessionsPage(kookkiesModule, userProfileModule) {
    return Component.define('sessions-page', class extends Component {
        constructor() {
            super();
            this.userProfileModule = userProfileModule;
            this.kookkiesModule = kookkiesModule;
            this.kookkies = [];
        }

        html() {
            let profile = this.userProfileModule.userProfile
            return `
                <style>
                    .kookkie-name {padding-right: 2em;}
                    li {}
                </style>
                <p class="profile-header"> ${profile.name} </p>
                <h1>Sessions</h1>
                <ul id="kookkies-listt">
                     ${this.kookkies.map(k => {
                        return `<li id="${k.id}"><a href="#/session/${k.id}"><span class="kookkie-name">${k.name}</span>
                                <span class="kook-name">${k.kook_name}</span></a></li>`
                    }).join('\n')}
                </ul>
                `
        }

        update() {
            this.kookkies = this.kookkiesModule.kookkies;
            this.render();
        }

        onInit() {
            this.kookkiesModule.registerView(this);
            this.kookkiesModule.obtainKookkies();
        }
    });
}
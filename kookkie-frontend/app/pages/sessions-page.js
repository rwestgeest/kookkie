import {Page} from "./page.js";

export class SessionsPage extends Page {
    constructor(kookkiesModule, userProfileModule) {
        super();
        this.userProfileModule = userProfileModule;
        this.kookkiesModule = kookkiesModule;
        this.kookkies = [];
        this.kookkiesModule.registerView(this);
    }

    open() {
        super.open();
        this.kookkiesModule.obtainKookkies();
    }

    render() {
        let profile = this.userProfileModule.userProfile
        document.querySelector('#router-view').innerHTML = `
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

}
import {elementById, hide, show, Page} from "./page.js";



export class SessionPage extends Page {
    constructor(kookkiesModule, userProfileModule) {
        super();
        this.userProfileModule = userProfileModule;
        this.kookkiesModule = kookkiesModule;
    }

    open({id}) {
        this.profile = this.userProfileModule.userProfile;
        this.kookkie = this.kookkiesModule.byId(id);
        super.open({id});
        elementById("open-meeting-button").addEventListener('click', () => {
            this.startSession(id);
        });
    }

    render({id}) {
        this.renderInPageView(`
            <style>
                .kookkie-name {padding-right: 2em;}
                li {}
            </style>
            <p class="profile-header"> ${this.profile.name} </p>
            <h1>Kookkie</h1>
            <p><span class="kookkie-name">${this.kookkie.name}</span>
            <span class="kook-name">${this.kookkie.kook_name}</span> </p>
            <p>Share this link to invite: <a href="#/join/${this.kookkie.id}">${window.location.origin}/#/join/${this.kookkie.id}</a></p>
            <div id="videowindow">
                 <button id="open-meeting-button">open</button>
                 <p id="open-meeting-throbber" hidden="true">opening</p>
            </div>
            `);

    }

    startSession(id) {
        hide("open-meeting-button");
        show("open-meeting-throbber");
        this.kookkiesModule.start(id).then(startedKookkie => {
            elementById("videowindow").innerHTML = `<jitsi-video jwt="${startedKookkie.jwt}" room="${startedKookkie.room_name}"></jitsi-video>`
        });
    }
}
import {Page} from "./page.js";

export class SessionPage extends Page {
    constructor(kookkiesModule, userProfileModule) {
        super();
        this.userProfileModule = userProfileModule;
        this.kookkiesModule = kookkiesModule;
    }

    render({id}) {
        let profile = this.userProfileModule.userProfile;
        let kookkie = this.kookkiesModule.byId(id);
        document.querySelector("#router-view").innerHTML = `
            <style>
                .kookkie-name {padding-right: 2em;}
                li {}
            </style>
            <p class="profile-header"> ${profile.name} </p>
            <h1>Kookkie</h1>
            <p><span class="kookkie-name">${kookkie.name}</span>
            <span class="kook-name">${kookkie.kook_name}</span> </p>
            <p><a href="#/join/${kookkie.id}">${window.location.origin}/#/join/${kookkie.id}</a></p>
            <div id="videowindow">
                 <button id="open-meeting-button">open</button>
                 <p id="open-meeting-throbber" hidden="true">opening</p>
            </div>
            `
        document.querySelector("#open-meeting-button").addEventListener('click', e => {
            document.getElementById("open-meeting-button").hidden = true;
            document.getElementById("open-meeting-throbber").hidden = false;
            const startedKookkie = this.kookkiesModule.start(id).then(startedKookkie => {
                document.getElementById("videowindow").innerHTML=`<jitsi-video jwt="${startedKookkie.jwt}" room="${startedKookkie.room_name}"></jitsi-video>`
            });
        });
    }

}
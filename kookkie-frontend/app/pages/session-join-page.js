export class SessionJoinPage {
    constructor(participantModule) {
        this.participantModule = participantModule;
    }

    get kookkie() {
        return this.participantModule.kookkie;
    }

    async render({id}) {
        await this.participantModule.join(id);

        document.querySelector("#router-view").innerHTML = `
            <style>
                .kookkie-name {padding-right: 2em;}
                li {}
            </style>
            <div id="participant-session-details" style="visibility: hidden">
                <h1>Welcome as participant to</h1>
                <p><span class="kookkie-name">${this.kookkie.name}</span>
                <span class="kook-name">${this.kookkie.kook_name}</span> </p>
                
                <div id="meet" style="height:700px; width:100%; border: 1px solid black">
            </div>
            <div id="error" style="visibility: hidden">
                <p>uh oh</p>
            </div>
            `

        if (this.kookkie) {
            document.getElementById("participant-session-details").style.visibility='visible';
            const domain = 'meet.jit.si';
            const options = {
                roomName: this.kookkie.callIdentifier(),
                parentNode: document.querySelector('#meet')
            };

            const api = new JitsiMeetExternalAPI(domain, options);
        } else {
            document.getElementById("error").style.visibility='visible';
        }

    }
}
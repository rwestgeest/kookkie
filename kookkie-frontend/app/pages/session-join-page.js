export class SessionJoinPage {
    constructor(participantModule) {
        this.participantModule = participantModule;
    }

    get kookkie() {
        return this.participantModule.started_kookie;
    }

    async render({id}) {
        await this.participantModule.join(id)
        document.querySelector("#router-view").innerHTML = `
            <style>
                .kookkie-name {padding-right: 2em;}
                li {}
            </style>
            <div id="participant-session-details" style="visibility: hidden">
                <h1>Joining as participant </h1>
                <p><span class="kookkie-name">${this.kookkie.name}</span> by 
                <span class="kook-name">${this.kookkie.kook_name}</span> </p>
                <div id="videowindow">
                    <jitsi-video jwt="${this.kookkie.jwt}" room="${this.kookkie.room_name}"></jitsi-video>
                </div>
            </div>
            <div id="error" hidden="true">
                <p>uh oh</p>
            </div>
            `

        if (this.kookkie) {
            document.getElementById("participant-session-details").style.visibility='visible';
            const domain = '8x8.vc';
            const options = {
                roomName: "vpaas-magic-cookie-6fddcef654f54c9eb12e42fe96ba432f/LekkerEtenMetRob",
                jwt: 'eyJhbGciOiJSUzI1NiIsImtpZCI6InZwYWFzLW1hZ2ljLWNvb2tpZS02ZmRkY2VmNjU0ZjU0YzllYjEyZTQyZmU5NmJhNDMyZi85OTczNTUiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE2ODg1NjAxNzMsIm5iZlRpbWUiOjE2ODg1NTI5NjMsInJvb20iOiJMZWtrZXJFdGVuTWV0Um9iIiwic3ViIjoidnBhYXMtbWFnaWMtY29va2llLTZmZGRjZWY2NTRmNTRjOWViMTJlNDJmZTk2YmE0MzJmIiwiY29udGV4dCI6eyJ1c2VyIjp7Im1vZGVyYXRvciI6ImZhbHNlIiwibmFtZSI6IkhhcnJ5IiwiZW1haWwiOiJIYXJyeUBrb29ra2llLmNvbSIsImlkIjoiOGIxNjU1NjEtMjMxMy00ZWJiLTk2YWItMWJmNWVkYmIzMmJjIn0sImZlYXR1cmVzIjp7ImxpdmVzdHJlYW1pbmciOiJmYWxzZSIsInJlY29yZGluZyI6ImZhbHNlIiwib3V0Ym91bmQtY2FsbCI6ImZhbHNlIiwidHJhbnNjcmlwdGlvbiI6ImZhbHNlIn19LCJpc3MiOiJjaGF0IiwiYXVkIjoiaml0c2kifQ.hMbOUpBd3tWAMO4bY-tX68COWFUBts0P7HzaXo9ErjPqAYiPPYN-RLkFZXTk8d5Q_kNGFADCQ8ZkpbpuhjlMEnB7DiN22tOKeHmxOWbn8yLg_3C_GWC-TTzV-piYcDA8MoL8ZOex1rr56CreGO85oJu6Ilrc1R8fwU_OI7XmXi8iAp4hezJf7EjGwEPEFpGMJ746n_980qXNvPV8lrldttcUhoD0ebJ3kVHWwVY-nwa9YicA9_YbudLxMu-E-X9xG-fL9yHYzddkxNmslBzw0Qo_gzy8FXnRpwTrpfCk9x0yV9zydVvxD8C4DwKjfIXN8sUcntReWM7YZj7pCWVZ-A',
                parentNode: document.querySelector('#meet')
            };

            const api = new JitsiMeetExternalAPI(domain, options);
        } else {
            document.getElementById("error").style.visibility='visible';
        }

    }
}
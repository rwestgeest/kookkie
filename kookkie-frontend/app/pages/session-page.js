
export class SessionPage {
    constructor(kookkiesModule, userProfileModule) {
        this.userProfileModule = userProfileModule;
        this.kookkiesModule = kookkiesModule;
    }

    render({id}) {
        let profile = this.userProfileModule.userProfile;
        console.log(profile);
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
            
            <div id="meet" style="height:700px; width:100%; border: 1px solid black">
            `

        const domain = '8x8.vc';
        const options = {
            roomName: "vpaas-magic-cookie-6fddcef654f54c9eb12e42fe96ba432f/LekkerEtenMetRob",
            jwt: 'eyJhbGciOiJSUzI1NiIsImtpZCI6InZwYWFzLW1hZ2ljLWNvb2tpZS02ZmRkY2VmNjU0ZjU0YzllYjEyZTQyZmU5NmJhNDMyZi85OTczNTUiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE2ODg1NjAwMDgsIm5iZlRpbWUiOjE2ODg1NTI3OTgsInJvb20iOiJMZWtrZXJFdGVuTWV0Um9iIiwic3ViIjoidnBhYXMtbWFnaWMtY29va2llLTZmZGRjZWY2NTRmNTRjOWViMTJlNDJmZTk2YmE0MzJmIiwiY29udGV4dCI6eyJ1c2VyIjp7Im1vZGVyYXRvciI6InRydWUiLCJuYW1lIjoiUm9iIiwiZW1haWwiOiJyb2JAcXdhbi5ldSIsImlkIjoiMTExMTExMTEtMTExMS0xMTExLTExMTEtMTExMTExMTExMTAwIn0sImZlYXR1cmVzIjp7ImxpdmVzdHJlYW1pbmciOiJmYWxzZSIsInJlY29yZGluZyI6ImZhbHNlIiwib3V0Ym91bmQtY2FsbCI6ImZhbHNlIiwidHJhbnNjcmlwdGlvbiI6ImZhbHNlIn19LCJpc3MiOiJjaGF0IiwiYXVkIjoiaml0c2kifQ.NIBrZghBvudeDN7G_jBd6II6ibgoaTbxjc4B-DtCXGCo0iZ_FKgXyKFgxfvy418RKrkUAnT9msq3JNwWxOiVNnE81OuVLgMb1sw2hsouPqr3gYQBJCAQCLSiI-CnOI2LUJ2DBAik7rZFo6U1BTg2yNv0SuzP0ZxLY9GtjzRylxzSqALe-pE9EKZvtENhGTOQUIavLONhEfy7P2hn4WglzLb4L24hUf3-zT7nc4fLXzrELPF34D-P0nIERTE6Rxfn1GwnrPg_49fLwRwKrNmYjq4EP3AnLoXfa47FmVLmVw8MFUSzyVG2-1gST81VD8kFPuPnoeJqZ1Q_VImxda_U_g',
            parentNode: document.querySelector('#meet')
        };

        const api = new JitsiMeetExternalAPI(domain, options);

    }

}
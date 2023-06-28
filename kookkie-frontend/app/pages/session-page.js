
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

        const domain = 'meet.jit.si';
        const options = {
            roomName: kookkie.callIdentifier(),
            userInfo: {
                email: profile.email,
                displayName:  profile.name
            },
            parentNode: document.querySelector('#meet')
        };

        const api = new JitsiMeetExternalAPI(domain, options);

    }

}
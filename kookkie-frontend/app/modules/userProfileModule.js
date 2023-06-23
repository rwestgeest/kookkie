export class UserProfileModule {
    constructor() {
        this.userProfile = {}
    }

    onSignIn() {
        this.getUserProfile().then(() => {
            window.location.hash = "#/sessions";
        });
    }

    async getUserProfile() {
        this.userProfile = await fetch('/api/profile', {
            headers: {
                "Content-Type": "application/json",
            }
        }).then(r => {
            if (r.ok) {
                return r.json();
            } else {
                return {name: "unknown"};
            }
        });
    }
}
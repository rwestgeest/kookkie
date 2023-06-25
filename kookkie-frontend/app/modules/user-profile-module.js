import {UserProfile} from "../domain/userProfile.js";

export class UserProfileModule {
    constructor(userProfileRepository) {
        this._userProfileRepository = userProfileRepository;
        this.userProfile = UserProfile.null();
    }

    async homePage() {
        await this._obtainUserProfile();
        return this.userProfile.homePage();
    }

    async _obtainUserProfile() {
        return this._userProfileRepository.get()
            .catch((reason) => this.userProfile = UserProfile.null())
            .then(userProfile => this.userProfile = userProfile);
    }

    onSignIn() {
        this._obtainUserProfile().then(() => {
            window.location.hash = "#/sessions";
        })
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
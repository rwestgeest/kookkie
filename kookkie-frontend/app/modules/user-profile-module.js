import {UserProfile} from "../domain/user-profile.js";
import {ObservableModel} from "../domain/observable-model.js";

export class UserProfileModule extends ObservableModel {
    constructor(userProfileRepository) {
        super();
        this._userProfileRepository = userProfileRepository;
        this._userProfile = UserProfile.null();
    }

    set userProfile(value) {
        const old_profile = this._userProfile;
        this._userProfile = value;
        if (JSON.stringify(old_profile) !== JSON.stringify(value)) {
            this.changed();
        }
    }
    get userProfile() {
        return this._userProfile;
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
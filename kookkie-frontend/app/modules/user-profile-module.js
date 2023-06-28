import {UserProfile} from "../domain/user-profile.js";
import {ObservableModel} from "../domain/observable-model.js";

export class UserProfileModule extends ObservableModel {
    constructor(userProfileRepository, router) {
        super();
        this._userProfileRepository = userProfileRepository;
        this._userProfile = UserProfile.null();
        this._router = router;
    }

    set userProfile(value) {
        if (JSON.stringify(this._userProfile) === JSON.stringify(value)) return;
        this._userProfile = value;
        this._router.goto(this.homePage());
    }

    get userProfile() {
        return this._userProfile;
    }

    homePage() {
        return this.userProfile.homePage();
    }

    async obtainUserProfile() {
        return this._userProfileRepository.get()
            .catch((reason) => this.userProfile = UserProfile.null())
            .then(userProfile => this.userProfile = userProfile);
    }

    onSignIn() {
        this.obtainUserProfile().then(() => {
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
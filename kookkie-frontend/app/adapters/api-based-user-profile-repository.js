import {UserProfileRepository} from "../domain/user-profile-repository.js";
import {UserProfile} from "../domain/user-profile.js";

export class ApiBasedUserProfileRepository extends UserProfileRepository {
    async get() {
        return await fetch('/api/profile', {
            headers: {
                "Content-Type": "application/json",
            }
        }).then(r => {
            if (r.ok) {
                return r.json().then( json => new UserProfile(json) );
            } else {
                return UserProfile.null();
            }
        });
    }
}
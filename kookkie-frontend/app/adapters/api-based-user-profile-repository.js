import {UserProfileRepository} from "../domain/user-profile-repository.js";
import {UserProfile} from "../domain/user-profile.js";

export class ApiBasedUserProfileRepository extends UserProfileRepository {
    constructor(http) {
        super();
        this._http = http;
    }

    async get() {
        return this._http.get('/api/profile')
            .then((response) => new UserProfile(response.data))
            .catch(e => UserProfile.null())
    }
}
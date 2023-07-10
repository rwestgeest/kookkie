import {StartedKookkie} from "../domain/kookkie.js";

export class ApiBasedKookkieJoiner {
    constructor(http) {
        this._http = http;
    }

    async join(joining_id) {
        return this._http.post(`/api/kookkie-sessions/${joining_id}/join`, {})
            .then(response => new StartedKookkie(response.data))
            .catch(e => Promise.reject(e.data));
    }
}
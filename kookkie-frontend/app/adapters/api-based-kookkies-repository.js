import {Kookkie, StartedKookkie} from "../domain/kookkie.js";

export class ApiBasedKookkiesRepository {
    constructor(http) {
        this._http = http;
    }
    async allKookkies() {
        return this._http.get('/api/kookkie-sessions')
            .then((response) => response.data.kookkies.map(kookkieJson => new Kookkie(kookkieJson)))
            .catch(e => Promise.reject({message: "unable to obtain kookkie sessions"}));
    }

    async start(id) {
        return this._http.post(`/api/kookkie-sessions/${id}/start`)
            .then((response) => new StartedKookkie(response.data))
            .catch(e => Promise.reject({message: "unable to start kookkie session"}));
    }
}
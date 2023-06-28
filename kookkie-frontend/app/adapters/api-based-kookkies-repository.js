import {Kookkie} from "../domain/kookkie.js";

export class ApiBasedKookkiesRepository {
    constructor(http) {
        this._http = http;
    }
    async allKookkies() {
        return this._http.get('/api/kookkie-sessions')
            .then((response) => response.data.map(kookkieJson => new Kookkie(kookkieJson)))
            .catch(e => Promise.reject({message: "unable to obtain kookkie sessions"}));

    }
}
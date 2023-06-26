import {Authenticator} from "../domain/authenticator.js";

export class ApiBasedAuthenticator extends Authenticator {
    constructor(http) {
        super();
        this._http = http
    }

    async authenticate(username, password) {
        return await this._http.post('/api/login', {username, password})
            .then(() => {
            })
            .catch((e) => Promise.reject(e.data));
    }
}
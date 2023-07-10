import {Kookkie} from "../domain/kookkie.js";

export class ParticipantModule {
    constructor(kookkiesJoiner) {
        this._kookkiesJoiner = kookkiesJoiner;
        this._started_kookie = undefined;
    }

    set started_kookie(value) {
        this._started_kookie = value;
    }

    get started_kookie() {
        return this._started_kookie;
    }

    async join(id) {
        this._started_kookie = await this._kookkiesJoiner.join(id);
    }
}
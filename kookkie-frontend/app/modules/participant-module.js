import {Kookkie} from "../domain/kookkie";

export class ParticipantModule {
    constructor(kookkiesJoiner) {
        this._kookkiesJoiner = kookkiesJoiner;
        this._kookkie = undefined;
    }

    set kookkie(value) {
        this._kookkie = value;
    }

    get kookkie() {
        return this._kookkie;
    }

    async join(id) {
        this._kookkie = await Promise.resolve(new Kookkie({
            id: "121123-123123-123123-123123",
            data: "2023-06-07",
            name: "Lekker eten met anton",
            kook_name: "anton"
        }));
        // this._kookkiesJoiner.join().then(kookkie => {
        //     this.kookkie = kookkie;
        // });
    }
}
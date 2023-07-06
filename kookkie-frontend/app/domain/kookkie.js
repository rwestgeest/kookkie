export class Kookkie {
    constructor({id, data, name, kook_name}) {
        this.id = id;
        this.data = data;
        this.name = name;
        this.kook_name = kook_name;
    }

    callIdentifier() {
        return `Kookkie ${this.name} by ${this.kook_name}`
    }
}

export class StartedKookkie {
    constructor({jwt, room_name, kookkie}) {
        this.jwt = jwt
        this.room_name = room_name
        this.kookkie = new Kookkie(kookkie)
    }
}
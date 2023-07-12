import {ObservableModel} from "../domain/observable-model.js";

export class KookkiesModule extends ObservableModel {
    constructor(kookkiesRepository) {
        super();
        this._kookkiesRepository = kookkiesRepository;
        this._kookkies = []
    }

    set kookkies(value) {
        this._kookkies = value;
    }

    get kookkies() {
        return this._kookkies;
    }

    byId(id) {
        return this.kookkies.find((k) => k.id === id);
    }

    async obtainKookkies() {
        this._kookkiesRepository.allKookkies().then(kookkies => {
            this.kookkies = kookkies;
            this.changed();
        });
    }
    async start(kookkieId) {
        return await this._kookkiesRepository.start(kookkieId);
    }
    async create(kookkieCreationParameters){
        return await this._kookkiesRepository.create(kookkieCreationParameters)
            .catch(e => {
                this.errorMessage = e.messageId;
            });
    }
}
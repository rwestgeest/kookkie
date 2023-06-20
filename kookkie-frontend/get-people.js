
class HttpBasedPersonRepository {
    async getPerson(id) {
        return fetch("/api/people/1.json").then(r => r.json());
    }
}

class GetPeople extends HTMLElement {

    constructor() {
        super();
        this._shadowRoot = this.attachShadow({ mode: "closed" });
        this.person = {};
        this.personRepository = new HttpBasedPersonRepository();
    }

    render() {
            this._shadowRoot.innerHTML = /*html*/ `
            <button id="get-person-button">get person</button>
            <p> ${JSON.stringify(this.person)} </p>
        `
        
    }


    async loadPerson() {
        
        this.person = await this.personRepository.getPerson(1);
        this.render();
    }

    connectedCallback() {
        this.render();
        this._shadowRoot.getElementById("get-person-button").addEventListener("click", e => {
            this.loadPerson();
        });
    }

}

customElements.define('get-people', GetPeople);

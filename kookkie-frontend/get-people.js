
export class HttpBasedPersonRepository  {
    async getPerson(id) {
        return fetch("/api/people/1.json").then(r => r.json());
    }
}

class MyHTMLElement extends HTMLElement {
    constructor() {
        super();
        this._shadowRoot = this.attachShadow({ mode: "closed" });
    }
    render() {
        this._shadowRoot.innerHTML = this.html()
    }
    attributeChangedCallback(property, oldValue, newValue) {
        if (oldValue === newValue) return;
        this.render();
    }
}

export function GetPeople(personRepository) {
    return class extends MyHTMLElement {
        static get observedAttributes() {
            return ['person'];
        }

        constructor() {
            super();
            this.personRepository = personRepository;

        }

        html() {
            return /*html*/ `
            <button id="get-person-button">get person</button>
            <p> ${JSON.stringify(this.person)} </p>
        `

        }

        get person() {
            return JSON.parse(this.getAttribute('person')) || 'no person';
        }

        set person(value) {
            this.setAttribute('person', JSON.stringify(value));
        }

        async loadPerson() {
            this.person = await this.personRepository.getPerson(1);
        }

        connectedCallback() {
            window.requestAnimationFrame(() => {
                this.render();
                this._shadowRoot.getElementById("get-person-button").addEventListener("click", e => {
                    this.loadPerson();
                });
            });
        }
    }
}


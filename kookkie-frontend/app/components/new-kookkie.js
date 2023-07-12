import {Component} from "./component.js";


export function NewKookkie(kookkies) {
    return class extends Component {
        constructor() {
            super();
            this.kookkies = kookkies;
        }
        static get tag_name() { return "new-kookkie"};
        html() {
            return `<form id="new-kookkie-form">
                <label for="new-kookkie-name">Kookkie name</label>
                <input name="new-kookkie-name" id="new-kookkie-name" type="text" placeholder="Name of the new kookkie"/>
                <label for="new-kookkie-date">Kookkie name</label>
                <input name="new-kookkie-date" id="new-kookkie-date" type="date"/>
                <button id="create-kookkie" class="button" type="button">Create Kookkie</button>
                </form>`
        }
        whenRendered() {
           this.elementById('create-kookkie').addEventListener('click', e => this.createKookkie());
        }

        createKookkie() {
            this.kookkies.create({
                name: this.elementById("new-kookkie-name").value,
                date: this.elementById("new-kookkie-date").value});
        }
    }
}

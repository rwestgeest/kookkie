import {Component} from "../../../app/components/component";

export function SomeTag() {
    return class extends Component {
        static tag_name = "some-tag";

        static get observedAttributes() {
            return ['name'];
        }

        get name() {
            return this._name;
        }

        set name(value) {
            this._name = value;
        }

        html() {
            return `<div>
                        <p id="some-id">Hoi</p>
                        <p id="name-paragraph">${this.name}</p>
                        </div>`;
        }
    }
}

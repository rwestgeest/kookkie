import {Component} from "./component.js";

export function JitsiVideo() {
    return class extends Component {
        static tag_name= "jitsi-video";

        static get observedAttributes() { return ['jwt', 'room']; }
        set jwt(value) {
            this._jwt = value;
        }

        get jwt() {
            return this._jwt;
        }

        set room(value) {
            this._room = value;
        }

        get room() {
            return this._room;
        }

        html() {
            return `<div id="meet" style="height:700px; width:100%; border: 1px solid black">
                    </div>`
        }

        whenRendered() {
            const domain = '8x8.vc';
            const options = {
                roomName: this.room,
                jwt: this.jwt,
                parentNode: this.elementById("meet")
            };
            new JitsiMeetExternalAPI(domain, options);
        }
    };
}

1
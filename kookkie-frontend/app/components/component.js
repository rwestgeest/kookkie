
export class Component extends HTMLElement {
    static define(tag, componentClass) {
        customElements.define(tag, componentClass);
    }

    constructor() {
        super();
        this._shadowRoot = this.attachShadow({ mode: "closed" });
    }
    elementById(id) {
        return this._shadowRoot.getElementById(id);
    }

    render(params) {
        window.requestAnimationFrame(() => {
            this._shadowRoot.innerHTML = this.html(params);
            this.whenRendered();
        });
    }

    attributeChangedCallback(property, oldValue, newValue) {
        if (oldValue === newValue) return;
        this[property] = newValue;
    }

    connectedCallback() {
        this.render();
        this.onInit();
    }

    html() {
        return `<p>define the html for this component please</p>`
    }

    onInit() { }
    whenRendered() { }
}



export class Component extends HTMLElement {
    constructor() {
        super();
        this._shadowRoot = this.attachShadow({ mode: "closed" });
    }
    elementById(id) {
        return this._shadowRoot.getElementById(id);
    }
    render() {
        this._shadowRoot.innerHTML = this.html()
    }
    attributeChangedCallback(property, oldValue, newValue) {
        if (oldValue === newValue) return;
        this.render();
    }
    connectedCallback() {
        window.requestAnimationFrame(() => {
            this.render();
            this.onInit();
        });
    }
    onInit() { }
}


export function defineComponent(componentClass) {
    customElements.define(componentClass.tag_name, componentClass);
    return componentClass;
}

export class Component extends HTMLElement {
    static define(tag, componentClass) {
        customElements.define(tag, componentClass);
    }

    constructor() {
        super();
        this._root = this.createShadowRoot();
    }

    createShadowRoot() {
        return this.attachShadow({mode: "closed"});
    }

    get root() {
        return this._root;
    }

    elementById(id) {
        return this.root.getElementById(id);
    }

    render(params) {
        this.root.innerHTML = this.html(params);
        this.whenRendered();
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


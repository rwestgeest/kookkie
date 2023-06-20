export class HelloWorld extends HTMLElement {
    static get observedAttributes() {
        return ['name'];
    }

    constructor() {
        super();
        this.name = 'World';
        this._shadowRoot = this.attachShadow({ mode: 'closed' });
    }


    render() {
        
        const template = document.getElementById('hello-world').content.cloneNode(true);
        const hwMsg = `Hello ${this.name}`;
        Array.from( template.querySelectorAll('.hw-text') )
            .forEach(n => n.textContent = hwMsg);
        this._shadowRoot.replaceChildren(template);
    }


    attributeChangedCallback(property, oldValue, newValue) {

        if (oldValue === newValue) return;
        
        this[ property ] = newValue;
        console.log("changing", property, oldValue, newValue);
        this.render();
    }

    connectedCallback() {
        this.render();
    }

}


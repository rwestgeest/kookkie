class HelloWorld extends HTMLElement {
    static get observedAttributes() {
        return ['name'];
    }

    constructor() {
        super();
        this.name = 'Willem';
    }

    render() {
        this.textContent = `Hello ${ this.name }!`;
    }

    attributeChangedCallback(property, oldValue, newValue) {
        if (oldValue === newValue) return;
        
        this[ property ] = newValue;
        this.render()
    }

    connectedCallback() {
        this.render()
    }

}

customElements.define('hello-world', HelloWorld);

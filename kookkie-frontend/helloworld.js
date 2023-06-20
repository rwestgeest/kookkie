class HelloWorld extends HTMLElement {
    static get observedAttributes() {
        return ['name'];
    }

    constructor() {
        super();
        this.name = 'World';
    }


    render() {
        
        const shadow = this.attachShadow({ mode: 'closed' });
        const template = document.getElementById('hello-world').content.cloneNode(true);
        const hwMsg = `Hello ${this.name}`;
        Array.from( template.querySelectorAll('.hw-text') )
            .forEach(n => n.textContent = hwMsg);
        shadow.append(template);
    }


    attributeChangedCallback(property, oldValue, newValue) {
        if (oldValue === newValue) return;
        
        this[ property ] = newValue;
    }

    connectedCallback() {
        this.render();
    }

}

customElements.define('hello-world', HelloWorld);

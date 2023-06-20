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
        shadow.innerHTML = /* html */`
            <style>
                p {
                    text-align: center;
                    font-weight: normal;
                    padding: 1em;
                    margin: 0 0 2em 0;
                    background-color: #eee;
                    border: 1px solid #666;
                }
                :host {
                    transform: rotate(180deg);
                }
            </style>
            <p>Hello ${ this.name }!</p>
        `;

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

export class InputAge extends HTMLElement {

    static formAssociated = true;

    constructor() {

        super();
        this.internals = this.attachInternals();
        this.setValue('');

    }

    // set form value

    setValue(v) {
        this.value = v  ;
        this.internals.setFormValue(v);

    }

    formAssociatedCallback(form) {
        console.log('form associated:', form.id);
    }

    connectedCallback() {

        const shadow = this.attachShadow({ mode: 'closed' });

        shadow.innerHTML = `
          <style>input { width: 4em; }</style>
          <input type="number" placeholder="age" min="18" max="120" />`;

        // monitor input values
        shadow.querySelector('input').addEventListener('input', e => {
            this.setValue(e.target.value);
        });

    }
}


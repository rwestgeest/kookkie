import { GetPeople, HttpBasedPersonRepository } from "./get-people.js";
import { HelloWorld } from "./helloworld.js";
import { InputAge } from "./inputage.js";

customElements.define('get-people', GetPeople(new HttpBasedPersonRepository()));

customElements.define('hello-world', HelloWorld);
customElements.define('input-age', InputAge);
import { GetPeople, HttpBasedPersonRepository } from "./get-people.js";
import { HelloWorld } from "./helloworld.js";
import { InputAge } from "./inputage.js";
import {PageThatRenders, Router} from "./router.js";

customElements.define('get-people', GetPeople(new HttpBasedPersonRepository()));

customElements.define('hello-world', HelloWorld);
customElements.define('input-age', InputAge);

const rou4ter = new Router(window)
    .addRoute('#/', new PageThatRenders('root-content'))
    .addRoute('#/foo', new PageThatRenders('foo-content'))
    .start();

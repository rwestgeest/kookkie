import { GetPeople, HttpBasedPersonRepository } from "./get-people.js";
import {PageThatRenders, Router} from "./router.js";

customElements.define('get-people', GetPeople(new HttpBasedPersonRepository()));

const rou4ter = new Router(window)
    .addRoute('#/', new PageThatRenders('root-content'))
    .addRoute('#/foo', new PageThatRenders('foo-content'))
    .start();

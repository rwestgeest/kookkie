import {PageThatRenders, Router} from "../app/router";

describe('router', () => {
    let router
    beforeEach(() => {
        document.body.innerHTML = /*html*/`<div id="app"></div>`
        router = new Router(window)
            .addRoute('#/', new PageThatRenders('root-content'))
            .addRoute('#/foo', new PageThatRenders('foo-content'))
            .start();
    });
    it('defaults to slash', () => {
        expect(window.location.hash).toBe('#/');
        expect(document.querySelector("div#app").innerHTML).toEqual('root-content');
    }) ;
    it('it renders another page when window location changes', async () => {
        window.location.hash = '/foo';
        window.dispatchEvent(new Event('hashchange'));
        expect(document.querySelector("div#app").innerHTML).toEqual('foo-content');
    }) ;
});
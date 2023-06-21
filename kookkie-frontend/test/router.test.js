import {PageThatRenders, Router} from "../app/router";

describe('router', () => {
    let router
    beforeEach(() => {
        document.body.innerHTML = /*html*/`<div id="router-view"></div>`
        router = new Router(window)
            .addRoute('#/', new PageThatRenders('root-content'))
            .addRoute('#/foo', new PageThatRenders('foo-content'))
            .start();
    });
    it('defaults to slash', () => {
        expect(window.location.hash).toBe('#/');
        expect(document.querySelector("#router-view").innerHTML).toEqual('root-content');
    }) ;
    it('it renders another page when window location changes', async () => {
        window.location.hash = '/foo';
        window.dispatchEvent(new Event('hashchange'));
        expect(document.querySelector("#router-view").innerHTML).toEqual('foo-content');
    }) ;
});
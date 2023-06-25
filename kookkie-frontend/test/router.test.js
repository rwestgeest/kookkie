import {PageThatRenders, Router} from "../app/router";
import expect from "expect";


class PageThatRendersWithParams extends PageThatRenders{
    constructor(barContent) {
        super(barContent)
    }
    render(params) {
        super.render();
        this.params = params;
    }
}

describe('router', () => {
    let router
    let pageWithParameters;
    beforeEach(() => {
        document.body.innerHTML = /*html*/`<div id="router-view"></div>`
        pageWithParameters = new PageThatRendersWithParams('bar-content');
        router = new Router(window)
            .withNotFound(new PageThatRenders('not found'))
            .addRoute('#/', new PageThatRenders('root-content'))
            .addRoute('#/foo', new PageThatRenders('foo-content'))
            .addRoute('#/bar/:id/:name', pageWithParameters)

    });
    describe('without specifying default path', () => {
        beforeEach(() => {
            router.start();
        });

        it('defaults to slash', () => {
            expect(router.currentLocation()).toBe('#/');
            expect(document.querySelector("#router-view").innerHTML).toEqual('root-content');
        });

        it('it renders another page when window location changes', async () => {
            router.goto('/foo');
            window.dispatchEvent(new Event('hashchange'));
            expect(document.querySelector("#router-view").innerHTML).toEqual('foo-content');
        });

        it('passes paramters to rendered page if any', async () => {
            router.goto('/bar/123/henk');
            window.dispatchEvent(new Event('hashchange'));
            expect(document.querySelector("#router-view").innerHTML).toEqual('bar-content');
            expect(pageWithParameters.params).toEqual({id: "123", name: "henk"});
        });
    });
    describe('when specifying default path', () => {
        beforeEach(() => {
            router.default("#/foo").start();
        });
        it('defaults to that path', () => {
            expect(window.location.hash).toBe('#/foo');
            expect(document.querySelector("#router-view").innerHTML).toEqual('foo-content');
        });

    });
});
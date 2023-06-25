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

class FakeUserProfileModule {
    constructor(homePage) {
        this._homePage = homePage;
    }
    homePage() {
        return Promise.resolve(this._homePage)
    }
}

describe('router', () => {
    let router
    let pageWithParameters;
    let userProfileModule;
    beforeEach(() => {
        document.body.innerHTML = /*html*/`<div id="router-view"></div>`
        pageWithParameters = new PageThatRendersWithParams('bar-content');
        userProfileModule = new FakeUserProfileModule("#/the_home_page");
        router = new Router(window, userProfileModule)
            .withNotFound(new PageThatRenders('not found'))
            .addRoute('#/the_home_page', new PageThatRenders('root-content'))
            .addRoute('#/foo', new PageThatRenders('foo-content'))
            .addRoute('#/bar/:id/:name', pageWithParameters)

    });
    describe('without specifying default path', () => {
        beforeEach(async () => {
            await router.start();
        });

        it('defaults to userProfilesHomePage', () => {
            expect(router.currentLocation()).toBe(userProfileModule._homePage);
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

});
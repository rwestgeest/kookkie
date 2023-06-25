import {PageThatRenders, Router} from "../app/router";
import expect from "expect";
import {ObservableModel} from "../app/domain/observable-model";

class PageThatRendersWithParams extends PageThatRenders{
    constructor(barContent) {
        super(barContent)
    }
    render(params) {
        super.render();
        this.params = params;
    }

}

class FakeUserProfileModule extends ObservableModel {
    constructor(homePage) {
        super()
        this._homePage = homePage;
    }
    homePage() {
        return Promise.resolve(this._homePage)
    }
    setHomePage(page) {
        const oldHome = this._homePage;
        this._homePage = page;
        if (oldHome !== page) {
            this.changed();
        }
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
    describe('when windows location is root', () => {
        beforeEach(async () => {
            window.location.hash = '';
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

        it('changes root when user profile changes', async () => {
            await userProfileModule.setHomePage('#/foo');
            expect(document.querySelector("#router-view").innerHTML).toEqual('foo-content');
        });
    });


    describe('when windows location is anything else', () => {
        beforeEach(async () => {
            window.location.hash = '/foo';
            await router.start();
        });

        it('goes to that page', async () => {
            router.goto('/foo');
            expect(document.querySelector("#router-view").innerHTML).toEqual('foo-content');
        });
    });
});
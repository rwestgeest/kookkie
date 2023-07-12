/**
 * @jest-environment jsdom
 */
import {KookkiesModule} from "../../app/modules/kookkies-module";
import {UserProfileModule} from "../../app/modules/user-profile-module";
import {elementById} from "../../app/pages/page";
import {SessionsPage} from "../../app/pages/sessions-page";
import {Kookkie} from "../../app/domain/kookkie";
import expect from "expect";
import {UserProfile} from "../../app/domain/user-profile";

describe('sessions-page', () => {
    describe('rendering', () => {
        let kookkies;
        let sessionsPage;

        beforeEach(() => {
            document.body.innerHTML = /*html*/`<div id="router-view"></div>`
            kookkies = [
                new Kookkie({id: "kookkie1", date: "2023-07-02", name: "some dinner", kook_name: "harry"}),
                new Kookkie({id: "kookkie2", date: "2023-07-02", name: "some other dinner", kook_name: "harry"})];
            sessionsPage = new SessionsPage(
                new class extends KookkiesModule {
                    get kookkies() {
                        return kookkies;
                    }

                    async obtainKookkies() {
                        this.changed();
                    }
                }(),
                new class extends UserProfileModule {
                    get userProfile() {
                        return new UserProfile({name: "profile name", email: "", role: ""})
                    }
                }()
            );
        });

        it('user profile', () => {
            sessionsPage.open();
            expect(document.querySelector(".profile-header").textContent).toContain("profile name");
        });

        it('contains a list of all sessions', () => {
            sessionsPage.open();
            expect(elementById("kookkies-list")).not.toBeNull();
            expect(document.querySelector("#kookkie1 .kookkie-name").textContent).toEqual("some dinner");
            expect(document.querySelector("#kookkie2 .kookkie-name").textContent).toEqual("some other dinner");
        });

        it('contains links to the sessions pages', () => {
            sessionsPage.open();
            expect(elementById("kookkies-list")).not.toBeNull();
            expect(document.querySelector("#kookkie1 a").href).toEqual("http://localhost/#/session/kookkie1");
            expect(document.querySelector("#kookkie2 a").href).toEqual("http://localhost/#/session/kookkie2");
        });


        it('contains a form to create a new session', () => {
            sessionsPage.open();
            expect(document.querySelector("new-kookkie")).not.toBeNull();
        });

    });
});
/**
 * @jest-environment jsdom
 */
import {defineComponent} from "../../app/components/component";
import {withoutShadowRoot} from "./without-shadow.root";
import {KookkiesModule} from "../../app/modules/kookkies-module";
import expect from "expect";
import {NewKookkie} from "../../app/components/new-kookkie";


describe("new kookkie tag", () => {
    let kookkies;
    beforeAll(() => {
        kookkies = new class extends KookkiesModule {
            create = jest.fn();
        }();

        defineComponent(withoutShadowRoot(NewKookkie(kookkies)));
    });

    it('contains a form with name and date', async () => {
        document.body.innerHTML = '<new-kookkie></new-kookkie>';
        expect(document.querySelector("form#new-kookkie-form input#new-kookkie-name")).not.toBeNull();
        expect(document.querySelector("form#new-kookkie-form input#new-kookkie-date")).not.toBeNull();
    });

    it('filling in the form and clicking create creates the kookkie', async () => {
        document.body.innerHTML = '<new-kookkie></new-kookkie>';

        document.querySelector("input#new-kookkie-name").value = "my meal";
        document.querySelector("input#new-kookkie-date").value = "2023-07-13";
        document.querySelector("button#create-kookkie").click();
        expect(kookkies.create).toHaveBeenCalledWith({name: "my meal", date: "2023-07-13"});
    });

});
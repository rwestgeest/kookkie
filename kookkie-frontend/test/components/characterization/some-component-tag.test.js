/**
 * @jest-environment jsdom
 */
import {defineComponent} from "../../../app/components/component";
import {withoutShadowRoot} from "../without-shadow.root";
import {SomeTag} from "./some-tag";

describe("some component tag", () => {
    beforeAll(() => {
        defineComponent(withoutShadowRoot(SomeTag()));
    });

    it('draws its html', async () => {
        document.body.innerHTML = '<some-tag></some-tag>';
        expect(document.getElementById("some-id").textContent).toEqual("Hoi");
    });

    it('can be passed an attribute', async () => {
        document.body.innerHTML = '<some-tag name="rob"></some-tag>';
        expect(document.getElementById("name-paragraph").textContent).toEqual("rob");
    });

});
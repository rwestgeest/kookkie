/**
 * @jest-environment jsdom
 */
import {withoutShadowRoot} from "../without-shadow.root";
import {SomeTag} from "./some-tag";
import {defineComponent} from "../../../app/components/component";

describe("some component tag", () => {

    it('can redefine component in another file', async () => {
        defineComponent(withoutShadowRoot(SomeTag()));
        document.body.innerHTML = '<some-tag></some-tag>';
        expect(document.getElementById("some-id").textContent).toEqual("Hoi");
    });
});
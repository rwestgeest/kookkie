export function withoutShadowRoot(componentClass) {
    return class extends componentClass {
        createShadowRoot() {
            return document.body;
        }
        get scopedDocument() {
            return document;
        }
    };
}
export function withoutShadowRoot(componentClass) {
    return class extends componentClass {
        createShadowRoot() {
            return this;
        }
    };
}
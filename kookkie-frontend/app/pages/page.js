
export class Page {
    open(args) {
        this.render(args);
    }
    render(args) {

    }

    renderInPageView(html) {
        document.querySelector("#router-view").innerHTML = html
    }
}

export function elementById(elementId) {
    return document.getElementById(elementId);
}
export function hide(elementId) {
    elementById(elementId).hidden = true;
}
export function show(elementId) {
    elementById(elementId).hidden = false;
}

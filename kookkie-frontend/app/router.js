
class Route {
    constructor(path, page) {
        this._page = page;
        this._params = []
        const pathExp = path.replace(/:(\w+)/g, (match, param) => {
            this._params.push(param);
            return '([^\\/]+)'
        }).replace(/\//g, '\\/')
        this._pathExp = new RegExp(`^${pathExp}$`);
    }
    renderPage(path) {
        this._page.render(this.paramsFor(path));
    }

    paramsFor(path) {
        const match = path.match(this._pathExp);
        match.shift();
        const params = {}
        match.forEach((param, index) => params[this._params[index]] = param);
        return params;
    }

    matches(path) {
        const match = path.match(this._pathExp);
        return match != null;
    }
}

export class Router {
    constructor(window) {
        this.routes = [];
        this._default_path = "#/"
        this._window = window
    }

    goto(path) {
        this._window.location.hash = path;
    }

    currentLocation() {
        return window.location.hash;
    }

    withNotFound(page) {
        this.notFoundPage = page;
        return this;
    }
    addRoute(path, page) {
        this.routes.push(new Route(path, page));
        return this;
    }

    renderPage() {
        const currentRoute = this.routes.find(route => route.matches(this.currentLocation()));
        if (currentRoute === undefined) {
            this.notFoundPage.render();
            return;
        }
        currentRoute.renderPage(this.currentLocation());
    }

    async start() {
        if (this.currentLocation() === "" || this.currentLocation() === '#/') {
            this._window.location.hash="#/signin"
        }
        this._window.addEventListener('hashchange', () => {
            this.renderPage()
        }, false);
        this.renderPage();
        return this;
    }

}

export class PageThatRenders {
    constructor(contentToRender) {
        this.contentToRender = contentToRender;
    }
    render() {
        document.querySelector("#router-view").innerHTML = this.contentToRender
    }
}

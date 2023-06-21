class Route {
    constructor(path, page) {
        this._path = path;
        this._page = page;
    }
    renderPage() {
        this._page.render();
    }
    matches(path) {
        return path === this._path    }
}

export class Router {
    constructor() {
        this.routes = [];
        this._default_path = "#/"
    }

    currentLocation() {
        return '/';
    }
    addRoute(path, page) {
        this.routes.push(new Route(path, page));
        return this;
    }

    renderPage() {
        const currentRoute = this.routes.find(route => route.matches(window.location.hash));
        currentRoute.renderPage();
    }

    default(path) {
        this._default_path = path;
        return this;
    }

    start() {
        window.addEventListener('hashchange', () => {
            this.renderPage()
        }, false);
        window.location.hash = this._default_path;
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

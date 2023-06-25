class Route {
    constructor(path, page) {
        this._path = path;
        this._page = page;
        this._params = []
        this._params2 = {}
        const pathExp = path.replace(/:(\w+)/g, (match, param) => {
            this._params.push(param);
            return '([^\\/]+)'
        }).replace(/\//g, '\\/')
        this._pathExp = new RegExp(`^${pathExp}$`);
    }
    renderPage() {
        this._page.render(this._params2);
    }
    matches(path) {
        const match = path.match(this._pathExp);
        if (match != null) {
            match.shift();
            this._params2 = {}
            match.forEach((param, index) => this._params2[this._params[index]] = param);
        }
        return match != null;
    }
}

export class Router {
    constructor() {
        this.routes = [];
        this._default_path = "#/"
    }

    currentLocation() {
        return '/';
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
        const currentRoute = this.routes.find(route => route.matches(window.location.hash));
        if (currentRoute === undefined) {
            this.notFoundPage.render();
            return;
        }
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

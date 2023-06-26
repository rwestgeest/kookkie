
class HTTPStubResponseExpression {
    constructor(httpOperation) {
        this._httpOperation = httpOperation;
    }

    reply(statusCode, data) {
        this._httpOperation.respondWith({status: statusCode, data: data});
    }
}

class HTTPOperation {
    constructor(url) {
        this._url = url;
        this._response = {};
    }
    respondWith(response) {
        this._response = response;
    }
    matches(url) {
        return this._url === url;
    }
    async stubOperation(){
        if (this._response.status >= 200 && this._response.status < 300) {
            return Promise.resolve(this._response);
        }
        return Promise.reject(this._response);
    }
}

export class HTTPStub {
    constructor() {
        this.httpOperation = {}
    }

    onGet(url) {
        this.httpOperation = new HTTPOperation(url);
        return new HTTPStubResponseExpression(this.httpOperation);
    }

    async get(url) {
        if (this.httpOperation.matches(url)) {
            return this.httpOperation.stubOperation();
        }
        return Promise.reject(`no mock operation defined for ${url}`)
    }
}
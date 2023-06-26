
class HTTPStubResponseExpression {
    constructor(httpOperation) {
        this._httpOperation = httpOperation;
    }

    reply(statusCode, data) {
        this._httpOperation.respondWith({status: statusCode, data: data});
    }
}

class HTTPOperation {
    constructor(url, body) {
        this._url = url;
        this._body = body;
        this._response = {};

    }
    respondWith(response) {
        this._response = response;
    }
    matches(url, body={}) {
        return this._url === url  && (this._body === undefined || JSON.stringify(this._body) === JSON.stringify(body));
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
        return Promise.reject(`no get operation prepared for ${url}`)
    }

    onPost(url, body) {
        this.httpOperation = new HTTPOperation(url, body);
        return new HTTPStubResponseExpression(this.httpOperation);
    }

    async post(url, body) {
        if (this.httpOperation.matches(url, body)) {
            return this.httpOperation.stubOperation();
        }
        return Promise.reject(`no post operation defined for ${url} and bpdy ${JSON.stringify(body)}`)
    }

}
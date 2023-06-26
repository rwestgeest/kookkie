import {ApiBasedUserProfileRepository} from "../../app/adapters/api-based-user-profile-repository";
import {UserProfile} from "../../app/domain/user-profile";


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

class HTTPStub {
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

describe(ApiBasedUserProfileRepository, () => {
    let http;
    let profileRepo
    beforeEach(() => {
        http = new HTTPStub();
        profileRepo = new ApiBasedUserProfileRepository(http);
    });

    describe('getting profile', () => {
        it('succeeds when api responds with ok and user profile', async () => {
            http.onGet('/api/profile').reply(200, { email:"rob@qwan.eu",name:"Rob Westgeest",role:"admin"});
            expect(profileRepo.get()).resolves.toEqual(
                new UserProfile({ email:"rob@qwan.eu",name:"Rob Westgeest",role:"admin"})
            );
        });

        it('fails when api responds with failure', async () => {
            http.onGet('/api/profile').reply(401, { reason:"unauthorized"});
            expect(profileRepo.get()).resolves.toEqual(
                UserProfile.null()
            );
        });

    });
});
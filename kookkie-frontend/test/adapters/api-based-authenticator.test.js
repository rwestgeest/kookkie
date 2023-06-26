import {HTTPStub} from "./http-stub";
import {ApiBasedAuthenticator} from "../../app/adapters/api-based.authenticator";

describe(ApiBasedAuthenticator, () => {
    let mock;
    let authenticator;
    beforeEach(() => {
        mock = new HTTPStub()
        authenticator = new ApiBasedAuthenticator(mock)
    })
    describe('authenticating', () => {
        it('should return a full name when authenticated successfully', async () => {
            mock.onPost('/api/login', {username: 'jan', password: 's3cr3t'}).reply(200);
            await authenticator.authenticate('jan', 's3cr3t').then(() =>{});
        });
        it('should take over the message id from the message id in the response on failure', async () => {
            mock.onPost('/api/login').reply(401, {messageId: 'error.authentication.blockedAccount'})
            await authenticator.authenticate('jan', 's3cr3t')
                .then(() => fail('should fail'))
                .catch(error => {
                    expect(error).toEqual({ messageId: 'error.authentication.blockedAccount'})
                });
        });

    });
});
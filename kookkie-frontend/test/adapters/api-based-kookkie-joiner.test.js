import {HTTPStub} from "./http-stub";
import {ApiBasedKookkieJoiner} from "../../app/adapters/api-based-kookkie-joiner";
import {Kookkie} from "../../app/domain/kookkie";

describe(ApiBasedKookkieJoiner, () => {
    let mock;
    let kookkieJoiner;
    beforeEach(() => {
        mock = new HTTPStub()
        kookkieJoiner = new ApiBasedKookkieJoiner(mock)
    });

    describe('joining', () => {
        it('should return a full name when authenticated successfully', async () => {
            mock.onPost('/api/kookkie-sessions/123123/join', {}).reply(200, {
                id: "some-id",
                date: "2023-06-07",
                name: "Lekker eten met anton",
                kook_name: "anton"
            });
            const kookkie = await kookkieJoiner.join('123123');
            expect(kookkie).toEqual(new Kookkie({
                id: "some-id",
                date: "2023-06-07",
                name: "Lekker eten met anton",
                kook_name: "anton"
            }));
        });
        it('should take over the message id from the message id in the response on failure', async () => {
            mock.onPost('/api/kookkie-sessions/123123/join', {}).reply(401, {messageId: 'some.problem'})
            await kookkieJoiner.join('123123')
                .then(() => fail('should fail'))
                .catch(error => {
                    expect(error).toEqual({messageId: 'some.problem'})
                });
        });

    });
});
import {ApiBasedKookkiesRepository} from "../../app/adapters/api-based-kookkies-repository";
import {HTTPStub} from "./http-stub";
import {Kookkie} from "../../app/domain/kookkie";

describe(ApiBasedKookkiesRepository, () => {
    let http;
    let profileRepo
    beforeEach(() => {
        http = new HTTPStub();
        profileRepo = new ApiBasedKookkiesRepository(http);
    });

    describe('getting kookkies', () => {
        it('succeeds when api responds with ok and user profile', async () => {
            http.onGet('/api/kookkie-sessions').reply(200, [{
                id: "some-id",
                date: "2023-06-07",
                name: "Lekker eten met anton",
                kook_name: "anton"
            }]);
            const kookkies = await profileRepo.allKookkies();
            expect(kookkies).toEqual([
                new Kookkie({
                    id: "some-id",
                    date: "2023-06-07",
                    name: "Lekker eten met anton",
                    kook_name: "anton"
                })
            ]);
        });

        it('fails when api responds with failure', async () => {
            http.onGet('/api/kookkie-sessions').reply(401, {message: "unauthorized"});
            expect(profileRepo.allKookkies()).rejects.toEqual(
                {message: "unable to obtain kookkie sessions"}
            );
        });
    });

});
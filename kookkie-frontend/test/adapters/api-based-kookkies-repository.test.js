import {ApiBasedKookkiesRepository} from "../../app/adapters/api-based-kookkies-repository";
import {HTTPStub} from "./http-stub";
import {Kookkie} from "../../app/domain/kookkie";

describe(ApiBasedKookkiesRepository, () => {
    let http;
    let kookkiesRepo
    beforeEach(() => {
        http = new HTTPStub();
        kookkiesRepo = new ApiBasedKookkiesRepository(http);
    });

    describe('getting kookkies', () => {
        it('succeeds when api responds with ok and user profile', async () => {
            http.onGet('/api/kookkie-sessions').reply(200, {
                kookkies: [{
                    id: "some-id",
                    date: "2023-06-07",
                    name: "Lekker eten met anton",
                    kook_name: "anton"
                }]
            });
            const kookkies = await kookkiesRepo.allKookkies();
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
            expect(kookkiesRepo.allKookkies()).rejects.toEqual(
                {message: "unable to obtain kookkie sessions"}
            );
        });
    });

    describe('createing kookkies', () => {
        it('succeeds when api responds with created', async () => {
            http.onPost('/api/kookkie-sessions', {
                    date: "2023-06-07",
                    name: "Lekker eten met anton"
                }).reply(201, {});
            const kookkies = await kookkiesRepo.create({
                date: "2023-06-07",
                name: "Lekker eten met anton"
            });
            expect(kookkies).toEqual({});
        });

        it('fails when api responds with failure', async () => {
            http.onPost('/api/kookkie-sessions', {}).reply(401, {message: "unauthorized"});
            expect(kookkiesRepo.create({})).rejects.toEqual(
                {message: "unable to create kookkie session"}
            );
        });
    });

});
import {KookkiesModule} from "../../app/modules/kookkies-module";
import {ApiBasedKookkiesRepository} from "../../app/adapters/api-based-kookkies-repository";

describe('kookkies module', () => {
    let kookkiesRepository;
    let kookkies;
    describe('creating a kookkie', () => {
        beforeEach(() => {
            kookkiesRepository = new class extends ApiBasedKookkiesRepository{
                create = jest.fn(() => Promise.resolve())
            } ();
            kookkies = new KookkiesModule(kookkiesRepository);
        });
        it('delegates to the kookkies repository', () => {
            kookkies.create({name: "meal", date: "2023-07-12"});
            expect(kookkiesRepository.create).toHaveBeenCalledWith({name: "meal", date: "2023-07-12"});
        });
        it('returns an error when repository returns an error', async () => {
            kookkiesRepository.create = jest.fn(() => Promise.reject({messageId: "error while creating kookkie"}));
            await kookkies.create({name: "meal", date: "2023-07-12"});
            expect(kookkies.errorMessage).toEqual("error while creating kookkie");
        });
    });
});
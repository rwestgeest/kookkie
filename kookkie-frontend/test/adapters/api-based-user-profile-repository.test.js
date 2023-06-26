import {ApiBasedUserProfileRepository} from "../../app/adapters/api-based-user-profile-repository";
import {UserProfile} from "../../app/domain/user-profile";
import {HTTPStub} from "./http-stub";

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
            const userProfile = await profileRepo.get();
            expect(userProfile).toEqual(
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
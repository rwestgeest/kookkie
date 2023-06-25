import {UserProfileModule} from "../../app/modules/userProfileModule";
import {UserProfile} from "../../app/domain/userProfile";
import {UserProfileRepository} from "../../app/domain/user-profile-repository";


describe(UserProfileModule, () => {

    describe('homePage', () => {
        it('is obtained from user profile repository', async () => {
            let theProfile = new UserProfile({name: "rob", email: "rob@kookkie.com", role: "kook"});
            let userProfileRepository = new class extends UserProfileRepository {
                get() {
                    return Promise.resolve(theProfile);
                }
            }
            let userProfileModule = new UserProfileModule(userProfileRepository);
            await expect(userProfileModule.homePage()).resolves.toEqual(theProfile.homePage());
        });
        it('returns a null profiles homepage when an error occurs', async () => {
            let theProfile = new UserProfile({name: "rob", email: "rob@kookkie.com", role: "kook"});
            let userProfileRepository = new class extends UserProfileRepository {
                get() {
                    return Promise.reject("the user was not logged in");
                }
            }
            let userProfileModule = new UserProfileModule(userProfileRepository);
            await expect(userProfileModule.homePage()).resolves.toEqual(UserProfile
                .null().homePage());
        });
    });
});
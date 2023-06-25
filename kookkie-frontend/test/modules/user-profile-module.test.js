import {UserProfileModule} from "../../app/modules/user-profile-module";
import {UserProfile} from "../../app/domain/userProfile";
import {UserProfileRepository} from "../../app/domain/user-profile-repository";


describe(UserProfileModule, () => {
    describe('homePage', () => {
        let theProfile;
        let userProfileRepository;
        let userProfileModule;

        beforeEach(() => {
            theProfile = new UserProfile({name: "rob", email: "rob@kookkie.com", role: "kook"});
            userProfileRepository = new class extends UserProfileRepository {
                get() {
                    return Promise.resolve(theProfile);
                }
            }
            userProfileModule = new UserProfileModule(userProfileRepository);
        });

        it('is obtained from user profile repository', async () => {
            await expect(userProfileModule.homePage()).resolves.toEqual(theProfile.homePage());
        });

        it('returns a null profiles homepage when an error occurs', async () => {
            userProfileRepository.get = () => {
                return Promise.reject("the user was not logged in");
            };

            await expect(userProfileModule.homePage()).resolves.toEqual(UserProfile
                .null().homePage());
        });
    });
    describe('when profile changes', () => {

    });
});
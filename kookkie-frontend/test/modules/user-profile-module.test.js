import {UserProfileModule} from "../../app/modules/user-profile-module";
import {UserProfile} from "../../app/domain/user-profile";
import {UserProfileRepository} from "../../app/domain/user-profile-repository";


describe(UserProfileModule, () => {
    let theProfile;
    let userProfileRepository;
    let userProfileModule;
    let router;
    beforeEach(() => {
        theProfile = new UserProfile({name: "rob", email: "rob@kookkie.com", role: "kook"});
        userProfileRepository = new class extends UserProfileRepository {
            get() { return Promise.resolve(theProfile); }
        }
        router = new class {
            goto(location) {
                this._currentLocation = location;
            }
            currentLocation() {
                return this._currentLocation;
            }
        }
        userProfileModule = new UserProfileModule(userProfileRepository, router);
    });

    describe('homePage', () => {

        it('is obtained from user profile repository', async () => {
            await userProfileModule.obtainUserProfile();
            expect(userProfileModule.homePage()).toEqual(theProfile.homePage());
        });

        it('returns a null profiles homepage when an error occurs', async () => {
            userProfileRepository.get = () => {
                return Promise.reject("the user was not logged in");
            };
            await userProfileModule.obtainUserProfile();
            expect(userProfileModule.homePage()).toEqual(UserProfile.null().homePage());
        });
    });

    describe('when profile changes', () => {
        it('navigates to the the new users homepage', async () => {
            await userProfileModule.obtainUserProfile();
            expect(router.currentLocation()).toEqual(userProfileModule.homePage());
        });
    });
});
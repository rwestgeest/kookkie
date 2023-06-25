import {UserProfileModule} from "../../app/modules/user-profile-module";
import {UserProfile} from "../../app/domain/user-profile";
import {UserProfileRepository} from "../../app/domain/user-profile-repository";
import {View} from "../../app/domain/view";


describe(UserProfileModule, () => {
    let theProfile;
    let userProfileRepository;
    let userProfileModule;

    beforeEach(() => {
        theProfile = new UserProfile({name: "rob", email: "rob@kookkie.com", role: "kook"});
        userProfileRepository = new class extends UserProfileRepository {
            get() { return Promise.resolve(theProfile); }
        }
        userProfileModule = new UserProfileModule(userProfileRepository);
    });

    describe('homePage', () => {

        it('is obtained from user profile repository', async () => {
            await expect(userProfileModule.homePage()).resolves.toEqual(theProfile.homePage());
        });

        it('returns a null profiles homepage when an error occurs', async () => {
            userProfileRepository.get = () => {
                return Promise.reject("the user was not logged in");
            };

            await expect(userProfileModule.homePage()).resolves.toEqual(UserProfile.null().homePage());
        });
    });

    describe('when profile changes', () => {
        it('updates its views', async () => {
            let updates = 0;

            const view = new class extends View {
                update() {
                    updates += 1;
                }
            }
            userProfileModule.registerView(view);
            await userProfileModule.homePage();
            expect(updates).toEqual(1);
        });
        it('does not update its views when the new profile is equal to the current', async () => {
            let updates = 0;

            const view = new class extends View {
                update() {
                    updates += 1;
                }
            }
            await userProfileModule.homePage();
            userProfileModule.registerView(view);
            theProfile = new UserProfile({name: "rob", email: "rob@kookkie.com", role: "kook"});
            await userProfileModule.homePage();
            expect(updates).toEqual(0);
        });
    });
});
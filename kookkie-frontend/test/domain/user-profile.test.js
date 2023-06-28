import {UserProfile} from "../../app/domain/user-profile.js";

describe(UserProfile, () => {
    describe('homePage', () => {
        it('is sign in when anonymous', () => {
            expect(UserProfile.null().homePage()).toEqual('#/signin')
        });
        it('is sessions when not anonymous', () => {
            expect(new UserProfile({role: "admin"}).homePage()).toEqual('#/sessions')
            expect(new UserProfile({role: "kookkie"}).homePage()).toEqual('#/sessions')
        });
    });
});
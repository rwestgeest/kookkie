import {PageThatRenders, Router} from "./router.js";
import {UserProfileModule} from './modules/user-profile-module.js'
import {SessionsPage} from './pages/sessions-page.js'
import {SignInPage} from './pages/sign-in-page.js'
import {ApiBasedUserProfileRepository} from './adapters/api-based-user-profile-repository.js'

let userProfileModule = new UserProfileModule(new ApiBasedUserProfileRepository());
SignInPage(userProfileModule);
SessionsPage(userProfileModule);

const router = new Router(window, userProfileModule)
    .withNotFound(new PageThatRenders("not found"))
    .addRoute('#/', new PageThatRenders('root-content'))
    .addRoute('#/sessions', new PageThatRenders('<sessions-page></sessions-page>'))
    .addRoute('#/signin', new PageThatRenders('<sign-in-page></sign-in-page>'))
    .addRoute('#/join-session/:joinlink', new PageThatRenders('joining session'))
    .start();


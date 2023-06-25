import {PageThatRenders, Router} from "./router.js";
import {UserProfileModule} from './modules/userProfileModule.js'
import {SessionsPage} from './pages/sessionsPage.js'
import {SignInPage} from './pages/signInPage.js'
import {ApiBasedUserProfileRepository} from './adapters/apiBasedUserProfileRepository.js'

let userProfileModule = new UserProfileModule(new ApiBasedUserProfileRepository());
SignInPage(userProfileModule);
SessionsPage(userProfileModule);

const router = new Router(window, userProfileModule)
    .withNotFound(new PageThatRenders("not found"))
    .addRoute('#/', new PageThatRenders('root-content'))
    .addRoute('#/sessions', new PageThatRenders('<sessions-page></sessions-page>'))
    .addRoute('#/signin', new PageThatRenders('<sign-in-page></sign-in-page>'))
    .start();


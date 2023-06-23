import {PageThatRenders, Router} from "./router.js";
import {UserProfileModule} from './modules/userProfileModule.js'
import {SessionsPage} from './pages/sessionsPage.js'
import {SignInPage} from './pages/signInPage.js'

let userProfileModule = new UserProfileModule();
SignInPage(userProfileModule);
SessionsPage(userProfileModule);

const router = new Router(window)
    .addRoute('#/', new PageThatRenders('root-content'))
    .addRoute('#/sessions', new PageThatRenders('<sessions-page></sessions-page>'))
    .addRoute('#/signin', new PageThatRenders('<sign-in-page></sign-in-page>'))
    .default('#/signin')
    .start();


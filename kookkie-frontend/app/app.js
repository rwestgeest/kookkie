import {PageThatRenders, Router} from "./router.js";
import {UserProfileModule} from './modules/user-profile-module.js'
import {SessionsPage} from './pages/sessions-page.js'
import {SignInPage} from './pages/sign-in-page.js'
import {ApiBasedUserProfileRepository} from './adapters/api-based-user-profile-repository.js'
import {FetchBasedHTTP} from "./adapters/fetch-based-http.js";
import {AuthenticationModule} from "./modules/authentication.module.js";
import {ApiBasedAuthenticator} from "./adapters/api-based.authenticator.js";

const http = new FetchBasedHTTP();
let userProfileModule = new UserProfileModule(new ApiBasedUserProfileRepository(http));
let authenticationModule = new AuthenticationModule(userProfileModule, new ApiBasedAuthenticator(http));

SignInPage(authenticationModule);
SessionsPage(userProfileModule);

const router = new Router(window, userProfileModule)
    .withNotFound(new PageThatRenders("not found"))
    .addRoute('#/', new PageThatRenders('root-content'))
    .addRoute('#/sessions', new PageThatRenders('<sessions-page></sessions-page>'))
    .addRoute('#/signin', new PageThatRenders('<sign-in-page></sign-in-page>'))
    .addRoute('#/join-session/:joinlink', new PageThatRenders('joining session'))
    .start();


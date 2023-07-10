import {PageThatRenders, Router} from "./router.js";
import {UserProfileModule} from './modules/user-profile-module.js'
import {SessionsPage} from './pages/sessions-page.js'
import {SignInPage} from './pages/sign-in-page.js'
import {ApiBasedUserProfileRepository} from './adapters/api-based-user-profile-repository.js'
import {FetchBasedHTTP} from "./adapters/fetch-based-http.js";
import {AuthenticationModule} from "./modules/authentication.module.js";
import {ApiBasedAuthenticator} from "./adapters/api-based.authenticator.js";
import {ApiBasedKookkiesRepository} from "./adapters/api-based-kookkies-repository.js";
import {SessionPage} from "./pages/session-page.js";
import {SessionJoinPage} from "./pages/session-join-page.js";
import {KookkiesModule} from "./modules/kookkies-module.js";
import {ParticipantModule} from "./modules/participant-module.js";
import {JitsiVideo} from "./components/jitsi-video.js";
import {ApiBasedKookkieJoiner} from "./adapters/api-based-kookkie-joiner.js";

const router = new Router(window)
const http = new FetchBasedHTTP();
const userProfileModule = new UserProfileModule(new ApiBasedUserProfileRepository(http), router);
const authenticationModule = new AuthenticationModule(userProfileModule, new ApiBasedAuthenticator(http));

const kookkiesModule = new KookkiesModule(new ApiBasedKookkiesRepository(http));
SignInPage(authenticationModule);
SessionsPage(kookkiesModule, userProfileModule);
JitsiVideo();
const sessionPage = new SessionPage(kookkiesModule, userProfileModule);
const sessionJoinPage = new SessionJoinPage(new ParticipantModule(new ApiBasedKookkieJoiner(http)));

router.withNotFound(new PageThatRenders("not found"))
    .addRoute('#/', new PageThatRenders('root-content'))
    .addRoute('#/sessions', new PageThatRenders('<sessions-page></sessions-page>'))
    .addRoute('#/session/:id', sessionPage)
    .addRoute('#/join/:id', sessionJoinPage)
    .addRoute('#/signin', new PageThatRenders('<sign-in-page></sign-in-page>'))
    .addRoute('#/join-session/:joinlink', new PageThatRenders('joining session'))
    .start();

userProfileModule.obtainUserProfile();
export class UserProfile {
    constructor({name, email, role}) {
        this.name = name;
        this.email = email;
        this.role = role;
    }

    static null() {
        return new UserProfile({name: "", email: "", role: "anonymous"});
    }

    homePage() {
        if (this.role === UserProfile.null().role)
            return "#/signin";
        return "#/sessions"
    }
}
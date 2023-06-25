export class UserProfile {
    constructor({name, email, role}) {
        this.name = name;
        this.email = email;
        this.role = role;
    }

    static null() {
        return new UserProfile({role: "anonymous"});
    }

    homePage() {
        return "#/signin";
    }
}
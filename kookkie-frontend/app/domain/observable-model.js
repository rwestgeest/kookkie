export class ObservableModel {
    registerView(view) {
        this.view = view;
    }

    changed() {
        if (this.view !== undefined) this.view.update();
    }
}
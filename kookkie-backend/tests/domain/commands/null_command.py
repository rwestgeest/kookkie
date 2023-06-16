from quiltz.domain import Success, Failure


class NullCommand:
    def __init__(self):
        self.return_value = Success()

    def __call__(self, **kwargs):
        self.called_with = kwargs
        return self.return_value

    def will_fail(self):
        self.return_value = Failure(message='failed')

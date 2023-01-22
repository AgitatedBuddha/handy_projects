class BaseTest:
    @classmethod
    def setup_class(cls):
        # define env setup here
        pass

    @classmethod
    def teardown_class(cls):
        # define cleanup here
        pass

    def setup_method(self):
        # setup needed before every testcase
        pass

    def teardown_method(self):
        # cleanup after every testcase in a class
        pass

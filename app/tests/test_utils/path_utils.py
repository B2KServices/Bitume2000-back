import os


def path_of_current_test():
    return os.getenv('PYTEST_CURRENT_TEST')


def path_relative_to_current_test(path: str):
    return os.path.join(os.path.dirname(path_of_current_test()), path)

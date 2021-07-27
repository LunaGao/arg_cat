
from arg_cat import ArgCat


def print_hi():
    argcat = ArgCat()
    argcat.add_key("env")
    argcat.add_key("release", is_a_bool=True)
    argcat.add_key("some_path", is_a_path=True)
    argcat.from_arg_and_environ(environ_override_all=True)
    argcat.from_arg()
    argcat.from_environ()
    argcat.remove("env")
    argcat.put("template", "true", is_a_path=False, is_a_bool=True)
    print(f'env: {argcat.get_string("env")}')
    print(f'release: {argcat.get_bool("release")}')
    print(f'some_path: {argcat.get_string("some_path")}')
    print(f'template: {argcat.get_bool("template")}')
    argcat.sync_to_file()


if __name__ == '__main__':
    print_hi()


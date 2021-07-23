# Arg Cat Package

This is a package for read params from args and env.

# How to Use

```python
argcat.add_key("env")
```
This will find args `-e` or `--env`, or find environment `ENV`.

* Only read arg: `argcat.from_arg()`
* Only read environment: `argcat.from_environ()`
* Read both arg and environment: `argcat.from_arg_and_environ()`

## Example
```python
from arg_cat import ArgCat
```
```python
argcat = ArgCat()
argcat.add_key("env")
argcat.add_key("release", is_a_bool=True)
argcat.add_key("some_path", is_a_path=True)
argcat.from_arg_and_environ(environ_override_all=False)
print(f'env: {argcat.get_string("env")}')
print(f'release: {argcat.get_bool("release")}')
print(f'some_path: {argcat.get_string("some_path")}')
```
* This example will get 3 params, `env`, `release` and `some_path`.
* ArgCat will find `-e` or `--env` in args for env.
* ArgCat will find `-r` or `--release` in args for release.
* ArgCat will find `-s` or `--some_path` in args for some_path.
* ArgCat will find `ENV` in environment for env.
* ArgCat will find `RELEASE` in environment for release.
* ArgCat will find `SOME_PATH` in environment for some_path.
* `from_arg_and_environ` will using environment first, then using the args value to override those values. Sometimes, you may want to use environment value to override the args value, you should let `environ_override_all` to be `Ture`. `environ_override_all` default value is `False`.
* Running this will be like: `python3 demo.py --env dev -r -s ./this/is/path`


### Situation 1
`environ_override_all=False`

Environment:
```
ENV=this is from env
RELEASE=False
```
Args:
```
--env "from arg" -s ./hello
```
Result:
```
env: from arg
release: False
some_path: YOUR_WORK_PATH/./hello
```

### Situation 2
`environ_override_all=True`

Environment:
```
ENV=this is from env
RELEASE=False
```
Args:
```
--env "from arg" -s ./hello
```
Result:
```
env: this is from env
release: False
some_path: YOUR_WORK_PATH/./hello
```


# Note for owner
### Build
```shell
python -m build 
```
### Release To Test
```shell
python3 -m twine upload --repository testpypi dist/*
```
### Release To Release
```shell
python3 -m twine upload dist/*
```
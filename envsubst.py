"""
Substitute environment variables in a string.

For more info:
>>> from envsubst import envsubst
>>> help(envsubst)
"""
# MIT License
# 
# Copyright (c) 2019 Alex Shafer, Demetry Pascal
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import Union, Optional

import re
import os
import sys
from pathlib import Path


#region UTILS

_simple_re = re.compile(r'(?<!\\)\$([A-Za-z0-9_]+)')
_extended_re = re.compile(r'(?<!\\)\$\{([A-Za-z0-9_]+)((:?-)([^}]+))?\}')


def _resolve_var(var_name: str, default=None):
    try:
        index = int(var_name)
        try:
            return sys.argv[index]
        except IndexError:
            return default
    except ValueError:
        return os.getenv(var_name, default)


def _repl_simple_env_var(m):
    var_name = m.group(1)
    return _resolve_var(var_name, '')


def _repl_extended_env_var(m):
    var_name = m.group(1)
    default_spec = m.group(2)
    if default_spec:
        default = m.group(4)
        default = _simple_re.sub(_repl_simple_env_var, default)
        if m.group(3) == ':-':
            # use default if var is unset or empty
            env_var = _resolve_var(var_name)
            if env_var:
                return env_var
            else:
                return default
        elif m.group(3) == '-':
            # use default if var is unset
            return _resolve_var(var_name, default)
        else:
            raise RuntimeError('unexpected string matched regex')
    else:
        return _resolve_var(var_name, '')


def mkdir_of_file(file_path: Union[str, os.PathLike]):
    """
    ensures file parent dir existence
    """
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

#endregion


def envsubst(string: str) -> str:
    """
    Substitute environment variables in the given string

    The following forms are supported:

    Simple variables - will use an empty string if the variable is unset
      $FOO

    Bracketed expressions
      ${FOO}
        identical to $FOO
      ${FOO:-somestring}
        uses "somestring" if $FOO is unset, or set and empty
      ${FOO-somestring}
        uses "somestring" only if $FOO is unset

    :param str string: A string possibly containing environment variables
    :return: The string with environment variable specs replaced with their values
    """
    # handle simple un-bracketed env vars like $FOO
    a = _simple_re.sub(_repl_simple_env_var, string)

    # handle bracketed env vars with optional default specification
    b = _extended_re.sub(_repl_extended_env_var, a)
    return b


def envsubst_from_file(path: Union[str, os.PathLike], encoding: Optional[str] = 'utf-8') -> str:
    """reads file with env variables substitutions"""
    text = Path(path).read_text(encoding=encoding)
    return envsubst(text)


def envsubst_file_convert(
    path_in: Union[str, os.PathLike],
    path_out: Optional[Union[str, os.PathLike]] = None,
    encoding: Optional[str] = 'utf-8'
) -> None:
    """performs env variables substitutions on file and saves result to file"""

    path_out = path_out or path_in
    mkdir_of_file(path_out)
    Path(path_out).write_text(
        envsubst_from_file(path_in, encoding=encoding),
        encoding=encoding
    )



def main():
    opened = False
    f = sys.stdin
    try:
        try:
            fn = sys.argv[1]
            if fn != '-':
                f = open(fn)
                opened = True
        except IndexError:
            pass

        data = f.read()
        try:
            data = data.decode('utf-8')
        except AttributeError:
            pass

        sys.stdout.write(envsubst(data))
    finally:
        if opened:
            f.close()


if __name__ == '__main__':
    main()

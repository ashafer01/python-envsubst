python-envsubst
===============

Substitute environment variables in a string::

    >>> import os
    >>> from envsubst import envsubst
    
    >>> del os.environ['PS1']
    >>> print(envsubst('$USER@$HOST ${PS1:-$}:'))
    ashafer01@github.com $:
    
    >>> os.environ['PS1'] = ''
    >>> print(envsubst('$USER@$HOST ${PS1:-$}:'))
    ashafer01@github.com $:
    
    >>> print(envsubst('$USER@$HOST ${PS1-foo}:'))
    ashafer01@github.com :

    >>> os.environ['DEFAULT_PROMPT'] = '$'
    >>> print(envsubst('$USER@$HOST ${PS1:-$DEFAULT_PROMPT}:'))

Also supports $0, $1, etc. from argv.

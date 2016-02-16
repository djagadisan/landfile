import os
import argparse


def get_base_parser():
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument('-h', '--help',
            action='store_true')
    
    
def sub_args(*args, **kwargs):
    def _modifier(func):
        add_sub(func, *args, **kwargs)
        return func
    
    return _modifier

def add_sub(f, *args, **kwargs):
    if not hasattr(f, 'arguments'):
        f.arguments = []
    if (args, kwargs) not in f.arguments:
        # Because of the semantics of decorator composition if we just append
        # to the options list positional options will appear to be backwards.
        f.arguments.insert(0, (args, kwargs))

def get_subparser():
    parser = get_base_parser()
    sub_parser = parser.add_subparsers(metavar='<subcommand>')
    
    return sub_parser
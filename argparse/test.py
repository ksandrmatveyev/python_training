#!/usr/bin/env python

# https://docs.python.org/3/library/logging.html
import logging
import argparse

logger = logging.getLogger("example")
logger.setLevel(logging.INFO)

def get_args():
    """get command line arguments"""
    parser = argparse.ArgumentParser(description="AWS wrapper")
    subparsers = parser.add_subparsers()

    parser_create = subparsers.add_parser("create", help="Create stacks hierarchy")
    parser_create.add_argument("stack_name", help="name of stack")
    parser_create.set_defaults(func=create)

    parser_delete = subparsers.add_parser("delete", help="Delete stacks hierarchy")
    parser_delete.add_argument("stack_name", help="name of stack")
    parser_delete.set_defaults(func=delete)

    return parser.parse_args()

def create(stack_name):
    print("creating stack {name}".format(name=stack_name))
    logger.info("creating stack %s", stack_name)

def delete(stack_name):
    print("delete stack {name}".format(name=stack_name))
    logger.info("delete stack %s", stack_name)

def main():
    """ entry point """
    args = get_args()
    print(args)
    kwargs = vars(get_args())
    print(kwargs)
    default_func = kwargs.pop("func")
    print(default_func)
    print(kwargs)
    default_func(**kwargs)

if __name__ in "__main__":
    # https://docs.python.org/3/library/stdtypes.html#printf-style-string-formatting
    logging.basicConfig(format="%(name)-12.12s : %(asctime)-8s %(levelname)-8s %(message)s",
                        datefmt="%X")
    main()

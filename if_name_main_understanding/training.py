#! /usr/bin/env python

def test(some):
    print("Hello " + some)

test(__name__)
if __name__ == "__main__":
    test("2")
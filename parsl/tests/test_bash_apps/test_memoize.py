import argparse
import os

import parsl
from parsl import File
from parsl.app.app import bash_app
from parsl.tests.configs.local_threads import config

from parsl.dataflow.memoization import id_for_memo

# this is bad because it will register for the whole test suite
# process, so only one registration for the whole test suite
# makes sense if done at module level
@id_for_memo.register(File)
def id_for_memo_file(file: File, output_ref: bool = False):
    return file.url


@bash_app(cache=True)
def fail_on_presence(outputs=[]):
    return 'if [ -f {0} ] ; then exit 1 ; else touch {0}; fi'.format(outputs[0])


def test_bash_memoization(n=2):
    """Testing bash memoization
    """
    temp_filename = "test.memoization.tmp"

    if os.path.exists(temp_filename):
        os.remove(temp_filename)

    temp_file = File(temp_filename)

    print("Launching: ", n)
    x = fail_on_presence(outputs=[temp_file])
    x.result()

    d = {}
    for i in range(0, n):
        d[i] = fail_on_presence(outputs=[temp_file])

    for i in d:
        assert d[i].exception() is None


@bash_app(cache=True)
def fail_on_presence_kw(outputs=[], foo={}):
    return 'if [ -f {0} ] ; then exit 1 ; else touch {0}; fi'.format(outputs[0])


def test_bash_memoization_keywords(n=2):
    """Testing bash memoization
    """
    temp_filename = "test.memoization.tmp"

    if os.path.exists(temp_filename):
        os.remove(temp_filename)

    temp_file = File(temp_filename)

    print("Launching: ", n)
    x = fail_on_presence_kw(outputs=[temp_file], foo={"a": 1, "b": 2})
    x.result()

    d = {}
    for i in range(0, n):
        d[i] = fail_on_presence_kw(outputs=[temp_file], foo={"b": 2, "a": 1})

    for i in d:
        assert d[i].exception() is None


if __name__ == '__main__':
    parsl.clear()
    parsl.load(config)

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--count", default="10",
                        help="Count of apps to launch")
    parser.add_argument("-d", "--debug", action='store_true',
                        help="Count of apps to launch")
    args = parser.parse_args()

    if args.debug:
        parsl.set_stream_logger()

    x = test_bash_memoization(n=4)

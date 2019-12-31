"""
Check portions of the sage test suite, with default mip solver set to ours.

    sage: M = MixedIntegerLinearProgram()
    sage: M.get_backend()
    <...sage_numerical_backends_cplex...>
"""

import sage_numerical_backends_cplex.cplex_backend as cplex_backend, sage.numerical.backends as backends, sys
sys.modules['sage.numerical.backends.cplex_backend'] = backends.cplex_backend = cplex_backend

from sage.numerical.backends.generic_backend import default_mip_solver
default_mip_solver('CPLEX')

from sage.doctest.control import DocTestController, DocTestDefaults
options = DocTestDefaults(nthreads=0, long=False, optional="sage,cplex", force_lib=True, abspath=True)

import os, sage.env, glob, sys
abs_file = os.path.abspath("check_sage_testsuite.py")
os.chdir(os.path.join(sage.env.SAGE_LIB, 'sage'))
files = ["coding",
         "combinat/designs", "combinat/integer_vector.py", "combinat/posets/",
         "game_theory/",
         "geometry/polyhedron/base.py", "geometry/cone.py",
         "graphs/",
         "homology/simplicial_complex.py",
         "knots/",
         "matroids/",
         "sat/"]

files += glob.glob("numerical/*.py*")

# First verify that we installed the default backend
DC = DocTestController(options, [abs_file])
err = DC.run()
if err != 0:
    print("Error: Setting the default solver did not work", file=sys.stderr)
    sys.exit(2)

# from $SAGE_SRC/bin/sage-runtests
DC = DocTestController(options, files)
err = DC.run()
if err != 0:
    sys.exit(1)

sys.exit(0)
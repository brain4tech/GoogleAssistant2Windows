from inspect import getmembers, isfunction
import callfunctions
callfunctions.foo()
print ([o for o in getmembers(callfunctions) if isfunction(o[1])])

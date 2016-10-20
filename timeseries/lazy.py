
class LazyOperation():
    """ Isolate the function call from the function execution.
    out = LazyOperation(function,*args,**kwargs) defines the operation.
    out.eval() evaluates the operation.
    out.eval() = function(*args,**kwargs).
    """
    
    def __init__(self,function,*args,**kwargs):
        self._f = function
        self._args = args
        self._kwargs = kwargs
        
    def eval(self):
        new_args = [a.eval() if isinstance(a,LazyOperation) else a for a in self._args]
        new_kwargs = {k:(v.eval() if isinstance(v,LazyOperation) else v) for k,v in self._kwargs.items()}
        return self._f(*new_args,**new_kwargs)
        


def lazy(function):
    """ Make a function return a LazyOperation instance"""
    def inner(*args,**kwargs):
        return LazyOperation(function,*args,**kwargs)
    return inner


"""Define lazy_add and lazy_mul for testing purposes"""    
@lazy
def lazy_add(x,y):
    return x+y
    
@lazy
def lazy_mul(x,y):
    return x*y


from goody import type_as_str
import inspect

class Check_All_OK:
    """
    Check_All_OK class implements __check_annotation__ by checking whether each
      annotation passed to its constructor is OK; the first one that
      fails (by raising AssertionError) prints its problem, with a list of all
      annotations being tried at the end of the check_history.
    """
       
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_All_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        for annot in self._annotations:
            # print(annot)
            check(param, annot, value, check_history+'Check_All_OK check: '+str(annot)+' while trying: '+str(self)+'\n')


class Check_Any_OK:
    """
    Check_Any_OK implements __check_annotation__ by checking whether at least
      one of the annotations passed to its constructor is OK; if all fail 
      (by raising AssertionError) this classes raises AssertionError and prints
      its failure, along with a list of all annotations tried followed by the
      check_history.
    """
    
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_Any_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        failed = 0
        for annot in self._annotations: 
            try:
                check(param, annot, value, check_history)
            except AssertionError:
                failed += 1
        if failed == len(self._annotations):
            assert False, repr(param)+' failed annotation check(Check_Any_OK): value = '+repr(value)+\
                         '\n  tried '+str(self)+'\n'+check_history                 


class Check_Annotation:
    # Begin by binding the class attribute to True allowing checking to occur
    #   (only if the object's attribute self._checking_on is also bound to True)
    checking_on  = True
  
    # To check the decorated function f, begin by binding self._checking_on to True
    def __init__(self, f):
        self._f = f
        self._checking_on = True

    # Check whether param's annot is correct for value, adding to check_history
    #    if recurs; defines many local function which use it parameters.  
    def check(self,param,annot,value,check_history='', string_locals=None):
        
        # Define local functions for checking, list/tuple, dict, set/frozenset,
        #   lambda/functions, and str (str for extra credit)
        # Many of these local functions called by check, call check on their
        #   elements (thus are indirectly recursive)
        def check_types():
            if not isinstance(value, annot):
                raise AssertionError(f"{param} failed annotation check (wrong type): "
                                     f"value = {value}\n was type {type_as_str(value)}"
                                     f"...should be type {annot.__name__}\n{check_history.strip()}")
            
        def check_lists(check_history=check_history, for_tuples=False):
            if not isinstance(value, list if not for_tuples else tuple):
                raise AssertionError(f"{param} failed annotation check (wrong type): "
                                     f"value = {value}\n was type {type_as_str(value)}"
                                     f"...should be type {type_as_str(annot)}\n{check_history.strip()}")

            if len(annot) != len(value) and len(annot) > 1:  # length check
                raise AssertionError(f"{param} failed annotation check (wrong number of elements): "
                                     f"value = {value}\n annotation has {len(annot)} elements {annot}")
            for v in range(len(value)):
                check_history += f"\n{type_as_str(annot)}[{v}] check: {annot[v if len(annot) > 1 else 0]}"
                self.check(param, annot[v if len(annot) > 1 else 0], value[v], check_history)
                ch_list = check_history.splitlines()
                ch_list.pop()
                check_history = "\n".join(ch_list)

        def check_dicts(check_history=check_history):
            if not isinstance(value, dict):
                raise AssertionError(f"{param} failed annotation check (wrong type): "
                                     f"value = {value}\n was type {type_as_str(value)}"
                                     f"...should be type {type_as_str(annot)}\n{check_history.strip()}")
            if len(annot) > 1:
                raise AssertionError(f"'{param}' annotation inconsistency: dict should have 1 item but had {len(annot)}\n"
                                     f"annotation = {annot}")

            _key = list(annot.keys())[0]
            _value = list(annot.values())[0]

            for k in value.keys():
                check_history += f"dict key check: {_key}"
                self.check(param, _key, k, check_history)
                ch_list = check_history.splitlines()
                ch_list.pop()
                check_history = "\n".join(ch_list)
            for v in value.values():
                check_history += f"dict value check: {_value}"
                self.check(param, _value, v, check_history)
                ch_list = check_history.splitlines()
                ch_list.pop()
                check_history = "\n".join(ch_list)

        def check_sets(check_history=check_history, for_frozensets=False):
            if not isinstance(value, set if not for_frozensets else frozenset):
                raise AssertionError(f"{param} failed annotation check (wrong type): "
                                     f"value = {value}\n was type {type_as_str(value)}"
                                     f"...should be type {type_as_str(annot)}\n{check_history.strip()}")
            if len(annot) > 1:
                raise AssertionError(f"'{param}' annotation inconsistency: {'set' if not for_frozensets else 'frozenset'}"
                                     f"should have 1 item but had {len(annot)}\n"
                                     f"annotation = {annot}")
            in_set_annot = list(annot)[0]
            for v in value:
                check_history += f"{'set' if not for_frozensets else 'frozenset'} value check: {in_set_annot}"
                self.check(param, in_set_annot, v, check_history)
                ch_list = check_history.splitlines()
                ch_list.pop()
                check_history = "\n".join(ch_list)

        def check_lambdas(check_history=check_history):
            sig = inspect.signature(annot).parameters
            if len(sig) == 0 or len(sig) > 1:
                raise AssertionError(f"AssertionError: '{param}' annotation inconsistency: "
                                     f"predicate should have 1 parameter but had {len(sig)}\n"
                                     f"predicate = {annot}")
            # calling the lambda on value
            try:
                if not annot(value):
                    raise AssertionError(f"AssertionError: '{param}' failed annotation check: value = {value}\n"
                                         f"predicate = {annot}\n{check_history.strip()}")
            except TypeError as e:
                raise AssertionError(f"AssertionError: '{param}' annotation "
                                     f"predicate({annot}) raised exception\n"
                                     f"exception = {e}\n"
                                     f"{check_history.strip()}")

        def check_str():
            try:
                if annot != "None" and string_locals is not None:  # only get the string annot
                    if not eval(annot, globals(), string_locals):
                        raise AssertionError
            except:
                raise AssertionError

        def check_others(param=param, check_history=check_history):
            try:
                annot.__check_annotation__(self.check, param, value, check_history)
            except AttributeError:
                raise AssertionError(f"'{param}' annotation undecipherable: {annot}")

        if annot is None:
            pass
        elif type(annot) is type:
            check_types()
        elif type_as_str(annot) == "list":
            check_lists()
        elif type_as_str(annot) == "tuple":
            check_lists(for_tuples=True)
        elif type_as_str(annot) == "dict":
            check_dicts()
        elif type_as_str(annot) == "set":
            check_sets()
        elif type_as_str(annot) == "frozenset":
            check_sets(for_frozensets=True)
        elif type_as_str(annot) == "function":
            check_lambdas()
        elif type_as_str(annot) == "str":
            check_str()
        else:
            check_others()

    # Return result of calling decorated function call, checking present
    #   parameter/return annotations if required
    def __call__(self, *args, **kargs):
        # Return the argument/parameter bindings in an OrderedDict (it's derived
        #   from a dict): bind the function header's parameters in its order
        def param_arg_bindings():
            f_signature  = inspect.signature(self._f)
            bound_f_signature = f_signature.bind(*args,**kargs)
            for param in f_signature.parameters.values():
                if not (param.name in bound_f_signature.arguments):
                    bound_f_signature.arguments[param.name] = param.default
            return bound_f_signature.arguments

        def args_to_str():
            output = ""
            for arg in args:
                if type_as_str(arg) == "str":
                    arg = "'" + arg + "'"
                output += str(arg) + ', '
            return output.rstrip(", ")

        # If annotation checking is turned off at the class or function level
        #   just return the result of calling the decorated function
        # Otherwise do all the annotation checking
        
        try:
            # For each found annotation, check it using the parameter's value

            # Compute/remember the value of the decorated function
            
            # If 'return' is in the annotation, check it
            
            # Return the decorated answer
            param_arg_binds = param_arg_bindings()
            annotations = self._f.__annotations__
            args_str = args_to_str()
            result_dict = dict()
            result_dict["self_f"] = self._f
            exec(f"result = self_f({args_str})", globals(), result_dict)
            result = result_dict["result"]

            if self._checking_on:
                for p in param_arg_binds.keys():

                    param = p
                    value = param_arg_binds[p]
                    annot = "None"

                    if p in annotations.keys():
                        annot = annotations[p]

                    self.check(param, annot, value, string_locals=param_arg_binds)
                if "return" in annotations.keys():
                    annot = annotations["return"]
                    value = result
                    self.check("return", annot, value)
                return result
            else:
                return result

        # On first AssertionError, print the source lines of the function and reraise 
        except AssertionError:
            # print(80*'-')
            # for l in inspect.getsourcelines(self._f)[0]: # ignore starting line #
            #     print(l.rstrip())
            # print(80*'-')
            raise

  
if __name__ == '__main__':
    def f(x, y: 'y>x'):pass
    f = Check_Annotation(f)
    f(0, 1)
    #driver tests
    import driver
    driver.default_file_name = 'bscp4S21.txt'
#     driver.default_show_exception= True
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()

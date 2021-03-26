import prompt, traceback

from goody import type_as_str

default_file_name              = "bsc.txt"
default_separator              = '-->'
default_show_comment           = True
default_show_all               = False
default_show_traceback         = False
default_show_exception         = False
default_show_exception_message = False


# batch_self_check reads/processes every test in a file. There are five forms
#  #/comment :  print it
#  c/command  : execute command
#                 (fail on exception)
#  e/evaluate : evaluate expression as string
#                 (fail on exception or != optional expected result )
#  ^/exception: execute command with expectation of exception
#                 (fail on no exception or wrong exception name -* means all names OK)
#  relop      : evaluate left relop right
#                 (fail on exception or relational operator returns False)

def batch_self_check(file_name              = None,\
                     separator              = None,\
                     show_comment           = None,\
                     show_all               = None,\
                     show_traceback         = None,\
                     show_exception         = None,\
                     show_exception_message = None,
                     TA_info                = None):
    def choose_param(param, default):
        return param if param != None else default
    
    print('Starting batch_self_check')
    file_name              = choose_param(file_name,              default_file_name)
    separator              = choose_param(separator,              default_separator)
    show_comment           = choose_param(show_comment,           default_show_comment)
    show_all               = choose_param(show_all,               default_show_all)
    show_traceback         = choose_param(show_traceback,         default_show_traceback)
    show_exception         = choose_param(show_exception,         default_show_exception)
    show_exception_message = choose_param(show_exception_message, default_show_exception_message)
    check_num, correct_count, wrong_count, wrong = 0, 0, 0, []
    
    # Use local for local names, to allow exec to add new locals
    #   and modify existing ones: see the use of local in
    #   local['...'] =  ... and as a third parameter to exec/eval
    local = locals()
    globl = globals()
    
    for line in open(file_name):
        line      =  line.rstrip()
        check_num += 1
        try: 
            command_string = f'{check_num:5} {line}\n'

             # Process blank lines (ignore them)
            if line == '':
                if local['show_all']:
                    print(command_string,end='')
                continue
            
            # Process #
            if line[0] == '#':
                if local['show_comment'] or local['show_all']:
                    print(command_string,end='')
                continue
            
            if local['show_all']:
                print(command_string,end='')
                command_string = ''
            
            # Unpack command
            command = line.split(separator)
            kind    = command[0]
            
            # Process Command
            if kind == 'c' and len(command) == 2:
                to_compute = command[1]
                exec(to_compute,globl)
                
            # Process Query/Expression
            elif kind == 'e' and len(command) == 3:
                to_compute, correct = command[1:3]
                computed = str(eval(to_compute,globl,local))
                # if correct != '': # removed so not returning '' is counted as wrong
                if computed == correct:
                    correct_count += 1
                else:
                    wrong_count += 1
                    wrong.append(check_num)
                    print(command_string,end='')
                    print(f'{" ":5} *Error: e--> failed')
                    print(f'{" ":8} left  value: {computed!r}\n{" ":8} right value: {correct!r}')

            # Process Command with expected Exception
            elif kind == '^' and len(command) == 3:
                to_compute, correct = command[1:3]
                try:
                    exec(to_compute,globl)   # should raise exception; if not error

                    wrong_count += 1
                    wrong.append(check_num)
                    print(command_string,end='')
                    print(f'{" ":5} *Error: ^--> failed to raise any exception')
                # Supposed to raise exception
                except Exception as exc: 
                    # KLUGE for pnamedtuple testing: correct += ',OSError' if correct != '*' else ''
                    if correct == '*' or any([isinstance(exc,eval(e,globl)) for e in correct.split(',')]): #KLUDGE: removed local
                        correct_count += 1
                        if local['show_exception']:
                            print(f'{check_num:5} +Right: Raised correct exception = {type_as_str(exc)} from specification = {correct}')
                            if local['show_exception_message']:
                                print(f'{" ":8} Message: {exc}')
                    else:
                        wrong_count += 1
                        wrong.append(check_num)
                        print(command_string,end='')
                        print(f'{" ":5} *Error: ^--> raised wrong exception:\n{" ":8} raised exception: {type_as_str(exc)}')
                        if local['show_exception_message']:
                            print(f'{" ":8} Message: {exc}')
                        
            # Process Relational Operator
            elif kind in ['==','!=','<','>','<=','>=','in','not in'] and len(command) == 3:
                to_compute, correct = command[1:3]
                try:
                    local['left']  = None
                    local['right'] = None
                    local['left']  = eval(to_compute,globl,local) #KLUDGE: must be local
                    local['right'] = eval(correct,globl,local)
                    if eval('(left)'+kind+'(right)',globl,local): # sides evaluated correctly: evaluate with operator
                        correct_count += 1
                    else:
                        wrong_count += 1
                        wrong.append(check_num)
                        print(command_string,end='')
                        print(f'{" ":5} *Error: {kind} operator failed to evaluate to True')
                        print(f'{" ":8} left  value: {local["left"]!r}\n{" ":8} right value: {local["right"]!r}')
                except Exception as exc:
                    wrong_count += 1
                    wrong.append(check_num)
                    print(command_string,end='')
                    print(f'{" ":5} *Error: {kind} operator raised {type_as_str(exc)} exception while evaluating argument(s)')
                    if local['left'] is None:
                        print(f'{" ":8} left argument raised exception\n{" ":8} right argument not evaluated')
                    elif local['right'] is None:
                        print(f'{" ":8} left value: {local["left"]!r}\n{" ":8} right argument raised exception')
                    if local['show_traceback']:
                        traceback.print_exc()
                    

            # Echo Unknown/Malformed Command line
            else:
                wrong_count += 1
                wrong.append(check_num)
                print(command_string,end='')
                print(f'{" ":5} *Error: Unknown/Malformed Command (ignored)')

        # c/e command incorrectly raised some exception during evaluations
        except Exception as e:
            wrong_count += 1
            wrong.append(check_num)
            print(command_string,end='')
            print(f'{" ":5} *Error: previous command raised exception\n{" ":8} exception: {type_as_str(e)}\n{" ":8} message  : {str(e)}')
            if local['show_traceback']:
                traceback.print_exc()
    print('Done batch_self_check:',correct_count,'correct;',wrong_count,'incorrect')
    print('Failed checks:',wrong)



# Obsolete
# batch_test reads/processes every command in a file (automating the user entering
#   these commands in the console). All exceptions are handled/traced.

# def batch_test(file_name,confirm=False):
#     print('Starting batch_test')
#     local = locals()
#     globl = globals()
#     for command in open(file_name,'r'):
#         try:
#             command = command.rstrip()
#             print('\nCommand:',command)
#             if confirm:
#                 prompt.for_string('Press enter to do command','')
#             exec(command,globl,local)
#         except Exception:
#             traceback.print_exc()
#     print('\nDone batch_test\n')




# Driver: prompts and executes commands (including calling the methods above)
# ! means call batch_self_check() with all arguments defaulted
# ? means call batch_self_check() prompting for all arguments
#    (with standard default values)

def driver():
    global default_file_name,default_separator,default_show_comment,\
           default_show_all,default_show_traceback,default_show_exception,\
           default_show_exception_message
    local = locals()
    globl = globals()
    print('Driver started')
    old = '!'
    while True:
        try:
            old = prompt.for_string('Command',default=old)
            if old == 'quit':
                print('Driver stopped')
                return None
            if old == '!':
                batch_self_check()
            elif old == '?':
                default_file_name              = prompt.for_string('file_name             ',default_file_name)
                default_separator              = prompt.for_string('separator             ',default_separator)
                default_show_comment           = prompt.for_bool  ('show_comment          ',default_show_comment)
                default_show_all               = prompt.for_bool  ('show_all              ',default_show_all)
                default_show_traceback         = prompt.for_bool  ('show_traceback        ',default_show_traceback)
                default_show_exception         = prompt.for_bool  ('show_exception        ',default_show_exception)
                default_show_exception_message = prompt.for_bool  ('show_exception_message',default_show_exception_message)
                batch_self_check()
                old = '!'
            else:
                exec(old,local,globl)
            print()
        except Exception:
            traceback.print_exc()
            print()

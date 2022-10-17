import clang.cindex

# AST representation for a single file

idx = clang.cindex.Index.create()

def verbose(*args, **kwargs):
    '''filter predicate for show_ast: show all'''
    return True

def no_system_includes(cursor, level):
    '''filter predicate for show_ast: filter out verbose stuff from system include files'''
    return (level!= 1) or (cursor.location.file is not None and not cursor.location.file.name.startswith('/usr/include'))

class Level(int):
    '''Represent currently visited level of a tree'''
    def show(self, *args):
        '''Print an indented line'''
        print ('\t'*self + ' '.join(map(str, args)))
    def __add__(self, inc):
        '''Increase level'''
        return Level(super(Level, self).__add__(inc))

def is_valid_type(t):
    '''Used to check if a cursor has a type'''
    return t.kind != clang.cindex.TypeKind.INVALID
    
def qualifiers(t):
    '''Set of qualifiers of a type'''
    q = set()
    if t.is_const_qualified(): q.add('const')
    if t.is_volatile_qualified(): q.add('volatile')
    if t.is_restrict_qualified(): q.add('restrict')
    return q

def show_type(t, level, title):
    '''Print type AST'''
    level.show(title, str(t.kind), ' '.join(qualifiers(t)))
    if is_valid_type(t.get_pointee()):
        show_type(t.get_pointee(), level+1, 'points to:')

def show_AST(cursor, filter_pred=verbose, level=Level()):
    '''Print cursor AST'''
    if filter_pred(cursor, level):
        level.show(cursor.kind, cursor.displayname, cursor.location)
        if is_valid_type(cursor.type):
            show_type(cursor.type, level+1, 'type:')
        for c in cursor.get_children():
            show_AST(c, filter_pred, level+1)

# showing the AST of the main.cpp file stored in the tests directory
tu = idx.parse(path = 'tests\main.cpp', args=None,  
            unsaved_files=None,  options=0)
show_AST(tu.cursor, no_system_includes)
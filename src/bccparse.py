import ply.yacc as yacc
import bcclex
import sys

tokens = bcclex.tokens

precedence = (
    ('right', 'AND_OP'),
    ('left', '+', '-'),
    ('left', '*', '/', '%'),
    ('left', '>', '<')
)

# statement --------------------------------


def p_statement_multiple(p):
    '''statement : statement NEWLINE statement
                 | statement NEWLINE statement NEWLINE'''
    p[0] = ('multiple_stm', p[1], p[3])


def p_statement_simple(p):
    '''statement : assignexp
                 | defineexp
                 | printexp
                 | sleepexp
                 | ifexp
                 | ifelseexp
                 | whileexp
                 | statement NEWLINE
                 | NEWLINE statement'''
    #  | loopexp NEWLINE
    if p[1] == '\n':
        p[0] = p[2]
    else:
        p[0] = p[1]

# assignexp --------------------------------


def p_assignexp_simple(p):
    '''assignexp : ID "=" expression
                 | arrayG "=" expression
                 | ID "=" INPUT
                 | arrayG "=" INPUT'''
    p[0] = ("assign", p[1], p[3])

# define --------------------------------


def p_defineexp_constant1(p):
    'defineexp : VAR ID'
    p[0] = ("var_constant", p[2], 0)


def p_defineexp_constant2(p):
    '''defineexp : VAR ID "=" val
                 | VAR ID "=" INPUT'''
    p[0] = ("var_constant", p[2], p[4])


def p_defineexp_array1(p):
    'defineexp : VAR ID "=" "{" arrayX "}"'
    p[0] = ("var_array", p[2], p[5])


def p_defineexp_array2(p):
    'defineexp : VAR ID "[" CONSTANT "]"'
    p[0] = ("var_array", p[2], p[4], 0)


def p_defineexp_array3(p):
    'defineexp : VAR ID "[" CONSTANT "]" "=" "{" arrayX "}"'
    p[0] = ("var_array", p[2], p[4], p[8])


def p_arrayX_simple(p):
    'arrayX : CONSTANT arrayY'
    p[0] = ("argument", p[1], p[2])


def p_arrayY_simple(p):
    '''arrayY : "," CONSTANT arrayY
              | empty empty empty'''
    p[0] = ("argument", p[2], p[3])

# print ----------------------------------------


def p_printexp_simple(p):
    'printexp : PRINT "(" STRING_LITERAL printX ")"'
    p[0] = ('print', p[3], p[4])


def p_printX_simple(p):
    '''printX : "," expression printX
              | empty empty empty'''
    p[0] = ('argument', p[2], p[3])

# sleep --------------------------------------


def p_sleepexp_simple(p):
    'sleepexp : SLEEP "(" val ")"'
    p[0] = ('sleep', p[3], None)

# if-else ---------------------------------------


def p_ifexp_simple(p):
    '''ifexp : IF expression "{" statement "}"
             | IF expression "{" NEWLINE statement "}"'''
    # p[0] = ('if',p[2],p[5],p[8])
    if p[4] == '\n':
        p[0] = ('if', p[2], p[5])
    else:
        p[0] = ('if', p[2], p[4])


def p_ifelseexp_simple(p):
    '''ifelseexp : ifexp elseexp'''
    p[0] = ('ifelse', p[1], p[2])


def p_elseexp_simple(p):
    '''elseexp : ELSE "{" statement "}"
               | ELSE "{" NEWLINE statement "}"'''
    if p[3] == '\n':
        p[0] = ('else', p[4])
    else:
        p[0] = ('else', p[3])


def p_whileexp_simple(p):
    '''whileexp : WHILE expression "{" statement "}"
             | WHILE expression "{" NEWLINE statement "}"'''
    if p[4] == '\n':
        p[0] = ('while', p[2], p[5])
    else:
        p[0] = ('while', p[2], p[4])

# def p_statement_var(p):
#     '''statement : VAR ID'''
#     p[0] = ('var', p[2])


# def p_statement_assign(p):
#     'statement : ID "=" expression'
#     p[0] = ('assign', p[1], p[3])


# def p_statement_if(p):
#     'statement : IF expression "{" statement "}"'
#     p[0] = ('if', p[2], p[4])


# def p_statement_while(p):
#     'statement : WHILE expression "{" statement "}"'
#     p[0] = ('while', p[2], p[4])


# Array gramma
def p_arrayG_simple(p):
    '''arrayG : ID "[" CONSTANT "]"
              | ID "[" ID "]"'''
    p[0] = ("array", p[1], p[3])

# Expression -----------------------------------------------


def p_val_simple(p):
    '''val : CONSTANT
           | arrayG
           | ID'''
    p[0] = p[1]


def p_expression_simple(p):
    '''expression : val'''
    p[0] = p[1]

# math
# + - * / % -val ()


def p_expression_math(p):
    '''expression : expression "+" expression
                  | val "+" val
                  | val "+" expression
                  | expression "-" expression
                  | val "-" val
                  | val "-" expression
                  | expression "*" expression
                  | val "*" val
                  | val "*" expression
                  | expression "/" expression
                  | val "/" val
                  | val "/" expression
                  | expression "%" expression
                  | val "%" val
                  | val "%" expression'''
    p[0] = (p[2], p[1], p[3])


def p_expression_minusValue(p):
    'expression : "-" expression'
    p[0] = ('minus', p[1])


def p_expression_bracket(p):
    'expression : "(" expression ")"'
    p[0] = p[2]

# boolean
#'EQ_OP', 'LE_OP', 'GE_OP', 'NE_OP' , 'AND_OP', 'OR_OP' , '<' , '>'


def p_expression_and(p):
    'expression : expression AND_OP expression'
    p[0] = ('&&', p[1], p[3])


def p_expression_or(p):
    'expression : expression OR_OP expression'
    p[0] = ('||', p[1], p[3])


def p_expression_EQ(p):
    '''expression : expression EQ_OP expression'''
    p[0] = ('==', p[1], p[3])


def p_expression_LE(p):
    'expression : expression LE_OP expression'
    p[0] = ('<=', p[1], p[3])


def p_expression_GE(p):
    'expression : expression GE_OP expression'
    p[0] = ('>=', p[1], p[3])


def p_expression_NE(p):
    'expression : expression NE_OP expression'
    p[0] = ('!=', p[1], p[3])


def p_expression_less(p):
    '''expression : expression "<" expression'''
    p[0] = ('<', p[1], p[3])


def p_expression_greaterthan(p):
    '''expression : expression ">" expression'''
    p[0] = ('>', p[1], p[3])


# -----------------------------------------------

def p_empty(p):
    'empty :'
    pass


def p_error(p):
    if p:
        if p.value == '\n':
            print("Syntax error at line %d" % p.lineno)
        else:
            print("Syntax error at '%s' at line %d" %
                  (p.value, p.lexer.lineno))
    else:
        print("Syntax error at EOF")
    sys.exit(1)


parser = yacc.yacc()


def parse(s, debug=False):
    return parser.parse(s, tracking=True, debug=debug)

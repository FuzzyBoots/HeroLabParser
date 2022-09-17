import sys
sys.path.insert(0, 'c:\\dev\\sly\\')
from sly import Lexer, Parser
from transitions import transitions, references, transition_set, reference_set

class HeroLabLexer(Lexer):

    tokens = { 
        NEWLINE,
        PLUS, MINUS, TIMES, DIVIDE, CONCAT, EQUAL, MOD, 
        PLUSEQUAL, MINUSEQUAL, TIMESEQUAL, DIVIDEEQUAL, CONCATEQUAL, MODEQUAL, 
        LPAREN, RPAREN, LSQUARE, RSQUARE, DOT, 
        LT, LE, GT, GE, NE, NOT, COLON,
        COMMA, PERCENT, FLOAT, QUESTION, SCONST,
        ID, NEWLINE,  AT, OR, XOR, TRANSITION, REFERENCE,
        IF,GOTO,THEN,ELSE,ELSIF,ENDIF,WHILE,LOOP,FOR,TO,NEXT,DONE,
        DONEIF,PERFORM,DEBUG,FOREACH,NEXTEACH,EACHTHING,PICK,THING,BOOTSTRAP,
        ACTOR,PORTFOLIO,IN,WHERE,SORTAS,NOTIFY,APPEND,TRUSTME,VAR,AS,
        NUMBER,STRING,THIS,COUNT,HIGH,LOW,VAL,FIELDVAL, TRUE, FALSE,
        COMMENT, MACRO,
        IF, GOTO, THEN, ELSE, ELSIF, ENDIF, WHILE, LOOP, FOR, TO, NEXT, DONE, DONEIF, PERFORM, DEBUG, FOREACH, NEXTEACH, EACHTHING, PICK, THING, BOOTSTRAP, ACTOR, PORTFOLIO, IN, WHERE, SORTAS, NOTIFY, APPEND, TRUSTME, VAR, AS, NUMBER, STRING, THIS, COUNT, HIGH, LOW, VAL, FIELDVAL, TRUE, FALSE
    }

    # String containing ignored characters between tokens
    ignore = ' \t'

    COMMENT = r'~ .*'

    FLOAT = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'

    # String literal
    SCONST = r'\"([^\\\n]|(\\.))*?\"'

    def SCONST(self, t):
        t.value = t.value[1:-1] #Strip the quotation marks
        return t

    MACRO=r'\#[A-Za-z0-9_]+'

    # Base ID rule
    ID = r'[a-zA-Z0-9_]+'

    ID['if'] = IF
    ID['goto'] = GOTO
    ID['then'] = THEN
    ID['else'] = ELSE
    ID['elsif'] = ELSIF
    ID['endif'] = ENDIF
    ID['while'] = WHILE
    ID['loop'] = LOOP
    ID['for'] = FOR
    ID['to'] = TO
    ID['next'] = NEXT
    ID['done'] = DONE
    ID['doneif'] = DONEIF
    ID['perform'] = PERFORM
    ID['debug'] = DEBUG
    ID['foreach'] = FOREACH
    ID['nexteach'] = NEXTEACH
    ID['eachthing'] = EACHTHING
    ID['pick'] = PICK
    ID['thing'] = THING
    ID['bootstrap'] = BOOTSTRAP
    ID['actor'] = ACTOR
    ID['portfolio'] = PORTFOLIO
    ID['in'] = IN
    ID['where'] = WHERE
    ID['sortas'] = SORTAS
    ID['notify'] = NOTIFY
    ID['append'] = APPEND
    ID['trustme'] = TRUSTME
    ID['var'] = VAR
    ID['as'] = AS
    ID['number'] = NUMBER
    ID['string'] = STRING
    ID['this'] = THIS
    ID['count'] = COUNT
    ID['high'] = HIGH
    ID['low'] = LOW
    ID['val'] = VAL
    ID['fieldval'] = FIELDVAL
    ID['TRUE'] = TRUE
    ID['FALSE'] = FALSE

    COLON = r':'
    EQUAL = r'='
    PLUSEQUAL = r'\+='
    MINUSEQUAL = r'-='
    TIMESEQUAL = r'\*='
    DIVIDEEQUAL = r'/='
    MODEQUAL = r'%='
    CONCATEQUAL = r'&='
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    MOD = r'%'
    CONCAT = r'&'
    LPAREN = r'\('
    RPAREN = r'\)'
    LSQUARE = r'\['
    RSQUARE = r'\]'
    DOT = r'\.'
    LT = r'<'
    LE = r'<='
    GT = r'>'
    GE = r'>='
    NE = r'!='
    COMMA = r'\,'
    PERCENT = r'%'
    QUESTION = r'\?'
    OR = r'\|'
    XOR = r'\^'
    NOT = r'\!'
    AT = r'@'
    NEWLINE = r'\n'
    
    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

class HeroLabParser(Parser):
    # Get the token list from the lexer (required)
    tokens = HeroLabLexer.tokens

    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE', 'MOD'),
        ('left', 'CONCAT'),
        ('right', 'UMINUS')
    )

    debugfile = 'HeroLab.out'
    dotfile = "HeroLab.dot"

    @_('script_ends_nl', 'script_ends_stmt')
    def script(self, p):
        return p[0]

    @_('')
    def script_ends_nl(self, p):
        return []

    @_(' script_ends_nl   NEWLINE ',
       ' script_ends_stmt NEWLINE ')
    def script_ends_nl(self, p):
        return p[0]

    @_('script_ends_nl statement')
    def script_ends_stmt(self, p):
        return p.script_ends_nl + [p.statement]

    @_('{ statement NEWLINE }')
    def statement_set(self, p):
        return p.statement

    @_( 'label', 'declaration', 'assignment', 'if_statement', 'goto_statement', 
        'binop_assign', 'doneif_statement', 'for_statement', 'while_statement')
    def statement(self, p):
        return p[0]

    @_('ID COLON')
    def label(self, p):
        return ('LABEL', p.ID)

    @_('VAR ID AS NUMBER', 
       'VAR ID AS STRING')
    def declaration(self, p):
        return ('DECLARE', p.ID, p[3])

    @_( 'reference EQUAL expression')
    def assignment(self, p):
        return ('ASSIGN', p.reference, p.expression)

    @_( 'expression PLUS expression',
        'expression MINUS expression',
        'expression TIMES expression',
        'expression DIVIDE expression',
        'expression MOD expression',
        'expression CONCAT expression')
    def expression(self, p):
        return ('BINOP', p[1], p[0], p[2])

    @_( 'field_ref', 'ID') # 
    def reference(self, p):
        # Check to see if it's on our transition or reference list
        if p._slice[0].type == 'ID':
            if p[0] in reference_set:
                return ('REFERENCE', p.ID)
            else:
                return p[0]
            
        return p[0]

    @_('LPAREN expression RPAREN')
    def expression(self, p):
        return ('GROUP', p.expression)

    @_('MINUS expression %prec UMINUS')
    def expression(self, p):
        return ('UNARY', '-', p.expression)

    @_('ID')
    def expression(self, p):
        return ('ID', p.ID)

    @_('FLOAT')
    def expression(self, p):
        return ('FLOAT', p.FLOAT)

    @_('SCONST')
    def expression(self, p):
        return ('STRING', p.SCONST)

    @_('THIS dotexpr', 'ID dotexpr')
    def field_ref(self, p):
        return ('FIELD_REF', p[0], p.dotexpr)

    @_('DOT transition')
    def dotexpr(self, p):
        return p.transition

    @_('ID')
    def transition(self, p):
        return ('REFERENCE', [], p.ID)

    @_('ID LSQUARE paramlist RSQUARE')
    def transition(self, p):
        return ('REFERENCE', p.paramlist, p.ID)

    @_('ID dotexpr')
    def transition(self, p):
        return ('TRANSITION', [], p.ID, p.dotexpr)

    @_('ID LSQUARE paramlist RSQUARE dotexpr')
    def transition(self, p):
        return ('TRANSITION', p.paramlist, p.ID, p.dotexpr)

    @_('expression { COMMA expression }') 
    def paramlist(self, p):
        return [p.expression0] + p.expression1

    @_( 'expression LT expression',
        'expression LE expression',
        'expression GT expression',
        'expression GE expression',
        'expression NE expression',
        'expression EQUAL expression')
    def expr_comp(self, p):
        return ('COMPOP', p[1], p.expression0, p.expression1)

    @_( 'reference PLUSEQUAL expression',
        'reference MINUSEQUAL expression',
        'reference TIMESEQUAL expression',
        'reference DIVIDEEQUAL expression',
        'reference MODEQUAL expression',
        'reference CONCATEQUAL expression')
    def binop_assign(self, p):
        return ('ASSIGNBINOP', p[1], p.reference, p.expression)

    @_('GOTO ID')
    def goto_statement(self, p):
        return ('GOTO', p.ID)

    @_( 'IF LPAREN expr_comp RPAREN THEN NEWLINE statement_set { elsif_statement } optional_else ENDIF',
        )
    def if_statement(self, p):
        expressions = []
        expressions.append((p.expr_comp, p.statement_set))
        else_statement = p.optional_else
        
        expressions.extend(p.elsif_statement_list)

        return ('IF', expressions, else_statement)

    @_('[ ELSE NEWLINE statement_set ]')
    def optional_else(self, p):
        return p.statement_set

    @_('{ elsif_statement }')
    def elsif_statement_list(self, p):
        return p.elsif_statement

    @_('ELSIF LPAREN expr_comp RPAREN THEN NEWLINE statement_set')
    def elsif_statement(self, p):
        return (p.expr_comp, p.statement_set)

    @_('WHILE LPAREN expr_comp RPAREN NEWLINE statement_set LOOP')
    def while_statement(self, p):
        return ('WHILE', p.expr_comp, p.statement_set)

    @_('FOR ID EQUAL expression TO expression NEWLINE statement_set NEXT')
    def for_statement(self, p):
        return ('FOR', p.ID, p.expr0, p.expr1, p.statement_set)

    @_('DONEIF LPAREN expr_comp RPAREN')
    def doneif_statement(self, p):
        return ('DONEIF', p.expr_comp)


if __name__ == '__main__':
    lexer = HeroLabLexer()
    
    data = '''567:
    
    var myID as number
    var myID2 as string

    myID = 567
    myID2 = myID

    this.field.subfield[5, "thin mint"].bob = "Hello!"
    '''

    data2 = '''bob =45
    width = 50
    this.width = 90
    this.bob = 120'''
    tokens = lexer.tokenize(data2)
    tokens_bak = lexer.tokenize(data2)
    for tok in tokens_bak:
        print('type=%r, value=%r' % (tok.type, tok.value))

    parser = HeroLabParser()
    result = parser.parse(tokens)
    print (result)
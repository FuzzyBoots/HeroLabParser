import sys
sys.path.insert(0, 'c:\\dev\\HeroLabParser\\')
from sly import Lexer

class HeroLabLexer(Lexer):

    tokens = { 
        NEWLINE,
        PLUS, MINUS, TIMES, DIVIDE, CONCAT, EQUAL, MOD, 
        PLUSEQUAL, MINUSEQUAL, TIMESEQUAL, DIVIDEEQUAL, CONCATEQUAL, MODEQUAL, 
        LPAREN, RPAREN, LSQUARE, RSQUARE, DOT, 
        LT, LE, GT, GE, NE, NOT, COLON,
        COMMA, PERCENT, FLOAT, QUESTION, SCONST,
        ID, NEWLINE,  OR, XOR, TRANSITION, REFERENCE,
        IF,GOTO,THEN,ELSE,ELSIF,ENDIF,WHILE,LOOP,FOR,TO,NEXT,DONE,
        DONEIF,PERFORM,DEBUG,FOREACH,NEXTEACH,PICK,THING,BOOTSTRAP,
        ACTOR,PORTFOLIO,IN,WHERE,SORTAS,NOTIFY,APPEND,TRUSTME,VAR,AS,EACHTHING,EACHPICK,
        INTEGER, NUMBER,STRING,THIS,COUNT,HIGH,LOW,VAL,FIELDVAL, TRUE, FALSE,
        COMMENT, MACRO, TAG, SPEC_SYMBOL,
    }

    # String containing ignored characters between tokens
    ignore = ' \t'

    COMMENT = r'\~.*'

    FLOAT = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'

    # String literal
    SCONST = r'\"([^\\\n]|(\\.))*?\"'

    def SCONST(self, t):
        t.value = t.value[1:-1] #Strip the quotation marks
        return t

    SPEC_SYMBOL = r'@[A-Za-z]'
    
    MACRO = r'\#[A-Za-z0-9_]+'

    TAG = r'[A-Za-z0-9_]*\?'

    INTEGER = r'[0-9]+'

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
    ID['eachpick'] = EACHTHING
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
    
    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

    @_(r'\n+')
    def NEWLINE(self, t):
        self.lineno += t.value.count('\n')
        return t
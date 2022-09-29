import sys
sys.path.insert(0, 'c:\\dev\\HeroLabParser\\')
from sly import Parser
from HeroLabLexer import HeroLabLexer
from transitions import transitions, references, transition_set, reference_set

class executionTuple():
        def __init__(self, name, params, lineno, index, end):
            self.name = name
            self.params = params
            self.lineno = lineno
            self.index = index
            self.end = end

        def __repr__(self):
            return '("%s", %s, %s, %s, %s)'\
                % (self.name, self.params, self.lineno, self.index, self.end)
            # return 'executionTuple name:%s params:%s lineno:%s index:%s, end:%s' \
                
        def __str__(self):
            return '("%s", %s, %s, %s, %s)'\
                % (self.name, self.params, self.lineno, self.index, self.end)



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

    # def error(self, tok):
    #     # Read ahead looking for a terminating newline
    #     while True:
    #         tok = next(self.tokens, None)           # Get the next token
    #         if not tok or tok.type == 'NEWLINE':
    #             break
    #         self.errok()

    #     # Return NEWLINE to the parser as the next lookahead token
    #     return tok

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
        return list(filter(lambda statement: statement != None, 
            p.script_ends_nl + [p.statement]))

    @_('statement NEWLINE { statement NEWLINE }')
    def statement_set(self, p):
        return list(filter(lambda statement: statement != None, 
            p.statement1 + [p.statement0]))

    @_( 'comment', 'label', 'declaration', 'assignment', 'if_statement', 'goto_statement', 
        'binop_assign', 'doneif_statement', 'for_statement', 'while_statement', 
        'foreach_statement', 'notify_statement', 'debug_statement', 'trustme_statement',
        'append_statement', 'perform_statement', 'done_statement')
    def statement(self, p):
        return p[0]

    @_('COMMENT')
    def comment(self, p):
        pass

    @_('ID', 'INTEGER') # 345 could be an integer or an ID. Checked at runtime.
    def id_or_integer(self, p):
        return p[0]

    @_('id_or_integer COLON')
    def label(self, p):
        return executionTuple('LABEL', [p.id_or_integer], p.lineno, p.index, p.end)

    @_('VAR id_or_integer AS NUMBER', 
       'VAR id_or_integer AS STRING')
    def declaration(self, p):
        return executionTuple('DECLARE', [p.id_or_integer, p[3]], p.lineno, p.index, p.end)

    @_( 'reference EQUAL expression')
    def assignment(self, p):
        return executionTuple('ASSIGN', [p.reference, p.expression], p.lineno, p.index, p.end)

    @_( 'reference EQUAL error')
    def assignment(self, p):
        return executionTuple('ERROR', ["Error evaluating right side of equation"], p.lineno, p.index, p.end)

    @_( 'expression PLUS expression',
        'expression MINUS expression',
        'expression TIMES expression',
        'expression DIVIDE expression',
        'expression MOD expression',
        'expression CONCAT expression')
    def expression(self, p):
        return executionTuple('BINOP', [p[1], p[0], p[2]], p.lineno, p.index, p.end)

    @_( 'field_ref', 'id_or_integer') # 
    def reference(self, p):
        # Check to see if it's on our transition or reference list
        if p._slice[0].type == 'id_or_integer':
            if p[0] in reference_set:
                return executionTuple('REFERENCE', [p.id_or_integer], p.lineno, p.index, p.end)
            else:
                return p[0]
            
        return p[0]

    @_('LPAREN expression RPAREN')
    def expression(self, p):
        return executionTuple('GROUP', [p.expression], p.lineno, p.index, p.end)

    @_('MINUS expression %prec UMINUS')
    def expression(self, p):
        return executionTuple('UNARY', ['-', p.expression], p.lineno, p.index, p.end)

    @_('id_or_integer')
    def expression(self, p):
        return executionTuple('ID', [p.id_or_integer], p.lineno, p.index, p.end)

    @_('FLOAT')
    def expression(self, p):
        return executionTuple('FLOAT', [p.FLOAT], p.lineno, p.index, p.end)

    @_('SCONST')
    def expression(self, p):
        return executionTuple('STRING', [p.SCONST], p.lineno, p.index, p.end)

    @_('SPEC_SYMBOL')
    def expression(self, p):
        return ('SPEC_SYMBOL', p.SPEC_SYMBOL)

    @_('THIS dotexpr', 'id_or_integer dotexpr')
    def field_ref(self, p):
        return ('FIELD_REF', p[0], p.dotexpr)

    @_('DOT transition')
    def dotexpr(self, p):
        return p.transition

    @_('id_or_integer')
    def transition(self, p):
        return executionTuple('REFERENCE', [[], p.id_or_integer], p.lineno, p.index, p.end)

    @_('id_or_integer LSQUARE paramlist RSQUARE')
    def transition(self, p):
        return executionTuple('REFERENCE', [p.paramlist, p.id_or_integer], p.lineno, p.index, p.end)

    @_('id_or_integer dotexpr')
    def transition(self, p):
        return executionTuple('TRANSITION', [[], p.id_or_integer, p.dotexpr], p.lineno, p.index, p.end)

    @_('id_or_integer LSQUARE paramlist RSQUARE dotexpr')
    def transition(self, p):
        return executionTuple('TRANSITION', [p.paramlist, p.id_or_integer, p.dotexpr], p.lineno, p.index, p.end)

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
        return executionTuple('COMPOP', [p[1], p.expression0, p.expression1], p.lineno, p.index, p.end)

    @_( 'reference PLUSEQUAL expression',
        'reference MINUSEQUAL expression',
        'reference TIMESEQUAL expression',
        'reference DIVIDEEQUAL expression',
        'reference MODEQUAL expression',
        'reference CONCATEQUAL expression')
    def binop_assign(self, p):
        return executionTuple('ASSIGNBINOP', [p[1], p.reference, p.expression], p.lineno, p.index, p.end)

    @_('GOTO id_or_integer')
    def goto_statement(self, p):
        return executionTuple('GOTO', [p.id_or_integer.value], p.lineno, p.index, p.end)

    @_( 'IF LPAREN expr_comp RPAREN THEN NEWLINE statement_set { elsif_statement } optional_else ENDIF')
    def if_statement(self, p):
        expressions = []
        expressions.append((p.expr_comp, p.statement_set))
        else_statement = p.optional_else
        
        expressions.extend(p.elsif_statement)

        return executionTuple('IF', [expressions, else_statement], p.lineno, p.index, p.end)

    @_('[ ELSE NEWLINE statement_set ]')
    def optional_else(self, p):
        return p.statement_set

    @_('ELSIF LPAREN expr_comp RPAREN THEN NEWLINE statement_set')
    def elsif_statement(self, p):
        return (p.expr_comp, p.statement_set)

    @_('WHILE LPAREN expr_comp RPAREN NEWLINE statement_set LOOP')
    def while_statement(self, p):
        return executionTuple('WHILE', [p.expr_comp, p.statement_set], p.lineno, p.index, p.end)

    @_('FOR id_or_integer EQUAL expression TO expression NEWLINE statement_set NEXT')
    def for_statement(self, p):
        return executionTuple('FOR', [p.id_or_integer, p.expr0, p.expr1, p.statement_set], p.lineno, p.index, p.end)

    @_('DONEIF LPAREN expr_comp RPAREN')
    def doneif_statement(self, p):
        return executionTuple('DONEIF', [p.expr_comp], p.lineno, p.index, p.end)

    @_('PERFORM field_ref')
    def perform_statement(self, p):
        return executionTuple('PERFORM', [p.field_ref], p.lineno, p.index, p.end)

    @_('APPEND expression')
    def append_statement(self, p):
        return executionTuple('APPEND', [p.expression], p.lineno, p.index, p.end)

    @_('TRUSTME')
    def trustme_statement(self, p):
        return ('TRUSTME')

    @_('DONE')
    def done_statement(self, p):
        return ('DONE')

    @_('NOTIFY expression')
    def notify_statement(self, p):
        return executionTuple('NOTIFY', [p.expression], p.lineno, p.index, p.end)

    @_('DEBUG expression')
    def debug_statement(self, p):
        return executionTuple('DEBUG', [p.expression], p.lineno, p.index, p.end)

    @_( 'FOREACH PICK IN id_or_integer [ where_clause ] [ sortas_clause ] NEWLINE statement_set NEXTEACH',
        'FOREACH THING IN id_or_integer [ where_clause ] [ sortas_clause ] NEWLINE statement_set NEXTEACH',
        'FOREACH BOOTSTRAP IN THIS [ where_clause ] [ sortas_clause ] NEWLINE statement_set NEXTEACH',
        'FOREACH BOOTSTRAP IN id_or_integer [ where_clause ] [ sortas_clause ] NEWLINE statement_set NEXTEACH',
        'FOREACH ACTOR IN PORTFOLIO [ where_clause ] [ sortas_clause ] NEWLINE statement_set NEXTEACH')
    def foreach_statement(self,p):
        return executionTuple('FOREACH', [p[1], p[3], p.where_claus, p.sortas_clause, p.statement_set], p.lineno, p.index, p.end)

    @_('WHERE tag_expression')
    def where_clause(self, p):
        return p.tag_expression

    @_('SORTAS id_or_integer')
    def sortas_clause(self, p):
        return p.id_or_integer
    
    # Tag operations (only used for WHERE and taxepr?)
    @_( 'id_or_integer DOT TAG')
    def tag_template(self, p):
        return executionTuple('TAGTEMPLATE', [p.id_or_integer, p.TAG], p.lineno, p.index, p.end)

    @_( 'TRUE', 'FALSE', 'tag_template')
    def tag_simple_term(self, p):
        return p[0]

    @_('tag_simple_term')
    def tag_expression(self, p):
        return ("SIMPLE_TERM", p.tag_simple_term)

    # @('ID')   # Not ideal... but integers are detected as potential IDs
    # def tag_value(self, p):

    # Macros are processed before plugging the script text in
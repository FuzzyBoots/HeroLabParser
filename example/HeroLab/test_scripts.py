import unittest
from HeroLab import HeroLabParser, HeroLabLexer 

def test_script(self):
    script = '''id:
    debug "Yo!"
    goto id'''

    lexer = HeroLabLexer()    
    tokens = lexer.tokenize(script)
    # tokens_bak = lexer.tokenize(data2)
    # for tok in tokens_bak:
    #     print('type=%r, value=%r' % (tok.type, tok.value))

    parser = HeroLabParser()
    result = parser.parse(tokens)
    assert(result == [('LABEL', 'id'), ('DEBUG', ('STRING', 'Yo!')), ('GOTO', 'id')])

 if __name__ == "__main__":
    unittest.main() # run all tests
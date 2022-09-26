from HeroLabLexer import HeroLabLexer
from HeroLabParser import HeroLabParser

if __name__ == '__main__':
    lexer = HeroLabLexer()
    
    data = '''567:
    
    var myID as number
    var myID2 as string

    myID = 5678
    myID2 = myID

    this.field.subfield[5, "thin mint"].bob = "Hello!"
    '''

    data2 = '''bob =45
    width = 50
    this.width = 90
    this.bob = 120
    
    if (bob > 40) then
      this.width = 90
      ~ Comment
      this.bob = width
    else
      this.index[50, "Alf"] = 4+5
    endif'''

    data3='''~ THis is a comment
    var bob as string
    bob = "Bill"
    debug bob'''

    data4='''debug "test"
    
    this.width.height = 40'''
    tokens = lexer.tokenize(data)
    tokens_bak = lexer.tokenize(data)
    for tok in tokens_bak:
        print('type=%r, value=%r, lineno=%r, index=%r' % (tok.type, tok.value, tok.lineno, tok.index))

    parser = HeroLabParser()
    result = parser.parse(tokens)
    print (result)
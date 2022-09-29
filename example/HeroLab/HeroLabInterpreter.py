class HeroLabInterpreter():
    def loadAST(self, ast):
        self.ast = ast
        code = []
        codeIndex = {}

    def interpret(self, tokens):
        if isinstance(tokens, list):
            for statement in tokens:
                self.interpret(statement)
        elif (tokens.name == 'DECLARE'):
            name, type = tokens.params
            if vars[name] is None:
                if type == 'NUMBER':
                    vars[name] = (name, 0.0)
                else:
                    vars[name] = ""
            else:
                if (vars[name][0] != type):
                    print ("Mismatched types") 
        elif (tokens.name == 'LABEL'):
            self.codeIndex(tokens.params[0], len(self.code))
        elif (tokens.name == 'GOTO'):
            self.code += ('JUMP', tokens.params[0])
            
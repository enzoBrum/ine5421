class RegEx:
    def __init__(self, rawRegEx):
        self.rawRegEx = rawRegEx
        self.transformedRegEx = ''

        self.transform(rawRegEx)

    def transform(self, rawRegEx):
        # Procura classes [a-d] e expande elas como (a|b|c|d)
        valid, expandedRegEx = self.expandClasses(rawRegEx)
        #print('Expanded:', expandedRegEx)
        if not(valid):
            print('Invalid Regular Expression')
            return

        # Adiciona oi simbolo de concatenaçao '.'
        valid, concatened = self.addConcat(expandedRegEx)
        #print('Concat: ', concatened )

        if not(valid):
            print('Invalid Regular Expression')
            return

        # Tranforma da notação infixada para pós-fixada utilizando
        # Shunting Yard
        valid, postFixed = self.postfix(concatened)
        #print('postFixed:', postFixed)

        if not(valid):
            print('Invalid Regular Expression')
            return

        self.transformedRegEx = postFixed

    def expandClasses(self, regEx):
        valid = True
        inside = False

        newRegex = ''
        for i in range(len(regEx)):
            token = regEx[i]
            if token == '[':
                # Controle para quando estamos dentro da classe [ ]
                inside = True
                # Controle interno, para os intervalos diferentes
                # intervalos dentro da classe
                # Ex: [a-zA-Z] -> ['a', '-', 'z'] / ['A', '-', 'Z']
                interval = []
                newRegex += '('
                continue

            if token == ']':
                inside = False
                newRegex = newRegex[:-1] + ')'
                continue

            if inside:
                interval.append(token)
                # ['a', '-']
                if len(interval) == 2 and token != '-':
                    valid = False
                    break

                # ['a', '-', 'z']
                elif len(interval) == 3:
                    start = ord(interval[0])
                    end = ord(interval[2])
                    # Verifica se o intervalo é válido
                    # > código ascii inicial < que o final
                    if start > end:
                        valid = False
                        break

                    # Gera a nova string do intervalo encontrado
                    for ascii in range(start, end+1):
                        newRegex += chr(ascii) + '|'

                    # Empty list to the nex interval. -> Ex: ['A', '-', 'Z']
                    # Limpa a lista para que seja utilizada no próximo intervalo
                    interval = []
            else:
                newRegex += token

        return valid, newRegex

    def addConcat(self, regExp):
        newRegex = ""
        valid = True
        for i in range(len(regExp)):
            currentToken= regExp[i]
            newRegex += currentToken

            if i == (len(regExp)-1):
                break

            nextToken = regExp[i + 1]

            # Verifica se a sequencia de tokens da
            # expressão está correta
            join = currentToken + nextToken
            if (join in ['()', '||', '(|', '|)']):
                valid = False
                break

            # currentToken != ( |
            # nextToken != ) | + * ?
            if (currentToken not in '(|' and nextToken not in ')|+*?'):
                newRegex += '.'

        return valid, newRegex

    # Shunting Yard
    def postfix(self, regExp):
        precedence = {'*': 3, '+': 3, '?': 3, '.': 2, '|': 1}
        operators = '(*+?.|)'

        valid = True

        # Lista para guardar operadores que ainda nao
        # foram organizados
        opStack = []
        newRegex = []

        for token in regExp:

            if token not in operators:
                # Coloca na saida o token "normal"
                newRegex.append(token)

            elif token == '(':
                # Guarda o inicio da precedencia
                # Analisar a regExpressão interna até esse ponto
                opStack.append(token)

            # Encontra o final da precedencia
            elif token == ')':
                # Coloca tudo que está na pilha na saida
                # Menos os parenteses
                while opStack and opStack[-1] != '(':
                    newRegex.append(opStack.pop())
                opStack.pop()

            else:
                # Desempilha os tokens da pilha que possuem precedencia maior que o token atual
                while (opStack and opStack[-1] != '(' and precedence[token] <= precedence[opStack[-1]]):
                    newRegex.append(opStack.pop())

                # Empilha operador atual
                opStack.append(token)

        # Após o fim da regExpressão, desempilha o que restou e coloca na saida
        while opStack:
            newRegex.append(opStack.pop())

        newRegex = ''.join(newRegex)

        if ('(' in newRegex) or (')' in newRegex):
            valid =  False

        return valid, newRegex
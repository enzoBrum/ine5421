
class ThompsonAFN:
    def __init__(self, regex):
        self.transitions = {}
        self.stateCount = 0
        self.regex = regex

        self.thompson(regex)

    def createTransition(self, start, input, end):
        if not(start in self.transitions.keys()):
            self.transitions[start] = {}

        # Verifica se ja existe uma transicao por esta entrada
        # Transicoes por ε permitem isto
        if input in self.transitions[start].keys():
            oldEnd = self.transitions[start][input]
            if isinstance(oldEnd, list):
                oldEnd.append(newEnd)
                newEnd = oldEnd

            else:
                newEnd = [oldEnd]
                newEnd.append(end)
        else:
            newEnd = end

        self.transitions[start][input] =  newEnd

    def newState(self):
        stateName = f"q{self.stateCount}"
        self.stateCount += 1
        return stateName

    # Operações de construção de fragmentos do AFN
    def thompsonSymbol(self, char):
        newStart = self.newState()
        newEnd = self.newState()

        self.createTransition(newStart, char, newEnd)

        return newStart, newEnd

    def thompsonConcat(self, afn1, afn2):
        start1, end1 = afn1
        start2, end2 = afn2

        self.createTransition(end1, '&', start2)

        return start1, end2

    def thompsonKleene(self, afn):
        start, end = afn
        newStart = self.newState()
        newEnd = self.newState()

        self.createTransition(newStart, '&', start)
        self.createTransition(newStart, '&', newEnd)

        self.createTransition(end, '&', start)
        self.createTransition(end, '&', newEnd)

        return newStart, newEnd

    # a+ // q0 -> a -> q1 // q0 -> a -> q1 -> ε -> q0
    def thompsonPlus(self, afn):
        start, end = afn

        self.createTransition(end, '&', start)

        return start, end

    # a? // q0 -> a -> q1 // q0 -> a,ε -> q1
    def thompsonOptional(self, afn):
        start, end = afn

        self.createTransition(start, '&', end)

        return start, end

    def thompsonUnion(self, afn1, afn2):
        # start1, end1 = (state_start, state_end)
        start1, end1 = afn1
        start2, end2 = afn2
        newStart = self.newState()
        newEnd = self.newState()


        self.createTransition(newStart, '&', start1)
        self.createTransition(newStart, '&', start2)

        self.createTransition(end1, '&', newEnd)
        self.createTransition(end2, '&', newEnd)

        return newStart, newEnd


    # Função principal que processa a notação pós-fixada
    def thompson(self, postfix):
        stack = []

        for char in postfix:
            if char in '*+?|.':
                if char == '*':
                    afn = stack.pop()
                    stack.append(self.thompsonKleene(afn))
                elif char == '+':
                    afn = stack.pop()
                    stack.append(self.thompsonPlus(afn))
                elif char == '?':
                    afn = stack.pop()
                    stack.append(self.thompsonOptional(afn))
                elif char == '|':
                    afn2 = stack.pop()
                    afn1 = stack.pop()
                    stack.append(self.thompsonUnion(afn1, afn2))
                elif char == '.':
                    afn2 = stack.pop()
                    afn1 = stack.pop()
                    stack.append(self.thompsonConcat(afn1, afn2))
            else:
                stack.append(self.thompsonSymbol(char))

        self.start, self.final = stack.pop()
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from transformER import RegEx
from generateAFN import ThompsonAFN
from finite_automaton import FiniteAutomaton
from determinizer import determinize


# Expressão base
expressao = "a?(a|b)+"

# Gera uma expressão regular no formatos pós fixado
expressao = RegEx(expressao)
expPosfix = expressao.transformedRegEx

# Valor experado:
print('Expressão pós fixada ->', expPosfix)


# Gera o autômato não determinístio
afn = ThompsonAFN(expPosfix)
afnTransicoes = afn.transitions


# Valor esperado: Imagem anexada nesta pasta
print('AFN Transicoes -> ', afnTransicoes)

# Determinizacao

# Converte para o formato necessário
automatoFinito = FiniteAutomaton.from_thompson_afn(afn) 
# Determiniza
automatoFinito = determinize(automatoFinito)

try:
    from draw import desenhar_automato
    desenhar_automato(
        "nao_determinizado", afnTransicoes, afn.start, afn.final, "test/"
        )
    desenhar_automato(
        "determinizado", automatoFinito.transitions, automatoFinito.initial_state, automatoFinito.final_states, "test/"
        )
except Exception as e:
    print(f"Erro ao tentar desenhar os autômatos: {e}")

print('Automato determinizado -> ', FiniteAutomaton.dumps(automatoFinito))
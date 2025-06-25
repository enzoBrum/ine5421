from collections import defaultdict
from copy import deepcopy
import json
from math import floor, log10
from utils import build_canonical_collection, closure, go_to
from dataclasses import dataclass
from first_follow import compute_first, compute_follow

Productions = list[tuple[str, list[str]]]

@dataclass
class SlrState:
    # DIcionário mapeando um token à uma acão
    actions: dict[str, str]
    
    # Especifica o desvio 
    goto: dict[str, int]

class SlrTable:
    
    # Estados presentes na tabela
    states: list[SlrState]

    # Mapeia o ID de uma produção à uma tupla contendo: a cabeça da produção e o comprimento do corpo dela.
    productions: Productions
    
    def __init__(self, states: list[SlrState], productions: Productions):
        self.states = states
        self.productions = productions

    
    def pretty_print(self):
        terminals = set()
        non_terminals = set()
        for st in self.states:
            terminals |= set(st.actions.keys())
            non_terminals |= set(st.goto.keys())
            
        alpha_terminals = [x for x in terminals if x.isalnum()]
        non_alpha_terminals = [x for x in terminals if not x.isalnum()]
        
        terminals = sorted(alpha_terminals) + sorted(non_alpha_terminals, reverse=True)

        non_terminals = sorted(non_terminals)
        n_terminals = len(terminals)
        n_non_terminals = len(non_terminals)
        
        
        longest_terminal = max([len(x) for x in terminals])
        longest_non_terminal = max([len(x) for x in non_terminals])
        
        longest = max(longest_terminal, longest_non_terminal, 3, floor(log10(len(self.states))) + 1)
        
        num_actions_padding = longest*n_terminals + (n_terminals-1)*3
        num_goto_padding = longest*n_non_terminals + (n_non_terminals-1)*3
        
        print("Produções: ")
        
        padding_prod_idx = floor(log10(len(self.productions))) + 1
        for i, (head, body) in enumerate(self.productions):
            print(f"    ({i:<{padding_prod_idx}}) {head:<{longest}} ::= {' '.join(body)}")


        print(f"\n\nTabela SLR:\n")
        print(f"{'Estado':^8}  |  {'Ação':^{num_actions_padding}}  |  {'Desvio':^{num_goto_padding}}")
        
        print(f"{' '*8}  |  {'   '.join(f'{x:<{longest}}' for x in terminals)}  |  {'   '.join(f'{x:<{longest}}' for x in non_terminals)}")
        
        print(f"{'-'*9} + {'-'*(num_actions_padding+2)} + {'-'*(num_goto_padding+2)}")
        
        for i, st in enumerate(self.states):
            formatted_actions = [f"{st.actions.get(x, ''):<{longest}}" for x in terminals]
            formatted_goto =[f"{st.goto.get(x, ''):<{longest}}" for x in non_terminals]
            print(f"{i:<8}  |  {'   '.join(formatted_actions)}  |  {'   '.join(formatted_goto)}")

    
    @staticmethod
    def _get_first_and_follows(non_terminal_symbols: set[str], productions: dict[str, list[list[str]]], start_symbol: str) -> tuple[set[str], set[str]]:
        first_sets = defaultdict(set)
        follow_sets = defaultdict(set)
        terminal_symbols = set()
        
        for body in productions.values():
            for rule in body:
                for token in rule:
                    if token not in non_terminal_symbols:
                        terminal_symbols.add(token)

        
        visited = set()
        for nt in non_terminal_symbols:
            # first_sets é mutável...
            compute_first(nt, first_sets, terminal_symbols, productions, visited)
            
        first_sets_tmp = deepcopy(first_sets)
        visited = set()
        for nt in non_terminal_symbols:
            # first_sets e follow_sets são mutáveis...
            compute_follow(nt, start_symbol, first_sets_tmp, follow_sets, productions, terminal_symbols, visited)
            
        return first_sets, follow_sets
            


    @staticmethod
    def build(productions: list[tuple[str, list[list[str]]]]):
        non_terminal_symbols = {prod[0] for prod in productions}
        
        old_start_state = productions[0][0]
        
        new_start_state = f"{old_start_state}'"
        
        # (<head>, <body>, <dot>)
        new_start_production = (new_start_state, (old_start_state,), 0)
        
        converted_productions = {head: body for head, body in productions}
        states = [closure([new_start_production], converted_productions)]
        canonical_collection = build_canonical_collection(states, converted_productions)
        canonical_item_to_idx = {str(sorted(item)): i for i, item in enumerate(canonical_collection)}

        slr_states: list[SlrState] = []
        first, follow = SlrTable._get_first_and_follows(non_terminal_symbols, converted_productions, old_start_state)
        
        slr_productions: Productions = []
        canonical_subitem_str_to_idx: dict[str, int] = {}
        for item in canonical_collection:
            for head, body, _ in item:
                if (key := f"{head} -> {' '.join(body)}") not in canonical_subitem_str_to_idx:
                    canonical_subitem_str_to_idx[key] = len(slr_productions)
                    slr_productions.append((head, body))

        for item in canonical_collection:
            actions = {}
            goto = {}
            for head, body, dot in item:
                if dot >= len(body):
                    if head == new_start_state:
                        assert '$' not in actions, "Gramática não é SLR(1)"
                        actions['$'] = "acc"
                        continue
                    
                    prod_idx = canonical_subitem_str_to_idx[f"{head} -> {' '.join(body)}"]
                    for terminal in follow[head]:
                        assert terminal not in actions, "Gramática não é SLR(1)"
                        actions[terminal] = f"r{prod_idx}"
                elif body[dot] not in non_terminal_symbols and (other_item := go_to(item, body[dot], converted_productions)):
                    idx = canonical_item_to_idx[str(sorted(other_item))]
                    assert body[dot] not in actions, "Gramática não é SLR(1)"
                    actions[body[dot]] = f"s{idx}"
                        
            for non_terminal in non_terminal_symbols:
                if (other_item := go_to(item, non_terminal, converted_productions)):
                    idx = canonical_item_to_idx[str(sorted(other_item))]
                    goto[non_terminal] = idx
                    
            slr_states.append(SlrState(actions, goto))
        
        
        return SlrTable(slr_states, slr_productions)

                    
    @staticmethod
    def dumps(table: "SlrTable") -> str:
        out_dict = {
            "productions": table.productions,
            'states': [{"actions": st.actions, "goto": st.goto} for st in table.states]
        }
        
        return json.dumps(out_dict)

    @staticmethod
    def loads(table: str) -> "SlrTable":
        in_dict = json.loads(table)
        
        productions = in_dict["productions"]
        states = []
        for st in in_dict["states"]:
            states.append(SlrState(st["actions"], st["goto"]))
        return SlrTable(states, productions)
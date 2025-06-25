import traceback
from slr_table import SlrTable


def parse(table: SlrTable, token_list: list[str]):
    token_types = [t.split(',')[0].strip()[1:] for t in token_list]
    
    if token_types[-1] != '$':
        token_types.append('$')
    
    stack = [0]
    i = 0
    
    while True:
        cur = token_types[i]
        
        try:
            s = stack[-1]
            state = table.states[s]
            if state.actions[cur].startswith('s'):
                s2 = int(state.actions[cur][1:])
                stack.append(cur)
                stack.append(s2)
                i += 1
            elif state.actions[cur].startswith('r'):
                prod_idx = int(state.actions[cur][1:])
                head, body = table.productions[prod_idx]
                len_body = len(body)
                
                for _ in range(2*len_body):
                    stack.pop()
                    
                s2 = stack[-1]
                state = table.states[s2]
                stack.append(head)
                stack.append(state.goto[head])
            elif state.actions[cur] == 'acc':
                print("Análise bem-sucedida!")
                return
        except:    
            error = traceback.format_exc()
            with open(".error-logs.txt", "w") as f:
                f.write(error)

            print(f"Erro durante o parsing! O símbolo {cur} não é ação válida para o estado {s}.")
            print(' '.join(token_types))
            spaces = 0
            for j in range(i):
                spaces += len(token_types[j]) + 1
            print(f"\033[31m{'~'*spaces}{'^'*len(cur)}\033[0m")
            exit(1)
            

    
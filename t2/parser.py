import traceback
from slr_table import SlrTable


def parse(table: SlrTable, token_list: list[str], symbol_table: list[str]):
    # Categoria do token
    token_types = [t.split(",")[0].strip()[1:] for t in token_list]

    # Endereço na tabela de símbolos
    token_addrs = [int(t.split(",")[1].strip()[:-1]) - 1 for t in token_list]

    if token_types[-1] != "$":
        token_types.append("$")

    stack = [0]
    i = 0

    while True:
        cur = token_types[i]

        try:
            s = stack[-1]
            state = table.states[s]
            if state.actions[cur].startswith("s"):
                s2 = int(state.actions[cur][1:])
                stack.append(cur)
                stack.append(s2)
                i += 1
            elif state.actions[cur].startswith("r"):
                prod_idx = int(state.actions[cur][1:])
                head, body = table.productions[prod_idx]
                len_body = len(body)

                for _ in range(2 * len_body):
                    stack.pop()

                s2 = stack[-1]
                state = table.states[s2]
                stack.append(head)
                stack.append(state.goto[head])
            elif state.actions[cur] == "acc":
                print("Análise bem-sucedida!")
                return
        except:
            error = traceback.format_exc()
            with open(".error-logs.txt", "w") as f:
                f.write(error)

            print(
                f"Erro durante o parsing! O lexema {cur} não é ação válida para o estado {s}."
            )

            sentence = []
            for j in range(len(token_addrs)):
                if j < i:
                    sentence.append(f"\033[32m{symbol_table[token_addrs[j]]}\033[0m")
                elif j == i:
                    sentence.append(f"\033[31m{symbol_table[token_addrs[j]]}\033[0m")
                else:
                    sentence.append(symbol_table[token_addrs[j]])

            print(" ".join(sentence))
            spaces = 0
            for j in range(i):
                spaces += len(sentence[j]) - 9 + 1

            if i >= len(sentence):
                print(f"\033[31m{'~'*spaces}{'^'*(5)}\033[0m")
            else:
                print(f"\033[31m{'~'*spaces}{'^'*(len(sentence[i]) - 9)}\033[0m")
            exit(1)

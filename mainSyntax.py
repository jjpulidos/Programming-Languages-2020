#initial_symbol_grammar = "expr"
# not_terminals = ["expr", "expr_aux", "expr_p2", "expr_p2_aux", "expr_p3", "expr_p3_aux", "expr_p4",
#                  "cexpr", "cexpr_aux","bin_op_log","cexpr_p6","cexpr_p6_aux","bin_op_p6","cexpr_p7",
#                  "cexpr_p7_aux", "bin_op_p7","cexpr_p8", "cexpr_p9","cexpr_p9_aux", "expr_list_no_req",
#                  "expr_list_0_more","member_expr","index_expr","target"]
#
# grammar = {
#     "expr": [["expr_p2", "expr_aux"]],
#     "expr_aux": [["if", "expr", "else", "expr"], [""]],
#     "expr_p2": [["expr_p3", "expr_p2_aux"]],
#     "expr_p2_aux": [["or", "expr_p3", "expr_p2_aux"], [""]],
#     "expr_p3": [["expr_p4", "expr_p3_aux"]],
#     "expr_p3_aux": [["and", "expr_p4", "expr_p3_aux"], [""]],
#     "expr_p4": [["not", "expr_p4"], ["cexpr"]],
#     "cexpr":[["cexpr_p6","cexpr_aux"]],
#     "cexpr_aux":[["bin_op_log","cexpr_p6"],[""]],
#     "bin_op_log": [["igual"],["diferente"],["mayor"],["menor"],["mayor_igual"],["menor_igual"],["is"]],
#     "cexpr_p6": [["cexpr_p7", "cexpr_p6_aux"]],
#     "cexpr_p6_aux": [["bin_op_p6","cexpr_p7","cexpr_p6_aux"],[""]],
#     "bin_op_p6": [["tk_suma"], ["tk_menos"]],
#     "cexpr_p7": [["cexpr_p8", "cexpr_p7_aux"]],
#     "cexpr_p7_aux": [["bin_op_p7", "cexpr_p8", "cexpr_p7_aux"], [""]],
#     "bin_op_p7": [["tk_multiplicacion"],["tk_division"],["tk_modulo"]],
#     "cexpr_p8": [["tk_menos", "cexpr_p9"], ["cexpr_p9"]],
#     "cexpr_p9": [["id"],["literal"],["tk_corch_izq","expr_list_no_req", "tk_corch_der"],
#                  ["tk_par_izq","expr","tk_par_der"],["member_expr","cexpr_p9_aux"],
#                  ["index_expr"],["id","tk_par_izq","expr_list_no_req","tk_par_der"]],
#     "cexpr_p9_aux": [["tk_par_izq","expr_list_no_req","tk_par_der"],[""]],
#     "expr_list_no_req": [["expr","expr_list_0_more"],[""]],
#     "expr_list_0_more": [["tk_coma", "expr", "expr_list_0_more"],[""]],
#     "member_expr": [["cexpr","tk_punto","id"]],
#     "index_expr": [["cexpr","tk_corch_izq","expr","tk_corch_der"]],
#     "target":[["id"],["member_expr"],["index_expr"]]
# }

initial_symbol_grammar = "A"
not_terminals = ["A","B"]

grammar = {
    "A": [["B", "2"]],
    "B": [["A", "3"], [""]]
}


# not {expr}
# {expr} and {expr}
# {expr} or {expr}

pred_rules = {}

for k in grammar.keys():
    pred_rules[k] = []

def log(s, debug=0):
    if debug:
        print(s)


def PRIMEROS(alpha, debug=0):

    alpha = [alpha] if type(alpha) is str else alpha

    set_primeros = set()
    if alpha[0] == "":  # 1. Si alpha == epsilon
        set_primeros = set_primeros.union([""])
        log("Se agregó " + "epsilon" + " al conjunto de primeros\n", debug)
        return set_primeros

    if alpha[0] not in not_terminals:  # 2a. a_1 es un terminal

        set_primeros = set_primeros.union([alpha[0]])
        log("Se agregó " + alpha[0] + " al conjunto de primeros\n", debug)
        return set_primeros

    else:  # 2b. a_1 es un no terminal

        if alpha[0] != alpha[0]:

            log("Hacemos unión con: PRIMEROS(" + alpha[0] + ")", debug)
            set_primeros = set_primeros.union(PRIMEROS(alpha[0], debug))

            if "" in set_primeros:
                log(str(alpha) + str(set_primeros), debug)
                if len(alpha) == 1:
                    pass
                else:
                    log("Hacemos unión con: PRIMEROS(" + str(alpha[1:]) + ")", debug)

                    # ??????
                    try:
                        set_primeros.remove("")
                    except KeyError:
                        pass

                    set_primeros = set_primeros.union(PRIMEROS(alpha[1:], debug))

            return set_primeros

        else:
            log("alpha[0] != alpha", debug)
            log("\nSe encontró que " + alpha[0] + " es un no terminal, asi que revisaremos sus reglas", debug)
            for regla in grammar[alpha[0]]:
                log("Regla a desglosar: " + str(regla), debug)
                set_primeros = set_primeros.union(PRIMEROS(regla, debug))
            log("Después de Revisar las Reglas de " + alpha[0] + " Se encontró que sus PRIMEROS son: " + str(set_primeros), debug)
            pass

    return set_primeros


def SIGUIENTES(no_terminal):
    set_siguientes = set()
    if no_terminal == initial_symbol_grammar:
        set_siguientes = set_siguientes.union(set("$"))

    for nt, rules in grammar.items():
        for rule in rules:
            try:
                index = rule.index(no_terminal)
                if index == len(rule) - 1:
                    beta = ""
                # print(index, nt, rule)
                else:
                    beta = rule[index+1:]

                if type(beta) == str:
                    beta = [beta]
                primeros_beta = PRIMEROS(beta)
                set_siguientes = set_siguientes.union(primeros_beta)
                set_siguientes.remove("")
                #print(set_siguientes)
                # len(set_siguientes) no ha cambiado break
                if "" in primeros_beta or beta == "":
                    #tmp_len = len(set_siguientes)
                    if nt != no_terminal:  # Ni idea si sirve
                        set_siguientes = set_siguientes.union(SIGUIENTES(nt))
                    # if len(set_siguientes) == tmp_len:
                    #     break

            except ValueError:
                pass
            except KeyError:
                pass

    return set_siguientes


def PRED(no_terminal):

    for rule in grammar[no_terminal]:
        set_prediccion = set()
        primeros_alpha = PRIMEROS(rule)
       # print(rule)
        if "" in primeros_alpha:
            set_prediccion = set_prediccion.union(primeros_alpha)
            #print(set_prediccion, "Soy un Castor")
            set_prediccion.remove("")
            set_prediccion = set_prediccion.union(SIGUIENTES(no_terminal))
            #print("---")
        else:
            set_prediccion = set_prediccion.union(primeros_alpha)
            #print("----")

        lst_tmp = []
        for i in set_prediccion:
            lst_tmp.append(i)

        pred_rules[no_terminal].append(lst_tmp)

def main():
    # alpha = ["expr_p2"]  # Cadena de Símbolos Terminales y No terminales
    # debug = False
    for nt in not_terminals:
        print(nt)
        PRED(nt)

    print(pred_rules)

if __name__ == '__main__':
    main()
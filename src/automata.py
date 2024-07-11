from typing import List, Tuple, Dict

def load_automata(filename: str) -> Tuple[List[str], List[str], Dict[str, Dict[str, List[str]]], str, List[str]]:
    """
    Carrega um autômato a partir de um arquivo.

    :param filename: Nome do arquivo contendo a descrição do autômato.
    :return: Uma tupla contendo (Q, Sigma, delta, q0, F).
    """
    with open(filename, 'r') as file:
        lines = file.readlines()
        
        # Extração de Q, Sigma, q0, F e delta do arquivo
        Sigma = lines[0].strip().split()
        Q = lines[1].strip().split()
        F = lines[2].strip().split()
        q0 = lines[3].strip()
        
        delta = {}
        for line in lines[4:]:
            parts = line.strip().split()
            if len(parts) == 3:
                origin, symbol, destination = parts
                if origin not in delta:
                    delta[origin] = {}
                if symbol not in delta[origin]:
                    delta[origin][symbol] = []
                delta[origin][symbol].append(destination)
        
        return Q, Sigma, delta, q0, F

def process(automata: Tuple[List[str], List[str], Dict[str, Dict[str, List[str]]], str, List[str]], word: List[str]) -> Dict[str, str]:
    """
    Processa uma palavra através de um autômato.

    :param automata: Uma tupla contendo (Q, Sigma, delta, q0, F).
    :param word: Lista de símbolos da palavra a ser processada.
    :return: Um dicionário indicando se a palavra é aceita, rejeitada ou inválida.
    """
    Q, Sigma, delta, q0, F = automata
    
    current_states = {q0}
    for symbol in word:
        if symbol not in Sigma:
            return {"Resultado": "INVÁLIDA"}
        next_states = set()
        for state in current_states:
            if state in delta and symbol in delta[state]:
                next_states.update(delta[state][symbol])
        current_states = next_states
    
    if current_states & set(F):
        return {"Resultado": "ACEITA"}
    else:
        return {"Resultado": "REJEITA"}

def convert_to_dfa(automata: Tuple[List[str], List[str], Dict[str, Dict[str, List[str]]], str, List[str]]) -> Tuple[List[str], List[str], Dict[str, Dict[str, str]], str, List[str]]:
    """
    Converte um autômato não determinístico (NFA) para um autômato determinístico (DFA).

    :param automata: Uma tupla contendo (Q, Sigma, delta, q0, F).
    :return: Uma tupla contendo (Q, Sigma, delta, q0, F) do DFA.
    """
    from itertools import chain, combinations

    Q, Sigma, delta, q0, F = automata

    def powerset(iterable):
        "powerset([1,2,3]) --> [(), (1,), (2,), (3,), (1,2), (1,3), (2,3), (1,2,3)]"
        s = list(iterable)
        return list(chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))
    
    Q_dfa = list(map(lambda x: frozenset(x), powerset(Q)))
    q0_dfa = frozenset([q0])
    F_dfa = list(filter(lambda x: set(x) & set(F), Q_dfa))
    
    delta_dfa = {}
    for state in Q_dfa:
        for symbol in Sigma:
            next_state = frozenset(chain.from_iterable(delta[q][symbol] for q in state if q in delta and symbol in delta[q]))
            if state not in delta_dfa:
                delta_dfa[state] = {}
            delta_dfa[state][symbol] = next_state
    
    return Q_dfa, Sigma, delta_dfa, q0_dfa, F_dfa

if __name__ == "__main__":
    automata_file = "C:/Users/fcarr/Documents/automata2_content.txt"  # Caminho absoluto atualizado
    word = list("abba")

    automata = load_automata(automata_file)
    result = process(automata, word)
    print(result)

    dfa_automata = convert_to_dfa(automata)
    print(dfa_automata)

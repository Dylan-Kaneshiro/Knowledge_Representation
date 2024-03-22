import sys


def read_input(filename):
    f = open(filename, "r")
    return [line.rstrip() for line in f.readlines()]

def negate(literal):
  if literal[0] == '~':
    return literal[1:]
  else:
    return '~' + literal

def negate_clause(clause_string):
  return [[negate(literal)] for literal in clause_string.split(' ')]

def unique(items):
  return list(dict.fromkeys(items))

def always_true(clause):
  clause_set = set(clause)
  for i in clause_set:
    if negate(i) in clause_set:
      return True
  return False

def resolve(clause_1, clause_2):
  clause_2_set = set(clause_2)
  for literal in clause_1:
    if negate(literal) in clause_2_set:
      return unique([i for i in clause_1 if not i==literal] + [i for i in clause_2 if not i==negate(literal)])
  return None

def redundant(clause, kb):
  return any([set(clause) == set(prev_clause) for prev_clause in kb])

def create_kb(lines):
    kb = [unique(line.split(' ')) for line in lines[:-1]]
    kb = [clause for clause in kb if not always_true(clause)]
    kb += negate_clause(lines[-1])
    return kb

def print_kb(kb):
  for i, clause in enumerate(kb):
    print(i+1,'. ', sep='', end='')
    print(*clause, '{}')


def main(input_file):
    # Create initial knowledge base
    kb = create_kb(read_input(input_file))
    kb_set = {set(clause) for clause in kb}
    print_kb(kb)
    '''
    kb is 2D list.
    Each row is a clause.
    Each clause is a list of literals.

    e.g.
    [['~p', 'q'],
    ['~z', 'y'],
    ['~q', 'p'],
    ['q', '~p', 'z'],
    ['q', '~p', '~z'],
    ['z'],
    ['~y'],
    ['p']]
    '''

    ##### Try to find contradiction #####
    cur = 0 # current line (clause) of knowledge base
    result = None # the clause formed by resolving 2 clauses in the kb
    step=len(kb) # the outputted step number (for printing)
    valid=False # if a contradiction was found

    # Go through each line in the kb one by one
    while cur < len(kb):

        # try to resolve current line with previous lines
        for i in range(cur):
            result = resolve(kb[cur], kb[i])
            if result is not None and not always_true(result) and not redundant(result, kb):
                step+=1
                kb.append(result)

                # Print out added clause
                print(step,'. ', sep='', end='')
                if len(result) == 0: # Empty clause, contradiction found
                    print('Contradiction {', cur+1, ', ', i+1, '}', sep='')
                    valid=True
                    break
                print(*result, end='')
                print(' {', cur+1, ', ', i+1, '}', sep='')

        if result is not None and len(result) == 0: # Contradiction found, break loop
            break
        cur += 1

    if valid:
       print('Valid')

if __name__ == "__main__":
    input_file = sys.argv[1]
    main(input_file)
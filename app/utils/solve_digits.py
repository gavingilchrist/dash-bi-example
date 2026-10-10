import numpy as np
import pandas as pd


def solve_digits(digits, target):
    """
    Find all distinct ways to calculate target number from digits.
    Output in NYT and Nerdle targets format.
    """
    poss_nums = np.array([digits])
    calcs = {}
    endpts = []
    while (x:=poss_nums.shape[1]-1):
        poss_nums, calcs[poss_nums.shape[1]] = get_poss(poss_nums)
        endpts += [' '.join(i) 
                   for i in poss_nums[np.any(poss_nums == target, 
                                             axis=1)]
                   .astype(str).tolist()]
    if endpts:
        solutions = expand_solutions(endpts, calcs)
        return (pd.DataFrame({'solutions': 
                              [get_nyt_format(expr) 
                              for expr in solutions]}),
                pd.DataFrame({'solutions': 
                              [get_nerdle_format(expr) 
                              for expr in solutions]}))
    return [pd.DataFrame({'solutions': ['NO SOLUTIONS']}) for i in '01'] 


def get_poss(poss_nums):
    """ 
    Generate all possible combinations of two values using +,-,* or / operator,
    filtering out div/0, non-integer and negative results.
    """
    calcs = {}
    new_poss_nums = np.unique(np.concat([get_op_poss(poss_nums, i, calcs) 
                                         for i in '+-*/']),
                              axis=0)
    return new_poss_nums, calcs


def get_op_poss(poss_nums, op, calcs):
    """ 
    Generate all possible combinations of two values using specified operator,
    filtering out div/0, no-effect operations, non-integer and non-positive results.
    """
    # Indices for all relevant pairs
    h,w = poss_nums.shape
    if op in '+*':
        pair_ix = [[i, j] for i in range(w-1) for j in range(i+1, w)]
    else:
        pair_ix = [[i, j] for i in range(w) for j in range(w) if i != j]
    rem_ix = [sorted([*{*range(w)}-{*i}]) for i in pair_ix]
    
    rix = np.repeat(np.arange(h), len(pair_ix))
    cix_pair = np.tile(pair_ix, (h,1))
    cix_rem = np.tile(np.array(rem_ix, dtype=int), (h,1))
    
    # Calculation and result for each combined pair
    f = {'+': np.add, '-': np.subtract, '*': np.multiply, '/': np.divide}[op]
    num_pairs = [poss_nums[rix, cix_pair[:,i]] for i in [0,1]]
    with np.errstate(divide='ignore'):
        combined_nums = f(*num_pairs)
    combined_nums = np.where((z:=np.nan_to_num(combined_nums, posinf=-1)) % 1, 
                             -1, z).astype(int)
    
    # Filter out invalid results, no-effect operations
    filt = ((combined_nums > 0)
            & (~((op in('*/')) & (num_pairs[1] == 1)))
            & (~((op == '*') & (num_pairs[0] == 1))))
    combined_nums = combined_nums[filt]
    expr_pairs = [(z:=poss_nums[rix[filt], cix_pair[filt,i]])
                      .astype(str)
                  for i in [0,1]]
    combined_expr = np_concat_txt(['(', expr_pairs[0], op, expr_pairs[1], ')'])
    
    rem_nums = poss_nums[np.expand_dims(rix[filt], 1), cix_rem[filt]]
        
    # Add calculation details to calcs dict
    for j,k,l in zip(*[i.tolist() for i in [combined_nums, combined_expr, rem_nums]]):
        if (m:=(str(j), ' '.join(sorted([str(n) for n in l])))) in calcs:
            calcs[m].add(k)
        else:
            calcs[m] = {k}
            
    # Return updated poss array
    return np.unique(np.sort(np.column_stack((combined_nums, rem_nums)), 
                             axis=1),
                     axis=0)
    
    
def np_concat_txt(arr):
    """
    Concatenate text from list of arrays.
    """
    return (np.char.add(arr[0], np_concat_txt(arr[1:])) if len(arr)>1 
            else arr[0])
    
    
def expand_solutions(endpts, calcs):
    """
    Use calcs dictionaries to trace back all routes to target from input numbers;
    return list of solution expressions with simple deduping.
    """
    solutions = {(-len(soln.split()), 
                  [i for i in soln.split() if not i.isnumeric()][0][1:-1])
                 for calctxt in endpts
                 for soln in expand_solutions_inner(calctxt, calcs)
                 if sum([not i.isnumeric() for i in soln.split()])==1}
    return [*[*zip(*sorted({(i,transform_soln(j)) 
                            for i,j in solutions}))][1]]
    
    
def expand_solutions_inner(calctxt, calcs):
    """
    Recursive inner function for expanding list of solutions.
    """
    numix = get_numix(calctxt)
    if (cd:=len(numix)) in calcs:
        return [p
                for i,j in enumerate(numix)
                for m in calcs[cd].get(tuple([calctxt[slice(*j)], 
                                              ' '.join(sorted([calctxt[slice(*l)] 
                                                               for k,l in enumerate(numix) 
                                                               if k != i]))]),
                                       [])
                for p in expand_solutions_inner(f'{calctxt[:j[0]]}{m}{calctxt[j[1]:]}',
                                                calcs)]
    else:
        return [calctxt]
    
    
def get_numix(calctxt):
    """
    Return start and end indices for numbers in calctxt.
    """
    return [*zip((z:=[j 
                      for nn in[[47<ord(i)<58 for i in calctxt]]
                      for j,(k,l) in enumerate(zip([*nn, False], 
                                                   [False, *nn])) 
                      if l^k])[::2],
                 z[1::2])]


def transform_soln(*args):
    """
    Remove parentheses, reorder terms, remove redundant ops to eliminate duplicate solutions
    """
    op, expr = args[:2] if len(args)>1 else ['?',*args]
    
    pdepth = get_pdepth(expr)
    if min(pdepth):
        expr = expr[1:-1]
        pdepth = [i-1 for i in pdepth[1:-1]]
    split_ix = [i for i,j in enumerate(expr) if pdepth[i]==0 and j in '+-*/']
    if split_ix:
        expr_split = [[[expr[i],'?'][i<0], expr[i+1:j]]
                      for i,j in zip([-1,*split_ix],[*split_ix,None])]
        expr_split[0][0] = (eop:={'-':'+', '/':'*'}.get((z:=expr_split[1][0]), z))
        expr2 = [j for i in expr_split for j in transform_soln(*i)]
        if op == '?':
            return ''.join(sum(sorted(expr2),[]))[1:]
        elif (op in '+-')^(eop in '+-'):
            return [[op, f"({''.join(sum(sorted(expr2),[]))[1:]})"]]
        elif op == '-':
            return sorted([[{'+':'-', '-':'+'}.get(i,i),j] for i,j in expr2])
        elif op == '/':
            return sorted([[{'*':'/', '/':'*'}.get(i,i),j] for i,j in expr2])
        else:
            return sorted(expr2)
    else:
        return [[op, expr]]
    
    
def get_pdepth(expr):
    """
    Check expression has balanced opening and closing parenthesis, and return
    parenthesis depth numbers in corresponding list.
    """
    assert expr.count('(')==expr.count(')')
    return [((z:=(z if i else 0)+{'(':1,')':-1}.get(j,0))+(j==')'))
            for i,j in enumerate(expr)]
    

def get_nyt_format(expr):
    """
    Format raw solutions in format used by NYT Digits
    """
    expr = f'({expr})'
    steps = []
    while not expr[1:-1].isnumeric():
        p = get_pdepth(expr)+[0]
        bs = p.index(m:=max(p))
        be = p.index(m-1,bs) if m-1 in p[bs:] else len(p)
        bks = [i 
               for i,j in enumerate(expr) 
               if p[i]==m and not(47<ord(j)<58) and bs<=i<be]
        if len(bks)<=2:
            expr = f'{expr[:bks[0]]}{expr[slice(*bks)][1:]}{expr[bks[1]:][1:]}'
        else:
            steps += [f'{(z:=expr[bks[0]+1:bks[2]])}={int(eval(z))}']
            expr = f'{expr[:bks[0]+1]}{int(eval(z))}{expr[bks[2]:]}'
            
    return f' {chr(8226)} '.join(steps)


def get_nerdle_format(expr):
    """
    Format raw solutions in format used by Nerdle Targets.
    (Remove parentheses made unnecessary by order of ops rules.)
    """
    p = get_pdepth(expr)+[0]
    target = int(eval(expr))
    for _,s,e in sorted([[-p[i],i,p.index(p[i]-1,i+1)-1] 
                         for i,j in enumerate(expr) if j=='(']):
        if int(eval(z:=f'{expr[:s]} {expr[s+1:e]} {expr[e+1:]}')) == target:
            expr = z
    return expr.replace(' ','')

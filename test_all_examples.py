# -*- coding: utf-8 -*-
"""Test completo: verifica tutti gli esempi delle dispense (6 esempi)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from fractions import Fraction
import numpy as np

# -------------------------------------------------------------------
# Motore Simplex con aritmetica esatta (Fraction) per confronto passo-passo
# -------------------------------------------------------------------
def fr(v):
    if isinstance(v, Fraction): return v
    return Fraction(v).limit_denominator(10**9)

def pivot_frac(M, k, h):
    M = [row[:] for row in M]
    m, ncols = len(M), len(M[0])
    piv = M[k][h]
    M[k] = [x / piv for x in M[k]]
    for i in range(m):
        if i == k: continue
        f = M[i][h]
        M[i] = [M[i][j] - f * M[k][j] for j in range(ncols)]
    return M

def simplex_fractions(c_in, A_in, b_in):
    """Two-phase simplex with Fraction arithmetic. Returns (stato, x, z, steps)."""
    m = len(A_in)
    n = len(c_in)
    c = [fr(v) for v in c_in]
    A = [[fr(v) for v in row] for row in A_in]
    b = [fr(v) for v in b_in]
    steps = []

    # forza b >= 0
    for i in range(m):
        if b[i] < 0:
            b[i] = -b[i]
            A[i] = [-v for v in A[i]]

    c_aux = [Fraction(0)] * n + [Fraction(1)] * m
    IB = list(range(n+1, n+m+1))
    IN = list(range(1, n+1))
    BinvN = [row[:] for row in A]
    Binvb = b[:]

    def run_phase(BinvN, Binvb, cB, cN, IB, IN, c_full, label):
        BinvN = [row[:] for row in BinvN]
        Binvb = Binvb[:]
        cB = cB[:]
        cN = cN[:]
        IB = IB[:]
        IN = IN[:]
        iters = []
        for _ in range(100):
            m_cur = len(IB)
            def calc_gamma(BinvN, cB, cN, m_c=m_cur):
                return [cN[h] - sum(cB[i]*BinvN[i][h] for i in range(m_c)) for h in range(len(cN))]
            gamma = calc_gamma(BinvN, cB, cN)
            if all(g >= 0 for g in gamma):
                n_tot = max(max(IB), max(IN)) if IN else max(IB)
                x = [Fraction(0)] * n_tot
                for i, j in enumerate(IB):
                    if Binvb[i] > 0:
                        x[j-1] = Binvb[i]
                z = sum(cB[i]*Binvb[i] for i in range(len(IB)))
                iters.append({'tipo': 'ottimo', 'IB': IB[:], 'IN': IN[:],
                              'gamma': gamma[:], 'Binvb': Binvb[:]})
                return 'ottimo', BinvN, Binvb, cB, cN, IB, IN, x, z, iters
            # illimitatezza
            for h in range(len(IN)):
                if gamma[h] < 0:
                    col = [BinvN[i][h] for i in range(len(IB))]
                    if all(v <= 0 for v in col):
                        return 'illimitato', None,None,None,None,None,None,None,None,iters
            # entrante: gamma minimo
            h_entr = min(range(len(gamma)), key=lambda i: gamma[i])
            pi_h = [BinvN[i][h_entr] for i in range(len(IB))]
            ratios = [(Binvb[i]/pi_h[i], i) for i in range(len(IB)) if pi_h[i] > 0]
            _, k = min(ratios)
            iters.append({'tipo': 'iter', 'IB': IB[:], 'IN': IN[:],
                          'gamma': gamma[:], 'Binvb': Binvb[:],
                          'h': h_entr, 'k': k, 'entrante': IN[h_entr], 'uscente': IB[k]})
            aug = [BinvN[i][:] + [Binvb[i]] for i in range(len(IB))]
            aug = pivot_frac(aug, k, h_entr)
            BinvN = [row[:-1] for row in aug]
            Binvb = [row[-1] for row in aug]
            IB[k] = iters[-1]['entrante']
            IN[h_entr] = iters[-1]['uscente']
            cB = [c_full[j-1] for j in IB]
            cN = [c_full[j-1] for j in IN]
        return 'errore',None,None,None,None,None,None,None,None,iters

    cB = [c_aux[j-1] for j in IB]
    cN = [c_aux[j-1] for j in IN]
    stato1, BinvN1, Binvb1, cB1, cN1, IB1, IN1, x1, z1, s1 = \
        run_phase(BinvN, Binvb, cB, cN, IB, IN, c_aux, "Fase I")
    steps.extend(s1)

    if stato1 != 'ottimo':
        return 'errore', None, None, steps
    if z1 != 0:
        return 'inammissibile', None, None, steps

    # Rimuovi artificiali
    IB, IN, BinvN, Binvb = IB1[:], IN1[:], BinvN1, Binvb1
    art_in_base = [j for j in IB if j > n]
    for j_art in art_in_base:
        k = IB.index(j_art)
        swapped = False
        for h_idx, j_orig in enumerate(IN):
            if j_orig <= n and BinvN[k][h_idx] != 0:
                aug = [BinvN[i][:] + [Binvb[i]] for i in range(len(IB))]
                aug = pivot_frac(aug, k, h_idx)
                BinvN = [row[:-1] for row in aug]
                Binvb = [row[-1] for row in aug]
                IB[k] = j_orig; IN[h_idx] = j_art
                swapped = True; break
        if not swapped:
            BinvN.pop(k); Binvb.pop(k); IB.pop(k)

    keep = [i for i, j in enumerate(IN) if j <= n]
    IN = [IN[i] for i in keep]
    BinvN = [[row[i] for i in keep] for row in BinvN]
    cB = [c[j-1] for j in IB]
    cN = [c[j-1] for j in IN]
    stato2, BinvN2, Binvb2, cB2, cN2, IB2, IN2, x2, z2, s2 = \
        run_phase(BinvN, Binvb, cB, cN, IB, IN, c, "Fase II")
    steps.extend(s2)

    if stato2 == 'illimitato':
        return 'illimitato', None, None, steps
    return 'ottimo', x2, z2, steps


# -------------------------------------------------------------------
# Test cases
# -------------------------------------------------------------------
tests = [
    {
        'nome': 'Esempio 6.4.11 (Fase II diretta)',
        'c': [1,2,1,1,1,1],
        'A': [[1,2,3,1,0,0],[2,-1,-5,0,1,0],[1,2,-1,0,0,1]],
        'b': [3,2,1],
        'ex_stato': 'ottimo',
        'ex_x': [Fraction(1),Fraction(0),Fraction(0),Fraction(2),Fraction(0),Fraction(0)],
        'ex_z': Fraction(3),
    },
    {
        'nome': 'Esempio 6.4.13 (Fase II, base iniziale diversa)',
        'c': [3,2,1,1],
        'A': [[1,0,-1,2],[0,1,2,-1]],
        'b': [5,3],
        'ex_stato': 'ottimo',
        'ex_x': [Fraction(0),Fraction(0),Fraction(11,3),Fraction(13,3)],
        'ex_z': Fraction(8),
    },
    {
        'nome': 'Esempio 6.4.4 (Illimitato)',
        'c': [-1,-1,0,0],
        'A': [[1,-1,1,0],[-1,1,0,1]],
        'b': [1,1],
        'ex_stato': 'illimitato',
    },
    {
        'nome': 'Esempio 6.5.2 (Fase I + Fase II)',
        'c': [2,3,1],
        'A': [[1,1,1],[-1,2,0],[0,3,1]],
        'b': [2,1,3],
        'ex_stato': 'ottimo',
        'ex_x': [Fraction(0),Fraction(1,2),Fraction(3,2)],
        'ex_z': Fraction(3),
    },
    {
        'nome': 'Esempio 6.5.3 (Fase I + Fase II, degenere)',
        'c': [-4,-1,-1],
        'A': [[2,1,2],[3,3,1]],
        'b': [4,3],
        'ex_stato': 'ottimo',
        'ex_x': [Fraction(1,2),Fraction(0),Fraction(3,2)],
        'ex_z': Fraction(-7,2),
    },
    {
        'nome': 'Esempio 6.5.4 (Inammissibile)',
        'c': [1,1,0,0],
        'A': [[1,-2,-1,0],[-1,1,0,-1]],
        'b': [1,1],
        'ex_stato': 'inammissibile',
    },
]

print("=" * 65)
print("  TEST COMPLETO - Tutti gli esempi delle dispense")
print("=" * 65)

all_ok = True
for t in tests:
    stato, x, z, steps = simplex_fractions(t['c'], t['A'], t['b'])
    ok = True
    msgs = []

    if stato != t['ex_stato']:
        ok = False
        msgs.append(f"stato={stato}, atteso={t['ex_stato']}")

    if t['ex_stato'] == 'ottimo' and stato == 'ottimo':
        for i, (got, exp) in enumerate(zip(x, t['ex_x'])):
            if got != exp:
                ok = False
                msgs.append(f"x[{i+1}]={got} atteso={exp}")
        if z != t['ex_z']:
            ok = False
            msgs.append(f"z={z} atteso={t['ex_z']}")

    # Conta iterazioni
    n_pivot = sum(1 for s in steps if s.get('tipo') == 'iter')

    tag = "[OK]  " if ok else "[FAIL]"
    print(f"{tag} {t['nome']}")
    if t['ex_stato'] == 'ottimo' and stato == 'ottimo':
        print(f"       x* = {[str(v) for v in x]}")
        print(f"       z* = {z}   |   pivot totali = {n_pivot}")
    else:
        print(f"       stato = {stato}   |   pivot totali = {n_pivot}")
    if msgs:
        for m in msgs: print(f"       ERRORE: {m}")
    all_ok = all_ok and ok
    print()

print("=" * 65)
print("RISULTATO:", "TUTTI E 6 SUPERATI" if all_ok else "ALCUNI FALLITI")
print("=" * 65)

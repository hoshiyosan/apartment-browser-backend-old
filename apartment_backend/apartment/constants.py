
prix_electricite_par_kwh = 0.1765

conso_kwhm2an_par_classe_energetique = {
    'A': 50,
    'B': 70,
    'C': 120,
    'D': 190,
    'E': 280,
    'F': 390,
    'G': 450
}

classe_energetique_par_conso_kwhm2an = {
    (0,50): 'A',
    (51,90): 'B',
    (91, 150): 'C',
    (151,230): 'D',
    (231,330): 'E',
    (331, 450): 'F',
    (450, 1000): 'G'
}

__all__ = (
    'prix_electricite_par_kwh',
    'conso_kwhm2an_par_classe_energetique',
    'classe_energetique_par_conso_kwhm2an'
)
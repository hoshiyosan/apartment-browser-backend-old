from .constants import (
    prix_electricite_par_kwh,
    conso_kwhm2an_par_classe_energetique
)

def facture_electricite(*, surface_m2, duree_annees, classe_energetique):
    conso_annuelle = conso_kwhm2an_par_classe_energetique[classe_energetique] * surface_m2
    return int(conso_annuelle * prix_electricite_par_kwh * duree_annees)

if __name__ == '__main__':
    surface_m2 = 40
    
    for classe_energetique in 'ABCDEFG':
        print('cout mensuel:', facture_electricite(surface_m2=surface_m2, duree_annees=1/12, classe_energetique=classe_energetique))
        print('cout annuel:', facture_electricite(surface_m2=surface_m2, duree_annees=1, classe_energetique=classe_energetique))
        print('cout 25 ans:', facture_electricite(surface_m2=surface_m2, duree_annees=25, classe_energetique=classe_energetique))
        print('='*80)

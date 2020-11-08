from .factures import facture_electricite
from .constants import classe_energetique_par_conso_kwhm2an, conso_kwhm2an_par_classe_energetique


class Apartment:
    def __init__(self, *, prix_euros, surface_m2, nombre_pieces, classe_energetique=None, conso_energetique=None, charges_annuelles=0, **other_infos):
        self.prix_euros = prix_euros
        self.surface_m2 = surface_m2
        self.nombre_pieces = nombre_pieces

        self.set_consommation_energetique(classe_energetique=classe_energetique, conso_energetique=conso_energetique)
        self.charges_annuelles = charges_annuelles

        self.other_infos = other_infos

    def set_consommation_energetique(self, classe_energetique=None, conso_energetique=None):
        assert classe_energetique is not None or conso_energetique is not None, \
                "classe_energetique ou conso_energetique doit etre fourni..."
        
        if classe_energetique:
            self.classe_energetique = classe_energetique
        else:
            for (mini, maxi), classe in classe_energetique_par_conso_kwhm2an.items():
                if conso_energetique >= mini and conso_energetique <= maxi:
                    self.classe_energetique = classe
                    break

        if conso_energetique:
            self.conso_energetique = conso_energetique
        else:
            self.conso_energetique = conso_kwhm2an_par_classe_energetique[classe_energetique]

    @property
    def frais_notaire(self):
        return 0.08 * self.prix_euros

    @property
    def duree_remboursement(self):
        # TODO: compute duration depending on credit, depending on price
        return 25

    @property
    def facture_electricite_totale(self):
        return facture_electricite(
            surface_m2=self.surface_m2, 
            duree_annees=self.duree_remboursement, 
            classe_energetique=self.classe_energetique)

    @property
    def autres_charges_totales(self):
        return self.duree_remboursement * self.charges_annuelles

    @property
    def cout_total(self):
        return self.prix_euros                      \
                + self.facture_electricite_totale   \
                + self.autres_charges_totales       \
                + self.frais_notaire

    def dump(self):
        return {
            'prix_euros': self.prix_euros,
            'surface_m2': self.surface_m2,
            'nombre_pieces': self.nombre_pieces,
            'classe_energetique': self.classe_energetique,
            'conso_energetique': self.conso_energetique,
            'duree_remboursement': self.duree_remboursement,
            'couts': [
                {'name': 'Electricite', 'value': self.facture_electricite_totale},
                {'name': 'Autre charges', 'value': self.autres_charges_totales},
                {'name': 'Fraise de notaire', 'value': self.frais_notaire},
                {'name': 'Cout total', 'value': self.cout_total}
            ],
            'bonus': self.other_infos
        }

    def __str__(self):
        return f"""
        == Caracteristiques ==================
        prix:       {self.prix_euros} €
        surface:    {self.surface_m2} m²
        pieces:     {self.nombre_pieces}
        classe:     {self.classe_energetique}
        prêt:       {self.duree_remboursement} ans

        == Factures sur {self.duree_remboursement} ans ===============
        elec:       {self.facture_electricite_totale} €
        charges:    {self.autres_charges_totales} €
        notaire:    {self.frais_notaire} €
        total:      {self.cout_total} €
        """
        
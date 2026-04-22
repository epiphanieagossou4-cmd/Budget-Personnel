"""
Module : services/rapport.py
Génération de rapports texte et export de données
Bloc 3 — Architecture POO
"""

from typing import Optional
from models.budget import Budget


class GenerateurRapport:
    """
    Produit des rapports lisibles depuis un objet Budget.
    Démontre la séparation des responsabilités (SRP).
    """

    LIGNE = "─" * 60

    def __init__(self, budget: Budget):
        self._budget = budget

    def rapport_mensuel(self, mois: str) -> str:
        resume = self._budget.resume(mois)
        depenses_cat = self._budget.depenses_par_categorie(mois)
        alertes = self._budget.alertes_depassement(mois)
        top5 = self._budget.top_depenses(5, mois)
        evol = self._budget.evolution_mensuelle()

        lignes = [
            "",
            f"{'═'*60}",
            f"  RAPPORT BUDGET — {mois}",
            f"{'═'*60}",
            "",
            "  RÉSUMÉ",
            self.LIGNE,
            f"  Transactions    : {resume['nb_transactions']}",
            f"  Total dépenses  : {resume['total_debits']:>12.2f} FCFA",
            f"  Total revenus   : {resume['total_credits']:>12.2f} FCFA",
            f"  Solde global    : {self._budget.solde_total():>12.2f} FCFA",
            f"  Taux d'épargne  : {resume['taux_epargne']:>11.1f} %",
            "",
            "  DÉPENSES PAR CATÉGORIE",
            self.LIGNE,
        ]
        total_dep = resume['total_debits'] or 1
        for cat, montant in depenses_cat.items():
            pct = montant / total_dep * 100
            bar = "█" * int(pct / 5)
            lignes.append(f"  {cat:<18} {montant:>10.2f} FCFA  {pct:5.1f}% {bar}")

        if top5:
            lignes += ["", "  TOP 5 DÉPENSES", self.LIGNE]
            for i, t in enumerate(top5, 1):
                lignes.append(f"  {i}. {t.date_str} | {t.montant:>10.2f} FCFA | {t.description[:30]}")

        if alertes:
            lignes += ["", "  ⚠ ALERTES DÉPASSEMENT BUDGET", self.LIGNE]
            for a in alertes:
                lignes.append(
                    f"  {a['categorie']:<18} {a['depense']:>10.2f} / "
                    f"{a['budget']:.2f} FCFA  ({a['pourcent']:.0f}%)"
                )

        lignes += ["", f"{'═'*60}", ""]
        return "\n".join(lignes)

    def rapport_complet(self) -> str:
        evol = self._budget.evolution_mensuelle()
        lignes = [
            "",
            f"{'═'*60}",
            f"  RAPPORT COMPLET — {self._budget.nom}",
            f"{'═'*60}",
            f"  Transactions totales : {len(self._budget)}",
            f"  Solde global         : {self._budget.solde_total():.2f} FCFA",
            f"  Moyenne mens. dépenses: {self._budget.moyenne_depenses_mensuelles():.2f} FCFA",
            "",
            "  ÉVOLUTION MENSUELLE",
            self.LIGNE,
            f"  {'Mois':<10} {'Dépenses':>12} {'Revenus':>12} {'Solde':>12}",
            self.LIGNE,
        ]
        for mois, d in evol.items():
            lignes.append(
                f"  {mois:<10} {d['debits']:>12.2f} {d['credits']:>12.2f} {d['solde']:>12.2f}"
            )
        lignes += ["", f"{'═'*60}", ""]
        return "\n".join(lignes)

    def exporter_json(self, mois: str = None) -> dict:
        """Export dict compatible JSON pour l'interface web."""
        evol = self._budget.evolution_mensuelle()
        mois_liste = sorted(evol.keys())
        dernier_mois = mois_liste[-1] if mois_liste else None
        m = mois or dernier_mois

        return {
            "budget_nom":    self._budget.nom,
            "solde":         self._budget.solde_total(),
            "total_debits":  self._budget.total_debits(),
            "total_credits": self._budget.total_credits(),
            "taux_epargne":  self._budget.taux_epargne(m),
            "nb_transactions": len(self._budget),
            "depenses_par_categorie": self._budget.depenses_par_categorie(m),
            "evolution_mensuelle": evol,
            "top_depenses": [
                {"date": t.date_str, "montant": t.montant,
                 "description": t.description, "categorie": t.categorie}
                for t in self._budget.top_depenses(10)
            ],
            "alertes": self._budget.alertes_depassement(m) if m else [],
            "transactions": [t.vers_dict() for t in self._budget],
        }

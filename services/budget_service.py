"""
Module  : services/budget_service.py
Bloc 4  — Persistance CSV
"""

import os
import csv
from typing import List, Dict

from models.budget import Budget
from models.transaction import Transaction
from services.csv_handler import CSVHandler


class BudgetService:

    DOSSIER_DONNEES = "data"
    FICHIER_TRANSACTIONS = "transactions.csv"
    FICHIER_RAPPORT = "rapport_mensuel.csv"

    def __init__(self, nom_budget: str = "Mon Budget", dossier: str = None):
        self._dossier = dossier or self.DOSSIER_DONNEES
        chemin_csv = os.path.join(self._dossier, self.FICHIER_TRANSACTIONS)
        self._budget = Budget(nom_budget)
        self._handler = CSVHandler(chemin_csv)
        self._charger_depuis_csv()

    @property
    def budget(self):
        return self._budget

    def _charger_depuis_csv(self):
        transactions = self._handler.lire_transactions()
        for t in transactions:
            self._budget.ajouter_transaction(t, auto_categoriser=False)
        if transactions:
            self._budget._prochain_id = max(
                t.id for t in transactions if t.id
            ) + 1
        return len(transactions)

    def sauvegarder(self):
        return self._handler.ecrire_transactions(self._budget.transactions)

    def ajouter_transaction(self, montant, description, date,
                            type_t="débit", categorie="Non catégorisé"):
        t = Transaction(
            montant=montant,
            description=description,
            date=date,
            type_transaction=type_t,
            categorie=categorie,
        )
        self._budget.ajouter_transaction(t, auto_categoriser=True)
        self._handler.ajouter_transaction(t)
        return t

    def supprimer_transaction(self, id_transaction):
        supprime = self._budget.supprimer_transaction(id_transaction)
        if supprime:
            self.sauvegarder()
        return supprime

    def modifier_categorie(self, id_transaction, nouvelle_cat):
        t = self._budget.trouver_par_id(id_transaction)
        if t:
            t.categorie = nouvelle_cat
            self.sauvegarder()
            return True
        return False

    def exporter_rapport_csv(self, mois=None, chemin=None):
        chemin = chemin or os.path.join(self._dossier, self.FICHIER_RAPPORT)
        os.makedirs(self._dossier, exist_ok=True)

        resume = self._budget.resume(mois)
        depenses_cat = self._budget.depenses_par_categorie(mois)
        alertes = self._budget.alertes_depassement(mois) if mois else []
        top5 = self._budget.top_depenses(5, mois)

        with open(chemin, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)

            w.writerow(["=== RÉSUMÉ ==="])
            w.writerow(["Budget", resume["nom"]])
            w.writerow(["Mois", resume["mois"]])
            w.writerow(["Nb transactions", resume["nb_transactions"]])
            w.writerow(["Total dépenses (FCFA)", resume["total_debits"]])
            w.writerow(["Total revenus (FCFA)", resume["total_credits"]])
            w.writerow(["Solde (FCFA)", resume["solde"]])
            w.writerow(["Taux épargne (%)", resume["taux_epargne"]])
            w.writerow([])

            w.writerow(["=== DÉPENSES PAR CATÉGORIE ==="])
            w.writerow(["Catégorie", "Montant (FCFA)", "% du total"])
            total_dep = resume["total_debits"] or 1
            for cat, montant in depenses_cat.items():
                pct = round(montant / total_dep * 100, 1)
                w.writerow([cat, round(montant, 2), pct])
            w.writerow([])

            w.writerow(["=== TOP 5 DÉPENSES ==="])
            w.writerow(["Rang", "Date", "Montant (FCFA)", "Catégorie", "Description"])
            for i, t in enumerate(top5, 1):
                w.writerow([i, t.date_str, t.montant, t.categorie, t.description])
            w.writerow([])

            if alertes:
                w.writerow(["=== ALERTES DÉPASSEMENT BUDGET ==="])
                w.writerow(["Catégorie", "Dépense", "Budget", "Dépassement", "%"])
                for a in alertes:
                    w.writerow([a["categorie"], a["depense"],
                                 a["budget"], a["depassement"], a["pourcent"]])
                w.writerow([])

            w.writerow(["=== DÉTAIL DES TRANSACTIONS ==="])
            w.writerow(["ID", "Date", "Montant", "Type", "Catégorie", "Description"])
            source = (self._budget.filtrer_par_mois(mois)
                      if mois else self._budget.transactions)
            for t in source:
                w.writerow([t.id, t.date_str, t.montant,
                             t.type_transaction, t.categorie, t.description])

        return chemin

    def solde(self):
        return self._budget.solde_total()

    def resume(self, mois=None):
        return self._budget.resume(mois)

    def transactions(self, mois=None):
        return (self._budget.filtrer_par_mois(mois)
                if mois else self._budget.transactions)

    def alertes(self, mois):
        return self._budget.alertes_depassement(mois)

    def __repr__(self):
        return (f"BudgetService(budget='{self._budget.nom}', "
                f"transactions={len(self._budget)})")
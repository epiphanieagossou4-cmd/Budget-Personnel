from typing import List, Dict, Optional
from collections import defaultdict
from models.transaction import Transaction
from models.categorie import CategoriseurAuto


class Budget:
    """
    Gestionnaire central du budget.
    Agrège des transactions, calcule soldes, statistiques, alertes.
    Démontre : agrégation, itérateurs, algorithmes de synthèse.
    """

    def __init__(self, nom: str = "Mon Budget"):
        self._nom = nom
        self._transactions: List[Transaction] = []
        self._catalogue = CategoriseurAuto.creer_catalogue_defaut()
        self._prochain_id = 1

    # ── Propriétés ──────────────────────────────────────────────────────────

    @property
    def nom(self):
        return self._nom

    @property
    def transactions(self):
        return list(self._transactions)

    @property
    def nombre_transactions(self):
        return len(self._transactions)

    # ── Gestion des transactions ─────────────────────────────────────────────

    def ajouter_transaction(self, transaction: Transaction,
                            auto_categoriser: bool = True) -> Transaction:
        """Ajoute une transaction et l'auto-catégorise si demandé."""
        if transaction.id is None:
            transaction._id = self._prochain_id
            self._prochain_id += 1

        if auto_categoriser and transaction.categorie == "Non catégorisé":
            cat = CategoriseurAuto.categoriser(
                transaction.description, self._catalogue
            )
            transaction.categorie = cat

        self._transactions.append(transaction)
        return transaction

    def supprimer_transaction(self, id_transaction: int) -> bool:
        """Supprime une transaction par son ID. Retourne True si trouvée."""
        for i, t in enumerate(self._transactions):
            if t.id == id_transaction:
                self._transactions.pop(i)
                return True
        return False

    def trouver_par_id(self, id_transaction: int) -> Optional[Transaction]:
        for t in self._transactions:
            if t.id == id_transaction:
                return t
        return None

    # ── Filtres ──────────────────────────────────────────────────────────────

    def filtrer_par_mois(self, mois: str) -> List[Transaction]:
        """Filtre par mois (format 'YYYY-MM')."""
        return [t for t in self._transactions if t.mois == mois]

    def filtrer_par_categorie(self, categorie: str) -> List[Transaction]:
        return [t for t in self._transactions
                if t.categorie.lower() == categorie.lower()]

    def filtrer_par_type(self, type_t: str) -> List[Transaction]:
        return [t for t in self._transactions if t.type_transaction == type_t]

    # ── Calculs algorithmiques ───────────────────────────────────────────────

    def solde_total(self) -> float:
        """Calcul du solde : somme des montants signés."""
        return round(sum(t.montant_signe for t in self._transactions), 2)

    def total_debits(self) -> float:
        return round(sum(t.montant for t in self._transactions
                         if t.type_transaction == "débit"), 2)

    def total_credits(self) -> float:
        return round(sum(t.montant for t in self._transactions
                         if t.type_transaction == "crédit"), 2)

    def depenses_par_categorie(self,
                               mois: str = None) -> Dict[str, float]:
        """Agrège les dépenses (débits) par catégorie, avec filtre mois optionnel."""
        source = self.filtrer_par_mois(mois) if mois else self._transactions
        totaux = defaultdict(float)
        for t in source:
            if t.type_transaction == "débit":
                totaux[t.categorie] += t.montant
        return dict(sorted(totaux.items(), key=lambda x: x[1], reverse=True))

    def evolution_mensuelle(self) -> Dict[str, Dict]:
        """Retourne l'évolution par mois : débits, crédits, solde."""
        mois_data = defaultdict(lambda: {"debits": 0.0, "credits": 0.0})
        for t in sorted(self._transactions, key=lambda x: x.date):
            m = t.mois
            if t.type_transaction == "débit":
                mois_data[m]["debits"] += t.montant
            else:
                mois_data[m]["credits"] += t.montant
        # Ajouter le solde calculé
        for m, d in mois_data.items():
            d["solde"] = round(d["credits"] - d["debits"], 2)
            d["debits"] = round(d["debits"], 2)
            d["credits"] = round(d["credits"], 2)
        return dict(sorted(mois_data.items()))

    def top_depenses(self, n: int = 5,
                     mois: str = None) -> List[Transaction]:
        """Retourne les N plus grandes dépenses."""
        source = self.filtrer_par_mois(mois) if mois else self._transactions
        debits = [t for t in source if t.type_transaction == "débit"]
        return sorted(debits, key=lambda t: t.montant, reverse=True)[:n]

    def moyenne_depenses_mensuelles(self) -> float:
        """Moyenne des dépenses sur tous les mois."""
        evol = self.evolution_mensuelle()
        if not evol:
            return 0.0
        total = sum(d["debits"] for d in evol.values())
        return round(total / len(evol), 2)

    def taux_epargne(self, mois: str = None) -> float:
        """Taux d'épargne = (revenus - dépenses) / revenus * 100."""
        source = self.filtrer_par_mois(mois) if mois else self._transactions
        credits = sum(t.montant for t in source if t.type_transaction == "crédit")
        debits  = sum(t.montant for t in source if t.type_transaction == "débit")
        if credits == 0:
            return 0.0
        return round((credits - debits) / credits * 100, 1)

    # ── Alertes budget ───────────────────────────────────────────────────────

    def alertes_depassement(self, mois: str) -> List[Dict]:
        """
        Compare les dépenses du mois aux budgets définis dans le catalogue.
        Retourne une liste d'alertes pour les catégories dépassées.
        """
        depenses = self.depenses_par_categorie(mois)
        alertes = []
        for cat in self._catalogue:
            if cat.budget_mensuel > 0 and cat.nom in depenses:
                depense = depenses[cat.nom]
                if depense > cat.budget_mensuel:
                    alertes.append({
                        "categorie": cat.nom,
                        "depense":   round(depense, 2),
                        "budget":    cat.budget_mensuel,
                        "depassement": round(depense - cat.budget_mensuel, 2),
                        "pourcent":  round(depense / cat.budget_mensuel * 100, 1),
                    })
        return sorted(alertes, key=lambda x: x["pourcent"], reverse=True)

    # ── Statistiques résumé ──────────────────────────────────────────────────

    def resume(self, mois: str = None) -> Dict:
        """Dictionnaire de synthèse pour affichage ou export."""
        return {
            "nom":           self._nom,
            "mois":          mois or "Tous",
            "nb_transactions": len(self.filtrer_par_mois(mois) if mois
                                   else self._transactions),
            "total_debits":  self.total_debits() if not mois else
                             round(sum(t.montant for t in
                                       self.filtrer_par_mois(mois)
                                       if t.type_transaction == "débit"), 2),
            "total_credits": self.total_credits() if not mois else
                             round(sum(t.montant for t in
                                       self.filtrer_par_mois(mois)
                                       if t.type_transaction == "crédit"), 2),
            "solde":         self.solde_total(),
            "taux_epargne":  self.taux_epargne(mois),
            "top_categories": self.depenses_par_categorie(mois),
        }

    def __repr__(self):
        return (f"Budget(nom='{self._nom}', "
                f"transactions={self.nombre_transactions}, "
                f"solde={self.solde_total():.2f} FCFA)")

    def __len__(self):
        return self.nombre_transactions

    def __iter__(self):
        return iter(self._transactions)

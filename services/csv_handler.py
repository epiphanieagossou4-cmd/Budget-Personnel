import csv
import os
from typing import List
from models.transaction import Transaction


class CSVHandler:
    """
    Service de persistance CSV.
    Encapsule toutes les opérations lecture/écriture sur fichiers CSV.
    """

    COLONNES = ["id", "date", "montant", "type", "categorie", "description"]

    def __init__(self, chemin_fichier: str):
        self._chemin = chemin_fichier
        self._assurer_repertoire()

    @property
    def chemin(self):
        return self._chemin

    def _assurer_repertoire(self):
        repertoire = os.path.dirname(self._chemin)
        if repertoire and not os.path.exists(repertoire):
            os.makedirs(repertoire)

    def lire_transactions(self) -> List[Transaction]:
        """Lit toutes les transactions depuis le fichier CSV."""
        if not os.path.exists(self._chemin):
            return []
        transactions = []
        try:
            with open(self._chemin, "r", encoding="utf-8", newline="") as f:
                lecteur = csv.DictReader(f)
                for i, ligne in enumerate(lecteur, start=1):
                    try:
                        t = Transaction.depuis_dict(ligne)
                        transactions.append(t)
                    except (ValueError, KeyError) as e:
                        print(f"⚠ Ligne {i} ignorée ({e}): {ligne}")
        except IOError as e:
            print(f"Erreur lecture fichier : {e}")
        return transactions

    def ecrire_transactions(self, transactions: List[Transaction]) -> bool:
        """Écrase le fichier CSV avec la liste fournie."""
        try:
            with open(self._chemin, "w", encoding="utf-8", newline="") as f:
                ecrivain = csv.DictWriter(f, fieldnames=self.COLONNES)
                ecrivain.writeheader()
                for t in transactions:
                    ecrivain.writerow(t.vers_dict())
            return True
        except IOError as e:
            print(f"Erreur écriture fichier : {e}")
            return False

    def ajouter_transaction(self, transaction: Transaction) -> bool:
        """Ajoute une transaction en fin de fichier (mode append)."""
        fichier_existe = os.path.exists(self._chemin)
        try:
            with open(self._chemin, "a", encoding="utf-8", newline="") as f:
                ecrivain = csv.DictWriter(f, fieldnames=self.COLONNES)
                if not fichier_existe:
                    ecrivain.writeheader()
                ecrivain.writerow(transaction.vers_dict())
            return True
        except IOError as e:
            print(f"Erreur ajout transaction : {e}")
            return False

    def fichier_existe(self) -> bool:
        return os.path.exists(self._chemin)

    def nombre_lignes(self) -> int:
        if not self.fichier_existe():
            return 0
        with open(self._chemin, "r", encoding="utf-8") as f:
            return sum(1 for _ in f) - 1  # -1 pour l'en-tête

    def __repr__(self):
        return f"CSVHandler(chemin='{self._chemin}', lignes={self.nombre_lignes()})"

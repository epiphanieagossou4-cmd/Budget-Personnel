import re
from typing import List
class Categorie:
    """
    Classe de base représentant une catégorie de dépenses/revenus.
    Démontre : encapsulation, __slots__, méthodes spéciales.
    """
 
    __slots__ = ("_nom", "_couleur", "_icone", "_budget_mensuel")
 
    COULEURS_DEFAUT = {
        "Alimentation":   "#e74c3c",
        "Transport":      "#3498db",
        "Logement":       "#9b59b6",
        "Santé":          "#2ecc71",
        "Loisirs":        "#f39c12",
        "Éducation":      "#1abc9c",
        "Vêtements":      "#e67e22",
        "Épargne":        "#27ae60",
        "Revenus":        "#16a085",
        "Non catégorisé": "#95a5a6",
    }
 
    def __init__(self, nom: str, couleur: str = None,
                 icone: str = "💳", budget_mensuel: float = 0.0):
        self._nom = nom.strip()
        self._couleur = couleur or self.COULEURS_DEFAUT.get(nom, "#7f8c8d")
        self._icone = icone
        self._budget_mensuel = round(float(budget_mensuel), 2)
 
    @property
    def nom(self):
        return self._nom
 
    @property
    def couleur(self):
        return self._couleur
 
    @property
    def icone(self):
        return self._icone
 
    @property
    def budget_mensuel(self):
        return self._budget_mensuel
 
    @budget_mensuel.setter
    def budget_mensuel(self, valeur):
        if valeur < 0:
            raise ValueError("Budget mensuel ne peut pas être négatif")
        self._budget_mensuel = round(float(valeur), 2)
 
    def __str__(self):
        return f"{self._icone} {self._nom}"
 
    def __repr__(self):
        return f"Categorie(nom='{self._nom}', budget={self._budget_mensuel:.2f})"
 
    def __eq__(self, other):
        if isinstance(other, Categorie):
            return self._nom.lower() == other._nom.lower()
        return False
 
    def __hash__(self):
        return hash(self._nom.lower())
 
 
class CategoriseurAuto(Categorie):
    """
    Hérite de Categorie et ajoute la logique de catégorisation automatique
    basée sur des mots-clés (pattern matching).
    Démontre : héritage, surcharge de méthode, polymorphisme.
    """
 
    # Dictionnaire de règles : catégorie → liste de mots-clés
    REGLES_DEFAUT = {
        "Alimentation":   ["supermarché", "restaurant", "café", "boulangerie",
                           "épicerie", "marché", "food", "pizza", "snack",
                           "gbèglo", "attiéké", "dépôt", "sodabi"],
        "Transport":      ["carburant", "essence", "taxi", "moto", "bus",
                           "parking", "uber", "zem", "zemidjan", "transport"],
        "Logement":       ["loyer", "électricité", "eau", "sbee", "soneb",
                           "internet", "wifi", "maison", "appartement"],
        "Santé":          ["pharmacie", "médecin", "hôpital", "clinique",
                           "médicament", "consultation", "dentiste"],
        "Loisirs":        ["cinéma", "bar", "discothèque", "sport", "musique",
                           "jeu", "concert", "voyage", "hôtel", "beach"],
        "Éducation":      ["école", "université", "formation", "livre",
                           "frais scolaires", "cours", "tutoriel"],
        "Vêtements":      ["boutique", "vêtement", "chaussure", "tissu",
                           "couturier", "mode", "habit"],
        "Épargne":        ["épargne", "virement", "placement", "investissement"],
        "Revenus":        ["salaire", "virement reçu", "remboursement",
                           "bonus", "revenu", "paiement reçu"],
    }
 
    def __init__(self, nom: str, mots_cles: List[str] = None,
                 couleur: str = None, icone: str = "🏷️",
                 budget_mensuel: float = 0.0):
        super().__init__(nom, couleur, icone, budget_mensuel)
        self._mots_cles = [m.lower() for m in (mots_cles or [])]
 
    @property
    def mots_cles(self):
        return list(self._mots_cles)
 
    def ajouter_mot_cle(self, mot: str):
        mot = mot.lower().strip()
        if mot not in self._mots_cles:
            self._mots_cles.append(mot)
 
    def correspond(self, description: str) -> bool:
        """Vérifie si la description correspond à cette catégorie."""
        desc = description.lower()
        return any(mc in desc for mc in self._mots_cles)
 
    def score(self, description: str) -> int:
        """Nombre de mots-clés trouvés (pour choisir la meilleure catégorie)."""
        desc = description.lower()
        return sum(1 for mc in self._mots_cles if mc in desc)
 
    # ── Méthode de classe : construire toutes les catégories ────────────────
 
    @classmethod
    def creer_catalogue_defaut(cls) -> List["CategoriseurAuto"]:
        """Crée la liste complète des catégoriseurs avec règles par défaut."""
        icones = {
            "Alimentation":   "",
            "Transport":      "",
            "Logement":       "",
            "Santé":          "",
            "Loisirs":        "",
            "Éducation":      "",
            "Vêtements":      "",
            "Épargne":        "",
            "Revenus":        "",
        }
        budgets = {
            "Alimentation": 80000,
            "Transport":    40000,
            "Logement":    150000,
            "Santé":        30000,
            "Loisirs":      50000,
            "Éducation":    60000,
            "Vêtements":    25000,
            "Épargne":      50000,
            "Revenus":           0,
        }
        return [
            cls(
                nom=nom,
                mots_cles=mots,
                icone=icones.get(nom, ""),
                budget_mensuel=budgets.get(nom, 0),
            )
            for nom, mots in cls.REGLES_DEFAUT.items()
        ]
 
    # ── Fonction de catégorisation globale ──────────────────────────────────
 
    @staticmethod
    def categoriser(description: str,
                    catalogue: List["CategoriseurAuto"] = None) -> str:
        """
        Détermine automatiquement la catégorie d'une transaction
        en fonction de sa description.
        """
        if catalogue is None:
            catalogue = CategoriseurAuto.creer_catalogue_defaut()
 
        # Choisir la catégorie avec le meilleur score
        meilleure = max(catalogue, key=lambda c: c.score(description),
                        default=None)
        if meilleure and meilleure.score(description) > 0:
            return meilleure.nom
        return "Non catégorisé"
 
    def __repr__(self):
        return (f"CategoriseurAuto(nom='{self._nom}', "
                f"mots_clés={len(self._mots_cles)}, "
                f"budget={self._budget_mensuel:.2f})")
 

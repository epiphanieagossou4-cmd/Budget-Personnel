from datetime import datetime


class Transaction:
    TYPES_VALIDES = ("débit", "crédit")

    def __init__(
        self,
        montant: float,
        description: str,
        date,
        type_transaction: str = "débit",
        categorie: str = "Non catégorisé",
        id_transaction=None,
    ):
        self._id = id_transaction
        self.montant = montant
        self._description = description.strip()
        self.date = date
        self.type_transaction = type_transaction
        self._categorie = categorie.strip()

    # ── Propriétés ──────────────────────────────────────────────────────────

    @property
    def id(self):
        return self._id

    @property
    def montant(self):
        return self._montant

    @montant.setter
    def montant(self, valeur):
        if not isinstance(valeur, (int, float)):
            raise TypeError(f"Montant doit être numérique, reçu : {type(valeur)}")
        if valeur < 0:
            raise ValueError(f"Montant ne peut pas être négatif : {valeur}")
        self._montant = round(float(valeur), 2)

    @property
    def description(self):
        return self._description

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, valeur):
        if isinstance(valeur, datetime):
            self._date = valeur
            return
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                self._date = datetime.strptime(valeur, fmt)
                return
            except ValueError:
                continue
        raise ValueError(f"Format de date invalide : '{valeur}'")

    @property
    def type_transaction(self):
        return self._type

    @type_transaction.setter
    def type_transaction(self, valeur):
        valeur = valeur.lower().strip()
        if valeur not in self.TYPES_VALIDES:
            raise ValueError(f"Type invalide '{valeur}'. Valeurs : {self.TYPES_VALIDES}")
        self._type = valeur

    @property
    def categorie(self):
        return self._categorie

    @categorie.setter
    def categorie(self, valeur):
        self._categorie = valeur.strip()

    @property
    def montant_signe(self):
        return -self._montant if self._type == "débit" else self._montant

    @property
    def date_str(self):
        return self._date.strftime("%Y-%m-%d")

    @property
    def mois(self):
        return self._date.strftime("%Y-%m")

    # ── Représentations ─────────────────────────────────────────────────────

    def __repr__(self):
        signe = "-" if self._type == "débit" else "+"
        return (f"Transaction(id={self._id}, {self.date_str}, "
                f"{signe}{self._montant:.2f} FCFA, "
                f"'{self._description}', [{self._categorie}])")

    def __str__(self):
        signe = "▼" if self._type == "débit" else "▲"
        return (f"{self.date_str} | {signe} {self._montant:>10.2f} FCFA | "
                f"{self._categorie:<18} | {self._description}")

    # ── Sérialisation ────────────────────────────────────────────────────────

    def vers_dict(self):
        return {
            "id": self._id,
            "date": self.date_str,
            "montant": self._montant,
            "type": self._type,
            "categorie": self._categorie,
            "description": self._description,
        }

    @classmethod
    def depuis_dict(cls, donnees):
        return cls(
            montant=float(donnees["montant"]),
            description=donnees["description"],
            date=donnees["date"],
            type_transaction=donnees.get("type", "débit"),
            categorie=donnees.get("categorie", "Non catégorisé"),
            id_transaction=int(donnees["id"]) if donnees.get("id") else None,
        )
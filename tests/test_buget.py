"""
tests/test_budget.py — Tests unitaires
Bloc 2 — Fondations (vérification des types et comportements)
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.transaction import Transaction
from models.categorie import Categorie, CategoriseurAuto
from models.budget import Budget


def test_transaction_validation():
    t = Transaction(10000, "Test", "2026-04-01")
    assert t.montant == 10000.0
    assert t.type_transaction == "débit"
    assert t.mois == "2026-04"
    assert t.montant_signe == -10000.0
    print("✓ test_transaction_validation")


def test_transaction_erreurs():
    try:
        Transaction(-500, "Bad", "2026-01-01")
        assert False, "Doit lever ValueError"
    except ValueError:
        pass
    try:
        Transaction(100, "Bad date", "32/13/2026")
        assert False, "Doit lever ValueError"
    except ValueError:
        pass
    print("✓ test_transaction_erreurs")


def test_categorie_heritage():
    base = Categorie("Alimentation", budget_mensuel=80000)
    cat  = CategoriseurAuto("Transport", ["taxi", "carburant"], budget_mensuel=40000)
    assert isinstance(cat, Categorie)  # héritage
    assert cat.correspond("taxi")
    assert not cat.correspond("restaurant")
    assert cat.score("taxi carburant") == 2
    print("✓ test_categorie_heritage")


def test_categorisation_auto():
    tests = {
        "Supermarché Jonquet": "Alimentation",
        "Carburant moto":      "Transport",
        "Loyer appartement":   "Logement",
        "Pharmacie":           "Santé",
    }
    for desc, attendu in tests.items():
        res = CategoriseurAuto.categoriser(desc)
        assert res == attendu, f"'{desc}' → '{res}' ≠ '{attendu}'"
    print("✓ test_categorisation_auto")


def test_budget_calculs():
    b = Budget("Test")
    b.ajouter_transaction(Transaction(100000, "Salaire", "2026-04-01", "crédit"))
    b.ajouter_transaction(Transaction(30000, "Loyer", "2026-04-05", "débit", "Logement"))
    b.ajouter_transaction(Transaction(15000, "Supermarché", "2026-04-10", "débit", "Alimentation"))

    assert b.solde_total() == 55000.0
    assert b.total_credits() == 100000.0
    assert b.total_debits() == 45000.0
    assert b.taux_epargne("2026-04") == 55.0
    assert len(b) == 3
    print("✓ test_budget_calculs")


def test_serialisation_csv():
    t = Transaction(5000, "Test CSV", "2026-04-15", "débit", "Loisirs", 42)
    d = t.vers_dict()
    assert d["montant"] == 5000.0
    assert d["categorie"] == "Loisirs"
    t2 = Transaction.depuis_dict(d)
    assert t2.montant == t.montant
    assert t2.categorie == t.categorie
    print("✓ test_serialisation_csv")


if __name__ == "__main__":
    print("\n=== TESTS UNITAIRES ===\n")
    test_transaction_validation()
    test_transaction_erreurs()
    test_categorie_heritage()
    test_categorisation_auto()
    test_budget_calculs()
    test_serialisation_csv()
    print("\n✓ TOUS LES TESTS PASSENT\n")

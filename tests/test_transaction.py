import pytest
from models.transaction import Transaction


def test_creation_debit():
    t = Transaction(5000, "Carburant moto", "2025-04-05", "débit")
    assert t.montant == 5000.0
    assert t.type_transaction == "débit"

def test_creation_credit():
    t = Transaction(85000, "Salaire", "2025-04-01", "crédit")
    assert t.montant == 85000.0
    assert t.type_transaction == "crédit"

def test_montant_signe_debit():
    t = Transaction(5000, "Achat", "2025-04-01", "débit")
    assert t.montant_signe == -5000.0

def test_montant_signe_credit():
    t = Transaction(10000, "Salaire", "2025-04-01", "crédit")
    assert t.montant_signe == 10000.0

def test_mois():
    t = Transaction(5000, "Test", "2025-04-15", "débit")
    assert t.mois == "2025-04"

def test_serialisation():
    t = Transaction(3000, "Taxi", "2025-04-10", "débit", "Transport", 1)
    d = t.vers_dict()
    assert d["montant"] == 3000.0
    assert d["categorie"] == "Transport"

def test_montant_negatif_interdit():
    with pytest.raises(ValueError):
        Transaction(-500, "Erreur", "2025-04-01", "débit")

def test_type_invalide_interdit():
    with pytest.raises(ValueError):
        Transaction(5000, "Test", "2025-04-01", "virement")

def test_date_invalide_interdit():
    with pytest.raises(ValueError):
        Transaction(5000, "Test", "date-incorrecte", "débit")
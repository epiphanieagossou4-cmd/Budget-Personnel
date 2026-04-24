import pytest
from models.budget import Budget
from models.transaction import Transaction


@pytest.fixture
def budget():
    b = Budget("Test")
    b.ajouter_transaction(Transaction(85000, "Salaire", "2025-04-01", "crédit"))
    b.ajouter_transaction(Transaction(45000, "Loyer", "2025-04-08", "débit"))
    b.ajouter_transaction(Transaction(5000, "Carburant moto", "2025-04-05", "débit"))
    b.ajouter_transaction(Transaction(10000, "Remboursement", "2025-04-18", "crédit"))
    return b


def test_solde_correct(budget):
    assert budget.solde_total() == 45000.0

def test_total_debits(budget):
    assert budget.total_debits() == 50000.0

def test_total_credits(budget):
    assert budget.total_credits() == 95000.0

def test_nombre_transactions(budget):
    assert budget.nombre_transactions == 4

def test_filtre_par_mois(budget):
    assert len(budget.filtrer_par_mois("2025-04")) == 4

def test_filtre_mois_vide(budget):
    assert len(budget.filtrer_par_mois("2025-03")) == 0

def test_suppression(budget):
    id1 = budget.transactions[0].id
    assert budget.supprimer_transaction(id1) == True
    assert budget.nombre_transactions == 3

def test_suppression_inexistant(budget):
    assert budget.supprimer_transaction(9999) == False

def test_taux_epargne(budget):
    assert budget.taux_epargne() > 0
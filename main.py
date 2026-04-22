#!/usr/bin/env python3
"""
main.py — Point d'entrée CLI du Moniteur de Budget
Projet 6 : Moniteur de Budget Personnel (Fintech)
Bloc 2 & 3 — Workflow, Fondations, Architecture POO
"""

import sys
import os
import json

# Ajouter le répertoire racine au path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.budget import Budget
from models.transaction import Transaction
from services.csv_handler import CSVHandler
from services.rapport import GenerateurRapport


FICHIER_CSV = "data/transactions.csv"
FICHIER_JSON_EXPORT = "data/rapport_export.json"


def charger_budget(chemin: str = FICHIER_CSV) -> tuple:
    """Charge les transactions depuis CSV dans un objet Budget."""
    handler = CSVHandler(chemin)
    budget = Budget("Mon Budget Personnel")
    transactions = handler.lire_transactions()

    for t in transactions:
        budget.ajouter_transaction(t, auto_categoriser=False)

    return budget, handler


def menu_principal():
    print("\n" + "═"*50)
    print("  MONITEUR DE BUDGET PERSONNEL")
    print("═"*50)
    print("  1. Afficher le résumé général")
    print("  2. Rapport mensuel")
    print("  3. Ajouter une transaction")
    print("  4. Lister les transactions")
    print("  5. Exporter données JSON")
    print("  6. Démonstration POO")
    print("  0. Quitter")
    print("─"*50)
    return input("  Votre choix : ").strip()


def afficher_resume(budget):
    rapport = GenerateurRapport(budget)
    print(rapport.rapport_complet())


def rapport_mensuel(budget):
    evol = budget.evolution_mensuelle()
    mois_dispo = sorted(evol.keys())
    if not mois_dispo:
        print("Aucune donnée disponible.")
        return
    print("\n  Mois disponibles :", ", ".join(mois_dispo))
    mois = input("  Entrez un mois (YYYY-MM) : ").strip()
    if mois not in mois_dispo:
        print(f"  Mois '{mois}' non trouvé.")
        return
    rapport = GenerateurRapport(budget)
    print(rapport.rapport_mensuel(mois))


def ajouter_transaction(budget, handler):
    print("\n  NOUVELLE TRANSACTION")
    print("  ─"*20)
    try:
        desc   = input("  Description : ").strip()
        montant = float(input("  Montant (FCFA) : "))
        date   = input("  Date (YYYY-MM-DD) : ").strip()
        type_t = input("  Type [débit/crédit] : ").strip() or "débit"

        t = Transaction(montant=montant, description=desc,
                        date=date, type_transaction=type_t)
        budget.ajouter_transaction(t, auto_categoriser=True)
        handler.ajouter_transaction(t)
        print(f"\n  ✓ Transaction ajoutée : {t}")
        print(f"    Catégorie détectée  : {t.categorie}")
    except (ValueError, TypeError) as e:
        print(f"  ✗ Erreur : {e}")


def lister_transactions(budget):
    print(f"\n  TRANSACTIONS ({len(budget)} au total)")
    print("  " + "─"*70)
    for t in sorted(budget.transactions, key=lambda x: x.date, reverse=True)[:20]:
        print(f"  {t}")
    if len(budget) > 20:
        print(f"  ... et {len(budget)-20} autres")


def exporter_json(budget):
    rapport = GenerateurRapport(budget)
    data = rapport.exporter_json()
    with open(FICHIER_JSON_EXPORT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n  ✓ Données exportées : {FICHIER_JSON_EXPORT}")
    return data


def demo_poo():
    """Démonstration des concepts POO implémentés."""
    from models.categorie import CategoriseurAuto

    print("\n" + "═"*60)
    print("  DÉMONSTRATION CONCEPTS POO")
    print("═"*60)

    print("\n  1. ENCAPSULATION — Transaction avec validation")
    t = Transaction(25000, "Supermarché Jonquet", "2026-04-22")
    print(f"     {t}")
    print(f"     Propriété protégée : t._montant = {t._montant}")
    print(f"     Accès via getter   : t.montant  = {t.montant}")
    try:
        t.montant = -500
    except ValueError as e:
        print(f"     Setter protège    : {e}")

    print("\n  2. HÉRITAGE — CategoriseurAuto hérite de Categorie")
    cat = CategoriseurAuto("Transport", ["taxi", "carburant", "zemidjan"],
                           icone="🚗", budget_mensuel=40000)
    print(f"     {repr(cat)}")
    print(f"     correspond('taxi'): {cat.correspond('taxi aéroport')}")
    print(f"     correspond('pizza'): {cat.correspond('pizza restaurant')}")

    print("\n  3. CATÉGORISATION AUTO — polymorphisme")
    tests = ["Supermarché Jonquet", "Carburant moto", "Loyer appartement",
             "Pharmacie médicament", "Concert musique", "Sodabi bar"]
    for desc in tests:
        cat_auto = CategoriseurAuto.categoriser(desc)
        print(f"     '{desc}' → {cat_auto}")

    print("\n  4. MÉTHODES SPÉCIALES")
    budget = Budget("Test")
    print(f"     len(budget) = {len(budget)}")
    budget.ajouter_transaction(
        Transaction(5000, "test", "2026-04-01"))
    print(f"     Après ajout: {repr(budget)}")
    print("\n" + "═"*60)


def main():
    print("\n  Chargement des données...")
    budget, handler = charger_budget()
    print(f"  ✓ {len(budget)} transactions chargées.")

    while True:
        choix = menu_principal()
        if choix == "1":
            afficher_resume(budget)
        elif choix == "2":
            rapport_mensuel(budget)
        elif choix == "3":
            ajouter_transaction(budget, handler)
        elif choix == "4":
            lister_transactions(budget)
        elif choix == "5":
            exporter_json(budget)
        elif choix == "6":
            demo_poo()
        elif choix == "0":
            print("\n  Au revoir !\n")
            break
        else:
            print("  Choix invalide.")


if __name__ == "__main__":
    main()

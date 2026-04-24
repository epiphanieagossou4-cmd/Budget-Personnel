from services.budget_service import BudgetService
from services.rapport import GenerateurRapport


def main():
    print("\n" + "=" * 60)
    print("  MONITEUR DE BUDGET PERSONNEL")
    print("=" * 60)

    service = BudgetService(nom_budget="Mon Budget")
    print(f"\nService demarre : {service}")
    print(f"Transactions en memoire : {len(service.transactions())}")

    print("\n-- Ajout de transactions --")
    donnees = [
        (85000,  "Salaire mensuel IUT",         "2025-04-01", "crédit"),
        (12500,  "Supermarche Erevan",           "2025-04-03", "débit"),
        (5000,   "Carburant moto",               "2025-04-05", "débit"),
        (45000,  "Loyer studio Parakou",         "2025-04-08", "débit"),
        (3200,   "Restaurant gbeglo",            "2025-04-10", "débit"),
        (8000,   "Pharmacie medicaments",        "2025-04-12", "débit"),
        (20000,  "Frais scolaires Python",       "2025-04-14", "débit"),
        (15000,  "Virement epargne",             "2025-04-15", "débit"),
        (10000,  "Remboursement ami",            "2025-04-18", "crédit"),
    ]

    for montant, desc, date, type_t in donnees:
        t = service.ajouter_transaction(montant, desc, date, type_t)
        signe = "+" if type_t == "crédit" else "-"
        print(f"   {signe} {montant:>8.0f} FCFA | {t.categorie:<18} | {desc}")

    print(f"\nSolde : {service.solde():.2f} FCFA")

    rapport = GenerateurRapport(service.budget)
    print(rapport.rapport_mensuel("2025-04"))

    chemin = service.exporter_rapport_csv(mois="2025-04")
    print(f"Rapport CSV exporte -> {chemin}")

    print("\n-- Verification persistance --")
    service2 = BudgetService(nom_budget="Budget recharge")
    print(f"   {service2}")
    print(f"   Solde recharge : {service2.solde():.2f} FCFA")
    print("\nLes donnees survivent apres redemarrage !")
    print("=" * 60)


if __name__ == "__main__":
    main()
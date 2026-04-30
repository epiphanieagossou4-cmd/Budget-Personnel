import tkinter as tk
from tkinter import ttk, messagebox
from services.budget_service import BudgetService

BG    = "#dadae3"
CARD  = "#e8e8f5"
ACCENT= "#e9e4f1"
VERT  = "#e5efeb"
ROUGE = "#e4e1e1"
TEXTE = "#f1f5f9"
GRIS  = "#94a3b8"


class AppBudget(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Moniteur de Budget Personnel")
        self.geometry("900x650")
        self.configure(bg=BG)
        self.service = BudgetService("Mon Budget")
        self._construire_interface()
        self._rafraichir_liste()

    def _construire_interface(self):
        tk.Label(self, text="Moniteur de Budget Personnel",
                 font=("Segoe UI", 18, "bold"),
                 bg=BG, fg=TEXTE).pack(pady=(15, 5))
        principal = tk.Frame(self, bg=BG)
        principal.pack(fill="both", expand=True, padx=15, pady=5)
        gauche = tk.Frame(principal, bg=BG, width=280)
        gauche.pack(side="left", fill="y", padx=(0, 10))
        gauche.pack_propagate(False)
        droite = tk.Frame(principal, bg=BG)
        droite.pack(side="left", fill="both", expand=True)
        self._formulaire(gauche)
        self._resume(gauche)
        self._liste_transactions(droite)

    def _formulaire(self, parent):
        cadre = tk.LabelFrame(parent, text=" Nouvelle Transaction ",
                              font=("Segoe UI", 10, "bold"),
                              bg=CARD, fg=TEXTE, bd=1, relief="solid")
        cadre.pack(fill="x", pady=(0, 10))
        self._vars = {}
        for label, cle in [("Montant (FCFA)", "montant"),
                            ("Description", "description"),
                            ("Date (AAAA-MM-JJ)", "date")]:
            tk.Label(cadre, text=label, bg=CARD, fg=GRIS,
                     font=("Segoe UI", 9)).pack(anchor="w", padx=10, pady=(8, 0))
            var = tk.StringVar()
            self._vars[cle] = var
            tk.Entry(cadre, textvariable=var, bg="#3a3a5e", fg=TEXTE,
                     insertbackground=TEXTE, relief="flat",
                     font=("Segoe UI", 10)).pack(fill="x", padx=10, pady=(2, 0))
        tk.Label(cadre, text="Type", bg=CARD, fg=GRIS,
                 font=("Segoe UI", 9)).pack(anchor="w", padx=10, pady=(8, 0))
        self._type_var = tk.StringVar(value="debit")
        tf = tk.Frame(cadre, bg=CARD)
        tf.pack(fill="x", padx=10, pady=(2, 8))
        for val, txt in [("debit", "Debit"), ("credit", "Credit")]:
            tk.Radiobutton(tf, text=txt, variable=self._type_var,
                           value=val, bg=CARD, fg=TEXTE,
                           selectcolor=ACCENT,
                           font=("Segoe UI", 9)).pack(side="left", padx=5)
        tk.Button(cadre, text="+ Ajouter", command=self._ajouter,
                  bg=ACCENT, fg="white", font=("Segoe UI", 10, "bold"),
                  relief="flat", cursor="hand2",
                  pady=6).pack(fill="x", padx=10, pady=(0, 10))

    def _resume(self, parent):
        cadre = tk.LabelFrame(parent, text=" Resume ",
                              font=("Segoe UI", 10, "bold"),
                              bg=CARD, fg=TEXTE, bd=1, relief="solid")
        cadre.pack(fill="x")
        self._lbl_solde = tk.Label(cadre, text="Solde : --",
                                   bg=CARD, fg=VERT,
                                   font=("Segoe UI", 13, "bold"))
        self._lbl_solde.pack(pady=(10, 2))
        self._lbl_debits = tk.Label(cadre, text="Depenses : --",
                                    bg=CARD, fg=ROUGE,
                                    font=("Segoe UI", 10))
        self._lbl_debits.pack()
        self._lbl_credits = tk.Label(cadre, text="Revenus : --",
                                     bg=CARD, fg=VERT,
                                     font=("Segoe UI", 10))
        self._lbl_credits.pack()
        self._lbl_epargne = tk.Label(cadre, text="Taux epargne : --",
                                     bg=CARD, fg=GRIS,
                                     font=("Segoe UI", 10))
        self._lbl_epargne.pack(pady=(0, 10))
        tk.Button(cadre, text="Supprimer selection",
                  command=self._supprimer,
                  bg="#7f1d1d", fg="white",
                  font=("Segoe UI", 9), relief="flat",
                  cursor="hand2", pady=4).pack(fill="x", padx=10, pady=(0, 10))

    def _liste_transactions(self, parent):
        tk.Label(parent, text="Transactions",
                 font=("Segoe UI", 12, "bold"),
                 bg=BG, fg=TEXTE).pack(anchor="w", pady=(0, 5))
        colonnes = ("id", "date", "montant", "type", "categorie", "description")
        self._table = tt
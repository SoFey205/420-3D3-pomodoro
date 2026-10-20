import tkinter as tk
from datetime import datetime


DUREE_TRAVAIL = 25 * 60   # 25 minutes en secondes
DUREE_PAUSE = 5 * 60      # 5 minutes en secondes


class App:
    def __init__(self):
        self.fenetre = tk.Tk()
        self.fenetre.title("Minuteur Pomodoro")
        self.fenetre.resizable(False, False)

        self.temps_restant = DUREE_TRAVAIL
        self.en_marche = False
        self.en_pause = False
        self.sessions_completees = 0

        # Affichage de l'état
        self.label_etat = tk.Label(
            self.fenetre,
            text="Travail",
            font=("Arial", 16, "bold")
        )
        self.label_etat.pack(pady=10)

        # Affichage du temps
        self.label_temps = tk.Label(
            self.fenetre,
            text="25:00",
            font=("Arial", 48, "bold")
        )
        self.label_temps.pack(pady=10)

        # Barre de progression
        self.canvas = tk.Canvas(
            self.fenetre,
            width=300,
            height=20,
            bg="white"
        )
        self.canvas.pack(pady=10)

        # Affichage des sessions
        self.label_sessions = tk.Label(
            self.fenetre,
            text="Sessions complétées : 0", #changer 
            font=("Arial", 12)
        )
        self.label_sessions.pack(pady=5)

        # Boutons
        frame_boutons = tk.Frame(self.fenetre)
        frame_boutons.pack(pady=10)

        self.btn_start = tk.Button(
            frame_boutons,
            text="Démarrer",
            command=self.demarrer
        )
        self.btn_start.pack(side=tk.LEFT, padx=5)

        self.btn_pause = tk.Button(
            frame_boutons,
            text="Pause",
            command=self.pause,
            state=tk.DISABLED
        )
        self.btn_pause.pack(side=tk.LEFT, padx=5)

        self.btn_reset = tk.Button(
            frame_boutons,
            text="Réinitialiser",
            command=self.reinitialiser
        )
        self.btn_reset.pack(side=tk.LEFT, padx=5)

        self.fenetre.mainloop()

    def demarrer(self):
        self.en_marche = True
        self.en_pause = False #meme quand il devient true il reste normal?
        self.btn_start.config(state=tk.DISABLED) #erreur?
        self.btn_pause.config(state=tk.NORMAL) #il reste normal? ahh car il est normal seulement dans demarrer, mais ailleur comme dans pause par exemple, c'est pas foncément le cas, il peut varier vu que dans pause on lui a pas imposé un état avec le ".config". So etat change selon le if !
        self.tick()

    def pause(self):
        if not self.en_pause: #quand ca tourne 
            self.en_pause = True #On veut le mettre en pause
            self.btn_pause.config(text="Reprendre")
        else:                 #quand c'est en pause
            self.en_pause = False #On veut le démarrer 
            self.btn_pause.config(text="Pause")
            self.tick()

    def reinitialiser(self):
        self.en_marche = False
        self.en_pause = False
        self.temps_restant = DUREE_TRAVAIL
        self.btn_start.config(state=tk.NORMAL)
        self.btn_pause.config(state=tk.DISABLED)
        self.btn_pause.config(text="Pause")
        self.label_etat.config(text="Travail", fg="black")
        self.label_temps.config(text="25:00")
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, 300, 20, fill="green", outline="")

    def tick(self):
        if not self.en_marche or self.en_pause:
            return

        if self.temps_restant > 0:
            self.temps_restant -= 1

            # Mettre à jour le temps
            minutes = self.temps_restant // 60
            secondes = self.temps_restant % 60
            self.label_temps.config(text=f"{minutes:02d}:{secondes:02d}")

            # Mettre à jour la barre de progression
            if self.en_pause is False and self.label_etat.cget("text") == "Travail":
                duree_totale = DUREE_TRAVAIL
            else:
                duree_totale = DUREE_PAUSE
            largeur = int(300 * self.temps_restant / duree_totale)
            self.canvas.delete("all")
            self.canvas.create_rectangle(0, 0, largeur, 20, fill="green", outline="")

            self.fenetre.after(1000, self.tick)

        else:
            # Session terminée
            if self.label_etat.cget("text") == "Travail":
                self.sessions_completees += 1
                self.label_sessions.config(
                    text=f"Sessions complétées : {self.sessions_completees}"
                )
                #LE SONNNN?
                self.jouer_son()
                self.label_etat.config(text="Pause", fg="blue")
                self.temps_restant = DUREE_PAUSE

                # Écrire dans le log
                horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open("pomodoro.log", 'a') as f:
                    f.write(
                        f"{horodatage} | Session {self.sessions_completees} "
                        f"complétée\n"
                    )
            else:
                self.label_etat.config(text="Travail", fg="black")
                self.temps_restant = DUREE_TRAVAIL

            self.fenetre.after(1000, self.tick)


if __name__ == "__main__":
    app = App()

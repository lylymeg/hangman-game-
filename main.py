import sys
import random
import unicodedata
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QPainterPath
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QGridLayout, QFrame
)

# ------------------------------------------------------------------------------
# BANQUE DE MOTS CATEGORISEES
# ------------------------------------------------------------------------------
WORD_CATEGORIES = {
    "Informatique 💻": [
        "ALGORITHME", "COMPILATEUR", "BASE DE DONNEES", "INTERFACE", 
        "DEVELOPPEUR", "RESEAU", "VARIABLE", "PROCESSEUR", "SYSTEME"
    ],
    "Animaux 🐾": [
        "CAMELEON", "DAUPHIN", "PANTHERE", "FLAMANT", 
        "ARMARDILLO", "KANGOUROU", "CORBEAU", "GIRAFE"
    ],
    "Pays 🌍": [
        "ALGERIE", "NORVEGE", "ARGENTINE", "JAPON", 
        "PORTUGAL", "CANADA", "AUSTRALIE", "BRESIL"
    ]
}


def remove_accents(text):
    """Normalise la chaîne pour supprimer les accents."""
    nfkd_form = unicodedata.normalize('NFKD', text)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


# ------------------------------------------------------------------------------
# WIDGET DESSIN VECTORIEL DU PENDU
# ------------------------------------------------------------------------------
class HangmanDrawingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(280, 320)
        self.wrong_attempts = 0

    def set_attempts(self, attempts):
        self.wrong_attempts = attempts
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Fond du widget
        painter.fillRect(self.rect(), QColor("#182030"))

        # Stylos
        gallow_pen = QPen(QColor("#00E1FF"), 4)
        man_pen = QPen(QColor("#FF3264"), 3)

        w = self.width()
        h = self.height()

        # Step 1: Potence (Base, Poteau, Traverse, Corde)
        if self.wrong_attempts >= 1:
            painter.setPen(gallow_pen)
            # Base
            painter.drawLine(int(w * 0.15), int(h * 0.88), int(w * 0.65), int(h * 0.88))
            # Poteau vertical
            painter.drawLine(int(w * 0.35), int(h * 0.88), int(w * 0.35), int(h * 0.12))
            # Traverse haute
            painter.drawLine(int(w * 0.35), int(h * 0.12), int(w * 0.70), int(h * 0.12))
            # Support oblique
            painter.drawLine(int(w * 0.35), int(h * 0.25), int(w * 0.48), int(h * 0.12))
            # Corde
            painter.drawLine(int(w * 0.70), int(h * 0.12), int(w * 0.70), int(h * 0.24))

        painter.setPen(man_pen)
        head_center_x = int(w * 0.70)
        head_center_y = int(h * 0.29)
        head_radius = 18

        # Step 2: Tête
        if self.wrong_attempts >= 2:
            painter.drawEllipse(QPointF(head_center_x, head_center_y), head_radius, head_radius)

        # Step 3: Tronc (Corps)
        body_top_y = head_center_y + head_radius
        body_bottom_y = body_top_y + 60
        if self.wrong_attempts >= 3:
            painter.drawLine(head_center_x, body_top_y, head_center_x, body_bottom_y)

        # Step 4: Bras gauche & droit
        if self.wrong_attempts >= 4:
            arm_y = body_top_y + 18
            painter.drawLine(head_center_x, arm_y, head_center_x - 22, arm_y + 25)  # Gauche
            painter.drawLine(head_center_x, arm_y, head_center_x + 22, arm_y + 25)  # Droit

        # Step 5: Jambe gauche
        if self.wrong_attempts >= 5:
            painter.drawLine(head_center_x, body_bottom_y, head_center_x - 22, body_bottom_y + 35)

        # Step 6: Jambe droite (Game Over)
        if self.wrong_attempts >= 6:
            painter.drawLine(head_center_x, body_bottom_y, head_center_x + 22, body_bottom_y + 35)

            # Yeux en X pour marquer la défaite
            painter.setPen(QPen(QColor("#FF3264"), 2))
            painter.drawLine(head_center_x - 7, head_center_y - 4, head_center_x - 2, head_center_y + 2)
            painter.drawLine(head_center_x - 2, head_center_y - 4, head_center_x - 7, head_center_y + 2)

            painter.drawLine(head_center_x + 2, head_center_y - 4, head_center_x + 7, head_center_y + 2)
            painter.drawLine(head_center_x + 7, head_center_y - 4, head_center_x + 2, head_center_y + 2)


# ------------------------------------------------------------------------------
# FENÊTRE PRINCIPALE DU JEU DU PENDU
# ------------------------------------------------------------------------------
class HangmanGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jeu du Pendu Épuré - PyQt5")
        self.setFixedSize(700, 780)
        self.setStyleSheet("""
            QWidget {
                background-color: #121824;
                color: #FFFFFF;
                font-family: 'Segoe UI', sans-serif;
            }
            QComboBox {
                background-color: #182030;
                color: #00E1FF;
                border: 2px solid #00E1FF;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 14px;
                font-weight: bold;
            }
            QComboBox QAbstractItemView {
                background-color: #182030;
                color: #FFFFFF;
                selection-background-color: #00E1FF;
                selection-color: #121824;
            }
            QPushButton {
                background-color: #182030;
                color: #FFFFFF;
                border: 1.5px solid #2A364F;
                border-radius: 6px;
                font-size: 15px;
                font-weight: bold;
                min-width: 40px;
                min-height: 42px;
            }
            QPushButton:hover {
                border-color: #00E1FF;
                color: #00E1FF;
            }
            QPushButton:disabled {
                background-color: #0E131D;
                border-color: #182030;
            }
        """)

        self.word_to_guess = ""
        self.normalized_word = ""
        self.guessed_letters = set()
        self.wrong_attempts = 0
        self.max_attempts = 6
        self.is_game_over = False

        self.keyboard_buttons = {}

        self.init_ui()
        self.start_new_game()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 20, 25, 20)
        main_layout.setSpacing(18)

        # 1. BARRE SUPÉRIEURE (Sélecteur de catégorie & Reset)
        top_bar = QHBoxLayout()

        category_label = QLabel("Catégorie :")
        category_label.setStyleSheet("font-size: 15px; color: #8A99AD;")

        self.category_combo = QComboBox()
        self.category_combo.addItems(list(WORD_CATEGORIES.keys()))
        self.category_combo.currentIndexChanged.connect(self.start_new_game)

        self.restart_btn = QPushButton("🔄 Recommencer")
        self.restart_btn.setStyleSheet("""
            QPushButton {
                background-color: #00E1FF;
                color: #121824;
                border: none;
                padding: 8px 18px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #33E7FF;
            }
        """)
        self.restart_btn.clicked.connect(self.start_new_game)

        top_bar.addWidget(category_label)
        top_bar.addWidget(self.category_combo)
        top_bar.addStretch()
        top_bar.addWidget(self.restart_btn)

        main_layout.addLayout(top_bar)

        # 2. ZONE CENTRAL (Dessin du Pendu)
        self.drawing_widget = HangmanDrawingWidget()
        main_layout.addWidget(self.drawing_widget, alignment=Qt.AlignCenter)

        # 3. AFFICHAGE DU MOT À DEVINER
        self.word_display_label = QLabel("")
        self.word_display_label.setFont(QFont("Segoe UI", 26, QFont.Bold))
        self.word_display_label.setStyleSheet("color: #00E1FF; letter-spacing: 8px;")
        self.word_display_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.word_display_label)

        # 4. MESSAGE D'ÉTAT (Victoire / Défaite / Erreurs)
        self.status_label = QLabel("")
        self.status_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

        # 5. CLAVIER VIRTUEL
        keyboard_layout = QGridLayout()
        keyboard_layout.setSpacing(8)

        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        cols = 7
        for i, letter in enumerate(alphabet):
            btn = QPushButton(letter)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, l=letter: self.process_letter(l))
            
            row = i // cols
            col = i % cols
            keyboard_layout.addWidget(btn, row, col)
            self.keyboard_buttons[letter] = btn

        main_layout.addLayout(keyboard_layout)

    # --------------------------------------------------------------------------
    # LOGIQUE DE JEU
    # --------------------------------------------------------------------------
    def start_new_game(self):
        category = self.category_combo.currentText()
        self.word_to_guess = random.choice(WORD_CATEGORIES[category])
        self.normalized_word = remove_accents(self.word_to_guess)
        self.guessed_letters.clear()
        self.wrong_attempts = 0
        self.is_game_over = False

        self.drawing_widget.set_attempts(0)
        self.status_label.setText(f"Essais restants : {self.max_attempts}")
        self.status_label.setStyleSheet("color: #8A99AD;")

        # Réinitialiser tous les boutons du clavier
        for letter, btn in self.keyboard_buttons.items():
            btn.setEnabled(True)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #182030;
                    color: #FFFFFF;
                    border: 1.5px solid #2A364F;
                }
                QPushButton:hover {
                    border-color: #00E1FF;
                    color: #00E1FF;
                }
            """)

        self.update_word_display()

    def update_word_display(self):
        display = []
        for orig_char, norm_char in zip(self.word_to_guess, self.normalized_word):
            if orig_char == ' ':
                display.append("  ")
            elif norm_char in self.guessed_letters:
                display.append(orig_char)
            else:
                display.append("_")

        self.word_display_label.setText(" ".join(display))

        # Vérification de la victoire
        if all(c in self.guessed_letters or c == ' ' for c in self.normalized_word):
            self.trigger_win()

    def process_letter(self, letter):
        if self.is_game_over or letter in self.guessed_letters:
            return

        self.guessed_letters.add(letter)
        btn = self.keyboard_buttons[letter]
        btn.setEnabled(False)

        if letter in self.normalized_word:
            # Lettre correcte (Bouton Vert Néon)
            btn.setStyleSheet("""
                QPushButton:disabled {
                    background-color: #003B2B;
                    color: #00FF9D;
                    border: 1.5px solid #00FF9D;
                }
            """)
            self.update_word_display()
        else:
            # Lettre incorrecte (Bouton Rouge Néon)
            btn.setStyleSheet("""
                QPushButton:disabled {
                    background-color: #3B0014;
                    color: #FF3264;
                    border: 1.5px solid #FF3264;
                }
            """)
            self.wrong_attempts += 1
            self.drawing_widget.set_attempts(self.wrong_attempts)
            remaining = self.max_attempts - self.wrong_attempts

            if remaining > 0:
                self.status_label.setText(f"Essais restants : {remaining}")
                self.status_label.setStyleSheet("color: #FF9D00;")
            else:
                self.trigger_loss()

    def trigger_win(self):
        self.is_game_over = True
        self.status_label.setText("🎉 BRAVO ! Vous avez trouvé le mot !")
        self.status_label.setStyleSheet("color: #00FF9D; font-size: 16px;")
        self.disable_all_keyboard()

    def trigger_loss(self):
        self.is_game_over = True
        self.word_display_label.setText(" ".join(list(self.word_to_guess)))
        self.status_label.setText(f"❌ DOMMAGE ! Le mot était : {self.word_to_guess}")
        self.status_label.setStyleSheet("color: #FF3264; font-size: 15px;")
        self.disable_all_keyboard()

    def disable_all_keyboard(self):
        for btn in self.keyboard_buttons.values():
            btn.setEnabled(False)

    # --------------------------------------------------------------------------
    # SAISIE CLAVIER PHYSIQUE
    # --------------------------------------------------------------------------
    def keyPressEvent(self, event):
        if self.is_game_over:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                self.start_new_game()
            return

        key_text = event.text().upper()
        if key_text in self.keyboard_buttons and self.keyboard_buttons[key_text].isEnabled():
            self.process_letter(key_text)


# ------------------------------------------------------------------------------
# POINT D'ENTRÉE DU PROGRAMME
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = HangmanGame()
    game.show()
    sys.exit(app.exec_())
# Nama : Valerine Jesika Dewi
# NIM : F1D02310027  
# Kelas : Visual Programming C

# Tugas 2 Week 4- Form Registrasi Multi-Step dengan Progress Bar Kustom

import sys
import re
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel,
    QLineEdit, QRadioButton, QDateEdit, QStackedWidget, QWidget,
    QVBoxLayout, QHBoxLayout, QTextEdit, QPlainTextEdit
)
from PySide6.QtCore import Qt, QDate, Signal, QObject, QRect, QPoint
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QBrush

# menampilkan progress bar di bagian atas form
class StepProgressBar(QWidget):
    def __init__(self, steps_labels, parent=None):
        super().__init__(parent)
        self.steps_labels = steps_labels
        self.current_step = 0
        self.setFixedHeight(80)

    def set_step(self, step_index):
        self.current_step = step_index
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        num_steps = len(self.steps_labels)
        margin = 40
        spacing = (width - 2 * margin) // (num_steps - 1)
        y_center = 35

        painter.setPen(QPen(QColor("#dcdde1"), 4))
        painter.drawLine(margin, y_center, width - margin, y_center)

        if self.current_step > 0:
            painter.setPen(QPen(QColor("#2ecc71"), 4))
            end_x = margin + (self.current_step * spacing)
            painter.drawLine(margin, y_center, end_x, y_center)

        for i in range(num_steps):
            x = margin + (i * spacing)
            is_completed = i < self.current_step
            is_active = i == self.current_step

            circle_color = QColor("#2ecc71") if (is_completed or is_active) else QColor("#dcdde1")
            text_color = QColor("#2ecc71") if (is_completed or is_active) else QColor("#7f8c8d")

            painter.setBrush(QBrush(circle_color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPoint(x, y_center), 18, 18)

            painter.setPen(QPen(Qt.white))
            font = QFont("Arial", 10, QFont.Bold)
            painter.setFont(font)

            if is_completed:
                painter.drawText(QRect(x - 18, y_center - 18, 36, 36), Qt.AlignCenter, "✓")
            else:
                painter.drawText(QRect(x - 18, y_center - 18, 36, 36), Qt.AlignCenter, str(i + 1))

            painter.setPen(QPen(text_color))
            painter.setFont(QFont("Arial", 8))
            label_rect = QRect(x - 50, y_center + 22, 100, 20)
            painter.drawText(label_rect, Qt.AlignCenter, self.steps_labels[i])

# signal system
class FormSignals(QObject):
    step_changed   = Signal(int)
    step_completed = Signal(int, bool)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Form Registrasi Multi-Step")
        self.setFixedSize(450, 600)

        self.signals = FormSignals()
        self.current_step = 0
        self.data = {}

        self._build_ui()
        self._connect_signals()
        self.signals.step_changed.emit(0)

        self.btn_next.setEnabled(False)

    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)
        layout.setContentsMargins(20, 10, 20, 20)

        self.progress_bar = StepProgressBar(["Data Pribadi", "Kontak", "Akun"])
        layout.addWidget(self.progress_bar)

        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        self.stack.addWidget(self._page_step1())
        self.stack.addWidget(self._page_step2())
        self.stack.addWidget(self._page_step3())
        self.stack.addWidget(self._page_review())

        btn_row = QHBoxLayout()
        self.btn_back = QPushButton("← Kembali")
        self.btn_next = QPushButton("Lanjut →")
        self.btn_back.setFixedHeight(38)
        self.btn_next.setFixedHeight(38)
        self.btn_back.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px 15px;")
        self.btn_next.setStyleSheet(
            "background:#3498db; color:white; border-radius:5px; padding:5px 15px; font-weight:bold;"
        )
        btn_row.addWidget(self.btn_back)
        btn_row.addStretch()
        btn_row.addWidget(self.btn_next)
        layout.addLayout(btn_row)

        self.status_label = QLabel("Lengkapi semua field untuk melanjutkan")
        self.status_label.setStyleSheet("color: #888; font-size: 11px;")
        layout.addWidget(self.status_label)

    def _page_step1(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("<b>Step 1: Data Pribadi</b>"))

        layout.addWidget(QLabel("Nama Lengkap"))
        self.input_nama = QLineEdit()
        self.input_nama.setPlaceholderText("Minimal 3 karakter")
        layout.addWidget(self.input_nama)
        self.err_nama = QLabel("")
        self.err_nama.setStyleSheet("color: #e74c3c; font-size: 10px;")
        layout.addWidget(self.err_nama)

        layout.addWidget(QLabel("Tanggal Lahir"))
        self.input_tgl = QDateEdit(QDate(2000, 1, 1))
        self.input_tgl.setCalendarPopup(True)
        layout.addWidget(self.input_tgl)

        layout.addWidget(QLabel("Jenis Kelamin"))
        self.radio_laki = QRadioButton("Laki-laki")
        self.radio_perempuan = QRadioButton("Perempuan")
        self.radio_laki.setChecked(True)
        layout.addWidget(self.radio_laki)
        layout.addWidget(self.radio_perempuan)

        layout.addStretch()
        return page

    def _page_step2(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("<b>Step 2: Informasi Kontak</b>"))

        layout.addWidget(QLabel("Email"))
        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("contoh@email.com")
        layout.addWidget(self.input_email)
        self.err_email = QLabel("")
        self.err_email.setStyleSheet("color: #e74c3c; font-size: 10px;")
        layout.addWidget(self.err_email)

        layout.addWidget(QLabel("Telepon"))
        self.input_telepon = QLineEdit()
        self.input_telepon.setPlaceholderText("Minimal 10 digit angka")
        layout.addWidget(self.input_telepon)
        self.err_telepon = QLabel("")
        self.err_telepon.setStyleSheet("color: #e74c3c; font-size: 10px;")
        layout.addWidget(self.err_telepon)

        layout.addWidget(QLabel("Alamat"))
        self.input_alamat = QPlainTextEdit()
        self.input_alamat.setPlaceholderText("Masukkan alamat lengkap (minimal 10 karakter)")
        self.input_alamat.setFixedHeight(70)
        layout.addWidget(self.input_alamat)
        self.err_alamat = QLabel("")
        self.err_alamat.setStyleSheet("color: #e74c3c; font-size: 10px;")
        layout.addWidget(self.err_alamat)

        layout.addStretch()
        return page

    def _page_step3(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("<b>Step 3: Informasi Akun</b>"))

        layout.addWidget(QLabel("Username"))
        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("Minimal 4 karakter")
        layout.addWidget(self.input_username)
        self.err_username = QLabel("")
        self.err_username.setStyleSheet("color: #e74c3c; font-size: 10px;")
        layout.addWidget(self.err_username)

        layout.addWidget(QLabel("Password"))
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setPlaceholderText("Minimal 8 karakter")
        layout.addWidget(self.input_password)
        self.err_password = QLabel("")
        self.err_password.setStyleSheet("color: #e74c3c; font-size: 10px;")
        layout.addWidget(self.err_password)

        layout.addWidget(QLabel("Konfirmasi Password"))
        self.input_konfirmasi = QLineEdit()
        self.input_konfirmasi.setEchoMode(QLineEdit.Password)
        self.input_konfirmasi.setPlaceholderText("Ulangi password")
        layout.addWidget(self.input_konfirmasi)
        self.err_konfirmasi = QLabel("")
        self.err_konfirmasi.setStyleSheet("color: #e74c3c; font-size: 10px;")
        layout.addWidget(self.err_konfirmasi)

        layout.addStretch()
        return page

    def _page_review(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("<b>Review Data Anda</b>"))
        self.review_box = QTextEdit()
        self.review_box.setReadOnly(True)
        self.review_box.setStyleSheet(
            "background:#f4f4f4; border:1px solid #ddd; border-radius:5px;"
        )
        layout.addWidget(self.review_box)
        return page

    def _connect_signals(self):
        self.btn_next.clicked.connect(self.on_next_clicked)
        self.btn_back.clicked.connect(self.on_back_clicked)
        self.signals.step_changed.connect(self.on_step_changed)
        self.signals.step_completed.connect(self.on_step_completed)

        self.input_nama.textChanged.connect(self.validate_step1)

        self.input_email.textChanged.connect(self.validate_step2)
        self.input_telepon.textChanged.connect(self.validate_step2)
        self.input_alamat.textChanged.connect(self.validate_step2)  

        self.input_username.textChanged.connect(self.validate_step3)
        self.input_password.textChanged.connect(self.validate_step3)
        self.input_konfirmasi.textChanged.connect(self.validate_step3)

    def on_step_changed(self, step: int):
        self.btn_back.setEnabled(step > 0)
        self.progress_bar.set_step(min(step, 2))

        status_msgs = [
            "Lengkapi semua field untuk melanjutkan",
            "Lengkapi semua field untuk melanjutkan",
            "Lengkapi semua field untuk melanjutkan",
            "Periksa data Anda sebelum submit",
        ]
        if step < 4:
            self.status_label.setText(status_msgs[step])

        validators = [self.validate_step1, self.validate_step2, self.validate_step3]
        if step < 3:
            validators[step]()
        else:
            self.btn_next.setEnabled(True)

    def on_next_clicked(self):
        if self.current_step == 0:
            self.data["nama"]          = self.input_nama.text()
            self.data["tanggal_lahir"] = self.input_tgl.date().toString("dd-MM-yyyy")
            self.data["jenis_kelamin"] = "Laki-laki" if self.radio_laki.isChecked() else "Perempuan"

        elif self.current_step == 1:
            self.data["email"]   = self.input_email.text()
            self.data["telepon"] = self.input_telepon.text()
            self.data["alamat"]  = self.input_alamat.toPlainText()

        elif self.current_step == 2:
            self.data["username"] = self.input_username.text()
            self.data["password"] = "••••••••"

        if self.current_step == 3:
            self.status_label.setText("✅ Registrasi berhasil!")
            self.btn_next.setEnabled(False)
            return

        self.current_step += 1
        self.stack.setCurrentIndex(self.current_step)
        self.signals.step_changed.emit(self.current_step)

        if self.current_step == 3:
            self._update_review()
            self.btn_next.setText("✓ Submit")

    def on_back_clicked(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.stack.setCurrentIndex(self.current_step)
            self.signals.step_changed.emit(self.current_step)
            self.btn_next.setText("Lanjut →")

    def on_step_completed(self, step: int, is_valid: bool):
        """Signal handler: enable / disable Next button based on validation result."""
        if self.current_step == step:
            self.btn_next.setEnabled(is_valid)
            if is_valid:
                self.btn_next.setStyleSheet(
                    "background:#3498db; color:white; border-radius:5px;"
                    " padding:5px 15px; font-weight:bold;"
                )
            else:
                self.btn_next.setStyleSheet(
                    "background:#b2bec3; color:white; border-radius:5px;"
                    " padding:5px 15px; font-weight:bold;"
                )

    def _style_input(self, field: QLineEdit, valid: bool, touched: bool):
        """Apply green/red border only when the field has been touched."""
        if not touched:
            field.setStyleSheet("")
            return
        color = "#2ecc71" if valid else "#e74c3c"
        bg    = "#f0fff4" if valid else "#fff5f5"
        field.setStyleSheet(
            f"border: 2px solid {color}; border-radius:5px; padding:4px; background:{bg};"
        )

    def _style_textarea(self, field: QPlainTextEdit, valid: bool, touched: bool):
        if not touched:
            field.setStyleSheet("")
            return
        color = "#2ecc71" if valid else "#e74c3c"
        bg    = "#f0fff4" if valid else "#fff5f5"
        field.setStyleSheet(
            f"border: 2px solid {color}; border-radius:5px; padding:4px; background:{bg};"
        )

    def validate_step1(self):
        nama    = self.input_nama.text()
        touched = len(nama) > 0
        ok      = len(nama.strip()) >= 3

        self._style_input(self.input_nama, ok, touched)
        if touched and not ok:
            self.err_nama.setText("⚠ Nama minimal 3 karakter")
        else:
            self.err_nama.setText("")

        self.signals.step_completed.emit(0, ok)

    def validate_step2(self):
        email   = self.input_email.text()
        telepon = self.input_telepon.text()
        alamat  = self.input_alamat.toPlainText()

        email_ok   = bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$', email))
        phone_ok   = len(re.sub(r'\D', '', telepon)) >= 10
        alamat_ok  = len(alamat.strip()) >= 10

        self._style_input(self.input_email, email_ok, len(email) > 0)
        if len(email) > 0 and not email_ok:
            self.err_email.setText("⚠ Format email tidak valid")
        else:
            self.err_email.setText("")

        self._style_input(self.input_telepon, phone_ok, len(telepon) > 0)
        if len(telepon) > 0 and not phone_ok:
            self.err_telepon.setText("⚠ Nomor telepon minimal 10 digit")
        else:
            self.err_telepon.setText("")

        self._style_textarea(self.input_alamat, alamat_ok, len(alamat) > 0)
        if len(alamat) > 0 and not alamat_ok:
            self.err_alamat.setText("⚠ Alamat minimal 10 karakter")
        else:
            self.err_alamat.setText("")

        self.signals.step_completed.emit(1, email_ok and phone_ok and alamat_ok)

    def validate_step3(self):
        username   = self.input_username.text()
        password   = self.input_password.text()
        konfirmasi = self.input_konfirmasi.text()

        u_ok = len(username) >= 4
        p_ok = len(password) >= 8
        c_ok = (konfirmasi == password) and len(konfirmasi) > 0

        self._style_input(self.input_username, u_ok, len(username) > 0)
        if len(username) > 0 and not u_ok:
            self.err_username.setText("⚠ Username minimal 4 karakter")
        else:
            self.err_username.setText("")

        self._style_input(self.input_password, p_ok, len(password) > 0)
        if len(password) > 0 and not p_ok:
            self.err_password.setText("⚠ Password minimal 8 karakter")
        else:
            self.err_password.setText("")

        self._style_input(self.input_konfirmasi, c_ok, len(konfirmasi) > 0)
        if len(konfirmasi) > 0 and not c_ok:
            self.err_konfirmasi.setText("⚠ Password tidak cocok")
        else:
            self.err_konfirmasi.setText("")

        self.signals.step_completed.emit(2, u_ok and p_ok and c_ok)

    def _update_review(self):
        label_map = {
            "nama":          "Nama Lengkap",
            "tanggal_lahir": "Tanggal Lahir",
            "jenis_kelamin": "Jenis Kelamin",
            "email":         "Email",
            "telepon":       "Telepon",
            "alamat":        "Alamat",
            "username":      "Username",
            "password":      "Password",
        }
        lines = [f"{label_map.get(k, k.upper())}: {v}" for k, v in self.data.items()]
        self.review_box.setText("\n".join(lines))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
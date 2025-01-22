import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QGridLayout, 
                            QGroupBox, QFrame, QHBoxLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class BodyFatCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Body Composition Calculator")
        self.setGeometry(100, 100, 400, 700)
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QWidget {
                font-family: 'Segoe UI', Arial;
                font-size: 12px;
            }
            QGroupBox {
                background-color: #2d2d2d;
                border-radius: 10px;
                margin-top: 12px;
                padding: 15px;
                border: none;
            }
            QGroupBox::title {
                color: #3498db;
                subcontrol-position: top center;
                padding: 3px 20px;
                background-color: #2d2d2d;
                border-radius: 8px;
                font-weight: bold;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #3a3a3a;
                border-radius: 6px;
                background-color: #3a3a3a;
                color: #ffffff;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
                background-color: #424242;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLabel {
                color: #ffffff;
                font-size: 12px;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Title
        title_label = QLabel("Body Composition Calculator")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #3498db; margin-bottom: 10px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Personal Info group
        personal_group = QGroupBox("Personal Information")
        personal_layout = QGridLayout()
        personal_group.setLayout(personal_layout)

        # Name input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")
        personal_layout.addWidget(QLabel("Name:"), 0, 0)
        personal_layout.addWidget(self.name_input, 0, 1)

        # Age input
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Age")
        personal_layout.addWidget(QLabel("Age:"), 1, 0)
        personal_layout.addWidget(self.age_input, 1, 1)

        # Height input
        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("cm")
        personal_layout.addWidget(QLabel("Height:"), 2, 0)
        personal_layout.addWidget(self.height_input, 2, 1)

        # Weight input
        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("kg")
        personal_layout.addWidget(QLabel("Weight:"), 3, 0)
        personal_layout.addWidget(self.weight_input, 3, 1)

        main_layout.addWidget(personal_group)

        # Skinfolds group
        skinfolds_group = QGroupBox("Skinfold Measurements (mm)")
        skinfolds_layout = QGridLayout()
        skinfolds_layout.setSpacing(8)
        skinfolds_group.setLayout(skinfolds_layout)

        self.measurements = {
            'Back': QLineEdit(),
            'Tricep': QLineEdit(),
            'Supra Iliac': QLineEdit(),
            'Abdomen': QLineEdit(),
            'Thighs': QLineEdit(),
            'Calves': QLineEdit()
        }

        for i, (label, input_field) in enumerate(self.measurements.items()):
            row = i // 2
            col = i % 2 * 2
            input_field.setPlaceholderText(label)
            skinfolds_layout.addWidget(input_field, row, col, 1, 2)

        main_layout.addWidget(skinfolds_group)

        # Calculate button
        calc_button = QPushButton("Calculate")
        calc_button.setFixedHeight(35)
        calc_button.clicked.connect(self.calculate)
        main_layout.addWidget(calc_button)

        # Results group
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout()
        results_layout.setSpacing(5)
        results_group.setLayout(results_layout)

        self.result_labels = {
            'name_label': QLabel("Name: --"),
            'age_label': QLabel("Age: --"),
            'bmi_label': QLabel("BMI: --"),
            'bmi_category_label': QLabel("BMI Category: --"),
            'sum_label': QLabel("Sum: --"),
            'bodyfat_label': QLabel("Body Fat: --"),
            'fat_mass_label': QLabel("Fat Mass: --"),
            'lean_mass_label': QLabel("Lean Mass: --")
        }

        for label in self.result_labels.values():
            results_layout.addWidget(label)

        main_layout.addWidget(results_group)

    def calculate_bmi_category(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal weight"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    def calculate(self):
        try:
            # Get personal info
            name = self.name_input.text()
            age = int(self.age_input.text())
            height = float(self.height_input.text()) / 100  # convert cm to meters
            weight = float(self.weight_input.text())
            
            # Calculate BMI
            bmi = weight / (height * height)
            bmi_category = self.calculate_bmi_category(bmi)
            
            # Calculate body fat
            measurements = [float(value.text()) for value in self.measurements.values()]
            total_sum = sum(measurements)
            body_fat_percentage = (0.1051 * total_sum) + 2.585
            fat_mass = (body_fat_percentage / 100) * weight
            lean_mass = weight - fat_mass
            
            # Update results
            self.result_labels['name_label'].setText(
                f"Name: <span style='color: #3498db'>{name}</span>")
            self.result_labels['age_label'].setText(
                f"Age: <span style='color: #3498db'>{age}</span>")
            self.result_labels['bmi_label'].setText(
                f"BMI: <span style='color: #3498db'>{bmi:.1f}</span>")
            self.result_labels['bmi_category_label'].setText(
                f"BMI Category: <span style='color: #3498db'>{bmi_category}</span>")
            self.result_labels['sum_label'].setText(
                f"Sum: <span style='color: #3498db'>{total_sum:.1f} mm</span>")
            self.result_labels['bodyfat_label'].setText(
                f"Body Fat: <span style='color: #3498db'>{body_fat_percentage:.1f}%</span>")
            self.result_labels['fat_mass_label'].setText(
                f"Fat Mass: <span style='color: #3498db'>{fat_mass:.1f} kg</span>")
            self.result_labels['lean_mass_label'].setText(
                f"Lean Mass: <span style='color: #3498db'>{lean_mass:.1f} kg</span>")
            
            for label in self.result_labels.values():
                label.setTextFormat(Qt.TextFormat.RichText)
                
        except ValueError:
            error_msg = "<span style='color: #e74c3c'>Invalid input</span>"
            for label in self.result_labels.values():
                label.setText(error_msg)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BodyFatCalculator()
    window.show()
    sys.exit(app.exec())

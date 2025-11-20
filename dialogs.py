from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QSizePolicy,
    QTextBrowser,
    QVBoxLayout,
)

from .model import AppConfig


class SettingsDialog(QDialog):
    """Application settings (theme, thumbnail size, directories)."""

    def __init__(self, parent, config: AppConfig):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.config = config

        layout = QVBoxLayout(self)

        # Appearance group
        grp_ui = QGroupBox("Appearance && Window")
        ui_layout = QFormLayout()

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["System", "Light", "Dark"])
        self.theme_combo.setCurrentIndex(
            {"system": 0, "light": 1, "dark": 2}.get(self.config.theme, 0)
        )

        self.remember_geom_cb = QCheckBox("Remember window size && position")
        self.remember_geom_cb.setChecked(self.config.remember_geometry)

        self.thumb_combo = QComboBox()
        self.thumb_combo.addItem("Small (25px)", 25)
        self.thumb_combo.addItem("Medium (64px)", 64)
        self.thumb_combo.addItem("Large (128px)", 128)
        idx = {25: 0, 64: 1, 128: 2}.get(self.config.thumb_size, 1)
        self.thumb_combo.setCurrentIndex(idx)

        ui_layout.addRow("Color theme:", self.theme_combo)
        ui_layout.addRow(self.remember_geom_cb)
        ui_layout.addRow("Thumbnail size:", self.thumb_combo)
        grp_ui.setLayout(ui_layout)
        layout.addWidget(grp_ui)

        # Directories group
        grp_dirs = QGroupBox("Directories && Recent Locations")
        dirs_layout = QFormLayout()

        self.remember_add_cb = QCheckBox("Remember last folder for Add")
        self.remember_add_cb.setChecked(self.config.remember_add_dir)

        self.remember_open_cb = QCheckBox("Remember last folder for Open")
        self.remember_open_cb.setChecked(self.config.remember_open_dir)

        self.remember_save_cb = QCheckBox("Remember last folder for Save / Save As")
        self.remember_save_cb.setChecked(self.config.remember_save_dir)

        self.remember_export_cb = QCheckBox("Remember last folder for Export")
        self.remember_export_cb.setChecked(self.config.remember_export_dir)

        dirs_layout.addRow(self.remember_add_cb)
        dirs_layout.addRow(self.remember_open_cb)
        dirs_layout.addRow(self.remember_save_cb)
        dirs_layout.addRow(self.remember_export_cb)
        grp_dirs.setLayout(dirs_layout)
        layout.addWidget(grp_dirs)

        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def apply_changes(self) -> None:
        """Copy UI state back into the AppConfig object."""
        self.config.theme = {
            0: "system",
            1: "light",
            2: "dark",
        }.get(self.theme_combo.currentIndex(), "system")

        self.config.remember_geometry = self.remember_geom_cb.isChecked()
        self.config.thumb_size = self.thumb_combo.currentData()
        self.config.remember_add_dir = self.remember_add_cb.isChecked()
        self.config.remember_open_dir = self.remember_open_cb.isChecked()
        self.config.remember_save_dir = self.remember_save_cb.isChecked()
        self.config.remember_export_dir = self.remember_export_cb.isChecked()


class AboutDialog(QDialog):
    """About dialog with logo, links, and license text."""

    def __init__(self, parent, assets_dir: Path, app_name: str):
        super().__init__(parent)
        self.setWindowTitle(f"About {app_name}")
        self.resize(520, 620)

        layout = QVBoxLayout(self)

        # Logo
        logo_label = QLabel()
        logo_path = assets_dir / "GeeksGIFEditorLogo.png"

        if logo_path.exists():
            from PyQt6.QtGui import QPixmap

            pix = QPixmap(str(logo_path))
            pix = pix.scaled(
                182,
                182,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            logo_label.setPixmap(pix)
            logo_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(logo_label)

        # Title and links
        title = QLabel(f"<h2>{app_name}</h2>")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(title)

        subtitle = QLabel(
            "© 2025 Dom Dominici (@geektoybox)<br>"
            'Website: <a href="https://3dp.lol">3DP.LOL</a><br>'
            'GitHub: <a href="https://github.com/geektoybox/GeeksGIFEditor">'
            "Geek's GIF Editor on GitHub</a>"
        )
        subtitle.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        subtitle.setOpenExternalLinks(True)
        layout.addWidget(subtitle)

        lic_label = QLabel("<b>License (AGPL-3.0-or-later):</b>")
        layout.addWidget(lic_label)

        self.license_view = QTextBrowser()
        self.license_view.setReadOnly(True)
        self.license_view.setOpenExternalLinks(True)
        self.license_view.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        layout.addWidget(self.license_view, 1)

        lic_path = assets_dir.parent / "LICENSE.txt"
        if lic_path.exists():
            try:
                text = lic_path.read_text(encoding="utf-8")
                self.license_view.setPlainText(text)
            except Exception as e:
                self.license_view.setPlainText(f"Error loading license:\n{e}")
        else:
            self.license_view.setPlainText(
                "LICENSE.txt not found.\nPlease add the AGPL license file."
            )

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)
        buttons.accepted.connect(self.accept)
        buttons.button(QDialogButtonBox.StandardButton.Close).clicked.connect(
            self.accept
        )
        layout.addWidget(buttons)

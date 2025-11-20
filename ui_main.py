from __future__ import annotations

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QSplitter,
    QStatusBar,
    QTreeWidget,
    QVBoxLayout,
    QWidget,
    QHeaderView,
)


def build_main_ui(win) -> None:
    """Build the central UI layout for the main window.

    This creates:
    - Left panel with frame list and buttons
    - Right panel with preview and playback controls
    - Status bar
    Widgets are attached as attributes on the window (win).
    """

    # Central widget with horizontal layout
    central = QWidget(win)
    main_layout = QHBoxLayout(central)
    main_layout.setContentsMargins(0, 0, 0, 0)
    win.setCentralWidget(central)

    splitter = QSplitter(Qt.Orientation.Horizontal, central)
    main_layout.addWidget(splitter)

    # ----- Left panel: frame list + controls -----
    left = QWidget(splitter)
    left_layout = QVBoxLayout(left)
    left_layout.setContentsMargins(4, 4, 4, 4)

    win.tree = QTreeWidget(left)
    win.tree.setColumnCount(4)
    win.tree.setHeaderLabels(["", "Thumb", "Filename", "Time (ms)"])
    win.tree.setRootIsDecorated(False)
    win.tree.setAlternatingRowColors(True)
    win.tree.setSelectionMode(QTreeWidget.SelectionMode.SingleSelection)
    win.tree.setIconSize(QSize(win.config.thumb_size, win.config.thumb_size))

    left_layout.addWidget(win.tree)

    # Button row under the list
    btn_row = QHBoxLayout()
    win.btn_add = QPushButton("Add", left)
    win.btn_remove = QPushButton("Remove", left)
    win.btn_duplicate = QPushButton("Duplicate", left)
    win.btn_up = QPushButton("Move Up", left)
    win.btn_down = QPushButton("Move Down", left)
    win.btn_export = QPushButton("Export", left)

    btn_row.addWidget(win.btn_add)
    btn_row.addWidget(win.btn_remove)
    btn_row.addWidget(win.btn_duplicate)
    btn_row.addWidget(win.btn_up)
    btn_row.addWidget(win.btn_down)
    btn_row.addWidget(win.btn_export)

    left_layout.addLayout(btn_row)
    splitter.addWidget(left)

    # ----- Right panel: preview + playback -----
    right = QWidget(splitter)
    right_layout = QVBoxLayout(right)
    right_layout.setContentsMargins(4, 4, 4, 4)

    win.preview_label = QLabel("No frames loaded.", right)
    win.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    win.preview_label.setMinimumSize(200, 200)
    win.preview_label.setStyleSheet(
        "QLabel { background:#202020; color:#c0c0c0; }"
    )
    right_layout.addWidget(win.preview_label, 1)

    # Playback controls
    controls = QHBoxLayout()
    win.btn_play_pause = QPushButton("▶", right)
    win.btn_prev = QPushButton("◀", right)
    win.btn_next = QPushButton("▶", right)

    # Smaller controls
    for btn in (win.btn_play_pause, win.btn_prev, win.btn_next):
        btn.setFixedSize(26, 26)
        btn.setIconSize(QSize(16, 16))

    controls.addWidget(win.btn_play_pause)
    controls.addWidget(win.btn_prev)
    controls.addWidget(win.btn_next)
    controls.addStretch(1)
    right_layout.addLayout(controls)

    # Duration / mode row
    dur_row = QHBoxLayout()
    dur_label = QLabel("Frame duration (ms):", right)
    win.spin_default_dur = QSpinBox(right)
    win.spin_default_dur.setRange(10, 60000)
    win.spin_default_dur.setValue(win.default_duration_ms)

    win.btn_overwrite_all = QPushButton("Overwrite All", right)
    win.mode_combo = QComboBox(right)
    win.mode_combo.addItem("Loop (1,2,3,1,2,3,...)", "loop")
    win.mode_combo.addItem("Wave (1,2,3,2,1,2,3,...)", "wave")

    dur_row.addWidget(dur_label)
    dur_row.addWidget(win.spin_default_dur)
    dur_row.addWidget(win.btn_overwrite_all)
    dur_row.addStretch(1)
    dur_row.addWidget(QLabel("Animation:", right))
    dur_row.addWidget(win.mode_combo)
    right_layout.addLayout(dur_row)

    splitter.addWidget(right)

    # Make left (file list) take ~2/3 of the width
    splitter.setStretchFactor(0, 2)
    splitter.setStretchFactor(1, 1)
    splitter.setSizes([600, 300])

    # Status bar
    status = QStatusBar(win)
    win.setStatusBar(status)
    win.file_label = QLabel("No file loaded.", status)
    status.addPermanentWidget(win.file_label)

    # Basic header behavior; fine-tuned later by apply_config_to_ui
    header = win.tree.header()
    header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
    header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
    header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
    header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

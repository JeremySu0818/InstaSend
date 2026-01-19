from PyQt5.QtGui import QIcon
import sys
import os

# import configparser  # <--- 移除
import time
import random
import subprocess
import urllib.request
import ssl

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QLineEdit,
    QTextEdit,
    QMessageBox,
    QDialog,
    QFormLayout,
    QComboBox,
    QSpinBox,
    QDoubleSpinBox,
    QGroupBox,
    QDialogButtonBox,
    QTabWidget,
    QSizePolicy,
)

# 新增 QSettings, QDialogButtonBox, QTabWidget, QSizePolicy
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize, QSettings

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def is_chrome_installed():
    possible_paths = [
        os.path.join(
            os.environ.get("ProgramFiles(x86)", ""),
            "Google\\Chrome\\Application\\chrome.exe",
        ),
        os.path.join(
            os.environ.get("ProgramFiles", ""),
            "Google\\Chrome\\Application\\chrome.exe",
        ),
        os.path.join(
            os.environ.get("LocalAppData", ""),
            "Google\\Chrome\\Application\\chrome.exe",
        ),
    ]
    return any(os.path.exists(p) for p in possible_paths)


def ensure_chrome_installed_with_ui_prompt(parent=None):
    if is_chrome_installed():
        return
    QMessageBox.information(
        parent,
        "安裝 Chrome",
        "本程式需要 Google Chrome。\n將自動為您下載並安裝，請稍候...",
        QMessageBox.Ok,
    )
    installer_url = "https://dl.google.com/chrome/install/latest/chrome_installer.exe"
    installer_path = os.path.join(os.environ.get("TEMP", "."), "chrome_installer.exe")
    try:
        ssl_ctx = ssl._create_unverified_context()
        with urllib.request.urlopen(installer_url, context=ssl_ctx) as r, open(
            installer_path, "wb"
        ) as f:
            f.write(r.read())
        subprocess.run([installer_path, "/silent", "/install"], check=True)
    except Exception as e:
        QMessageBox.critical(
            parent, "錯誤", f"Chrome 安裝失敗：{e}\n請手動安裝後再試", QMessageBox.Ok
        )
        sys.exit(1)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# CONFIG_FILE = "credentials.txt" # <--- 移除
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

QSS_STYLE = """
QWidget {
    background-color: #1e1e1e;
    color: #f0f0f0;
    font-size: 16px;
    font-family: "Microsoft JhengHei", "Noto Sans TC", Arial;
}

/* ===== 按鈕 ===== */
QPushButton {
    background-color: #2b2b2b;
    color: #f0f0f0;
    border-radius: 8px;
    padding: 8px 18px;
    font-weight: bold;
    font-size: 16px;
    border: 1px solid #3a3a3a;
}
QPushButton:disabled {
    background-color: #2a2a2a;
    color: #888888;
    border: 1px solid #2f2f2f;
}
QPushButton:hover:!disabled {
    background-color: #3d3d3d;
}
QPushButton:pressed {
    background-color: #333333;
}

/* ===== 清單、輸入框 ===== */
QListWidget {
    background: #232323;
    color: #f0f0f0;
    border: 1px solid #3a3a3a;
    font-size: 15px;
    selection-background-color: #3d3d3d;
    selection-color: #ffffff;
}
QLineEdit, QTextEdit {
    background: #262626;
    color: #f0f0f0;
    border: 1px solid #3c3c3c;
    border-radius: 5px;
    font-size: 15px;
    padding: 4px;
}
QLineEdit:focus, QTextEdit:focus {
    border: 1px solid #5a5a5a;
}

/* ===== 標籤與群組框 ===== */
QLabel {
    font-size: 17px;
    font-weight: bold;
}
QGroupBox {
    border: 2px solid #3a3a3a;
    border-radius: 10px;
    margin-top: 12px;
    padding: 6px 6px 8px 6px;
    background-color: #1a1a1a;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    color: #cccccc;
    font-size: 16px;
    font-weight: bold;
    letter-spacing: 1px;
}

/* ===== 下拉選單與數值框 ===== */
QComboBox, QSpinBox, QDoubleSpinBox {
    background: #262626;
    color: #f0f0f0;
    border-radius: 5px;
    border: 1px solid #3c3c3c;
    font-size: 15px;
    padding: 4px 6px;
}
QComboBox:hover, QSpinBox:hover, QDoubleSpinBox:hover {
    border: 1px solid #5a5a5a;
}

/* ===== 分頁標籤 ===== */
QTabBar::tab {
    background: #2b2b2b;
    color: #aaaaaa;
    padding: 6px 14px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    font-weight: bold;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background: #3d3d3d;
    color: #ffffff;
}
QTabBar::tab:hover {
    background: #333333;
    color: #ffffff;
}

/* ===== 額外按鈕樣式 ===== */
QPushButton#togglePasswordBtn {
    padding: 6px 12px;
    font-size: 16px;
    font-weight: bold;
    border-radius: 6px;
    background-color: #2b2b2b;
    border: 1px solid #3a3a3a;
}
QPushButton#togglePasswordBtn:hover {
    background-color: #3d3d3d;
}
"""

# ----- 移除 load_profiles 和 save_profiles 函式 -----
# def load_profiles(config_file): ...
# def save_profiles(config, config_file=CONFIG_FILE): ...


class SendDMThread(QThread):
    status_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    end_signal = pyqtSignal()

    def __init__(self, profile):
        super().__init__()
        self.profile = profile
        self._paused = False
        self._stopped = False

    def run(self):

        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        try:
            driver.get("https://www.instagram.com/")
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            driver.find_element(By.NAME, "username").send_keys(self.profile["username"])
            driver.find_element(By.NAME, "password").send_keys(
                self.profile["password"] + Keys.RETURN
            )
            time.sleep(5)
            self.handle_popup(driver)
            driver.get(self.profile["dm_url"])
            WebDriverWait(driver, 20).until(EC.url_contains("direct/t/"))
            time.sleep(2)
            self.handle_popup(driver)

            messages = [
                line
                for line in self.profile.get("message", "").splitlines()
                if line.strip()
            ]
            if not messages:
                self.error_signal.emit("訊息內容不得為空")
                return
            if self.profile.get("send_mode", "single") == "single":
                messages = [messages[0]]  # 只發第一條

            mode = self.profile.get("send_mode", "single")
            interval_mode = self.profile.get("interval_mode", "fixed")
            # QSettings 會自動轉型，這裡確保它們是正確的型態
            interval = float(self.profile.get("send_interval", "0"))
            interval_min = float(self.profile.get("send_interval_min", "0"))
            interval_max = float(self.profile.get("send_interval_max", "0"))
            count = int(self.profile.get("send_count", "1") or "1")

            if mode == "single":
                loop = 1
            elif mode == "multi":
                loop = count
            elif mode == "infinite":
                loop = float("inf")
            else:
                loop = 1

            msg_index = 0
            msg_count = 0
            while not self._stopped and msg_count < loop:
                if self._paused:
                    self.status_signal.emit("狀態：暫停中")
                    time.sleep(1)
                    continue
                self.status_signal.emit("狀態：運行中")
                msg_count += 1
                try:
                    msg = messages[msg_index]
                    msg_index = (msg_index + 1) % len(messages)
                    box = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//div[@role='textbox' and @aria-label='訊息']")
                        )
                    )
                    box.send_keys(msg)
                    send_btn = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//div[@role='button' and text()='Send']")
                        )
                    )
                    send_btn.click()
                    self.status_signal.emit(f"發送第 {msg_count} 條訊息：{msg}")
                    if msg_count >= loop:
                        break
                    if interval_mode == "fixed":
                        sec = interval
                    else:
                        sec = random.uniform(interval_min, interval_max)
                    if sec > 0:
                        for _ in range(int(sec * 10)):
                            if self._stopped:
                                break
                            time.sleep(0.1)
                    else:
                        if self._stopped:
                            break
                        time.sleep(0)
                except Exception as e:
                    self.error_signal.emit(f"❌ 發送失敗：{e}")
                    break
        finally:
            time.sleep(3)
            driver.quit()
            self.end_signal.emit()

    def pause(self):
        self._paused = True

    def resume(self):
        self._paused = False

    def stop(self):
        self._stopped = True

    def handle_popup(self, driver):
        try:
            btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//button[contains(text(), '稍後再說') or contains(text(), 'Not Now')]",
                    )
                )
            )
            btn.click()
            time.sleep(1)
        except:
            pass


class ProfileDialog(QDialog):
    def __init__(self, parent=None, profile_data=None, title="編輯設定檔"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(560, 500)

        self.tabs = QTabWidget(self)
        self.tab_basic = QWidget()
        self.tab_message = QWidget()
        self.tab_settings = QWidget()
        self.tabs.addTab(self.tab_basic, "基本資料")
        self.tabs.addTab(self.tab_message, "發送訊息")
        self.tabs.addTab(self.tab_settings, "發送設定")

        # === 基本資料分頁 ===
        layout_basic = QFormLayout()
        self.edit_name = QLineEdit()
        self.edit_username = QLineEdit()
        self.edit_password = QLineEdit()
        self.edit_password.setEchoMode(QLineEdit.Password)

        self.toggle_password_btn = QPushButton("顯示")
        self.toggle_password_btn.setObjectName("togglePasswordBtn")
        self.toggle_password_btn.setMinimumWidth(80)
        self.toggle_password_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.toggle_password_btn.clicked.connect(self.toggle_password)

        self.edit_dmurl = QLineEdit()
        self.edit_note = QLineEdit()
        pw_layout = QHBoxLayout()
        pw_layout.setSpacing(8)
        pw_layout.addWidget(self.edit_password, 1)
        pw_layout.addWidget(self.toggle_password_btn, 0)
        layout_basic.addRow("設定檔名稱 *", self.edit_name)
        layout_basic.addRow("Instagram 帳號 *", self.edit_username)
        layout_basic.addRow("Instagram 密碼 *", pw_layout)
        layout_basic.addRow("聊天室 URL *", self.edit_dmurl)
        layout_basic.addRow("聊天室說明", self.edit_note)
        self.tab_basic.setLayout(layout_basic)

        # === 發送訊息分頁 ===
        layout_msg = QVBoxLayout()
        self.edit_message = QTextEdit()
        self.edit_message.setPlaceholderText("請輸入要發送的訊息（多行可循環發送）")
        self.edit_message.setFixedHeight(200)
        layout_msg.addWidget(self.edit_message)
        self.tab_message.setLayout(layout_msg)

        # === 發送設定分頁 ===
        layout_send = QFormLayout()
        self.combo_mode = QComboBox()
        self.combo_mode.addItems(["發送單條", "發送多條", "無限發送"])
        self.spin_count = QSpinBox()
        self.spin_count.setRange(1, 9999)
        self.combo_interval_mode = QComboBox()
        self.combo_interval_mode.addItems(["固定間隔", "亂數間隔"])
        self.spin_interval = QDoubleSpinBox()
        self.spin_interval.setRange(0, 3600)
        self.spin_interval.setSuffix("秒")
        self.spin_interval.setSingleStep(0.5)
        self.spin_interval_min = QDoubleSpinBox()
        self.spin_interval_min.setRange(0, 3600)
        self.spin_interval_min.setSuffix("秒")
        self.spin_interval_min.setSingleStep(0.5)
        self.spin_interval_max = QDoubleSpinBox()
        self.spin_interval_max.setRange(0, 3600)
        self.spin_interval_max.setSuffix("秒")
        self.spin_interval_max.setSingleStep(0.5)
        layout_send.addRow("發送模式 *", self.combo_mode)
        layout_send.addRow("發送條數", self.spin_count)
        layout_send.addRow("間隔模式 *", self.combo_interval_mode)
        layout_send.addRow("固定間隔", self.spin_interval)
        layout_send.addRow("最小間隔", self.spin_interval_min)
        layout_send.addRow("最大間隔", self.spin_interval_max)
        self.tab_settings.setLayout(layout_send)

        # === 底部按鈕列 ===
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        main_layout.addWidget(self.button_box)
        self.setLayout(main_layout)

        # 連動控制
        self.combo_mode.currentIndexChanged.connect(self.on_mode_change)
        self.combo_interval_mode.currentIndexChanged.connect(
            self.on_interval_mode_change
        )
        self.on_mode_change()
        self.on_interval_mode_change()

        if profile_data:
            self.load_profile(profile_data)

    def toggle_password(self):
        if self.edit_password.echoMode() == QLineEdit.Password:
            self.edit_password.setEchoMode(QLineEdit.Normal)
            self.toggle_password_btn.setText("隱藏")
        else:
            self.edit_password.setEchoMode(QLineEdit.Password)
            self.toggle_password_btn.setText("顯示")

    def on_mode_change(self):
        mode_index = self.combo_mode.currentIndex()  # 0:單條, 1:多條, 2:無限
        show_count = mode_index == 1
        self.spin_count.setVisible(show_count)
        label = self.tab_settings.layout().labelForField(self.spin_count)
        if label:
            label.setVisible(show_count)

        show_interval = mode_index != 0
        self.combo_interval_mode.setVisible(show_interval)
        label = self.tab_settings.layout().labelForField(self.combo_interval_mode)
        if label:
            label.setVisible(show_interval)
        self.on_interval_mode_change()

    def on_interval_mode_change(self):
        mode_index = self.combo_mode.currentIndex()
        if mode_index == 0:
            for w in [
                self.spin_interval,
                self.spin_interval_min,
                self.spin_interval_max,
            ]:
                w.setVisible(False)
                label = self.tab_settings.layout().labelForField(w)
                if label:
                    label.setVisible(False)
            return

        is_fixed = self.combo_interval_mode.currentIndex() == 0
        self.spin_interval.setVisible(is_fixed)
        self.spin_interval_min.setVisible(not is_fixed)
        self.spin_interval_max.setVisible(not is_fixed)

        for w, visible in [
            (self.spin_interval, is_fixed),
            (self.spin_interval_min, not is_fixed),
            (self.spin_interval_max, not is_fixed),
        ]:
            label = self.tab_settings.layout().labelForField(w)
            if label:
                label.setVisible(visible)

    def load_profile(self, p):
        SEND_MODES = ["single", "multi", "infinite"]
        INTERVAL_MODES = ["fixed", "random"]
        mode_map = {
            "fixed_count": "multi",
            "single": "single",
            "multi": "multi",
            "infinite": "infinite",
        }
        mode = mode_map.get(p.get("send_mode", "single"), "single")
        interval = (
            p.get("interval_mode", "fixed")
            if p.get("interval_mode", "fixed") in INTERVAL_MODES
            else "fixed"
        )

        self.edit_name.setText(p.get("section", ""))
        self.edit_username.setText(p.get("username", ""))
        self.edit_password.setText(p.get("password", ""))
        self.edit_dmurl.setText(p.get("dm_url", ""))
        self.edit_note.setText(p.get("dm_note", ""))
        self.edit_message.setPlainText(p.get("message", ""))

        self.combo_mode.setCurrentIndex(SEND_MODES.index(mode))
        # QSettings 會自動轉型，但為求保險，仍做轉換
        self.spin_count.setValue(int(p.get("send_count", 1)))
        self.combo_interval_mode.setCurrentIndex(INTERVAL_MODES.index(interval))
        self.spin_interval.setValue(float(p.get("send_interval", 0)))
        self.spin_interval_min.setValue(float(p.get("send_interval_min", 0)))
        self.spin_interval_max.setValue(float(p.get("send_interval_max", 0)))

    def get_profile(self):
        mode_val = ["single", "multi", "infinite"][self.combo_mode.currentIndex()]
        interval_mode_val = ["fixed", "random"][self.combo_interval_mode.currentIndex()]
        message_text = self.edit_message.toPlainText().strip()

        if mode_val == "single" and "\n" in message_text:
            QMessageBox.warning(
                self,
                "提示",
                "您選擇的是『發送單條』模式，但輸入了多行訊息。\n\n系統將只會發送第一行。",
            )

        return {
            "section": self.edit_name.text().strip(),
            "username": self.edit_username.text().strip(),
            "password": self.edit_password.text().strip(),
            "dm_url": self.edit_dmurl.text().strip(),
            "dm_note": self.edit_note.text().strip(),
            "message": message_text,
            "send_mode": mode_val,
            "send_count": self.spin_count.value() if mode_val == "multi" else 1,
            "interval_mode": interval_mode_val,
            "send_interval": self.spin_interval.value(),
            "send_interval_min": self.spin_interval_min.value(),
            "send_interval_max": self.spin_interval_max.value(),
        }


class DMWindow(QWidget):
    STATUS_IDLE = 0
    STATUS_RUNNING = 1
    STATUS_PAUSED = 2
    STATUS_ENDED = 3

    def __init__(self):
        super().__init__()
        time.sleep(0.1)
        self.setWindowIcon(QIcon(resource_path("icon.ico")))
        self.status = self.STATUS_IDLE
        self.setWindowTitle("InstaSend")
        self.setMinimumSize(QSize(650, 520))
        self.setStyleSheet(QSS_STYLE)

        main = QHBoxLayout(self)
        self.profile_list = QListWidget()
        self.profile_list.setFixedWidth(220)
        self.profile_list.itemDoubleClicked.connect(self.edit_profile)
        self.profile_list.currentRowChanged.connect(self.update_buttons)
        main.addWidget(self.profile_list, 1)

        right = QVBoxLayout()
        group_manage = QGroupBox("帳號管理")
        manage_btns = QHBoxLayout()
        self.btn_new = QPushButton("新增")
        self.btn_edit = QPushButton("編輯")
        self.btn_del = QPushButton("刪除")
        manage_btns.addWidget(self.btn_new)
        manage_btns.addWidget(self.btn_edit)
        manage_btns.addWidget(self.btn_del)
        group_manage.setLayout(manage_btns)
        right.addWidget(group_manage)

        group_run = QGroupBox("發送控制")
        run_btns = QHBoxLayout()
        self.btn_send = QPushButton("發送")
        self.btn_pause = QPushButton("暫停")
        self.btn_resume = QPushButton("繼續")
        self.btn_stop = QPushButton("結束")
        run_btns.addWidget(self.btn_send)
        run_btns.addWidget(self.btn_pause)
        run_btns.addWidget(self.btn_resume)
        run_btns.addWidget(self.btn_stop)
        group_run.setLayout(run_btns)
        right.addWidget(group_run)

        right.addSpacing(12)
        self.status_label = QLabel("狀態：未啟動")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFixedHeight(44)
        right.addWidget(self.status_label)
        right.addStretch()
        main.addLayout(right, 0)

        self.btn_new.clicked.connect(self.add_profile)
        self.btn_edit.clicked.connect(self.edit_profile)
        self.btn_del.clicked.connect(self.del_profile)
        self.btn_send.clicked.connect(self.start_dm)
        self.btn_pause.clicked.connect(self.pause_dm)
        self.btn_resume.clicked.connect(self.resume_dm)
        self.btn_stop.clicked.connect(self.stop_dm)

        # ----- 初始化 QSettings -----
        # 參數分別是 組織名稱 和 應用程式名稱
        # 這會決定設定檔的儲存位置
        self.settings = QSettings("MyCompany", "InstaSend")

        self.profile_names = []  # 用來儲存列表中的設定檔名稱，便於索引
        self.refresh_profiles()
        self.active_thread = None
        self.active_profile = None
        self.status = self.STATUS_IDLE
        self.update_buttons()

    def refresh_profiles(self):
        self.profile_list.clear()
        # QSettings.childGroups() 獲取所有頂層群組，即我們的設定檔名稱
        self.profile_names = sorted(self.settings.childGroups())
        for name in self.profile_names:
            # 進入指定群組讀取資料
            self.settings.beginGroup(name)
            # value() 可以有預設值，如果找不到 key
            note = self.settings.value("dm_note", "")
            self.settings.endGroup()  # 讀取完畢後離開群組

            display = name if not note else f"{name}（{note}）"
            self.profile_list.addItem(display)
        self.update_buttons()

    def get_selected_section(self):
        row = self.profile_list.currentRow()
        # 從 self.profile_names 列表中安全地獲取名稱
        if 0 <= row < len(self.profile_names):
            return self.profile_names[row]
        return None

    def add_profile(self):
        dialog = ProfileDialog(self, title="新增設定檔")
        if dialog.exec_():
            d = dialog.get_profile()
            name = d["section"]
            if not all([name, d["username"], d["password"], d["dm_url"], d["message"]]):
                QMessageBox.warning(self, "欄位不完整", "請輸入所有必填欄位。")
                return
            if name in self.settings.childGroups():
                QMessageBox.warning(self, "名稱重複", "此名稱已存在。")
                return

            # 使用 QSettings 寫入資料
            self.settings.beginGroup(name)
            for key, value in d.items():
                if key != "section":  # 不需要把名稱本身存進去
                    self.settings.setValue(key, value)
            self.settings.endGroup()

            self.refresh_profiles()

    def edit_profile(self):
        section = self.get_selected_section()
        if not section:
            QMessageBox.information(self, "請先選擇", "請點選要編輯的設定檔。")
            return

        # 從 QSettings 讀取現有資料
        profile_data = {}
        self.settings.beginGroup(section)
        for key in self.settings.childKeys():
            profile_data[key] = self.settings.value(key)
        self.settings.endGroup()
        profile_data["section"] = section  # 將名稱加回去給對話框顯示

        dialog = ProfileDialog(self, profile_data=profile_data, title="編輯設定檔")
        if dialog.exec_():
            d2 = dialog.get_profile()
            new_section = d2["section"]
            if not all(
                [
                    new_section,
                    d2["username"],
                    d2["password"],
                    d2["dm_url"],
                    d2["message"],
                ]
            ):
                QMessageBox.warning(self, "欄位不完整", "請輸入所有必填欄位。")
                return

            # 如果改了名稱
            if new_section != section:
                if new_section in self.settings.childGroups():
                    QMessageBox.warning(self, "名稱重複", "新的名稱已存在。")
                    return
                # 刪除舊的群組
                self.settings.remove(section)

            # 寫入新的 (或更新的) 資料
            self.settings.beginGroup(new_section)
            for key, value in d2.items():
                if key != "section":
                    self.settings.setValue(key, value)
            self.settings.endGroup()

            self.refresh_profiles()

    def del_profile(self):
        section = self.get_selected_section()
        if not section:
            QMessageBox.information(self, "請先選擇", "請點選要刪除的設定檔。")
            return
        reply = QMessageBox.question(
            self,
            "確定刪除",
            f"確定要刪除 [{section}] 嗎？",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            # 直接移除整個群組
            self.settings.remove(section)
            self.refresh_profiles()

    def start_dm(self):
        section = self.get_selected_section()
        if not section:
            QMessageBox.information(self, "請先選擇", "請點選一個設定檔啟動。")
            return
        if self.active_thread and self.active_thread.isRunning():
            QMessageBox.warning(self, "進程已啟動", "請先停止現有進程。")
            return

        # 從 QSettings 讀取要執行的設定檔資料
        profile_data = {}
        self.settings.beginGroup(section)
        for key in self.settings.childKeys():
            profile_data[key] = self.settings.value(key)
        self.settings.endGroup()

        self.active_profile = profile_data
        self.active_thread = SendDMThread(profile_data)
        self.active_thread.status_signal.connect(self.status_label.setText)
        self.active_thread.error_signal.connect(self.status_label.setText)
        self.active_thread.end_signal.connect(self.on_thread_end)
        self.active_thread.start()
        self.status = self.STATUS_RUNNING
        self.update_buttons()
        self.status_label.setText("狀態：運行中")

    def pause_dm(self):
        if self.active_thread:
            self.active_thread.pause()
            self.status = self.STATUS_PAUSED
            self.update_buttons()
            self.status_label.setText("狀態：暫停中")

    def resume_dm(self):
        if self.active_thread:
            self.active_thread.resume()
            self.status = self.STATUS_RUNNING
            self.update_buttons()
            self.status_label.setText("狀態：運行中")

    def stop_dm(self):
        if self.active_thread:
            self.active_thread.stop()
            self.active_thread.wait()
            self.active_thread = None
            self.status = self.STATUS_ENDED
            self.update_buttons()
            self.status_label.setText("狀態：已結束")

    def on_thread_end(self):
        self.active_thread = None
        self.status = self.STATUS_ENDED
        self.update_buttons()

    def update_buttons(self):
        selected = self.get_selected_section() is not None
        if self.status == self.STATUS_IDLE:
            self.btn_new.setEnabled(True)
            self.btn_edit.setEnabled(selected)
            self.btn_del.setEnabled(selected)
            self.btn_send.setEnabled(selected)
            self.btn_pause.setEnabled(False)
            self.btn_resume.setEnabled(False)
            self.btn_stop.setEnabled(False)
        elif self.status == self.STATUS_RUNNING:
            self.btn_new.setEnabled(False)
            self.btn_edit.setEnabled(False)
            self.btn_del.setEnabled(False)
            self.btn_send.setEnabled(False)
            self.btn_pause.setEnabled(True)
            self.btn_resume.setEnabled(False)
            self.btn_stop.setEnabled(True)
        elif self.status == self.STATUS_PAUSED:
            self.btn_new.setEnabled(False)
            self.btn_edit.setEnabled(False)
            self.btn_del.setEnabled(False)
            self.btn_send.setEnabled(False)
            self.btn_pause.setEnabled(False)
            self.btn_resume.setEnabled(True)
            self.btn_stop.setEnabled(True)
        elif self.status == self.STATUS_ENDED:
            self.btn_new.setEnabled(True)
            self.btn_edit.setEnabled(selected)
            self.btn_del.setEnabled(selected)
            self.btn_send.setEnabled(selected)
            self.btn_pause.setEnabled(False)
            self.btn_resume.setEnabled(False)
            self.btn_stop.setEnabled(False)

    def showEvent(self, event):
        self.update_buttons()
        super().showEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(QSS_STYLE)
    ensure_chrome_installed_with_ui_prompt(parent=None)
    window = DMWindow()
    window.show()
    sys.exit(app.exec_())

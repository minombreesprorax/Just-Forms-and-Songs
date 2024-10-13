import sys
import configparser
from typing import Tuple, Iterable, Optional
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTreeWidgetItem
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt
from modules.ui import Ui_MainWindow
from modules import game

class App(QMainWindow, Ui_MainWindow):
    def __init__(self, modList: Optional[Iterable[Tuple[str, str, str]]] = None):
        super(App, self).__init__()
        self.setupUi(self)
        
        self.modList = modList if modList else []
        self.populate_level_select()

        # Connect "Launch" button to a method
        self.Launch.clicked.connect(self.launch_game)

        # Connect selection change signal
        self.LevelList.selectionModel().selectionChanged.connect(self.update_line_edit)

    def populate_level_select(self):
        """Populate LevelList with level information from each .ini file in modList."""
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Load Id", "Song Name", "Author", "Difficulty", "Game Version"])

        for i in range(len(self.modList)):
            mod = self.modList[i]
            csv_path, ini_path, wav_path = mod
            level_info = self.read_level_info_from_ini(ini_path)

            if level_info:
                id_item = QStandardItem(f"{i}")
                level_name_item = QStandardItem(level_info["SongName"])
                author_item = QStandardItem(level_info["LevelAuthor"])
                difficulty_item = QStandardItem(str(level_info["Difficulty"]))
                game_version_item = QStandardItem(str(level_info["GameVersion"]))
                
                # Set the flags to make items non-editable
                id_item.setEditable(False)
                level_name_item.setEditable(False)
                author_item.setEditable(False)
                difficulty_item.setEditable(False)
                game_version_item.setEditable(False)

                model.appendRow([id_item, level_name_item, author_item, difficulty_item, game_version_item])

        self.LevelList.setModel(model)

    def read_level_info_from_ini(self, ini_path: str) -> Optional[dict]:
        """Reads level information from the provided .ini file."""
        config = configparser.ConfigParser()
        try:
            config.read(ini_path)
            return {
                "SongName": config.get('LevelInfo', 'SongName', fallback="Unknown"),
                "LevelAuthor": config.get('LevelInfo', 'LevelAuthor', fallback="Unknown"),
                "Difficulty": config.getint('LevelInfo', 'Difficulty', fallback=0),
                "GameVersion": config.get('LevelInfo', 'GameVersion', fallback="Unknown"),
            }
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to read {ini_path}: {e}")
            return None

    def update_line_edit(self):
        """Updates the QLineEdit with the selected Load Id."""
        index = self.LevelList.currentIndex()
        if index.isValid():
            # Get the row of the current index
            row = index.row()
            # Access the model
            model = self.LevelList.model()
            # Get the Load Id from the first column (column 0)
            load_id_item = model.item(row, 0)  # 0 is the column index for Load Id
            # Set the Load Id to the lineEdit
            self.lineEdit.setText(load_id_item.text())

    def launch_game(self):
        """Handles the 'Launch' button click."""
        level_id = self.lineEdit.text()
        
        # Get the model from the LevelList
        model = self.LevelList.model()
        
        # Check if the level_id is valid
        is_valid_id = False
        for row in range(model.rowCount()):
            id_item = model.item(row, 0)  # Get the item in the first column (Load Id)
            if id_item.text() == level_id:
                is_valid_id = True
                break

        if not is_valid_id:
            if id_item.text() == "":
                QMessageBox.warning(self, "Warning", "Please select a level.")
            else:
                QMessageBox.warning(self, "Warning", "Invalid level ID!")
        else:
            self.hide()
            try:
                game.loadLevel(self.modList[int(level_id)])
            except ValueError as e:
                QMessageBox.critical(self, "Error", f"Value Error during deserialization: {e}", QMessageBox.StandardButton.Close)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Exception during execution: {e}", QMessageBox.StandardButton.Close)
            finally:
                sys.exit()
            

def main(modList: Optional[Iterable[Tuple[str, str]]] = None): 
    # Example modList format: [("path\\level1.csv", "path\\level1.ini"), ("path\\level2.csv", "path\\level2.ini")]
    app = QApplication(sys.argv)
    
    window = App(modList=modList)
    window.show()
    
    sys.exit(app.exec())

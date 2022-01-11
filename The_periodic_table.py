import sys
import random
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from periodic_table_template import TPoE_MainWindow
from Elements_info_template import Ui_Form


class TreasureVault(QWidget):
    def __init__(self):
        super().__init__()


class ElementInfo(QWidget, Ui_Form):
    def __init__(self, element):
        super().__init__()
        self.element_symbol = element
        self.setupUi(self)
        self.setWindowTitle(f'{self.element_symbol}-brief information')
        self.con = sqlite3.connect('El_info.db')
        self.cur = self.con.cursor()
        self.initUi()

    def initUi(self):
        self.picture.setText(self.element_symbol)

        ar = str(*self.cur.execute(f"""SELECT ram FROM information
        WHERE id=(SELECT id FROM Idname
        WHERE symbol = '{self.element_symbol}')""").fetchall()[0])
        if str(*self.cur.execute(f"""SELECT stable FROM information
        WHERE id=(SELECT id FROM Idname
        WHERE symbol = '{self.element_symbol}')""").fetchall()[0]) == 'False':
            ar = f'[{int(float(ar))}]'
        self.ar_data_label.setText(str(ar))

        info = str(*self.cur.execute(f"""SELECT info FROM information
        WHERE id=(SELECT id FROM Idname
        WHERE symbol='{self.element_symbol}')""").fetchall()[0]) + '\n' +\
            str(*self.cur.execute(f"""SELECT quote FROM information
        WHERE id=(SELECT id FROM Idname
        WHERE symbol='{self.element_symbol}')""").fetchall()[0])
        self.interesting_facts_label.setText(info)

        self.name_data_label.setText(str(*self.cur.execute(f"""
        SELECT name FROM information
        WHERE id=(SELECT id FROM Idname
        WHERE symbol = '{self.element_symbol}')""").fetchall()[0]))
        electroneg = self.cur.execute(f"""
        SELECT electronegativity FROM information
        WHERE
        id=(SELECT id FROM Idname
        WHERE symbol = '{self.element_symbol}')""").fetchall()[0][0]
        if electroneg == 0.0:
            electroneg = '-'
        self.electronegativity_data_label.setText(str(electroneg))

        self.config_data_label.setText(str(*self.cur.execute(f"""SELECT config FROM information
        WHERE
        id=(SELECT id FROM Idname
        WHERE symbol='{self.element_symbol}')""").fetchall()[0]))

        self.type_data_label.setText(str(*self.cur.execute(f"""SELECT type FROM information
        WHERE
        id=(SELECT id FROM Idname
        WHERE symbol='{self.element_symbol}')""").fetchall()[0]))

        self.ox_states_data.setText(str(*self.cur.execute(f"""SELECT oxidation_states FROM information
        WHERE
        id=(SELECT id FROM Idname
        WHERE symbol='{self.element_symbol}')""").fetchall()[0]))

        link = str(*self.cur.execute(f"""SELECT wiki FROM information
        WHERE
        id=(SELECT id FROM Idname
        WHERE symbol = '{self.element_symbol}')""").fetchall()[0])

        self.quote_label.setText(f'<a href={link}>{"Read more"}</a>')
        self.show()


class PToE(QMainWindow, TPoE_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect('El_info.db')
        self.cur = self.con.cursor()
        self.elements = self.cur.execute("""SELECT symbol FROM Idname""").fetchall()
        self.elements = [i[0] for i in self.elements]
        self.buttons = [self.btn_1,
                        self.btn_2,
                        self.btn_3,
                        self.btn_4, self.btn_5,
                        self.btn_6, self.btn_7, self.btn_8, self.btn_9, self.btn_10,
                        self.btn_11, self.btn_12, self.btn_13, self.btn_14, self.btn_15,
                        self.btn_16, self.btn_17, self.btn_18, self.btn_19, self.btn_20,
                        self.btn_21, self.btn_22, self.btn_23, self.btn_24, self.btn_25,
                        self.btn_26, self.btn_27, self.btn_28, self.btn_29, self.btn_30,
                        self.btn_31, self.btn_32, self.btn_33, self.btn_34, self.btn_35,
                        self.btn_36, self.btn_37, self.btn_38, self.btn_39, self.btn_40,
                        self.btn_41, self.btn_42, self.btn_43, self.btn_44, self.btn_45,
                        self.btn_46, self.btn_47, self.btn_48, self.btn_49, self.btn_50,
                        self.btn_51, self.btn_52, self.btn_53, self.btn_54, self.btn_55,
                        self.btn_56, self.btn_57, self.btn_58, self.btn_59, self.btn_60,
                        self.btn_61, self.btn_62, self.btn_63, self.btn_64, self.btn_65,
                        self.btn_66, self.btn_67, self.btn_68, self.btn_69, self.btn_70,
                        self.btn_71, self.btn_72, self.btn_73, self.btn_74, self.btn_75,
                        self.btn_76, self.btn_77, self.btn_78, self.btn_79, self.btn_80,
                        self.btn_81, self.btn_82, self.btn_83, self.btn_84, self.btn_85,
                        self.btn_86, self.btn_87, self.btn_88, self.btn_89, self.btn_90,
                        self.btn_91, self.btn_92, self.btn_93, self.btn_94, self.btn_95,
                        self.btn_96, self.btn_97, self.btn_98, self.btn_99, self.btn_100,
                        self.btn_101, self.btn_102, self.btn_103, self.btn_104, self.btn_105,
                        self.btn_106, self.btn_107, self.btn_108, self.btn_109, self.btn_110,
                        self.btn_111, self.btn_112, self.btn_113, self.btn_114, self.btn_115,
                        self.btn_116, self.btn_117, self.btn_118]
        self.active_windows = []
        self.initUi()

    def initUi(self):
        for i in self.buttons:
            i.clicked.connect(self.showInfo)
        self.rnd_element_btn.clicked.connect(self.get_rnd_element)

    def showInfo(self, *args):
        element = self.sender().text()
        info = ElementInfo(element)
        self.active_windows.append(info)

    def get_rnd_element(self):
        el = random.choice(self.elements)
        info = ElementInfo(el)
        self.active_windows.append(info)


app = QApplication(sys.argv)
pt = PToE()
pt.show()
sys.exit(app.exec())

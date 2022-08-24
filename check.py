"""
The module checks input values
of left and right borders of the frequency band.
It returns the boolean if the necessary condition is true or false.
"""
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox


# todo: check_value
def check_value(line_1: str, line_2: str) -> bool:
    """
    checks if values are eligible for further plots
    :return: left and right borders of a chosen frequency band from the second window
    """
    left_border = float(line_1)
    right_border = float(line_2)
    return 0 <= left_border < right_border


# todo: error_window
def error_window():
    """
    pop-up warning window about incorrect format of input values
    :return: None
    """
    icon = QIcon('icon.png')
    error_head = 'Input Error!'
    msg = 'First value must be 0 or positive of float type,' \
          '\nSecond value must be positive of float type and bigger than the first!'
    msg_question = QMessageBox()
    msg_question.setWindowTitle(error_head)
    msg_question.setWindowIcon(icon)
    msg_question.setIcon(QMessageBox.Icon.Warning)
    msg_question.setText(msg)
    msg_question.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg_question.buttonClicked.connect(msg_button)
    msg_question.exec()


# todo: msg_button
def msg_button():
    """
    realises closing pop-up window
    :param: None
    :return: None
    """
    pass

from PyQt5.QtWidgets import QDesktopWidget


def centrar_ventana(window):
    dim_ventana = window.frameGeometry()
    centro_monitor = QDesktopWidget().availableGeometry().center()
    dim_ventana.moveCenter(centro_monitor)
    window.move(dim_ventana.topLeft())


stylesheet = """
QScrollArea > QWidget > QWidget
{
    background: none;
    border: 0px;
    margin: 0px 0px 0px 0px;
}

 QScrollBar:vertical
 {
     background-color: #2A2929;
     width: 15px;
     margin: 15px 3px 15px 3px;
     border: 1px transparent #2A2929;
     border-radius: 4px;
 }
 QScrollBar::handle:vertical
 {
     background-color: BLACK;
     min-height: 5px;
     border-radius: 4px;
 }
 QScrollBar::sub-line:vertical
 {
     margin: 3px 0px 3px 0px;
     border-image: url(Recursos/arrow_up.jpg);
     height: 10px;
     width: 10px;
     subcontrol-position: top;
     subcontrol-origin: margin;
 }
 QScrollBar::add-line:vertical
 {
     margin: 3px 0px 3px 0px;
     border-image: url(Recursos/arrow_down.jpg);
     height: 10px;
     width: 10px;
     subcontrol-position: bottom;
     subcontrol-origin: margin;
 }
 QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on
 {
     border-image: url(Recursos/arrow_up.jpg);
     height: 10px;
     width: 10px;
     subcontrol-position: top;
     subcontrol-origin: margin;
 }
 QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on
 {
     border-image: url(Recursos/arrow_down.jpg);
     height: 10px;
     width: 10px;
     subcontrol-position: bottom;
     subcontrol-origin: margin;
 }
 QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
 {
     background: none;
     border-radius: 4px;
     min-height: 5px;
 }
 QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
 {
     background: none;
     border-radius: 4px;
     min-height: 5px;
 }
"""
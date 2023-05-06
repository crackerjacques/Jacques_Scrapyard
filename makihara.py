import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QSlider, QComboBox, QPushButton
from PySide6.QtCore import Qt
import mido

# Mackie control test script

class MackieControlFader(QWidget):
    def __init__(self, *args, **kwargs):
        super(MackieControlFader, self).__init__(*args, **kwargs)
        self.init_ui()
        self.init_midi()  
        self.update_fader_range()  

    def init_midi(self):
        available_ports = mido.get_output_names()
        selected_port_index = self.port_edit.value() - 1  

        if 0 <= selected_port_index < len(available_ports):
            out_port_name = available_ports[selected_port_index]
            self.out_port = mido.open_output(out_port_name)
        else:
            print(f"Invalid port number. Please select a port number between 1 and {len(available_ports)}")

    def init_ui(self):
        self.setWindowTitle('Mackie Control Fader')

        vbox = QVBoxLayout()

        form_layout = QHBoxLayout()

        form_layout.addWidget(QLabel('Port:'))
        self.port_edit = QSpinBox()
        self.port_edit.setRange(1, 16)
        form_layout.addWidget(self.port_edit)
        self.port_edit.valueChanged.connect(self.init_midi)

        form_layout.addWidget(QLabel('Channel:'))
        self.channel_edit = QSpinBox()
        self.channel_edit.setRange(1, 16)
        form_layout.addWidget(self.channel_edit)

        form_layout.addWidget(QLabel('Type:'))
        self.type_combobox = QComboBox()
        self.type_combobox.addItems(['control_change', 'note_on', 'note_off', 'pitchwheel', 'aftertouch', 'polytouch'])
        form_layout.addWidget(self.type_combobox)

        form_layout.addWidget(QLabel('CC/Note:'))
        self.cc_edit = QSpinBox()
        self.cc_edit.setRange(0, 127)
        form_layout.addWidget(self.cc_edit)

        form_layout.addWidget(QLabel('Value Range:'))
        self.value_range_combobox = QComboBox()
        self.value_range_combobox.addItems([f"{i} bit" for i in range(1, 17)])
        form_layout.addWidget(self.value_range_combobox)

        vbox.addLayout(form_layout)


        self.fader = QSlider(Qt.Orientation.Horizontal)
        self.update_fader_range()  
        self.fader.valueChanged.connect(self.send_mackie_control_message)

        vbox.addWidget(self.fader)

        button_layout = QHBoxLayout()
        self.plus_button = QPushButton("+")
        self.plus_button.clicked.connect(lambda: self.fader.setValue(self.fader.value() + 1))
        button_layout.addWidget(self.plus_button)

        self.minus_button = QPushButton("-")
        self.minus_button.clicked.connect(lambda: self.fader.setValue(self.fader.value() - 1))
        button_layout.addWidget(self.minus_button)

        vbox.addLayout(button_layout)

        self.setLayout(vbox)


        self.value_range_combobox.currentIndexChanged.connect(self.update_fader_range)

    def update_fader_range(self):
        bit_ranges = {f"{i} bit": (0, 2**i - 1) for i in range(1, 17)}
        bit_ranges["14 bit"] = (0, 16383)  

        value_range = self.value_range_combobox.currentText()
        min_value, max_value = bit_ranges[value_range]

        self.fader.setMinimum(min_value)
        self.fader.setMaximum(max_value)

    def send_mackie_control_message(self, value):
        try:
            port = self.port_edit.value()
            channel = self.channel_edit.value() - 1
            msg_type = self.type_combobox.currentText().strip()
            cc_or_note = self.cc_edit.value()

            if self.out_port is not None:
                if msg_type in ['control_change', 'note_on', 'note_off', 'aftertouch', 'polytouch']:
                    msg = mido.Message(msg_type, control=cc_or_note, value=value, channel=channel)
                elif msg_type == 'pitchwheel':
                    
                    value = value - 8192
                    msg = mido.Message(msg_type, pitch=value, channel=channel)
                self.out_port.send(msg)
                print(f'Sent: {msg}')
        except ValueError:
            
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MackieControlFader()
    w.show()

    sys.exit(app.exec())

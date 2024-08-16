




class Chart:
    def __init__(self, data, title, x_label, y_label):
        self.data = data
        self.title = title
        self.x_label = x_label
        self.y_label = y_label

    def generate(self):
        pass

    def build(self):
        print(f"Building the chart with title: {self.title}, x_label: {self.x_label}, y_label: {self.y_label}")
        self.generate()
        print("Chart built successfully.")

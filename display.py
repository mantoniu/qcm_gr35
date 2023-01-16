from display_types import Display_types

class Display():
    def __init__(self, display_type: Display_types, display_coding: str = "", displays: list = []) -> None:
        self.display_type = display_type
        self.display_coding = display_coding
        self.displays = displays
        if (self.display_type == Display_types.CONTAINER):
            pass
        elif (self.display_type == Display_types.MARKDOWN):
            pass

    def get_display_str(self):
        result = ""
        if (self.display_type == Display_types.CONTAINER):
            for display in self.displays:
                result += display
        elif (self.display_type == Display_types.MARKDOWN):
            pass
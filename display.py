from __future__ import annotations
from display_types import Display_types
from re import finditer

class Display():
    def __init__(self, display_type: Display_types, display_coding: str = "") -> None:
        self.display_type = display_type
        self.display_coding = display_coding
        self.displays = []
        if (self.display_type == Display_types.CONTAINER):
            pass
        elif (self.display_type == Display_types.MARKDOWN):
            pass
    
    def add_display(self, display: Display) -> None:
        if (self.display_type == Display_types.CONTAINER):
            self.displays.append(display)

    def get_display_str(self) -> str:
        result = ""
        if (self.display_type == Display_types.CONTAINER):
            for display in self.displays:
                result += display.get_display_str()
            return result
        elif (self.display_type == Display_types.MARKDOWN):
            return self.display_coding
        elif (self.display_type == Display_types.MERMAID):
            return "<div class='mermaid'>" + self.display_coding + "</div>"
    
    @staticmethod
    def analyse_markdown(markdown: str) -> Display:
        container = Display(Display_types.CONTAINER)
        blocks_pos = [m.start() for m in finditer("```", markdown)]
        mermaid_pos = [m.start() for m in finditer("mermaid", markdown)]
        start_index = 0
        for pos in blocks_pos:
            if pos + 3 in mermaid_pos:
                if pos - 1 >= 0:
                    container.add_display(Display(Display_types.MARKDOWN, markdown[start_index:pos-1]))
                print(blocks_pos.index(pos) + 1)
                print(blocks_pos)
                end_pos = blocks_pos[blocks_pos.index(pos) + 1]
                if end_pos + 3 not in mermaid_pos:
                    container.add_display(Display(Display_types.MERMAID, display_coding=markdown[pos+10:end_pos-1]))
                    start_index = end_pos + 4
                else:
                    return "Erreur : un Mermaid est peut être mal fermé."
        if start_index < len(markdown):
            container.add_display(Display(Display_types.MARKDOWN, markdown[start_index:]))
        return container
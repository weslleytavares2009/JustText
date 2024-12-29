from app.app import App
from src.utils.keybinds import Keybinds

app: App = App("JustText")
keybinds: Keybinds = Keybinds(app)

app.mainloop()

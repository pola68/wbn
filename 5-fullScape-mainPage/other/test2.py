from webkit2png import WebkitRenderer, init_qtgui
from PyQt4.QtCore import QTimer

def renderer_func():   
    renderer = WebkitRenderer()
    renderer.width = 800
    renderer.height = 600
    renderer.timeout = 10
    renderer.wait = 1
    renderer.format = "png"
    renderer.grabWholeWindow = False

    outfile = open("stackoverflow.png", "w")
    renderer.render_to_file(url="http://stackoverflow.com", file=outfile)
    outfile.close()

app = init_qtgui()
QTimer.singleShot(0, renderer_func)
sys.exit(app.exec_())
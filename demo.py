from bespoken import ui
from bespoken.tools.filesystem import FileTool
from bespoken.config import DEBUG_MODE

ui.print("Hello, World!")
ui.print_empty_line()
fs = FileTool("demo.py")
ui.print_empty_line()

fs.read_file()
ui.start_streaming()
ui.stream("yes this is so important")
ui.end_streaming()
ui.start_streaming()
ui.stream("yes this is so important")
ui.end_streaming()
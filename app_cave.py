from FUTIL.my_logging import *
my_logging(console_level = DEBUG, logfile_level = INFO, details = True)

from pages.index import layout_index
import callbacks
from app import app,server

app.layout = layout_index

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', dev_tools_hot_reload = False)
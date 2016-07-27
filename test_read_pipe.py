import time
from system_start import read_pipe

while True:

    state = read_pipe(4, 5)
    print state
    time.sleep(1)

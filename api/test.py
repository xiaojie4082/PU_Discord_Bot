import requests
import time
start_time = time.time()
gs = requests.post('http://localhost:5000/gschat', json={'message':"嗨，你好嗎？"})
end_time = time.time()
print(gs.text)
print("Time taken: ", end_time-start_time)
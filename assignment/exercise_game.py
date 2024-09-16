"""
Response time - single-threaded
"""

from machine import Pin
import time
import random
import json
import urequests

N: int = 3 #change this number to 3 to save time for testing
sample_ms = 10.0
on_ms = 500
t_new = []

def random_time_interval(tmin: float, tmax: float) -> float:
    """return a random time interval between max and min"""
    return random.uniform(tmin, tmax)


def blinker(N: int, led: Pin) -> None:
    # %% let user know game started / is over

    for _ in range(N):
        led.high()
        time.sleep(0.1)
        led.low()
        time.sleep(0.1)


def write_json(json_filename: str, data: dict) -> None:
    """Writes data to a JSON file.

    Parameters
    ----------

    json_filename: str
        The name of the file to write to. This will overwrite any existing file.

    data: dict
        Dictionary data to write to the file.
    """

    with open(json_filename, "w") as f:
        json.dump(data, f)

def sender(data: dict, json_filename: str, UID: str) -> None:
    url = "https://mini-mt-default-rtdb.firebaseio.com/UID/" + UID + "/" + json_filename
    response = urequests.put(url, json=data)
    print(response.status_code)
    
    response.close()
    

def scorer(t: list[int | None]) -> None:
    # %% collate results
    min_score = 0
    max_score = 0
    average = 0
    
    misses = t.count(None)
    print(f"You missed the light {misses} / {len(t)} times")

    t_good = [x for x in t if x is not None]

    #print(t_good)

    
    t_new = [i for i in t if i is not None] #removes "none" from list so we can calculate min, max and avg

    if len(t_new) != 0:  #if t_new is NOT empty do the calulations 
        min_score = min(t_new) # type: ignore #reads array and stores smallest value
        max_score = max(t_new) # type: ignore #reads array and stores largest value
        average = sum(t_new)/len(t_new) #type: ignore #sum of array over lenght of array
        average = round(average) #rounds the average to an integer
   
    # add key, value to this dict to store the minimum, maximum, average response time
    # and score (non-misses / total flashes) i.e. the score a floating point number
    # is in range [0..1]

    data = {'min': min_score,
            'max': max_score,
            'average': average,
            'score': (N-misses)/N
            }
    
    # %% make dynamic filename and write JSON

    now: tuple[int] = time.localtime()

    now_str = "-".join(map(str, now[:3])) + "T" + "_".join(map(str, now[3:6]))
    filename = f"score-{now_str}.json"

    #print("write", filename)
    #print(data)

    if len(t_new) == 0: #if t_new is empty print one thing else print the other thing
     print('You missed every click!')
    else:
        print("Fastest response time: " + str(min_score)) #prints minimum value of data
        print("Slowest response time: " + str(max_score)) #prints maximum value of data
        print("Average response time: " + str(average)) #prints average response time
    
    exUID = "qN9nGtRMvVdXcqmQpCmdLRrJlkv1";
    sender(data, filename, exUID)
    #write_json(filename, data)
    

if __name__ == "__main__":
    # using "if __name__" allows us to reuse functions in other script files

    led = Pin("LED", Pin.OUT)
    button = Pin(15, Pin.IN, Pin.PULL_UP)

    t: list[int | None] = []

    blinker(3, led)

    for i in range(N):
        time.sleep(random_time_interval(0.5, 5.0))

        led.high()

        tic = time.ticks_ms()
        t0 = None
        while time.ticks_diff(time.ticks_ms(), tic) < on_ms:
            if button.value() == 0:
                t0 = time.ticks_diff(time.ticks_ms(), tic)
                led.low()
                break
        t.append(t0)

        led.low()

    blinker(5, led)

    scorer(t)

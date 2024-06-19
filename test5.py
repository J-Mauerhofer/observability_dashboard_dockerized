import re

def extract_stats():

    with open(r'C:\Users\Julian Seminar\Desktop\read.txt', 'r') as file:
        raw_string = file.read()

    # Regex pattern to capture stats of this individual, namely id, rank, fitness, distance, and code 

    #write this into a file for debugging purposes
    #with open(r'C:\Users\Julian Seminar\Desktop\write.txt', 'w') as file:
        #file.write("raw string: \n\n\n" + self.raw_string) 

    match = re.search(r'\{ "id": "([a-zA-Z0-9\-]+)", "rank": (-?\d+), "fitness": (\d+(\.\d+)?), "distance": (\d+(\.\d+)?), "code":\{(.*?)\}\n\}', raw_string, re.DOTALL)
    #match = re.search(r'\{ "id": "([a-zA-Z0-9\-]+)", "rank": (\d+), "fitness": (\d+(\.\d+)?), "distance": (\d+(\.\d+)?), "code":\{(.*?)\}\n\}', raw_string, re.DOTALL)
    
    
    #match = re.search(r'\{ "id": ([a-zA-Z0-9\-]+), "rank": (\d+), "fitness": (\d+(\.\d+)?), "distance": (\d+(\.\d+)?), "code":\{(.*?)\} \}', self.raw_string, re.DOTALL)

    if match:

        #stats = {"id": match.group(1), "rank": int(match.group(2)), "fitness": float(match.group(3)), "distance": float(match.group(5)), "code": match.group(7)}
        with open(r'C:\Users\Julian Seminar\Desktop\write.txt', 'w') as file:
            file.write("success")

        #return stats
    else:
        raise ValueError(f"No match found for individual stats in individual with raw_string{raw_string}")
    

print("start")
extract_stats()
print("end")
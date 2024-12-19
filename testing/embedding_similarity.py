import numpy as np
import json

resume_name = "embedding_resume.json"
job_names = ["job_{}.json".format(i) for i in range(3)]

def get_vector(name):
    with open(name, "r") as f:
        data = json.load(f)
        vector = np.array(data["data"][0]["embedding"])
    
    return vector

rv = get_vector(resume_name)

for job_name in job_names:
    jv = get_vector(job_name)
    similarity = np.dot(rv, jv) / (np.linalg.norm(rv) * np.linalg.norm(jv))
    print(similarity)

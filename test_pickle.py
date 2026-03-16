import pickle

with open("movie_dict.pkl", "rb") as f:
    data = pickle.load(f)

print(type(data))

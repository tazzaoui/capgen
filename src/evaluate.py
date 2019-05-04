import json
import pickle
from nltk.tokenize import word_tokenize
from nltk.translate.bleu_score import sentence_bleu

from filepaths import *
from inference import get_caption

def compute_bleu(real, pred, n=4):
    weights = (1.0 / n,) * n 
    pred = " ".join(pred.split()[1:-2])
    pred = [i for i in word_tokenize(pred.lower()) if i.isalpha()] 
    real = [i for i in word_tokenize(real.lower()) if i.isalpha()] 
    score = sentence_bleu([real], pred, weights=weights) 
    return score

def generate_index():
    with open(VAL_CAP_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    imgs = data["images"]
    caps = data["annotations"]

    print("Generating Index...")
    index = {}
    for c in caps:
        id = c["image_id"]
        if id not in index:
            index[id] = list()
        index[id].append(c["caption"])

    img_caps = list()

    for i in imgs: 
        id = i["id"]
        file_name = i["file_name"]
        caps = index[id]
        caps.sort(key=len)
        img_caps.append((id, file_name, caps[0]))

    return index, img_caps

if __name__ == "__main__":

    index, img_caps = generate_index()
    results_path = os.path.join(DATA_PATH, "results.pkl")
    
    if not os.path.exists(results_path):
        i = 0
        num_res = 1000
        results = {}
        for (id, file_name, cap) in image_caps:
            i += 1
            path = os.path.join(VAL_IMG_DIR, file_name)
            try:
                pred_cap = get_caption(path)
            except RuntimeError:
                print("ERROR!")
                continue
            results[id] = (pred_cap, cap)
            if i >= num_res: break
        
        with open(results_path, "wb") as f:
            pickle.dump(results, f)

    else:
        with open(results_path, "rb") as f:
            results = pickle.load(f)
    
    bleu_scores = [0, 0, 0, 0] 
    for n in range(1, 5):
        for res in results: 
            (real_cap, pred_cap) = results[res]
            all_caps = index[res]
            scores = []
            for cap in all_caps:
                score = compute_bleu(pred_cap, cap, n)
                scores.append(score if score else 0)
            bleu_scores[n - 1] += (sum(scores) / len(scores)) 
        bleu_scores[n - 1] /= len(results)

    print("Scores = {}".format(bleu_scores))

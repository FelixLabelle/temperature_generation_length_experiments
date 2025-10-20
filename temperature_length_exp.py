import csv
import json
import itertools
import os
import time
from pathlib import Path
from typing import List, Dict

import pandas as pd
import requests
from tqdm.auto import tqdm

# NOTE: You need to have an env.py file with these variables
# defined or otherwise define them here
from env import api_key, base_url

def load_prompts(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path, dtype=str)
    if not {"prompt_id", "prompt_text"}.issubset(df.columns):
        raise ValueError("Input CSV must contain columns: prompt_id,prompt_text")
    return df[["prompt_id", "prompt_text"]]


def make_completion(
    prompt: str,
    temperature: float,
    seed : int,
    model: str,
    base_url: str = base_url,
) -> Dict:
    system_prompt = (
        "You are a creative writing assistant. "
        "Write a story using the following prompt."
    )
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,          # adjust as needed
        "n": 1,
        "stop": None,
        "seed" : seed,
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    url = f"{base_url}/chat/completions"

    resp = requests.post(url, headers=headers, json=data)
    resp.raise_for_status()
    return resp.json()


def extract_response_and_tokens(response_json: Dict) -> (str, int):
    content = response_json["choices"][0]["message"]["content"].strip()
    usage = response_json.get("usage", {})
    total_tokens = usage.get("completion_tokens", -1)

    return content, total_tokens

if __name__ == "__main__":
    # define variables for sweep
    models = ["llama-3.2-1b-instruct", "llama-3.2-3b-instruct", "meta-llama-3-8b-instruct" ]
    restart_pos = 0 # used this variable to skip ahead if there was a model crash
    num_divisions = 5
    temperatures = [(1/num_divisions) * i for i in range(2*num_divisions + 1)]
    max_tokens = 2048
    seeds = [686579303, 119540831, 26855092, 796233790, 295310485, 262950628, 239670711, 149827706, 790779946, 110053353, 726600539, 795285932, 957970516, 585582861, 93349856, 634036506, 453035110, 34126396, 31994523, 100604502]
    input_csv: str = "data/sample_prompts.csv"          # must contain prompt_id,prompt_text
    output_csv: str = "results/results_temperature_experiment_v2.csv"
    
    # load data
    prompts_df = load_prompts(input_csv)
    results: List[Dict] = []

    # create experiments with different variables
    experiments = [tpl for tpl in itertools.product(models,prompts_df.iterrows(),temperatures, enumerate(seeds))]
    total_runs = len(experiments)
    pbar = tqdm(total=total_runs, desc="Running experiments")
    
    # run experiments
    count = 0
    for exp_idx, (model,(_,row), temp, (seed_pos, seed)) in enumerate(experiments):
        if exp_idx < restart_pos:
            count += 1
            pbar.update(1)
            continue
        # skips multiple seeds for temperature == 0
        if temp == 0.0 and seed_pos > 0:
            continue
            
        prompt_id = row["prompt_id"]
        prompt_text = row["prompt_text"]

        try:
            resp_json = make_completion(
                prompt=prompt_text,
                temperature=temp,
                seed=seed,
                model=model,
                base_url=BASE_URL,
            )
            response_text, tokens_used = extract_response_and_tokens(resp_json)

            results.append(
                {
                    "prompt_id": prompt_id,
                    "temperature": temp,
                    "response_text": response_text,
                    "usage_tokens": tokens_used,
                    "model" : model,
                    "seed" : seed,
                }
            )

        except Exception as e:
            results.append(
                {
                    "prompt_id": prompt_id,
                    "prompt_text": prompt_text,
                    "temperature": temp,
                    "response_text": None,
                    "usage_tokens": None,
                    "model" : model,
                    "seed" : seed,
                    "error" : str(e),
                }
            )

        count += 1
        pbar.update(1)
        if count % 20 == 0:
            output_df = pd.DataFrame(results)
            output_df.to_csv(output_csv, index=False)
    pbar.close()

    output_df = pd.DataFrame(results)
    output_df.to_csv(output_csv, index=False)

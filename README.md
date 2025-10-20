# temperature_generation_length_experiments  

Code that runs an experiment to check if **temperature** when decoding a language model influences the **number of tokens a model generates**.

## Overview  
* Generate a sampled dataset of prompts
* Run prompts through an OpenAI compatible API at several temperatures and other variables 
* Record how many tokens are produced for each run and analyze the relationship 
* Output a markdown report and plots in results

## Repository structure  

```
temperature_generation_length_experiments/
│
├─ data/                     # automatically created; holds the generated prompts
│   └─ sample_prompts.csv # data file
│
├─ env.py                    # → edit your API credentials & base URL here
│
├─ sample_dataset_generator.py  # creates `data/sample_dataset.json`
│
├─ temperate_length_exp.py       # main experiment driver (calls the API)
│
└─ analysis.py                # builds markdown report with tables + graphs
```



## How to run  

*All scripts are self contained and can be executed directly from the command line.*  

1. **Set your credentials**  
   ```python
   # env.py
   base_url = "https://api.openai.com/v1"
   api_key  = "sk-YOUR_API_KEY"
   ```

2. **Generate a sample dataset**
   ```bash
   python sample_dataset_generator.py
   ```
   → `data/sample_prompts.csv` is created.

3. **Run the temperature experiments**  
   ```bash
   python temperate_length_exp.py
   ```
   The script will iterate over a predefined list of temperatures (e.g., `[0.0, 0.5, 1.0]`), models, and write results to `results.csv`.

4. **Produce the analysis report**  
   ```bash
   python analysis.py
   ```
   This reads `results.csv` and writes `temperature_experiment_report.md`, which contains:
   * Summary statistics (mean/median & std of tokens per temperature)  
   * Correlation coefficient (Spearman)  
   * Plots and md report (saved as PNGs and md in the results directory)
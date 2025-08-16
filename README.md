# DS207AppliedMachineLearning
UC Berkeley Masters of Data Science course DS207: Applied Machine Learning

# w207FinalProject

# California Wage Prediction

## Motivation 
Income inequality is a persistent issue in the U.S., with implications for policy, economic development, and social justice. Using demographic and economic data from the American Community Survey (ACS), our goal is to build predictive models that estimate an individual's income level based on key attributes.

This question is not only socially relevant but also technically interesting due to the high-dimensional, categorical nature of survey data. Previous work has used regression-based or tree-based models, but few have conducted extensive experimentation with tuned models, ensemble learning or blended models with detailed hyperparameter analysis.

### Our Plan:
- Use California ACS PUMS "person" data filtered for working-age adults with wages.
- Conduct Exploratory Data Analysis (EDA) and feature engineering.
- Build a series of models: baseline models (KNN, Polynomial regression), tree-based models (Random Forest, XGBoost, LGBM, CatBoost).
- Tune and evaluate models using R² and accuracy.
- Share insights from modeling experiments and hyperparameter tuning.

## Data 
We use the **ACS Public Use Microdata Sample (PUMS)** for California, provided by the U.S. Census Bureau. The dataset includes responses from a representative sample of individuals and covers four domains:
- Social
- Economic
- Housing
- Demographic

### Filters Applied:
- `AGE >= 18`
- `WAGE > 0` and `< 684,000` (to avoid top-coded data)

### Preprocessing:
- Categorical encoding (Label Encoding / One-Hot)
- Handling missing values
- Feature transformations (e.g., log-wage)
- Derived features (e.g., age groups, education levels, race)

## Modeling 
We developed and evaluated **10+ modeling pipelines**, including:

### 🔹 Baseline Classical and Preliminary Models::
- **K-Nearest Neighbors (KNN):** A non-parametric model used for early benchmarking.
- **Polynomial Regression:** Applied to capture non-linear trends and tested on the transformed wage feature.

### 🔹 Tree-Based Models:
- Random Forest (basic and tuned)
- XGBoost (binary and regression targets)
- LightGBM (with blend models)
- CatBoostRegressor with hyperparameter search

### See Notebooks:
All models and experiments are located in the [`california_wage_prediction_model/`](california_wage_prediction_model/) folder and organized sequentially.

## Experiments
We ran extensive hyperparameter tuning across tree-based models:

- **Random Forest:** tuned `n_estimators`, `max_depth`
- **XGBoost:** used log-transformed target, tuned `learning_rate`, `max_depth`, `n_estimators`
- **LGBM and CatBoost:** explored regularization and depth vs iteration tradeoffs

Our best XGBoost configuration from grid search was:
- `max_depth=6`
- `learning_rate=0.05`
- `n_estimators=300`

This configuration was selected based on the highest test R² score (0.9115), as shown in the hyperparameter tuning slide.

### Key Results:
| Model                            | R² Score | Notes                                                         |
|----------------------------------|----------|---------------------------------------------------------------|
| K-Nearest Neighbors (KNN)        | -0.73    | Overfit due to memorization effect, poor generalization |
| Polynomial Regression            | 0.73     | Best performing baseline, non-linear fit with 7-degree tuning |
| Random Forest (Tuned)            | 0.628    | Best non-boosted tree model            |
| CatBoostRegressor (Tuned)        | 0.60     | Strong regularized performance         |
| LGBM                             | 0.637    | Efficient with large dataset and hyperparameter tuning |
| XGBoost                          | 0.71     | Strong results, though tuning was time-intensive        |
| XGB-LGBM Blend                   | 0.64     | Blending showed minimal gains, added complexity         |
| XGBoost (Final Tuned)            | **0.91** | Best performing model after log transformation, outlier handling, and imbalance correction |


Tuning comparisons are available in:
- `california_wage_prediction_model/03_*` to `08_*` and  `XGBoostFinal*`


## Conclusions 
- Feature engineering (e.g., combining top features, removing less impactful ones) helped improve the signal.
- Tree-based models outperformed classical models consistently.
- Hyperparameter tuning was especially effective for XGBoost, leading to a significant jump in R² from ~0.63 to **0.91**.
- Imbalance correction by undersampling low-wage categories created a more even distribution and helped generalization.
- Log-transforming the target wage improved error stability.
- Ensemble blending did not improve performance beyond tuned XGBoost.
- Extreme wage outliers still present a challenge and future iterations should improve this further.

### Future Work:
- Incorporate household-level data and cost-of-living adjustments.
- Try deep learning models or automated feature engineering tools.
- Explore fairness metrics across demographic subgroups.

## Code Submission
All code is available in this repository:
- [`california_wage_prediction_model/`](california_wage_prediction_model/): Filtered input dataset, Modeling experiments, Reusable preprocessing, modeling, and utility functions


---

## How to Run This Project
1. Clone the repo:
   ```bash
   git clone https://github.com/UC-Berkeley-I-School/w207FinalProject.git
   cd w207FinalProject


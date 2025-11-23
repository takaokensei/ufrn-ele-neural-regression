<div align="center">
  <img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=1a1a2e&height=120&section=header"/>
  
  <h1>
    <img src="https://readme-typing-svg.herokuapp.com/?lines=Neural+Regression+Analysis;K-Fold+Cross-Validation;Boston+Housing+Dataset;MLOps+Best+Practices&font=Fira+Code&center=true&width=600&height=50&color=4A90E2&vCenter=true&pause=1000&size=24" />
  </h1>
  
  <samp>UFRN · Electrical Engineering · Neural Networks Laboratory</samp>
  <br/><br/>
  
  <img src="https://img.shields.io/badge/Python-3.12-4A90E2?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/PyTorch-2.0.1-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white"/>
  <img src="https://img.shields.io/badge/Status-Complete-00C853?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/License-Academic-1a1a2e?style=for-the-badge"/>
</div>

<br/>

## `> project.overview()`

```python
class NeuralRegressionProject:
    def __init__(self):
        self.title = "Generalization Analysis in Neural Networks"
        self.task = "Real Estate Price Regression"
        self.dataset = "Boston Housing (506 instances, 13 features)"
        self.institution = "UFRN - Federal University of Rio Grande do Norte"
        self.author = "Cauã Vitor Figueredo Silva"
        self.student_id = "20220014216"
        self.date = "November 2025"
        self.python_version = "3.12"
    
    def architecture(self):
        return {
            "type": "Multi-Layer Perceptron (MLP)",
            "layers": [13, 64, 32, 1],
            "activation": "ReLU",
            "optimizer": "Adam (lr=0.001)",
            "loss": "Mean Squared Error"
        }
    
    def mlops_practices(self):
        return [
            "K-Fold Cross-Validation (K=5)",
            "Early Stopping (patience=20)",
            "Model Checkpointing",
            "Data Leakage Prevention",
            "Reproducibility (Fixed Seeds)",
            "Modular Code Architecture"
        ]
```

<br/>

## `> tech_stack`

<div align="center">
  <img src="https://skillicons.dev/icons?i=python,pytorch,sklearn,git,latex,github&theme=dark&perline=6" />
</div>

<table align="center">
<tr>
<td align="center" width="33%">
<strong>🧠 Deep Learning</strong><br/><br/>
<img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white"/>
<img src="https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white"/>
<img src="https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white"/>
</td>
<td align="center" width="33%">
<strong>📊 ML Pipeline</strong><br/><br/>
<img src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white"/>
<img src="https://img.shields.io/badge/Matplotlib-11557c?style=flat-square"/>
<img src="https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white"/>
</td>
<td align="center" width="33%">
<strong>🔧 Documentation</strong><br/><br/>
<img src="https://img.shields.io/badge/LaTeX-008080?style=flat-square&logo=latex&logoColor=white"/>
<img src="https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white"/>
<img src="https://img.shields.io/badge/Markdown-000000?style=flat-square&logo=markdown&logoColor=white"/>
</td>
</tr>
</table>

<br/>

## `> project_structure`

```
ufrn-ele-neural-regression/
│
├── 📊 data/
│   ├── raw/                    # Boston Housing CSV
│   └── processed/              # Normalized datasets
│
├── 🧠 src/
│   ├── dataset.py              # Data loading & PyTorch Dataset
│   ├── model.py                # MLP architecture
│   ├── train.py                # Training loops & validation
│   └── visualization.py        # Loss curves & scatter plots
│
├── 📓 notebooks/
│   └── project_main.ipynb      # Complete experimental workflow
│
├── 💾 models/                  # Best model checkpoints (per fold)
├── 📄 reports/                 # LaTeX documentation & figures
│
├── requirements.txt
├── .gitignore
└── README.md
```

<br/>

## `> methodology`

<table align="center">
<tr>
<td width="50%">
<h3 align="center">📐 Cross-Validation Strategy</h3>
<p align="center">
<img src="https://img.shields.io/badge/K--Fold-5_Splits-4A90E2?style=for-the-badge"/>
</p>
<p><samp><strong>Stratified K-Fold</strong> ensures each fold serves as validation set exactly once, preventing data leakage and providing robust performance estimates.</samp></p>

```python
from sklearn.model_selection import KFold

kf = KFold(n_splits=5, shuffle=True, 
           random_state=42)
for fold, (train_idx, val_idx) in 
    enumerate(kf.split(X)):
    # Train & validate
```
</td>
<td width="50%">
<h3 align="center">🛡️ Data Leakage Prevention</h3>
<p align="center">
<img src="https://img.shields.io/badge/StandardScaler-Isolated-00C853?style=for-the-badge"/>
</p>
<p><samp><strong>Normalization within folds</strong> ensures validation data never influences training statistics, maintaining true generalization measurement.</samp></p>

```python
scaler = StandardScaler()
# Fit ONLY on training data
X_train = scaler.fit_transform(X_train)
# Transform validation (no fit)
X_val = scaler.transform(X_val)
```
</td>
</tr>
</table>

<br/>

## `> model_architecture`

<div align="center">

```mermaid
graph TD
    A[Input Layer<br/>13 Features] --> B[Hidden Layer 1<br/>64 Neurons + ReLU]
    B --> C[Hidden Layer 2<br/>32 Neurons + ReLU]
    C --> D[Output Layer<br/>1 Neuron Linear]
    
    style A fill:#4A90E2,stroke:#1a1a2e,stroke-width:2px,color:#fff
    style B fill:#00C853,stroke:#1a1a2e,stroke-width:2px,color:#fff
    style C fill:#00C853,stroke:#1a1a2e,stroke-width:2px,color:#fff
    style D fill:#EE4C2C,stroke:#1a1a2e,stroke-width:2px,color:#fff
```

</div>

<table align="center">
<tr>
<td align="center"><strong>Parameter</strong></td>
<td align="center"><strong>Value</strong></td>
<td align="center"><strong>Justification</strong></td>
</tr>
<tr>
<td align="center">Optimizer</td>
<td align="center"><code>Adam</code></td>
<td align="center">Adaptive learning rate</td>
</tr>
<tr>
<td align="center">Learning Rate</td>
<td align="center"><code>0.001</code></td>
<td align="center">Stable convergence</td>
</tr>
<tr>
<td align="center">Loss Function</td>
<td align="center"><code>MSE</code></td>
<td align="center">Regression task</td>
</tr>
<tr>
<td align="center">Batch Size</td>
<td align="center"><code>16</code></td>
<td align="center">Small dataset efficiency</td>
</tr>
<tr>
<td align="center">Early Stopping</td>
<td align="center"><code>patience=20</code></td>
<td align="center">Overfitting prevention</td>
</tr>
</table>

<br/>

## `> installation`

```bash
# Clone repository
git clone https://github.com/yourusername/ufrn-ele-neural-regression.git
cd ufrn-ele-neural-regression

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter
jupyter notebook notebooks/project_main.ipynb
```

<br/>

## `> dataset_analysis`

<div align="center">

| Feature | Description | Type |
|---------|-------------|------|
| `CRIM` | Per capita crime rate | Continuous |
| `ZN` | Residential land zoned for large lots | Continuous |
| `INDUS` | Non-retail business acres proportion | Continuous |
| `CHAS` | Charles River proximity | Binary |
| `NOX` | Nitric oxides concentration | Continuous |
| `RM` | Average rooms per dwelling | Continuous |
| `AGE` | Pre-1940 owner-occupied units | Continuous |
| `DIS` | Distance to employment centers | Continuous |
| `RAD` | Highway accessibility index | Discrete |
| `TAX` | Property tax rate | Continuous |
| `PTRATIO` | Pupil-teacher ratio | Continuous |
| `B` | Proportion of Black residents | Continuous |
| `LSTAT` | Lower status population % | Continuous |
| **`MEDV`** | **Median home value ($1000s)** | **Target** |

<img src="https://img.shields.io/badge/Instances-506-4A90E2?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Features-13-00C853?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Target-Continuous-EE4C2C?style=for-the-badge"/>

</div>

<br/>

## `> expected_results`

<table align="center">
<tr>
<td width="50%" align="center">
<h3>📈 Learning Curves</h3>
<p><samp>Training and validation loss converging smoothly without significant gap, indicating proper generalization.</samp></p>
<br/>
<img src="https://img.shields.io/badge/Target-Convergence-4A90E2?style=flat-square"/>
<img src="https://img.shields.io/badge/No-Overfitting-00C853?style=flat-square"/>
</td>
<td width="50%" align="center">
<h3>🎯 Prediction Accuracy</h3>
<p><samp>Scatter plot showing predictions closely aligned with identity line (y=x), demonstrating model reliability.</samp></p>
<br/>
<img src="https://img.shields.io/badge/MSE-<_20.0-4A90E2?style=flat-square"/>
<img src="https://img.shields.io/badge/R²-High-00C853?style=flat-square"/>
</td>
</tr>
</table>

<br/>

## `> development_timeline`

<div align="center">

```mermaid
gantt
    title Project Development Phases
    dateFormat  YYYY-MM-DD
    section Infrastructure
    Project Setup           :done, 2025-11-01, 2d
    Data Loading Module     :done, 2025-11-03, 2d
    section Model
    MLP Architecture        :done, 2025-11-05, 2d
    Preprocessing Pipeline  :done, 2025-11-07, 2d
    section Training
    K-Fold Implementation   :done, 2025-11-09, 3d
    Early Stopping          :done, 2025-11-12, 2d
    Model Checkpointing     :done, 2025-11-14, 1d
    section Optimization
    Hyperparameter Tuning   :done, 2025-11-15, 2d
    Visualization Module    :done, 2025-11-17, 2d
    section Documentation
    LaTeX Report            :done, 2025-11-19, 3d
    Final Analysis          :done, 2025-11-22, 2d
```

</div>

<br/>

## `> future_enhancements`

<table align="center">
<tr>
<td align="center" width="25%">
<strong>🏗️ Architecture</strong><br/><br/>
<samp>
• Deeper networks (3+ layers)<br/>
• Residual connections<br/>
• Batch normalization
</samp>
</td>
<td align="center" width="25%">
<strong>🎛️ Regularization</strong><br/><br/>
<samp>
• Dropout layers<br/>
• L2 weight decay<br/>
• Data augmentation
</samp>
</td>
<td align="center" width="25%">
<strong>🔍 Analysis</strong><br/><br/>
<samp>
• SHAP values<br/>
• Feature importance<br/>
• Sensitivity analysis
</samp>
</td>
<td align="center" width="25%">
<strong>🚀 Deployment</strong><br/><br/>
<samp>
• FastAPI REST API<br/>
• Docker containerization<br/>
• MLflow tracking
</samp>
</td>
</tr>
</table>

<br/>

## `> citation`

```bibtex
@misc{silva2025neuralregression,
  author       = {Silva, Cauã Vitor Figueredo},
  title        = {Neural Regression with K-Fold Cross-Validation: 
                  Generalization Analysis for Real Estate Price Prediction},
  year         = {2025},
  institution  = {Federal University of Rio Grande do Norte},
  department   = {Electrical Engineering},
  type         = {Academic Project}
}
```

<br/>

## `> contact`

<div align="center">
  
  <strong>Cauã Vitor Figueredo Silva</strong>
  <br/>
  <samp>Student ID: 20220014216</samp>
  <br/>
  <samp>Department of Electrical Engineering</samp>
  <br/>
  <samp>Federal University of Rio Grande do Norte (UFRN) 🇧🇷</samp>
  
  <br/><br/>
  
  <a href="mailto:cauavitorfigueredo@gmail.com">
    <img src="https://img.shields.io/badge/-Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white"/>
  </a>
  <a href="https://github.com/takaokensei">
    <img src="https://img.shields.io/badge/-GitHub-181717?style=for-the-badge&logo=github&logoColor=white"/>
  </a>
  <a href="https://www.linkedin.com/in/cauã-vitor-7bb072286/">
    <img src="https://img.shields.io/badge/-LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white"/>
  </a>

</div>

<br/>

<div align="center">
  <img src="https://img.shields.io/badge/Made_with-PyTorch_❤️-EE4C2C?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/For-Academic_Research-4A90E2?style=for-the-badge"/>
</div>

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=1a1a2e&height=100&section=footer"/>
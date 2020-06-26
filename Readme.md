# Adversarial Attacks & Defences on Phishing Detection Model

## Introduction
Here we introduce a new adversarial attack called 'Feature Importance Guided Method' (FIGM). It is basically a white-box attack which aims at breaking the integrity of the model and cause misprediction of phishing samples. The dataset used contains HTML-based features of a website obtained through crawling and feature extraction of legitimate (Majestic Million) and phishing (PhishTank) websites.

## Code Overview
We attack a decision tree based phishing detection model built using Scikit-Learn which is used to predict phishing websites. The attack we  performed is called ‘Feature Importance Guided Method’ (FIGM). ‘adv_attack_train.py’ contains the class ‘FeatureImportanceAttack’ for launching FIGM. Here we use ‘Gini-importance’ to identify the most important features in our dataset. Along with that we generate an attack direction vector ‘sorted_attack_dir’  (sorted based on feature importance hight to low) by taking the difference in median of feature values between legitimate and phishing samples in the training set. This gives the direction that each feature has to be perturbed to make it more legitimate.

For attacking the model an attacker can choose two parameters; ‘ε’ (the total percentage of the site to modify) and ‘n’ (the number of features to perturb), which controls the strength of the attack. First we transform the data using ‘Min_Max’ scaler into a scaled feature space in order to ensure that each feature will be perturbed proportionally to its magnitude. Then we find a perturbation amount ‘e_budjet’ by taking sum of the feature values of the phishing sample and multiply it by (n/ε). This is now relative to both the number of features we will perturb and the total feature
magnitude of the site and is evenly distributed across the number of features. Then we update each feature individually according to their corresponding feature directions. Any resultant feature value less than 0 is kept 0 to avoid negative values. After that we take the inverse transform of the data and round down any feature which increased in size and round up any feature which decreased in size. This will guarantee that the perturbation is <= ε; the desired site perturbation percentage. 

Next stage is performing ‘Adversarial Training’ to understand its effectiveness against FIGM. Here we train the model with adversarial samples created using FIGM and then test the effectiveness of the attack on the model.

## Pre-requisites 
```bash
    • Conda
    • Jupyter Notebook
    • Sklearn
    • Python (>= 3.6)
    • Numpy
    • Pandas 
    • Matplotlib
    • Seaborn
    • Itertools
    • Importlib
```

## Scripts & Usage
The functions defined in the class ‘FeatureImportanceAttack’ in ‘adv_attack_train.py’ is used to launch FIGM and to perform adversarial training. 
Following are the steps  :

  
``` python                                                                                       
import importlib                                                                                   
import adv_attack_train as adt                                                                  
``` 
                                                                                                      

```python
attack = adt.FeatureImportanceAttack(<input dataset>) # training of model
attack.feat_imp() # feature importance & attack direction
```


```python
#--------------------------Attack ------------------------------#
attack.get_baseline_test_scores()
attack.adv_attack(ε,n) # attack.adv_attack(0.1,4)
attack.get_attack_score()
```


```python
#------------------Adv Training-------------------------------#
attack.adv_training(ε,n) 
attack.get_baseline_test_scores()
attack.adv_attack(ε,n)
attack.get_attack_score()

```



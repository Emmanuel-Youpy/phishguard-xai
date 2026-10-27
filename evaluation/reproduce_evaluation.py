#!/usr/bin/env python3
"""Independent, safe reconstruction of a PhishGuard URL-only model evaluation.

Does NOT unpickle, load, modify or execute either saved project model or notebook.

Use: python PhishGuard_XAI_v28_Reproduce_Evaluation.py \
  --input data/processed/phishing_url_features_v2.csv --output results/reproduced_v28

This is a *new* controlled experiment, not proof of the original deployed model's
training recipe or performance. In particular, no group/temporal/external test is claimed.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import platform
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import (accuracy_score, balanced_accuracy_score,
                             confusion_matrix, precision_recall_fscore_support,
                             roc_auc_score, roc_curve)
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_sample_weight

FEATURES = [
    'url_length','domain_length','path_length','query_length','tld_length',
    'subdomain_count','is_domain_ip','digit_count','letter_count','dot_count',
    'hyphen_count','underscore_count','slash_count','question_mark_count',
    'equals_count','ampersand_count','at_symbol_count','percent_count',
    'special_char_count','is_https'
]

def run(input_csv:Path, out:Path) -> dict:
    out.mkdir(parents=True,exist_ok=True)
    source = pd.read_csv(input_csv)
    expected=set(FEATURES+['label'])
    if set(source.columns) != expected:
        raise ValueError('Unexpected CSV columns: '+str(set(source.columns)^expected))
    if source.isna().any().any():
        raise ValueError('Missing entries; cannot reproduce specified preprocessing')
    if set(source.label.unique()) != {0,1}:
        raise ValueError('Unexpected labels; expected 0=phishing,1=legitimate')
    # Exclude *all* feature patterns that have contradictory labels, rather than
    # arbitrarily picking one, then take one representative of each remaining.
    distinct = source.drop_duplicates(subset=FEATURES+['label']).copy()
    counts = distinct.groupby(FEATURES,dropna=False)['label'].transform('nunique')
    clean = distinct.loc[counts==1].drop_duplicates(subset=FEATURES).copy()
    assert not clean.duplicated(subset=FEATURES).any()
    X=clean[FEATURES]
    y=clean['label'].astype(int)
    X_train,X_test,y_train,y_test=train_test_split(
        X,y,test_size=0.2,stratify=y,random_state=42)
    weights=compute_sample_weight(class_weight='balanced',y=y_train)
    model=HistGradientBoostingClassifier(
        max_iter=200,learning_rate=0.1,random_state=42)
    model.fit(X_train,y_train,sample_weight=weights)
    y_pred=model.predict(X_test)
    y_prob=model.predict_proba(X_test)
    phishing_idx=list(model.classes_).index(0)
    phishing_prob=y_prob[:,phishing_idx]
    cm=confusion_matrix(y_test,y_pred,labels=[0,1])
    precision,recall,f1,_=precision_recall_fscore_support(
        y_test,y_pred,labels=[0,1],zero_division=0)
    roc=roc_auc_score((y_test==0).astype(int),phishing_prob)
    results={
        'experiment_type':'independent reconstruction; NOT a verification of saved model',
        'source_input':str(input_csv),
        'source_sha256':hashlib.sha256(input_csv.read_bytes()).hexdigest(),
        'input_rows':int(len(source)),
        'original_label_counts':{str(k):int(v) for k,v in source.label.value_counts().sort_index().items()},
        'distinct_feature_patterns':int(source[FEATURES].drop_duplicates().shape[0]),
        'conflicting_feature_patterns':int((distinct.groupby(FEATURES)['label'].nunique()==2).sum()),
        'cleaned_rows':int(len(clean)),
        'cleaned_label_counts':{str(k):int(v) for k,v in y.value_counts().sort_index().items()},
        'train_rows':int(len(X_train)),'test_rows':int(len(X_test)),
        'test_label_counts':{str(k):int(v) for k,v in y_test.value_counts().sort_index().items()},
        'split':'80:20 stratified; random_state=42; unique feature patterns before splitting',
        'model':'HistGradientBoostingClassifier(max_iter=200,learning_rate=0.1,random_state=42)',
        'sample_weights':'compute_sample_weight(class_weight=balanced) on training labels',
        'classes':'0=phishing; 1=legitimate',
        'accuracy':float(accuracy_score(y_test,y_pred)),
        'balanced_accuracy':float(balanced_accuracy_score(y_test,y_pred)),
        'phishing_precision':float(precision[0]),
        'phishing_recall':float(recall[0]),
        'phishing_f1':float(f1[0]),
        'legitimate_precision':float(precision[1]),
        'legitimate_recall':float(recall[1]),
        'legitimate_f1':float(f1[1]),
        'roc_auc_phishing_positive':float(roc),
        'confusion_matrix_rows_actual_cols_predicted_labels_0_1':cm.tolist(),
        'test_errors':int((y_test!=y_pred).sum()),
        'sklearn_version':sklearn.__version__,'python_version':platform.python_version(),
        'no_joblib_or_pickle_loaded':True,
        'limitations':[
           'Different algorithms/settings/cleaning from unknown original notebook may change outcomes',
           'Single stratified split, not group-aware by URL/domain, chronological or independent',
           'Extreme class imbalance after deduplication; balanced accuracy and class recalls matter',
           'No claim about deployed saved model until its provenance and test predictions are available',
           'No evidence of operational performance on unseen live domains or websites'
        ]
    }
    with open(out/'reproduction_metrics.json','w',encoding='utf8') as f:json.dump(results,f,indent=2)
    with open(out/'reproduction_metrics.csv','w',newline='',encoding='utf8') as f:
        fields=['accuracy','balanced_accuracy','phishing_precision','phishing_recall','phishing_f1',
                'legitimate_precision','legitimate_recall','legitimate_f1','roc_auc_phishing_positive',
                'test_rows','test_errors']
        w=csv.DictWriter(f,fieldnames=['metric','score']);w.writeheader()
        for key in fields:w.writerow({'metric':key,'score':results[key]})
    pd.DataFrame(cm,index=['actual_phishing_0','actual_legitimate_1'],
                 columns=['predicted_phishing_0','predicted_legitimate_1']).to_csv(out/'reproduction_confusion_matrix.csv')
    # Evaluation fold IDs (original CSV indices) to make this reconstruction auditable.
    pd.DataFrame({'source_csv_row_index':X_test.index,
                  'actual_label':y_test.to_numpy(), 'predicted_label':y_pred,
                  'probability_phishing':phishing_prob}).to_csv(out/'reproduction_holdout_predictions.csv',index=False)
    fig,ax=plt.subplots(figsize=(6.5,5.3))
    img=ax.imshow(cm,cmap='Blues')
    for (i,j),count in np.ndenumerate(cm):
        ax.text(j,i,f'{count:,}',ha='center',va='center',fontsize=14,
                color='white' if count>(cm.max()/2) else 'black')
    ax.set(xticks=[0,1],yticks=[0,1],xticklabels=['Phishing','Legitimate'],
           yticklabels=['Phishing','Legitimate'],xlabel='Predicted class',ylabel='Actual class',
           title='Reconstructed holdout confusion matrix (n=6,100)')
    fig.tight_layout();fig.savefig(out/'reproduction_confusion_matrix.png',dpi=170);plt.close(fig)
    fpr,tpr,_=roc_curve((y_test==0).astype(int),phishing_prob)
    fig,ax=plt.subplots(figsize=(6.5,5.3))
    ax.plot(fpr,tpr,label=f'Phishing ROC–AUC={roc:.4f}')
    ax.plot([0,1],[0,1],'--',label='Chance baseline')
    ax.set(xlabel='False positive rate',ylabel='True positive rate',title='Reconstructed holdout ROC (phishing positive)')
    ax.legend();fig.tight_layout();fig.savefig(out/'reproduction_roc_curve.png',dpi=170);plt.close(fig)
    return results

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    a=parser.parse_args()
    report=run(a.input,a.output)
    print(json.dumps({k:report[k] for k in ('cleaned_rows','cleaned_label_counts','train_rows','test_rows','accuracy','balanced_accuracy','phishing_recall','legitimate_recall','roc_auc_phishing_positive','confusion_matrix_rows_actual_cols_predicted_labels_0_1')},indent=2))

"""Đọc CSV Iris, kiểm tra dữ liệu và so sánh bốn mô hình phân loại."""
from pathlib import Path
import argparse
import json
import platform
import hashlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import sklearn
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

FEATURES=['sepal_length','sepal_width','petal_length','petal_width']
CLASSES=['Iris-setosa','Iris-versicolor','Iris-virginica']
COLORS=['#286b9a','#d48238','#549467']

def setup_plot():
    font_path=Path('C:/Windows/Fonts/arial.ttf')
    if font_path.exists():
        font_manager.fontManager.addfont(font_path)
        plt.rcParams['font.family']='Arial'
    plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':120})

def save_plot(fig, folder, name):
    fig.tight_layout()
    fig.savefig(folder/(name+'.png'),dpi=300,bbox_inches='tight')
    fig.savefig(folder/(name+'.pdf'),bbox_inches='tight')
    plt.close(fig)

def run(data_path, out, seed=42):
    out.mkdir(parents=True,exist_ok=True)
    figures=out/'figures';figures.mkdir(exist_ok=True)
    df=pd.read_csv(data_path)
    required=['source_id',*FEATURES,'species']
    if not set(required).issubset(df.columns):raise ValueError('CSV thiếu cột bắt buộc')
    if df['source_id'].duplicated().any():raise ValueError('source_id phải duy nhất')
    for c in FEATURES:df[c]=pd.to_numeric(df[c],errors='raise')
    if df[required].isna().any().any():raise ValueError('Cần xử lý giá trị thiếu trước khi chạy')
    if not np.isfinite(df[FEATURES].to_numpy()).all():raise ValueError('Đặc trưng phải là số hữu hạn')
    if (df[FEATURES]<=0).any().any():raise ValueError('Kích thước hoa phải dương')
    if set(df.species)!=set(CLASSES):raise ValueError('Nhãn loài không khớp dữ liệu Iris')
    duplicated=df.duplicated(subset=FEATURES+['species'],keep='first')
    df.loc[duplicated].to_csv(out/'dong_trung.csv',index=False,encoding='utf-8-sig')
    clean=df.loc[~duplicated].copy()
    clean.to_csv(out/'iris_sach.csv',index=False,encoding='utf-8-sig')
    train, test=train_test_split(clean,test_size=.30,random_state=seed,stratify=clean.species)
    train.to_csv(out/'train.csv',index=False,encoding='utf-8-sig')
    test.to_csv(out/'test.csv',index=False,encoding='utf-8-sig')
    assert set(train.source_id).isdisjoint(test.source_id)
    assert len(train)+len(test)==len(clean)
    models={
        'kNN':make_pipeline(StandardScaler(),KNeighborsClassifier(n_neighbors=5)),
        'SVM':make_pipeline(StandardScaler(),SVC(C=1.0,kernel='rbf',gamma='scale')),
        'Decision Tree':DecisionTreeClassifier(max_depth=3,random_state=seed),
        'Random Forest':RandomForestClassifier(n_estimators=200,random_state=seed,n_jobs=2),
    }
    cv=StratifiedKFold(n_splits=5,shuffle=True,random_state=seed)
    rows=[];folds=[];predictions=test[['source_id','species']].copy()
    for name,model in models.items():
        scores=cross_val_score(model,train[FEATURES],train.species,cv=cv,scoring='f1_macro',n_jobs=1)
        model.fit(train[FEATURES],train.species)
        predicted=model.predict(test[FEATURES])
        predictions[name]=predicted
        rows.append({'model':name,'cv_f1_mean':float(scores.mean()),'cv_f1_std':float(scores.std(ddof=1)),
                     'test_accuracy':float(accuracy_score(test.species,predicted)),
                     'test_f1_macro':float(f1_score(test.species,predicted,average='macro')),
                     'correct':int((predicted==test.species).sum()),'test_n':len(test)})
        for i,value in enumerate(scores,1):folds.append({'model':name,'fold':i,'f1_macro':float(value)})
    metrics=pd.DataFrame(rows)
    metrics.to_csv(out/'metrics.csv',index=False,encoding='utf-8-sig',float_format='%.8f')
    pd.DataFrame(folds).to_csv(out/'cv_scores.csv',index=False,encoding='utf-8-sig')
    predictions.to_csv(out/'predictions.csv',index=False,encoding='utf-8-sig')
    cm=confusion_matrix(test.species,predictions['SVM'],labels=CLASSES)
    pd.DataFrame(cm,index=CLASSES,columns=CLASSES).to_csv(out/'svm_confusion_matrix.csv',encoding='utf-8-sig')
    meta={'raw_rows':len(df),'clean_rows':len(clean),'duplicates_removed':int(duplicated.sum()),
          'missing_cells':int(df[required].isna().sum().sum()),'train_rows':len(train),'test_rows':len(test),
          'seed':seed,'test_ratio':.30,'cv_folds':5,'class_counts':clean.species.value_counts().sort_index().to_dict(),
          'train_class_counts':train.species.value_counts().sort_index().to_dict(),
          'test_class_counts':test.species.value_counts().sort_index().to_dict(),
          'python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__,
          'scikit_learn':sklearn.__version__,'matplotlib':matplotlib.__version__,
          'data_file':str(data_path.name),'data_sha256':hashlib.sha256(data_path.read_bytes()).hexdigest()}
    (out/'summary.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8')
    setup_plot()
    fig,ax=plt.subplots(figsize=(7.2,4.2))
    for name,color in zip(CLASSES,COLORS):
        part=clean[clean.species==name]
        ax.scatter(part.petal_length,part.petal_width,s=36,c=color,label=name.removeprefix('Iris-'),alpha=.85)
    ax.set(xlabel='Chiều dài cánh hoa (cm)',ylabel='Chiều rộng cánh hoa (cm)')
    ax.legend(frameon=False,fontsize=10);ax.grid(alpha=.18)
    save_plot(fig,figures,'01_petal_scatter')
    fig,ax=plt.subplots(figsize=(5,3.4))
    counts=clean.species.value_counts().reindex(CLASSES)
    bars=ax.bar([s.removeprefix('Iris-') for s in CLASSES],counts,color=COLORS,width=.6)
    ax.bar_label(bars,padding=4);ax.set(ylabel='Số mẫu',ylim=(0,60))
    save_plot(fig,figures,'02_class_counts')
    fig,ax=plt.subplots(figsize=(5,3.6))
    corr=clean[FEATURES].corr()
    ax.imshow(corr,cmap='RdBu_r',vmin=-1,vmax=1)
    labels=['Dài đài','Rộng đài','Dài cánh','Rộng cánh']
    ax.set_xticks(range(4),labels,rotation=20);ax.set_yticks(range(4),labels)
    for i in range(4):
        for j in range(4):ax.text(j,i,f'{corr.iloc[i,j]:.2f}',ha='center',va='center',color='white' if abs(corr.iloc[i,j])>.65 else '#111')
    save_plot(fig,figures,'03_correlation')
    fig,ax=plt.subplots(figsize=(5,3.4))
    bars=ax.bar(['kNN','SVM','DT','RF'],metrics.cv_f1_mean,yerr=metrics.cv_f1_std,capsize=5,color='#286b9a',width=.6)
    ax.set(ylabel='F1 macro trên 5 fold',ylim=(0,1.08))
    for bar,value in zip(bars,metrics.cv_f1_mean):ax.text(bar.get_x()+bar.get_width()/2,value+.04,f'{value:.3f}',ha='center')
    save_plot(fig,figures,'04_cv_f1')
    fig,ax=plt.subplots(figsize=(5,3.6))
    ax.imshow(cm,cmap='Blues',vmin=0,vmax=15)
    short=[s.removeprefix('Iris-') for s in CLASSES]
    ax.set_xticks(range(3),short,rotation=15);ax.set_yticks(range(3),short)
    ax.set(xlabel='Nhãn dự đoán',ylabel='Nhãn thực tế')
    for i in range(3):
        for j in range(3):ax.text(j,i,str(cm[i,j]),ha='center',va='center',color='white' if cm[i,j]>7 else '#111',fontsize=15)
    save_plot(fig,figures,'05_svm_confusion')
    print('DỮ LIỆU VÀ CÁCH CHIA')
    print(f'CSV gốc: {len(df)} dòng; thiếu: {meta["missing_cells"]}; loại dòng trùng: {int(duplicated.sum())}')
    print(f'Sau làm sạch: {len(clean)} dòng; train: {len(train)}; test: {len(test)}; random_state={seed}')
    print('Số mẫu theo loài:',meta['class_counts'])
    print('\nKẾT QUẢ CHẠY')
    print(metrics.to_string(index=False,float_format=lambda x:f'{x:.4f}'))
    print('\nMA TRẬN NHẦM LẪN SVM (hàng thực tế, cột dự đoán)')
    print(cm)
    print('\nĐã lưu CSV, summary.json và 5 hình PNG/PDF vào',out)
    return meta,metrics

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data',type=Path,default=Path('data/iris.csv'))
    parser.add_argument('--out',type=Path,default=Path('results'))
    parser.add_argument('--seed',type=int,default=42)
    args=parser.parse_args();run(args.data,args.out,args.seed)

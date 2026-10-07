from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance

SEED=42

def generate(n=20000):
    rng=np.random.default_rng(SEED)
    x=rng.dirichlet([2,2,2,8],size=n)
    df=pd.DataFrame(x,columns=["scavenger_a","scavenger_b","binder","carrier"])
    # Software benchmark only: known optimum ratio A:B ~= 5 and positive A*B interaction.
    ratio=df.scavenger_a/(df.scavenger_b+1e-6)
    capture=90-18*(np.log1p(ratio)-np.log1p(5))**2+110*df.scavenger_a*df.scavenger_b-35*df.binder
    drying=3+35*df.binder+8*(df.scavenger_a+df.scavenger_b)
    swelling=0.02+0.22*(df.scavenger_a+df.scavenger_b)+0.08*df.binder
    cost=0.01+0.35*df.scavenger_a+0.22*df.scavenger_b+0.18*df.binder
    df["capture_score"]=capture.clip(0,100)
    df["drying_min"]=drying
    df["swelling_score"]=swelling
    df["cost_score"]=cost
    return df

def pareto(df):
    # Practical prefilter for v0; preserve multiple objectives in output.
    q=df[(df.drying_min<=df.drying_min.quantile(.35)) & (df.swelling_score<=df.swelling_score.quantile(.35))]
    return q.sort_values(["capture_score","cost_score"],ascending=[False,True]).head(200)

def main(out):
    out=Path(out); out.mkdir(parents=True,exist_ok=True)
    df=generate()
    features=["scavenger_a","scavenger_b","binder","carrier"]
    model=RandomForestRegressor(n_estimators=120,min_samples_leaf=3,random_state=SEED,n_jobs=-1)
    model.fit(df[features],df.capture_score)
    pred=model.predict(df[features])
    trees=np.stack([t.predict(df[features].values) for t in model.estimators_[:40]])
    df["prediction"]=pred
    df["uncertainty"]=trees.std(axis=0)
    imp=permutation_importance(model,df[features].iloc[:3000],df.capture_score.iloc[:3000],random_state=SEED,n_repeats=3)
    pd.DataFrame({"component":features,"importance":imp.importances_mean}).sort_values("importance",ascending=False).to_csv(out/"component_importance.csv",index=False)
    df.to_csv(out/"candidates.csv",index=False)
    p=pareto(df); p.to_csv(out/"pareto_frontier.csv",index=False)
    df["a_to_b_ratio"]=df.scavenger_a/(df.scavenger_b+1e-6)
    top=df.nlargest(1000,"capture_score")
    pd.DataFrame([{"metric":"top1000_a_to_b_ratio_median","value":top.a_to_b_ratio.median()},
                  {"metric":"top1000_a_to_b_ratio_p10","value":top.a_to_b_ratio.quantile(.1)},
                  {"metric":"top1000_a_to_b_ratio_p90","value":top.a_to_b_ratio.quantile(.9)}]).to_csv(out/"optimal_ranges.csv",index=False)
    # Simple interaction diagnostic: correlation of engineered pair products with target.
    rows=[]
    for i,a in enumerate(features):
        for b in features[i+1:]:
            rows.append({"pair":f"{a}*{b}","score":np.corrcoef(df[a]*df[b],df.capture_score)[0,1]})
    pd.DataFrame(rows).sort_values("score",key=lambda s:s.abs(),ascending=False).to_csv(out/"interaction_effects.csv",index=False)
    df.nlargest(20,"uncertainty")[features+["prediction","uncertainty"]].to_csv(out/"next_experiments.csv",index=False)
    (out/"report.md").write_text("# Synthetic discovery report\n\nThis run validates software behavior only; it makes no real chemistry or safety claim.\n\n"+top[["a_to_b_ratio","capture_score"]].describe().to_markdown()+"\n")
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--out",default="artifacts"); args=ap.parse_args(); main(args.out)

from src.discover import generate

def test_mixture_sums_to_one():
    df=generate(1000)
    assert ((df[["scavenger_a","scavenger_b","binder","carrier"]].sum(axis=1)-1).abs()<1e-9).all()

def test_known_ratio_is_recoverable():
    df=generate(20000)
    df["ratio"]=df.scavenger_a/(df.scavenger_b+1e-6)
    median=df.nlargest(1000,"capture_score").ratio.median()
    assert 3.0 < median < 7.0

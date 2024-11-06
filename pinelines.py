from pyhealth.datasets import MIMIC3Dataset
from pyhealth.tasks import drug_recommendation_mimic3_fn
from pyhealth.medcode import InnerMap

def get_dataset():
    '''
    获取mimic3数据集
    '''
    base_dataset = MIMIC3Dataset(
        root="/amax/data/liangfangyi/work3/data/mimiciii",
        tables=["DIAGNOSES_ICD", "PROCEDURES_ICD", "PRESCRIPTIONS"],
        code_mapping={"NDC": ("ATC", {"target_kwargs": {"level": 3}})},
        dev=False,
        refresh_cache=False,
    )
    base_dataset.stat()

    # STEP 2: set task
    sample_dataset = base_dataset.set_task(drug_recommendation_mimic3_fn)
    sample_dataset.stat()
    return sample_dataset

def get_samples():
    '''
    获取mimic3数据集的样本
    '''
    dataset = get_dataset()
    return dataset.samples

def get_all_tokens(key):
    '''
    获取mimic3数据集某个视图的所有token（一共有drugs, conditions, procedures三个视图）
    '''
    if key not in ["drugs", "conditions", "procedures"]:
        raise ValueError(f"不支持的key: {key}")
    dataset = get_dataset()
    return dataset.get_all_tokens(key=key)

def get_token2name(key):
    '''
    获取mimic3数据集某个视图的token到名称的映射
    '''
    voc = get_all_tokens(key) # voc是所有token的集合

    key_map = {
        "drugs": ("ATC", lambda x: x),
        "conditions": ("ICD9CM", lambda x: x),
        "procedures": ("ICD9PROC", lambda x: x[:2] if len(x) > 2 else x)
    }

    inner_map_name, fallback_func = key_map[key]
    inner_map = InnerMap.load(inner_map_name)

    token2name = {}
    for token in voc:
        try:
            name = inner_map.lookup(token)
        except Exception as e:
            print(f"在{inner_map_name}中没有找到代码 {token}: {e}")
            name = inner_map.lookup(fallback_func(token))
        token2name[token] = name

    return token2name

if __name__ == '__main__':
    sample = get_samples()
    print(sample)



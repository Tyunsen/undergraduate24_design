from pinelines import get_dataset, get_samples
from pyhealth.datasets import MIMIC3Dataset
from pyhealth.datasets import split_by_patient, get_dataloader
from pyhealth.models import Transformer
from pyhealth.tasks import drug_recommendation_mimic3_fn
from pyhealth.trainer import Trainer

def train():
    # STEP 1: load data
    sample_dataset = get_dataset()

    train_dataset, val_dataset, test_dataset = split_by_patient(
        sample_dataset, [0.8, 0.1, 0.1]
    )
    train_dataloader = get_dataloader(train_dataset, batch_size=32, shuffle=True)
    val_dataloader = get_dataloader(val_dataset, batch_size=32, shuffle=False)
    test_dataloader = get_dataloader(test_dataset, batch_size=32, shuffle=False)

    # STEP 2: define model
    model = Transformer(
        dataset=sample_dataset,
        feature_keys=["conditions", "procedures"],
        label_key="drugs",
        mode="multilabel",
    )

    # STEP 3: define trainer
    trainer = Trainer(
        model=model,
        metrics=["jaccard_samples", "f1_samples", "pr_auc_samples"],
    )

    trainer.train(
        train_dataloader=train_dataloader,
        val_dataloader=val_dataloader,
        epochs=20,
        monitor="pr_auc_samples",
    )

    # STEP 4: evaluate
    print (trainer.evaluate(test_dataloader))
    return model



if __name__ == '__main__':
    # model = train()

    patient = get_samples()[0]
    conditions = patient["conditions"]
    procedures = patient["procedures"]
    drugs = patient["drugs"]

    print(patient)
    # res = model(patient)

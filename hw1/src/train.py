import argparse
import logging
import os
import pdb
import pickle
import sys
import traceback
import json
from callbacks import ModelCheckpoint, MetricsLogger
from metrics import Recall


def main(args):
    config_path = os.path.join(args.model_dir, 'config.json')
    with open(config_path) as f:
        config = json.load(f)

    logging.info('loading embedding...')
    with open(config['model_parameters']['embedding'], 'rb') as f:
        embedding = pickle.load(f)
        config['model_parameters']['embedding'] = embedding.vectors

    logging.info('loading valid data...')
    with open(config['model_parameters']['valid'], 'rb') as f:
        config['model_parameters']['valid'] = pickle.load(f)

    logging.info('loading train data...')
    with open(config['train'], 'rb') as f:
        train = pickle.load(f)

    if config['arch'] == 'BiGruMaxFocalNet':
        train.n_negative = 4
        from example_predictor import ExamplePredictor
        PredictorClass = ExamplePredictor
        predictor = PredictorClass(
            arch=config['arch'],
            loss='FocalLoss',
            batch_size=500, 
            max_epochs=1024, 
            metrics=[Recall(1), Recall(10)],
            grad_accumulate_steps=1,
            device=args.device,
            **config['model_parameters']
        )
    elif config['arch'] == 'BiGruBattMaxBCENet':
        train.n_negative = 4
        from example_predictor import ExamplePredictor
        PredictorClass = ExamplePredictor
        predictor = PredictorClass(
            arch=config['arch'],
            loss='BCELoss',
            batch_size=100, 
            max_epochs=1024, 
            metrics=[Recall(1), Recall(10)],
            grad_accumulate_steps=1,
            device=args.device,
            **config['model_parameters']
        )
    elif config['arch'] == 'BiGruBattMaxFocalNet' or config['arch'] == 'BiGruBattMeanFocalNet':
        train.n_negative = 4
        from example_predictor import ExamplePredictor
        PredictorClass = ExamplePredictor
        predictor = PredictorClass(
            arch=config['arch'],
            loss='FocalLoss',
            batch_size=100, 
            max_epochs=1024, 
            metrics=[Recall(1), Recall(10)],
            grad_accumulate_steps=1,
            device=args.device,
            **config['model_parameters']
        )
    elif config['arch'] == 'BiGruBatt5MaxFocalNet':
        train.n_negative = 4
        from example_predictor import ExamplePredictor
        PredictorClass = ExamplePredictor
        predictor = PredictorClass(
            arch=config['arch'],
            loss='FocalLoss',
            batch_size=100, 
            max_epochs=1024, 
            metrics=[Recall(1), Recall(10)],
            grad_accumulate_steps=1,
            device=args.device,
            **config['model_parameters']
        )
    elif config['arch'] == 'BiGruBattDropMaxFocalNet':
        train.n_negative = 4
        from example_predictor import ExamplePredictor
        PredictorClass = ExamplePredictor
        predictor = PredictorClass(
            arch=config['arch'],
            loss='FocalLoss',
            batch_size=100, 
            max_epochs=1024, 
            metrics=[Recall(1), Recall(10)],
            grad_accumulate_steps=1,
            device=args.device,
            **config['model_parameters']
        )
    elif config['arch'] == 'BiGruLattMaxFocalNet':
        train.n_negative = 4
        from example_predictor import ExamplePredictor
        PredictorClass = ExamplePredictor
        predictor = PredictorClass(
            arch=config['arch'],
            loss='FocalLoss',
            batch_size=70, 
            max_epochs=1024, 
            metrics=[Recall(1), Recall(10)],
            grad_accumulate_steps=1,
            device=args.device,
            **config['model_parameters']
        )
    elif config['arch'] == 'BiGruBNattMaxFocalNet':
        train.n_negative = 4
        from example_predictor import ExamplePredictor
        PredictorClass = ExamplePredictor
        predictor = PredictorClass(
            arch=config['arch'],
            loss='FocalLoss',
            batch_size=70, 
            max_epochs=1024, 
            metrics=[Recall(1), Recall(10)],
            grad_accumulate_steps=1,
            device=args.device,
            **config['model_parameters']
        )
    elif config['arch'] == 'BiGruLNattMaxFocalNet':
        train.n_negative = 4
        from example_predictor import ExamplePredictor
        PredictorClass = ExamplePredictor
        predictor = PredictorClass(
            arch=config['arch'],
            loss='FocalLoss',
            batch_size=45, 
            max_epochs=1024, 
            metrics=[Recall(1), Recall(10)],
            grad_accumulate_steps=1,
            device=args.device,
            **config['model_parameters']
        )
    elif config['arch'] == 'BiLstmBattMaxBCENet':
        train.n_negative = 4
        from example_predictor import ExamplePredictor
        PredictorClass = ExamplePredictor
        predictor = PredictorClass(
            arch=config['arch'],
            loss='BCELoss',
            batch_size=100, 
            max_epochs=1024, 
            metrics=[Recall(1), Recall(10)],
            grad_accumulate_steps=1,
            device=args.device,
            **config['model_parameters']
        )
    elif config['arch'] == 'BiLstmBattMaxFocalNet' or config['arch'] == 'BiLstmBattMeanFocalNet':
        train.n_negative = 4
        from example_predictor import ExamplePredictor
        PredictorClass = ExamplePredictor
        predictor = PredictorClass(
            arch=config['arch'],
            loss='FocalLoss',
            batch_size=100, 
            max_epochs=1024, 
            metrics=[Recall(1), Recall(10)],
            grad_accumulate_steps=1,
            device=args.device,
            **config['model_parameters']
        )
    elif config['arch'] == 'BiLstmBatt5MaxFocalNet':
        train.n_negative = 4
        from example_predictor import ExamplePredictor
        PredictorClass = ExamplePredictor
        predictor = PredictorClass(
            arch=config['arch'],
            loss='FocalLoss',
            batch_size=100, 
            max_epochs=1024, 
            metrics=[Recall(1), Recall(10)],
            grad_accumulate_steps=1,
            device=args.device,
            **config['model_parameters']
        )
    elif config['arch'] == 'DeepBiGruBattMaxFocalNet':
        train.n_negative = 4
        from example_predictor import ExamplePredictor
        PredictorClass = ExamplePredictor
        predictor = PredictorClass(
            arch=config['arch'],
            loss='FocalLoss',
            batch_size=90, 
            max_epochs=1024, 
            metrics=[Recall(1), Recall(10)],
            grad_accumulate_steps=1,
            device=args.device,
            **config['model_parameters']
        )
    elif config['arch'] == 'FatBiGruBattMaxFocalNet':
        train.n_negative = 4
        from example_predictor import ExamplePredictor
        PredictorClass = ExamplePredictor
        predictor = PredictorClass(
            arch=config['arch'],
            loss='FocalLoss',
            batch_size=50, 
            max_epochs=1024, 
            metrics=[Recall(1), Recall(10)],
            grad_accumulate_steps=1,
            device=args.device,
            **config['model_parameters']
        )
    elif config['arch'] == 'ThinBiGruBattMaxFocalNet':
        train.n_negative = 4
        from example_predictor import ExamplePredictor
        PredictorClass = ExamplePredictor
        predictor = PredictorClass(
            arch=config['arch'],
            loss='FocalLoss',
            batch_size=150, 
            max_epochs=1024, 
            metrics=[Recall(1), Recall(10)],
            grad_accumulate_steps=1,
            device=args.device,
            **config['model_parameters']
        )
    
    if args.load is not None:
        predictor.load(args.load)

    model_checkpoint = ModelCheckpoint(
        os.path.join(args.model_dir, 'model.pkl'),
        'Recall@{}'.format(10), 1, 'max'
    )
    metrics_logger = MetricsLogger(
        os.path.join(args.model_dir, 'log.json')
    )

    logging.info('start training!')
    predictor.fit_dataset(train,
                          train.collate_fn,
                          [model_checkpoint, metrics_logger])


def _parse_args():
    parser = argparse.ArgumentParser(
        description="Script to train.")
    parser.add_argument('model_dir', type=str,
                        help='Directory to the model checkpoint.')
    parser.add_argument('--device', default=None,
                        help='Device used to train. Can be cpu or cuda:0,'
                        ' cuda:1, etc.')
    parser.add_argument('--load', default=None, type=str)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = _parse_args()
    logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s',
                        level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
    try:
        main(args)
    except KeyboardInterrupt:
        pass
    except BaseException:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)

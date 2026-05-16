import argparse

def train(args):
    print(f"Training with data={args.data}, epochs={args.epochs}")

parser = argparse.ArgumentParser(description='ML Workflow CLI')
subparsers = parser.add_subparsers(dest='command')

train_parser = subparsers.add_parser('train', help='Train the model')
train_parser.add_argument('--data', required=True, help='Path to the training data')
train_parser.add_argument('--epochs', type=int, default=10, help='Number of epochs to train')

args = parser.parse_args()
if args.command == 'train':
    train(args)
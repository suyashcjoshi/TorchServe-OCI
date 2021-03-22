
from dataset import *
from util import *
from model import *
from torchvision import transforms
from tqdm import tqdm
from skimage import io
import torch
#torch.backends.cudnn.benchmark = True
#device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

def predict(model, filename, transform):
    numpy_img = io.imread(filename)
    img = torch.from_numpy(numpy_img)
    img = transform(img)

    # Create batch of size one
    img = img.unsqueeze(0).cuda()

    with torch.no_grad():
        result = model(img)

    if result.data[0][0] >= result.data[0][1]:
        print("Image is a cat!")
    else:
        print("Image is a dog!")


def eval(model, dataloader, loss_fn):
    total = 0
    total_correct = 0
    with torch.no_grad():
        for i, batch in enumerate(tqdm(dataloader)):
            inputs, labels = batch['image'], batch['label']
            inputs = inputs.cuda()
            labels = labels.cuda()

            # Forward pass: compute predicted labels
            label_scores = model(inputs)
            label_pred = label_scores.argmax(1)

            # Compute stats for accuracy
            total += len(inputs)
            total_correct += label_pred.eq(labels).sum().item()

    return float(total_correct)/total


def run_epoch(model, dataloader, loss_fn, optimizer):
    for i, batch in enumerate(tqdm(dataloader), 0):
        # Forward pass: compute predicted labels
        inputs, labels = batch['image'], batch['label']
        inputs = inputs.cuda()
        labels = labels.cuda()

        # Zero gradients
        optimizer.zero_grad()

        # Forward step
        label_scores = model(inputs)

        # Compute loss
        loss = loss_fn(label_scores, labels)

        # Backward pass: compute gradient of the loss with respect to model
        # parameters
        loss.backward()

        # Calling the step function on an Optimizer makes an update to its
        # parameters
        optimizer.step()


def main():
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize(256),
        transforms.RandomCrop(224),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    dataset = DogsCatsDataset('train', transform=transform)

    batch_size = 20
    print("Batch size:", batch_size)
    train_loader, valid_loader = create_dataloaders(dataset, batch_size=batch_size,
        num_workers=4)

    model = Net()
    model = model.cuda()

    predict(model, 'train/cat.24.jpg', transform=transform)

    loss_fn = torch.nn.CrossEntropyLoss()
    learning_rate = 1e-4
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # Get the intitial validation score
    print("Initial score: %.2f%%" % (100 * eval(model, valid_loader, loss_fn)))

    for epoch in range(15):
        score = run_epoch(model, train_loader, loss_fn, optimizer)
        print("Epoch %d: %.2f%%" % (epoch + 1, 100 * eval(model, valid_loader, loss_fn)))

    predict(model, 'train/cat.24.jpg', transform=transform)

if __name__ == "__main__":
    main()

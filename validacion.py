import os
import glob
from image import *
from model import CSRNet
import math
import torch
from torchvision import transforms
# torch.cuda.empty_cache()

transform = transforms.Compose([
    transforms.ToTensor(), transforms.Normalize(mean=[1, 1, 1], std=[1, 1, 1])])
root = 'Dataset'
# part_A_train = os.path.join(root, 'part_A/train_data', 'images')
part_A_test = os.path.join(root, 'part_A/test_data', 'images')
part_A_test_Gray = os.path.join(root, 'part_A_gray/test_data', 'images')
# part_B_train = os.path.join(root, 'part_B/train_data', 'images')
part_B_test = os.path.join(root, 'part_B/test_data', 'images')
part_B_test_Gray = os.path.join(root, 'part_B_gray/test_data', 'images')
# part_A_B_train = os.path.join(root, 'part_A_B/train_data', 'images')
part_A_B_test = os.path.join(root, 'part_A_B/test_data', 'images')
part_A_B_test_Gray = os.path.join(root, 'part_A_B_gray/test_data', 'images')
path_sets = [part_A_test]
img_paths = []
for path in path_sets:
    for img_path in glob.glob(os.path.join(path, '*.jpg')):
        img_paths.append(img_path)
model = CSRNet()
model = model.cuda()
checkpoint = torch.load('Modelos Entrenados/Multitudes_Densas.pth.tar')
model.load_state_dict(checkpoint['state_dict'])
mae = 0
mse = 0
for i in range(len(img_paths)):
    img = transform(Image.open(img_paths[i]).convert('RGB')).cuda()
    img = img.cuda()
    gt_file = h5py.File(img_paths[i].replace('.jpg', '.h5').replace('images', 'ground_truth'), 'r')
    groundtruth = np.asarray(gt_file['density'])
    output = model(img.unsqueeze(0))
    mae += abs(output.detach().cpu().sum().numpy() - np.sum(groundtruth))
    mse += abs(output.detach().cpu().sum().numpy() - np.sum(groundtruth)) ** 2
    print(i, "MAE ", mae, "|", "MSE ", mse)
print("MAE", mae / len(img_paths), "|", "MSE", math.sqrt(mse / len(img_paths)))

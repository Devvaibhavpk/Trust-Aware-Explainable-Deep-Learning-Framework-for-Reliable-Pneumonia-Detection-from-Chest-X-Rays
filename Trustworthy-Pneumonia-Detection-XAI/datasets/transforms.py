"""
Image transforms for chest X-ray classification.
"""

from torchvision import transforms

# Default normalization for ImageNet-style models (used with transfer learning)
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

# For grayscale X-rays we use single-channel; normalize to [0,1] or match ImageNet
DEFAULT_MEAN = [0.5]
DEFAULT_STD = [0.5]


def get_transforms(
    phase: str = "train",
    image_size: int = 224,
    use_imagenet_norm: bool = True,
) -> transforms.Compose:
    """
    Get torchvision transforms for train/val/test.

    Args:
        phase: 'train', 'val', or 'test'.
        image_size: Target spatial size (height, width).
        use_imagenet_norm: If True, use ImageNet mean/std (for ResNet/VGG).

    Returns:
        Composed transform pipeline.
    """
    mean = IMAGENET_MEAN if use_imagenet_norm else DEFAULT_MEAN * 3
    std = IMAGENET_STD if use_imagenet_norm else DEFAULT_STD * 3

    if phase == "train":
        return transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(10),
            transforms.ColorJitter(brightness=0.1, contrast=0.1),
            transforms.ToTensor(),
            transforms.Normalize(mean=mean, std=std),
        ])

    return transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=mean, std=std),
    ])

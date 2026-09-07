"""
CNN-based models for chest X-ray binary classification.
Supports: Custom CNN, ResNet18, VGG16.
Binary classification via single output + sigmoid or two outputs + softmax.
"""

import torch
import torch.nn as nn
from torchvision import models
from typing import Optional, Literal

ModelType = Literal["custom", "resnet18", "vgg16", "densenet121", "efficientnet_b0"]
NUM_CLASSES = 2  # NORMAL, PNEUMONIA



class ChestXRayCNN(nn.Module):
    """
    Custom CNN for 224x224 RGB input, binary classification.
    Architecture: Conv blocks -> FC -> 1 logit (sigmoid) for PNEUMONIA probability.
    """

    def __init__(self, num_classes: int = 1):
        super().__init__()
        self.num_classes = num_classes
        # 224 -> 112 -> 56 -> 28 -> 14 -> 7
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),  # 112
            nn.Conv2d(32, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),  # 56
            nn.Conv2d(64, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),  # 28
            nn.Conv2d(128, 256, 3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),  # 14
            nn.Conv2d(256, 512, 3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),  # 7
        )
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(512, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes if num_classes > 1 else 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        x = self.avgpool(x)
        x = self.classifier(x)
        return x

    def get_last_conv_layer(self) -> nn.Module:
        """Return the last conv layer for Grad-CAM (custom CNN: last Conv2d in features)."""
        for m in reversed(list(self.features.modules())):
            if isinstance(m, nn.Conv2d):
                return m
        raise RuntimeError("No Conv2d found in features")


def get_resnet18(pretrained: bool = True, num_classes: int = 1) -> nn.Module:
    """
    ResNet18 for binary classification.
    Single output + sigmoid: num_classes=1. Optionally 2 outputs + softmax: num_classes=2.
    """
    model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1 if pretrained else None)
    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, num_classes if num_classes > 1 else 1)
    return model


def get_vgg16(pretrained: bool = True, num_classes: int = 1) -> nn.Module:
    """
    VGG16 for binary classification.
    Replace classifier head; keep features for Grad-CAM (last conv in features).
    """
    model = models.vgg16(weights=models.VGG16_Weights.IMAGENET1K_V1 if pretrained else None)
    in_features = model.classifier[6].in_features
    model.classifier[6] = nn.Linear(in_features, num_classes if num_classes > 1 else 1)
    return model


def get_densenet121(pretrained: bool = True, num_classes: int = 1) -> nn.Module:
    """
    DenseNet121 for binary classification.
    Replaces classifier with a single logit (or num_classes outputs).
    """
    model = models.densenet121(
        weights=models.DenseNet121_Weights.IMAGENET1K_V1 if pretrained else None
    )
    in_features = model.classifier.in_features
    model.classifier = nn.Linear(in_features, num_classes if num_classes > 1 else 1)
    return model


def get_efficientnet_b0(pretrained: bool = True, num_classes: int = 1) -> nn.Module:
    """
    EfficientNet-B0 for binary classification.
    Uses torchvision EfficientNet implementation.
    """
    model = models.efficientnet_b0(
        weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1 if pretrained else None
    )
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, num_classes if num_classes > 1 else 1)
    return model


def build_model(
    model_type: ModelType = "resnet18",
    pretrained: bool = True,
    num_classes: int = 1,
) -> nn.Module:
    """
    Build classifier model. num_classes=1 gives single logit (use sigmoid for probability).
    """
    if model_type == "custom":
        return ChestXRayCNN(num_classes=num_classes)
    if model_type == "resnet18":
        return get_resnet18(pretrained=pretrained, num_classes=num_classes)
    if model_type == "vgg16":
        return get_vgg16(pretrained=pretrained, num_classes=num_classes)
    if model_type == "densenet121":
        return get_densenet121(pretrained=pretrained, num_classes=num_classes)
    if model_type == "efficientnet_b0":
        return get_efficientnet_b0(pretrained=pretrained, num_classes=num_classes)
    raise ValueError(f"Unknown model_type: {model_type}")


def get_last_conv_layer_for_model(model: nn.Module, model_type: ModelType) -> nn.Module:
    """
    Return the last convolutional layer of the model for Grad-CAM.
    """
    if model_type == "custom":
        assert isinstance(model, ChestXRayCNN)
        return model.get_last_conv_layer()
    if model_type == "resnet18":
        return model.layer4[-1].conv2
    if model_type == "vgg16":
        return model.features[-1]  # last conv in VGG features
    if model_type == "densenet121":
        # Last dense block's last conv layer
        return model.features.denseblock4.denselayer16.conv2
    if model_type == "efficientnet_b0":
        # Last convolutional block before pooling
        return model.features[-1][0]
    raise ValueError(f"Unknown model_type: {model_type}")

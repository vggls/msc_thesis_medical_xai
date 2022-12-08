from collections import OrderedDict
from torchvision import models
from torch import nn

class EfficientNet():
    
    '''
    ATTRIBUTES: see README_attributes.md
    '''
    
    def __init__(self, type_, no_of_classes, trainable_feature_layers=None, custom_classifier=None):
        
        self.type_ = type_
        self.no_of_classes = no_of_classes
        self.trainable_feature_layers = trainable_feature_layers
        self.custom_classifier = custom_classifier
        
        if self.type_ == 'b1':
            self.model = models.efficientnet_b1(pretrained=True)
        elif self.type_ == 'b2':
            self.model = models.efficientnet_b2(pretrained=True)
        elif self.type_ == 'b3':
            self.model = models.efficientnet_b3(pretrained=True)
        elif self.type_ == 'b4':
            self.model = models.efficientnet_b4(pretrained=True)
        elif self.type_ == 'b5':
            self.model = models.efficientnet_b5(pretrained=True)
        elif self.type_ == 'b6':
            self.model = models.efficientnet_b6(pretrained=True)
        elif self.type_ == 'b7':
            self.model = models.efficientnet_b7(pretrained=True)
        
        # CLASSIFIER
        num_filters = self.model.classifier[-1].in_features
        if self.custom_classifier==None:
            default_classifier = nn.Sequential(OrderedDict([
                ('0', nn.Dropout(p=0.4, inplace=True)),
                ('1', nn.Linear(num_filters, self.no_of_classes)),
                ('2', nn.Softmax(dim=1))
            ]))
            self.model.classifier = default_classifier
        else:
            assert self.custom_classifier[-2].out_features == self.no_of_classes
            assert type(custom_classifier[-1]) == nn.modules.activation.Softmax
            self.model.classifier = self.custom_classifier
        
        # LAYERS TO FREEZE DURING TRAINING
        if self.trainable_feature_layers==None:
            self.freeze = self.model.features
        else:
            len_ = len(self.model.features)
            assert all(x in range(len_) for x in self.trainable_feature_layers)
            self.freeze = [self.model.features[j] for j in range(len_) if j not in self.trainable_feature_layers]
            
        for child in self.freeze:
            for param in child.parameters():
                param.requires_grad = False
        
        
    def trainable_params(self):
        # below is equivalent to summary from torchsummary
        print('No. of trainable params', sum(p.numel() for p in self.model.parameters() if p.requires_grad))

    def unfreeze(self):
        for child in self.freeze:
            for param in child.parameters():
                param.requires_grad = True

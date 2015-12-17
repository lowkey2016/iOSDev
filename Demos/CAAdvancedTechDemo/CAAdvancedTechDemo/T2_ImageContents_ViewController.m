//
//  T2_ImageContents_ViewController.m
//  CAAdvancedTechDemo
//
//  Created by Jymn_Chen on 15/11/13.
//  Copyright © 2015年 com.youmi. All rights reserved.
//

#import "T2_ImageContents_ViewController.h"

@interface T2_ImageContents_ViewController ()

@property (strong, nonatomic) IBOutlet UIView *layerView;

@end

@implementation T2_ImageContents_ViewController

#pragma mark - View

- (void)viewDidLoad {
    [super viewDidLoad];
}

- (void)addStretchableImage:(UIImage *)image withContentCenter:(CGRect)rect toLayer:(CALayer *)layer {
    layer.contents = (__bridge id)image.CGImage;
    layer.contentsCenter = rect;
}

#pragma mark - Button Actions

- (IBAction)showAction:(id)sender {
    UIImage *image = [UIImage imageNamed:@"dola"];
    _layerView.layer.contents = (__bridge id)image.CGImage;
    _layerView.layer.contentsGravity = kCAGravityResizeAspectFill;
    _layerView.layer.contentsScale = [[UIScreen mainScreen] scale];
    _layerView.layer.masksToBounds = YES;
}

- (IBAction)stretchAction:(id)sender {
    UIImage *image = [UIImage imageNamed:@"dola"];
    [self addStretchableImage:image withContentCenter:CGRectMake(0.25, 0.25, 0.5, 0.5) toLayer:_layerView.layer];
}

@end

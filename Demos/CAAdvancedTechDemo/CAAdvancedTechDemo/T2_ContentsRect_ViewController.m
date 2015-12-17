//
//  T2_ContentsRect_ViewController.m
//  CAAdvancedTechDemo
//
//  Created by Jymn_Chen on 15/11/13.
//  Copyright © 2015年 com.youmi. All rights reserved.
//

#import "T2_ContentsRect_ViewController.h"

@interface T2_ContentsRect_ViewController ()

@property (strong, nonatomic) IBOutlet UIView *view1;
@property (strong, nonatomic) IBOutlet UIView *view2;
@property (strong, nonatomic) IBOutlet UIView *view3;
@property (strong, nonatomic) IBOutlet UIView *view4;

@end

@implementation T2_ContentsRect_ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    UIImage *image = [UIImage imageNamed:@"F4.jpg"];
    [self addImage:image withContentRect:CGRectMake(0, 0, 0.25, 1) toLayer:_view1.layer];
    [self addImage:image withContentRect:CGRectMake(0.25, 0, 0.25, 1) toLayer:_view2.layer];
    [self addImage:image withContentRect:CGRectMake(0.5, 0, 0.25, 1) toLayer:_view3.layer];
    [self addImage:image withContentRect:CGRectMake(0.75, 0, 0.25, 1) toLayer:_view4.layer];
}

- (void)addImage:(UIImage *)image withContentRect:(CGRect)rect toLayer:(CALayer *)layer {
    layer.contents = (__bridge id)image.CGImage;
    layer.contentsGravity = kCAGravityResizeAspect;
    layer.contentsRect = rect;
}

@end

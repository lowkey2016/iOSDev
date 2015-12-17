//
//  ViewController.m
//  RoundCornerDemo
//
//  Created by Jymn_Chen on 15/11/21.
//  Copyright © 2015年 com.youmi. All rights reserved.
//

#import "ViewController.h"
#import "RoundCornerView.h"

@interface ViewController ()

@property (strong, nonatomic) IBOutlet RoundCornerView *roundView;

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    _roundView.clipsToBounds = YES;
//    UIImage *image = [UIImage imageNamed:@"Ship"];
    UIImageView *imgView = [[UIImageView alloc] init];
    imgView.opaque = YES;
    imgView.clipsToBounds = YES;
    imgView.contentMode = UIViewContentModeScaleAspectFill;
    imgView.backgroundColor = [UIColor clearColor];
    imgView.frame = CGRectMake(0, 128 - 40, 240, 40);
    imgView.image = [self cropedImgWithSize:CGSizeMake(240, 40)];
    [_roundView addSubview:imgView];
}

- (UIImage *)cropedImgWithSize:(CGSize)size  {
    UIImage *image = [UIImage imageNamed:@"com_gradientBg"];
    CGFloat scale = [[UIScreen mainScreen] scale];
    UIGraphicsBeginImageContextWithOptions(size, NO, scale);
    CGRect drawingRect = (CGRect){CGPointZero, size};
    [[UIBezierPath bezierPathWithRoundedRect:drawingRect byRoundingCorners:UIRectCornerBottomLeft|UIRectCornerBottomRight cornerRadii:CGSizeMake(20, 20)] addClip];
    [image drawInRect:drawingRect];
    UIImage *cropedImage = UIGraphicsGetImageFromCurrentImageContext();
    UIGraphicsEndImageContext();
    
    return cropedImage;
}

@end

//
//  ViewController.m
//  DrawMaskDemo
//
//  Created by Jymn_Chen on 15/11/22.
//  Copyright © 2015年 com.youmi. All rights reserved.
//

#import "ViewController.h"
#import "HGCRoundCornerMaskView.h"

@interface ViewController ()

@property (strong, nonatomic) IBOutlet HGCRoundCornerMaskView *maskView;
@property (strong, nonatomic) IBOutlet UIImageView *imgv;

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    UIImageView *tmpImgView = [[UIImageView alloc] initWithFrame:_imgv.frame];
    tmpImgView.backgroundColor = [UIColor lightGrayColor];
    [self.view addSubview:tmpImgView];
    tmpImgView.image = [self createImageWithRect:_imgv.bounds];
}


void _drawArcInContext(CGContextRef context, CGPoint *p) {
    CGContextSetFillColorWithColor(context, [UIColor lightGrayColor].CGColor);
    CGContextMoveToPoint(context, p[0].x, p[0].y);
    CGContextAddArcToPoint(context, p[1].x, p[1].y, p[2].x, p[2].y, 30.0);
    CGContextAddLineToPoint(context, p[1].x, p[1].y);
    CGContextClosePath(context);
    
    CGContextDrawPath(context, kCGPathFill);
}


- (UIImage *)createImageWithRect:(CGRect)rect {
    NSMutableData *data = [NSMutableData dataWithLength:rect.size.width * rect.size.height * 1];
    // Create a bitmap context
    CGContextRef context = CGBitmapContextCreate([data mutableBytes], rect.size.width, rect.size.height, 8, rect.size.width, NULL, (CGBitmapInfo)kCGImageAlphaOnly);
    // Set the blend mode to copy to avoid any alteration of the source data
    CGContextSetBlendMode(context, kCGBlendModeCopy);
    
    CGContextSetFillColorWithColor(context, [UIColor lightGrayColor].CGColor);
    CGContextAddPath(context, [[UIBezierPath bezierPathWithRoundedRect:rect cornerRadius:30.0f] CGPath]);
    CGContextFillPath(context);
    
//    CGPoint p_topLeft[3] = {
//        CGPointMake(0.0, rect.size.height / 2),
//        CGPointZero,
//        CGPointMake(rect.size.width / 2, 0.0)
//    };
//    _drawArcInContext(context, p_topLeft);
//    
//    CGPoint p_topRight[3] = {
//        CGPointMake(rect.size.width / 2, 0.0),
//        CGPointMake(rect.size.width, 0.0),
//        CGPointMake(rect.size.width, rect.size.height / 2)
//    };
//    _drawArcInContext(context, p_topRight);
//    
//    CGPoint p_bottomLeft[3] = {
//        CGPointMake(0.0, rect.size.height / 2),
//        CGPointMake(0.0, rect.size.height),
//        CGPointMake(rect.size.width / 2, rect.size.height),
//    };
//    _drawArcInContext(context, p_bottomLeft);
//    
//    CGPoint p_bottomRight[3] = {
//        CGPointMake(rect.size.width, rect.size.height / 2),
//        CGPointMake(rect.size.width, rect.size.height),
//        CGPointMake(rect.size.width / 2, rect.size.height)
//    };
//    _drawArcInContext(context, p_bottomRight);
    
    // Now the alpha channel has been copied into our NSData object above, so discard the context and lets make an image mask.
    CGContextRelease(context);
    // Create a data provider for our data object (NSMutableData is tollfree bridged to CFMutableDataRef, which is compatible with CFDataRef)
    CGDataProviderRef dataProvider = CGDataProviderCreateWithCFData((__bridge CFMutableDataRef)data);
    // Create our new mask image with the same size as the original image
    CGImageRef maskingImage = CGImageMaskCreate(rect.size.width, rect.size.height, 8, 8, rect.size.width, dataProvider, NULL, YES);
    // And release the provider.
    CGDataProviderRelease(dataProvider);
    
    return [[UIImage alloc] initWithCGImage:maskingImage];
}

@end

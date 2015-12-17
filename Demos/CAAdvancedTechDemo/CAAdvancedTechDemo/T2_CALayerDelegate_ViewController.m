//
//  T2_CALayerDelegate_ViewController.m
//  CAAdvancedTechDemo
//
//  Created by Jymn_Chen on 15/11/13.
//  Copyright © 2015年 com.youmi. All rights reserved.
//

#import "T2_CALayerDelegate_ViewController.h"

@interface T2_CALayerDelegate_ViewController ()

@property (strong, nonatomic) IBOutlet UIView *layerView;

@end

@implementation T2_CALayerDelegate_ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    CALayer *blueLayer = [CALayer layer];
    blueLayer.frame = CGRectMake(0.0f, 0.0f, 100.0f, 100.0f);
    blueLayer.backgroundColor = [UIColor blueColor].CGColor;
    
    // set controller as layer delegate
    blueLayer.delegate = self;
    
    blueLayer.contentsScale = [UIScreen mainScreen].scale;
    [self.layerView.layer addSublayer:blueLayer];
    
    // force layer to redraw
    [blueLayer display];
    /*
     我们在 blueLayer上显式地调用了-display
     不同于UIView，当图层显示在屏幕上时，CALayer不会自动重绘它的内容。它把重绘的决定权交给了开发者
     */
}

/*
 除非你创建了一个单独的图层，你几乎没有机会用到CALayerDelegate协议。因为当UIView创建了它的宿主图层时，它就会自动地把图层的delegate设置为它自己，并提供了一个-displayLayer:的实现
 
 当使用寄宿了视图的图层的时候，你也不必实现-displayLayer:和-drawLayer:inContext:方法来绘制你的寄宿图。通常做法是实现UIView的-drawRect:方法，UIView就会帮你做完剩下的工作，包括在需要重绘的时候调用-display方法。
 */

- (void)drawLayer:(CALayer *)layer inContext:(CGContextRef)ctx {
    CGContextSetLineWidth(ctx, 10.0f);
    CGContextSetStrokeColorWithColor(ctx, [UIColor redColor].CGColor);
    CGContextStrokeEllipseInRect(ctx, layer.bounds);
}

@end

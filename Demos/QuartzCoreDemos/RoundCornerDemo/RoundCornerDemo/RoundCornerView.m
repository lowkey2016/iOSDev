//
//  RoundCornerView.m
//  RoundCornerDemo
//
//  Created by Jymn_Chen on 15/11/21.
//  Copyright © 2015年 com.youmi. All rights reserved.
//

#import "RoundCornerView.h"

@implementation RoundCornerView

- (void)drawRect:(CGRect)rect {
    CGContextRef context = UIGraphicsGetCurrentContext();
    
    UIBezierPath *path = [UIBezierPath bezierPathWithRoundedRect:rect cornerRadius:20.0f];
    CGContextAddPath(context, path.CGPath);
    CGContextClosePath(context);
    
    CGContextSaveGState(context);
    CGContextClip(context);
    CGContextSetFillColorWithColor(context, [UIColor greenColor].CGColor);
    CGContextFillRect(context, rect);
    CGContextRestoreGState(context);
}

@end

//
//  HGCRoundCornerMaskView.m
//  DrawMaskDemo
//
//  Created by Jymn_Chen on 15/11/22.
//  Copyright © 2015年 com.youmi. All rights reserved.
//

#import "HGCRoundCornerMaskView.h"

@implementation HGCRoundCornerMaskView

void drawArcInContext(CGContextRef context, CGPoint *p) {
    CGContextSetFillColorWithColor(context, [UIColor lightGrayColor].CGColor);
    CGContextMoveToPoint(context, p[0].x, p[0].y);
    CGContextAddArcToPoint(context, p[1].x, p[1].y, p[2].x, p[2].y, 30.0);
    CGContextAddLineToPoint(context, p[1].x, p[1].y);
    CGContextClosePath(context);
    
    CGContextDrawPath(context, kCGPathFill);
}

- (void)drawRect:(CGRect)rect {
    CGContextRef context = UIGraphicsGetCurrentContext();
    
    CGPoint p_topLeft[3] = {
        CGPointMake(0.0, rect.size.height / 2),
        CGPointZero,
        CGPointMake(rect.size.width / 2, 0.0)
    };
    drawArcInContext(context, p_topLeft);
    
    CGPoint p_topRight[3] = {
        CGPointMake(rect.size.width / 2, 0.0),
        CGPointMake(rect.size.width, 0.0),
        CGPointMake(rect.size.width, rect.size.height / 2)
    };
    drawArcInContext(context, p_topRight);
    
    CGPoint p_bottomLeft[3] = {
        CGPointMake(0.0, rect.size.height / 2),
        CGPointMake(0.0, rect.size.height),
        CGPointMake(rect.size.width / 2, rect.size.height),
    };
    drawArcInContext(context, p_bottomLeft);
    
    CGPoint p_bottomRight[3] = {
        CGPointMake(rect.size.width, rect.size.height / 2),
        CGPointMake(rect.size.width, rect.size.height),
        CGPointMake(rect.size.width / 2, rect.size.height)
    };
    drawArcInContext(context, p_bottomRight);
}

@end

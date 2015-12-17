//
//  T3_HitTestingViewController.m
//  CAAdvancedTechDemo
//
//  Created by Jymn_Chen on 15/11/14.
//  Copyright © 2015年 com.youmi. All rights reserved.
//

#import "T3_HitTestingViewController.h"

#if 1
#define T3_UseHitTestingCode
#endif

@interface T3_HitTestingViewController ()

@property (strong, nonatomic) IBOutlet UIView *layerView;
@property (nonatomic, strong) CALayer *blueLayer;

@end

@implementation T3_HitTestingViewController

#pragma mark - View

- (void)viewDidLoad {
    [super viewDidLoad];
    
    self.blueLayer = [CALayer layer];
    self.blueLayer.frame = CGRectMake(100.0f, 50.0f, 100.0f, 100.0f);
    self.blueLayer.backgroundColor = [UIColor blueColor].CGColor;
    [self.layerView.layer addSublayer:self.blueLayer];
}

#pragma mark - UIResponder Methods

#ifdef T3_UseHitTestingCode

- (void)touchesBegan:(NSSet *)touches withEvent:(UIEvent *)event {
    CGPoint point = [[touches anyObject] locationInView:self.view];
    CALayer *layer = [self.layerView.layer hitTest:point];
    if (layer == self.blueLayer) {
        [[[UIAlertView alloc] initWithTitle:@"Inside Blue Layer"
                                    message:nil
                                   delegate:nil
                          cancelButtonTitle:@"OK"
                          otherButtonTitles:nil] show];
    }
    else if (layer == self.layerView.layer) {
        [[[UIAlertView alloc] initWithTitle:@"Inside White Layer"
                                    message:nil
                                   delegate:nil
                          cancelButtonTitle:@"OK"
                          otherButtonTitles:nil] show];
    }
}

#else

- (void)touchesBegan:(NSSet *)touches withEvent:(UIEvent *)event {
    CGPoint point = [[touches anyObject] locationInView:self.view];
    point = [self.layerView.layer convertPoint:point fromLayer:self.view.layer];
    if ([self.layerView.layer containsPoint:point]) {
        point = [self.blueLayer convertPoint:point fromLayer:self.layerView.layer];
        if ([self.blueLayer containsPoint:point]) {
            [[[UIAlertView alloc] initWithTitle:@"Inside Blue Layer"
                                        message:nil
                                       delegate:nil
                              cancelButtonTitle:@"OK"
                              otherButtonTitles:nil] show];
        }
        else {
            [[[UIAlertView alloc] initWithTitle:@"Inside White Layer"
                                        message:nil
                                       delegate:nil
                              cancelButtonTitle:@"OK"
                              otherButtonTitles:nil] show];
        }
    }
    else {
        [[[UIAlertView alloc] initWithTitle:@"Inside self.view Layer"
                                    message:nil
                                   delegate:nil
                          cancelButtonTitle:@"OK"
                          otherButtonTitles:nil] show];
    }
}

#endif

@end

//
//  ViewController.m
//  VFLDemo
//
//  Created by Jymn_Chen on 15/12/27.
//  Copyright © 2015年 com.youmi. All rights reserved.
//

#import "ViewController.h"

@interface ViewController ()

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
//    [self demo1];
    [self demo2];
}

- (void)demo1 {
    UIButton *button=[[UIButton alloc]init];
    [button setTitle:@"点击一下" forState:UIControlStateNormal];
    button.translatesAutoresizingMaskIntoConstraints=NO;
    [button setBackgroundColor:[UIColor blackColor]];
    [self.view addSubview:button];
    
    // 表示间隙的 `-` 如果不指明间隙大小，则为默认值
    // 当表示两个兄弟 views 之间的间隙，则为 8
    // 当表示两个父子 views 之间的间隙，则为 20
    NSArray *constraints1=[NSLayoutConstraint constraintsWithVisualFormat:@"H:|-[button]-|" options:0 metrics:nil views:NSDictionaryOfVariableBindings(button)];
    
    NSDictionary *metrics2 = @{@"leftMargin" : @20, @"buttonHeight" : @30};
    NSArray *constraints2=[NSLayoutConstraint constraintsWithVisualFormat:@"V:|-leftMargin-[button(==buttonHeight)]" options:0 metrics:metrics2 views:NSDictionaryOfVariableBindings(button)];
    
    [self.view addConstraints:constraints1];
    [self.view addConstraints:constraints2];
    
    UIButton *button1=[[UIButton alloc]init];
    button1.translatesAutoresizingMaskIntoConstraints=NO;
    [button1 setTitle:@"请不要点击我" forState:UIControlStateNormal];
    [button1 setBackgroundColor:[UIColor redColor]];
    [self.view addSubview:button1];
    
//    NSArray *constraints3=[NSLayoutConstraint constraintsWithVisualFormat:@"H:|-[button1]-|" options:0 metrics:nil views:NSDictionaryOfVariableBindings(button1)];
////    NSArray *constraints4=[NSLayoutConstraint constraintsWithVisualFormat:@"V:[button]-[button1(==30)]" options:0 metrics:nil views:NSDictionaryOfVariableBindings(button1,button)];
//    NSArray *constraints4=[NSLayoutConstraint constraintsWithVisualFormat:@"V:[button]-[button1(==height)]" options:0 metrics:@{@"height":@30} views:NSDictionaryOfVariableBindings(button1,button)];
    
    NSArray *constraints3=[NSLayoutConstraint constraintsWithVisualFormat:@"H:|-[button1(button)]" options:0 metrics:nil views:NSDictionaryOfVariableBindings(button1,button)];
    NSArray *constraints4=[NSLayoutConstraint constraintsWithVisualFormat:@"V:[button]-[button1(button)]" options:0 metrics:nil views:NSDictionaryOfVariableBindings(button1,button)];
    
    [self.view addConstraints:constraints3];
    [self.view addConstraints:constraints4];
}

- (void)demo2 {
    NSInteger viewsCount = 3;
    UIView *view1 = [UIView new];
    UIView *view2 = [UIView new];
    UIView *view3 = [UIView new];
    view1.backgroundColor = [UIColor redColor];
    view2.backgroundColor = [UIColor greenColor];
    view3.backgroundColor = [UIColor blueColor];
    view1.translatesAutoresizingMaskIntoConstraints = NO;
    view2.translatesAutoresizingMaskIntoConstraints = NO;
    view3.translatesAutoresizingMaskIntoConstraints = NO;
    [self.view addSubview:view1];
    [self.view addSubview:view2];
    [self.view addSubview:view3];
    NSDictionary *viewsDict = NSDictionaryOfVariableBindings(view1, view2, view3);
    NSLog(@"binding dict = %@", viewsDict);
    
    CGFloat leftMargin = 30;
    CGFloat rightMargin = 30;
    CGFloat topMargin = 100;
    CGFloat viewsWidth = 60;
    CGFloat viewsHeight = 44;
    CGFloat viewsMargin = ([UIScreen mainScreen].bounds.size.width - leftMargin - rightMargin - viewsWidth * viewsCount) / (viewsCount - 1);
    NSDictionary *metricsDict = @{@"leftMargin" : @(leftMargin), @"rightMargin" : @(rightMargin), @"viewsMargin" : @(viewsMargin), @"topMargin" : @(topMargin), @"viewsWidth" : @(viewsWidth), @"viewsHeight" : @(viewsHeight)};
    
    // 实现方案一：
//    NSArray *constraints1 = [NSLayoutConstraint constraintsWithVisualFormat:@"H:|-leftMargin-[view1(viewsWidth)]-viewsMargin-[view2(view1)]-viewsMargin-[view3(view2)]-rightMargin-|" options:NSLayoutFormatAlignAllTop metrics:metricsDict views:viewsDict];
//    NSArray *constraints2 = [NSLayoutConstraint constraintsWithVisualFormat:@"V:|-topMargin-[view1(viewsHeight)]" options:0 metrics:metricsDict views:viewsDict];
//        NSArray *constraints3 = [NSLayoutConstraint constraintsWithVisualFormat:@"V:[view2(view1)]" options:0 metrics:metricsDict views:viewsDict];
//        NSArray *constraints4 = [NSLayoutConstraint constraintsWithVisualFormat:@"V:[view3(view2)]" options:0 metrics:metricsDict views:viewsDict];
//    
//    [self.view addConstraints:constraints1];
//    [self.view addConstraints:constraints2];
//    [self.view addConstraints:constraints3];
//    [self.view addConstraints:constraints4];
    
    // 实现方案二：
    NSArray *constraints1 = [NSLayoutConstraint constraintsWithVisualFormat:@"H:|-leftMargin-[view1(viewsWidth)]-viewsMargin-[view2(view1)]-viewsMargin-[view3(view2)]-rightMargin-|" options:NSLayoutFormatAlignAllTop|NSLayoutFormatAlignAllBottom metrics:metricsDict views:viewsDict];
    NSArray *constraints2 = [NSLayoutConstraint constraintsWithVisualFormat:@"V:|-topMargin-[view1(viewsHeight)]" options:0 metrics:metricsDict views:viewsDict];
    
    [self.view addConstraints:constraints1];
    [self.view addConstraints:constraints2];
}

@end

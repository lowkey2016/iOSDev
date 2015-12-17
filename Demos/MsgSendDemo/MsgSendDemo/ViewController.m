//
//  ViewController.m
//  MsgSendDemo
//
//  Created by Jymn_Chen on 15/12/9.
//  Copyright © 2015年 com.youmi. All rights reserved.
//

#import "ViewController.h"
#import <objc/message.h>

#define HGCMsgSend(target, selector, ...) \
((void (*)(id, SEL, ...))objc_msgSend)(target, selector, ##__VA_ARGS__)

@interface ViewController ()

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    NSString *astr = @"AA";
    NSString *bstr = @"BB";
    
    Book *bk = [Book new];
    HGCMsgSend(bk, @selector(print));
    HGCMsgSend(bk, @selector(printA:), @"AAAA");
    
    void (*msgSendVoidStrStr)(id, SEL, NSString *, NSString *) = (void *)objc_msgSend;
    msgSendVoidStrStr(bk, @selector(printA:B:), astr, bstr);
    
    objc_msgSend()
}

@end

@implementation Book

- (void)print {
    NSLog(@"123");
}

- (void)printA:(NSString *)A {
    NSLog(@"%@", A);
}

- (void)printA:(NSString *)A B:(NSString *)B {
    NSLog(@"%@ %@", A, B);
}

@end
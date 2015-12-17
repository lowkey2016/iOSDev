//
//  ViewController.h
//  MsgSendDemo
//
//  Created by Jymn_Chen on 15/12/9.
//  Copyright © 2015年 com.youmi. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface ViewController : UIViewController


@end



@interface Book : NSObject

- (void)print;
- (void)printA:(NSString *)A;
- (void)printA:(NSString *)A B:(NSString *)B;

@end

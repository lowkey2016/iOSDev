//
//  T3_ClockViewController.m
//  CAAdvancedTechDemo
//
//  Created by Jymn_Chen on 15/11/14.
//  Copyright © 2015年 com.youmi. All rights reserved.
//

#import "T3_ClockViewController.h"

@interface T3_ClockViewController ()

@property (strong, nonatomic) IBOutlet UIView *clockView;

@property (strong, nonatomic) IBOutlet UIView *hourHand;
@property (strong, nonatomic) IBOutlet UIView *minuteHand;
@property (strong, nonatomic) IBOutlet UIView *secondHand;
@property (nonatomic, weak) NSTimer *timer;

@end

@implementation T3_ClockViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    _clockView.layer.masksToBounds = YES;
    _clockView.layer.cornerRadius = 100.0f;
    
    // adjust anchor points
    self.secondHand.layer.anchorPoint = CGPointMake(0.5f, 0.9f);
    self.minuteHand.layer.anchorPoint = CGPointMake(0.5f, 0.9f);
    self.hourHand.layer.anchorPoint = CGPointMake(0.5f, 0.9f);
    
    self.secondHand.layer.zPosition = 1.0f;
    self.minuteHand.layer.zPosition = 2.0f;
    self.hourHand.layer.zPosition = 3.0f;
    
    self.timer = [NSTimer scheduledTimerWithTimeInterval:1.0 target:self selector:@selector(tick) userInfo:nil repeats:YES];
    
    // set initial hand positions
    [self tick];
}

- (void)tick {
    // convert time to hours, minutes and seconds
    NSCalendar *calendar = [[NSCalendar alloc] initWithCalendarIdentifier:NSCalendarIdentifierGregorian];
    NSUInteger units = NSCalendarUnitHour | NSCalendarUnitMinute | NSCalendarUnitSecond;
    NSDateComponents *components = [calendar components:units fromDate:[NSDate date]];
    CGFloat hoursAngle = (components.hour / 12.0) * M_PI * 2.0;
    CGFloat minsAngle = (components.minute / 60.0) * M_PI * 2.0;
    CGFloat secsAngle = (components.second / 60.0) * M_PI * 2.0;
    
    // rotate hands
    self.hourHand.transform = CGAffineTransformMakeRotation(hoursAngle);
    self.minuteHand.transform = CGAffineTransformMakeRotation(minsAngle);
    self.secondHand.transform = CGAffineTransformMakeRotation(secsAngle);
}

@end

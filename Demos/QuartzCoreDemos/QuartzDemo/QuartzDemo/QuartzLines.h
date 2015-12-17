

#import <UIKit/UIKit.h>
#import "QuartzView.h"


#pragma mark -

@interface QuartzLineView : QuartzView

@end


#pragma mark -

@interface QuartzCapJoinWidthView : QuartzView

@property(nonatomic, readwrite) CGLineCap cap;
@property(nonatomic, readwrite) CGLineJoin join;
@property(nonatomic, readwrite) CGFloat width;

@end


#pragma mark -

@interface QuartzDashView : QuartzView

@property(nonatomic, readwrite) CGFloat dashPhase;
-(void)setDashPattern:(CGFloat*)pattern count:(size_t)count;

@end


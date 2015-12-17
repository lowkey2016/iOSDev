

#import <UIKit/UIKit.h>

@interface QuartzView : UIView

// As a matter of convinience we'll do all of our drawing here in subclasses of QuartzView.
-(void)drawInContext:(CGContextRef)context;

@end

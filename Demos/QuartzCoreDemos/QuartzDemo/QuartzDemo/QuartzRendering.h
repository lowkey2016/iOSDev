

#import <UIKit/UIKit.h>
#import "QuartzView.h"

@interface QuartzPatternView : QuartzView

@end


typedef enum : NSInteger
{
	kLinearGradient = 0,
	kRadialGradient = 1
} GradientType;


@interface QuartzGradientView : QuartzView

@property (nonatomic) GradientType type;
@property (nonatomic) BOOL extendsPastStart;
@property (nonatomic) BOOL extendsPastEnd;

@end

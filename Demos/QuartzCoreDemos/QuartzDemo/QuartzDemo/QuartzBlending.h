

#import <UIKit/UIKit.h>
#import "QuartzView.h"

@interface QuartzBlendingView : QuartzView

@property (nonatomic) UIColor *sourceColor;
@property (nonatomic) UIColor *destinationColor;
@property (nonatomic) CGBlendMode blendMode;

@end

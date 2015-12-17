

#import <UIKit/UIKit.h>
#import "QuartzView.h"

@interface QuartzRectView : QuartzView

@end


@interface QuartzPolygonView : QuartzView

@property(nonatomic, readwrite) CGPathDrawingMode drawingMode;

@end

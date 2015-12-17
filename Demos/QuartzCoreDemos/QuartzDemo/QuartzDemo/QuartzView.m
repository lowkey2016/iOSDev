

#import "QuartzView.h"

@implementation QuartzView

/*
 Common view properties are set in the storyboard.
 backgroundColor = [UIColor blackColor];
 opaque = YES;
 clearsContextBeforeDrawing = YES;
*/

/*
 Because we use the CGContext a lot, it is convienient for our demonstration classes to do the real work inside of a method that passes the context as a parameter, rather than having to query the context continuously, or setup that parameter for every subclass.
 */

-(void)drawInContext:(CGContextRef)context
{
	// Default is to do nothing.
}

-(void)drawRect:(CGRect)rect
{
	[self drawInContext:UIGraphicsGetCurrentContext()];
}

@end
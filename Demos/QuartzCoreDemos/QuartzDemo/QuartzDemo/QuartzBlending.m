

#import "QuartzBlending.h"


@implementation QuartzBlendingView

-(void)drawInContext:(CGContextRef)context
{
	// Start with a background whose color we don't use in the demo
	CGContextSetGrayFillColor(context, 0.2, 1.0);
	CGContextFillRect(context, self.bounds);
	// We want to just lay down the background without any blending so we use the Copy mode rather than Normal
	CGContextSetBlendMode(context, kCGBlendModeCopy);
	// Draw a rect with the "background" color - this is the "Destination" for the blending formulas
	CGContextSetFillColorWithColor(context, self.destinationColor.CGColor);
	CGContextFillRect(context, CGRectMake(110.0, 20.0, 100.0, 100.0));
	// Set up our blend mode
	CGContextSetBlendMode(context, self.blendMode);
	// And draw a rect with the "foreground" color - this is the "Source" for the blending formulas
	CGContextSetFillColorWithColor(context, self.sourceColor.CGColor);
	CGContextFillRect(context, CGRectMake(60.0, 45.0, 200.0, 50.0));
}


-(void)setSourceColor:(UIColor*)src
{
	if (src != _sourceColor)
	{
		_sourceColor = src;
		[self setNeedsDisplay];
	}
}


-(void)setDestinationColor:(UIColor*)dest
{
	if (dest != _destinationColor)
	{
		_destinationColor = dest;
		[self setNeedsDisplay];
	}
}


-(void)setBlendMode:(CGBlendMode)mode
{
	if (mode != _blendMode)
	{
		_blendMode = mode;
		[self setNeedsDisplay];
	}
}


@end

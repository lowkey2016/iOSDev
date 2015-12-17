

#import "QuartzRendering.h"

#pragma mark - QuartzPatternView


// Colored patterns specify colors as part of their drawing
void ColoredPatternCallback(void *info, CGContextRef context)
{
	// Dark Blue
	CGContextSetRGBFillColor(context, 29.0 / 255.0, 156.0 / 255.0, 215.0 / 255.0, 1.00);
	CGContextFillRect(context, CGRectMake(0.0, 0.0, 8.0, 8.0));
	CGContextFillRect(context, CGRectMake(8.0, 8.0, 8.0, 8.0));

	// Light Blue
	CGContextSetRGBFillColor(context, 204.0 / 255.0, 224.0 / 255.0, 244.0 / 255.0, 1.00);
	CGContextFillRect(context, CGRectMake(8.0, 0.0, 8.0, 8.0));
	CGContextFillRect(context, CGRectMake(0.0, 8.0, 8.0, 8.0));
}


// Uncolored patterns take their color from the given context
void UncoloredPatternCallback(void *info, CGContextRef context)
{
	CGContextFillRect(context, CGRectMake(0.0, 0.0, 8.0, 8.0));
	CGContextFillRect(context, CGRectMake(8.0, 8.0, 8.0, 8.0));
}



@interface QuartzPatternView ()

@property (nonatomic, readonly) CGColorRef coloredPatternColor;
@property (nonatomic, readonly) CGColorSpaceRef uncoloredPatternColorSpace;

@end


@implementation QuartzPatternView
{
	CGColorRef _coloredPatternColor;
	CGPatternRef _uncoloredPattern;
	CGColorSpaceRef _uncoloredPatternColorSpace;
}


- (CGColorRef)coloredPatternColor
{
    if (_coloredPatternColor == NULL)
    {
        // Colored Pattern setup
        CGPatternCallbacks coloredPatternCallbacks = {0, ColoredPatternCallback, NULL};
        // First we need to create a CGPatternRef that specifies the qualities of our pattern.
        CGPatternRef coloredPattern = CGPatternCreate(
                                                      NULL, // 'info' pointer for our callback
                                                      CGRectMake(0.0, 0.0, 16.0, 16.0), // the pattern coordinate space, drawing is clipped to this rectangle
                                                      CGAffineTransformIdentity, // a transform on the pattern coordinate space used before it is drawn.
                                                      16.0, 16.0, // the spacing (horizontal, vertical) of the pattern - how far to move after drawing each cell
                                                      kCGPatternTilingNoDistortion,
                                                      true, // this is a colored pattern, which means that you only specify an alpha value when drawing it
                                                      &coloredPatternCallbacks); // the callbacks for this pattern.

        // To draw a pattern, you need a pattern colorspace.
        // Since this is an colored pattern, the parent colorspace is NULL, indicating that it only has an alpha value.
        CGColorSpaceRef coloredPatternColorSpace = CGColorSpaceCreatePattern(NULL);
        CGFloat alpha = 1.0;
        // Since this pattern is colored, we'll create a CGColorRef for it to make drawing it easier and more efficient.
        // From here on, the colored pattern is referenced entirely via the associated CGColorRef rather than the
        // originally created CGPatternRef.
        _coloredPatternColor = CGColorCreateWithPattern(coloredPatternColorSpace, coloredPattern, &alpha);
        CGColorSpaceRelease(coloredPatternColorSpace);
        CGPatternRelease(coloredPattern);
    }

    return _coloredPatternColor;
}


- (CGPatternRef)uncoloredPattern
{
    if (_uncoloredPattern == NULL)
    {
        CGPatternCallbacks uncoloredPatternCallbacks = {0, UncoloredPatternCallback, NULL};
        // As above, we create a CGPatternRef that specifies the qualities of our pattern
        _uncoloredPattern = CGPatternCreate(
                                            NULL, // 'info' pointer
                                            CGRectMake(0.0, 0.0, 16.0, 16.0), // coordinate space
                                            CGAffineTransformIdentity, // transform
                                            16.0, 16.0, // spacing
                                            kCGPatternTilingNoDistortion,
                                            false, // this is an uncolored pattern, thus to draw it we need to specify both color and alpha
                                            &uncoloredPatternCallbacks); // callbacks for this pattern
    }

    return _uncoloredPattern;
}



-(CGColorSpaceRef)uncoloredPatternColorSpace;

{
    if (_uncoloredPatternColorSpace == NULL) {
		// With an uncolored pattern we still need to create a pattern colorspace, but now we need a parent colorspace
		// We'll use the DeviceRGB colorspace here. We'll need this colorspace along with the CGPatternRef to draw this pattern later.
		CGColorSpaceRef deviceRGB = CGColorSpaceCreateDeviceRGB();
		_uncoloredPatternColorSpace = CGColorSpaceCreatePattern(deviceRGB);
		CGColorSpaceRelease(deviceRGB);
	}

	return _uncoloredPatternColorSpace;
}


-(void)drawInContext:(CGContextRef)context
{
	// Draw the colored pattern. Since we have a CGColorRef for this pattern, we just set
	// that color current and draw.
	CGContextSetFillColorWithColor(context, self.coloredPatternColor);
	CGContextFillRect(context, CGRectMake(10.0, 10.0, 90.0, 90.0));

	// You can also stroke with a pattern.
	CGContextSetStrokeColorWithColor(context, self.coloredPatternColor);
	CGContextStrokeRectWithWidth(context, CGRectMake(120.0, 10.0, 90.0, 90.0), 8.0);

	// Since we aren't encapsulating our pattern in a CGColorRef for the uncolored pattern case, setup requires two steps.
	// First you have to set the context's current colorspace (fill or stroke) to a pattern colorspace,
	// indicating to Quartz that you want to draw a pattern.
	CGContextSetFillColorSpace(context, self.uncoloredPatternColorSpace);
	// Next you set the pattern and the color that you want the pattern to draw with.
	CGFloat color1[] = {1.0, 0.0, 0.0, 1.0};
	CGContextSetFillPattern(context, self.uncoloredPattern, color1);
	// And finally you draw!
	CGContextFillRect(context, CGRectMake(10.0, 120.0, 90.0, 90.0));
	// As long as the current colorspace is a pattern colorspace, you are free to change the pattern or pattern color
	CGFloat color2[] = {0.0, 1.0, 0.0, 1.0};
	CGContextSetFillPattern(context, self.uncoloredPattern, color2);
	CGContextFillRect(context, CGRectMake(10.0, 230.0, 90.0, 90.0));

	// And of course, just like the colored case, you can stroke with a pattern as well.
	CGContextSetStrokeColorSpace(context, self.uncoloredPatternColorSpace);
	CGContextSetStrokePattern(context, self.uncoloredPattern, color1);
	CGContextStrokeRectWithWidth(context, CGRectMake(120.0, 120.0, 90.0, 90.0), 8.0);
	// As long as the current colorspace is a pattern colorspace, you are free to change the pattern or pattern color
	CGContextSetStrokePattern(context, self.uncoloredPattern, color2);
	CGContextStrokeRectWithWidth(context, CGRectMake(120.0, 230.0, 90.0, 90.0), 8.0);
}


-(void)dealloc
{
	CGColorRelease(_coloredPatternColor);
	CGPatternRelease(_uncoloredPattern);
	CGColorSpaceRelease(_uncoloredPatternColorSpace);
}


@end



#pragma mark - QuartzGradientView


@interface QuartzGradientView ()

@property (nonatomic, readonly) CGGradientRef gradient;

@end



@implementation QuartzGradientView
{
    CGGradientRef _gradient;
}


-(CGGradientRef)gradient
{
	if(_gradient == NULL)
	{
		CGColorSpaceRef rgb = CGColorSpaceCreateDeviceRGB();
		CGFloat colors[] =
		{
			204.0 / 255.0, 224.0 / 255.0, 244.0 / 255.0, 1.00,
            29.0 / 255.0, 156.0 / 255.0, 215.0 / 255.0, 1.00,
            0.0 / 255.0,  50.0 / 255.0, 126.0 / 255.0, 1.00,
		};
		_gradient = CGGradientCreateWithColorComponents(rgb, colors, NULL, sizeof(colors)/(sizeof(colors[0])*4));
		CGColorSpaceRelease(rgb);
	}
	return _gradient;
}


// Returns an appropriate starting point for the demonstration of a linear gradient
CGPoint demoLGStart(CGRect bounds)
{
	return CGPointMake(bounds.origin.x, bounds.origin.y + bounds.size.height * 0.25);
}


// Returns an appropriate ending point for the demonstration of a linear gradient
CGPoint demoLGEnd(CGRect bounds)
{
	return CGPointMake(bounds.origin.x, bounds.origin.y + bounds.size.height * 0.75);
}


// Returns the center point for for the demonstration of the radial gradient
CGPoint demoRGCenter(CGRect bounds)
{
	return CGPointMake(CGRectGetMidX(bounds), CGRectGetMidY(bounds));
}


// Returns an appropriate inner radius for the demonstration of the radial gradient
CGFloat demoRGInnerRadius(CGRect bounds)
{
	CGFloat r = bounds.size.width < bounds.size.height ? bounds.size.width : bounds.size.height;
	return r * 0.125;
}


// Returns an appropriate outer radius for the demonstration of the radial gradient
CGFloat demoRGOuterRadius(CGRect bounds)
{
	CGFloat r = bounds.size.width < bounds.size.height ? bounds.size.width : bounds.size.height;
	return r * 0.5;
}


-(CGGradientDrawingOptions)drawingOptions
{
	CGGradientDrawingOptions options = 0;
	if (self.extendsPastStart)
	{
		options |= kCGGradientDrawsBeforeStartLocation;
	}
	if (self.extendsPastEnd)
	{
		options |= kCGGradientDrawsAfterEndLocation;
	}
	return options;
}


-(void)drawInContext:(CGContextRef)context
{
	// Use the clip bounding box, sans a generous border
	CGRect clip = CGRectInset(CGContextGetClipBoundingBox(context), 20.0, 20.0);

	CGPoint start, end;
	CGFloat startRadius, endRadius;

	// Clip to area to draw the gradient, and draw it. Since we are clipping, we save the graphics state
	// so that we can revert to the previous larger area.
	CGContextSaveGState(context);
	CGContextClipToRect(context, clip);

	CGGradientDrawingOptions options = [self drawingOptions];
	switch(self.type)
    {
            /**
             *  1.
             */
		case kLinearGradient:
			// A linear gradient requires only a starting & ending point.
			// The colors of the gradient are linearly interpolated along the line segment connecting these two points
			// A gradient location of 0.0 means that color is expressed fully at the 'start' point
			// a location of 1.0 means that color is expressed fully at the 'end' point.
			// The gradient fills outwards perpendicular to the line segment connectiong start & end points
			// (which is why we need to clip the context, or the gradient would fill beyond where we want it to).
			// The gradient options (last) parameter determines what how to fill the clip area that is "before" and "after"
			// the line segment connecting start & end.
			start = demoLGStart(clip);
			end = demoLGEnd(clip);
			CGContextDrawLinearGradient(context, self.gradient, start, end, options);
			CGContextRestoreGState(context);
			break;
            
            
            /**
             *  2.
             */
		case kRadialGradient:
			// A radial gradient requires a start & end point as well as a start & end radius.
			// Logically a radial gradient is created by linearly interpolating the center, radius and color of each
			// circle using the start and end point for the center, start and end radius for the radius, and the color ramp
			// inherant to the gradient to create a set of stroked circles that fill the area completely.
			// The gradient options specify if this interpolation continues past the start or end points as it does with
			// linear gradients.
			start = end = demoRGCenter(clip);
			startRadius = demoRGInnerRadius(clip);
			endRadius = demoRGOuterRadius(clip);
			CGContextDrawRadialGradient(context, self.gradient, start, startRadius, end, endRadius, options);
			CGContextRestoreGState(context);
			break;
	}
    
    
    /**
     *  3.
     */
	// Show the clip rect
	CGContextSetRGBStrokeColor(context, 1.0, 0.0, 0.0, 1.0);
	CGContextStrokeRectWithWidth(context, clip, 2.0);
}


-(void)setType:(GradientType)newType
{
	if (newType != _type)
	{
		_type = newType;
		[self setNeedsDisplay];
	}
}


-(void)setExtendsPastStart:(BOOL)yn
{
	if (yn != _extendsPastStart)
	{
		_extendsPastStart = yn;
		[self setNeedsDisplay];
	}
}


-(void)setExtendsPastEnd:(BOOL)yn
{
	if (yn != _extendsPastEnd)
	{
		_extendsPastEnd = yn;
		[self setNeedsDisplay];
	}
}


-(void)dealloc
{
	CGGradientRelease(_gradient);
}


@end




#import "QuartzLines.h"

#pragma mark -

@implementation QuartzLineView

-(void)drawInContext:(CGContextRef)context
{
    /**
     *  1.
     */
	// Drawing lines with a white stroke color
	CGContextSetRGBStrokeColor(context, 1.0, 1.0, 1.0, 1.0);
	// Draw them with a 2.0 stroke width so they are a bit more visible.
	CGContextSetLineWidth(context, 2.0);
	
	// Draw a single line from left to right
	CGContextMoveToPoint(context, 10.0, 30.0);
	CGContextAddLineToPoint(context, 310.0, 30.0);
	CGContextStrokePath(context);
	
    
    /**
     *  2.
     */
	// Draw a connected sequence of line segments
	CGPoint addLines[] =
	{
		CGPointMake(10.0, 90.0),
		CGPointMake(70.0, 60.0),
		CGPointMake(130.0, 90.0),
		CGPointMake(190.0, 60.0),
		CGPointMake(250.0, 90.0),
		CGPointMake(310.0, 60.0),
	};
	// Bulk call to add lines to the current path.
	// Equivalent to MoveToPoint(points[0]); for(i=1; i<count; ++i) AddLineToPoint(points[i]);
	CGContextAddLines(context, addLines, sizeof(addLines)/sizeof(addLines[0]));
	CGContextStrokePath(context);
	
    
    /**
     *  3.
     */
	// Draw a series of line segments. Each pair of points is a segment
	CGPoint strokeSegments[] =
	{
		CGPointMake(10.0, 150.0),
		CGPointMake(70.0, 120.0),
		CGPointMake(130.0, 150.0),
		CGPointMake(190.0, 120.0),
		CGPointMake(250.0, 150.0),
		CGPointMake(310.0, 120.0),
	};
	// Bulk call to stroke a sequence of line segments.
	// Equivalent to for(i=0; i<count; i+=2) { MoveToPoint(point[i]); AddLineToPoint(point[i+1]); StrokePath(); }
	CGContextStrokeLineSegments(context, strokeSegments, sizeof(strokeSegments)/sizeof(strokeSegments[0]));
}

@end


#pragma mark -

@implementation QuartzCapJoinWidthView


-(void)drawInContext:(CGContextRef)context
{
    /**
     *  1.
     */
	// Drawing lines with a white stroke color
	CGContextSetRGBStrokeColor(context, 1.0, 1.0, 1.0, 1.0);
	
	// Preserve the current drawing state
	CGContextSaveGState(context);
	
	// Setup the horizontal line to demostrate caps
	CGContextMoveToPoint(context, 40.0, 30.0);
	CGContextAddLineToPoint(context, 280.0, 30.0);
    
	// Set the line width & cap for the cap demo
	CGContextSetLineWidth(context, self.width);
	CGContextSetLineCap(context, self.cap);
	CGContextStrokePath(context);
	
	// Restore the previous drawing state, and save it again.
	CGContextRestoreGState(context);
    
    
    /**
     *  2.
     */
	CGContextSaveGState(context);
	
	// Setup the angled line to demonstrate joins
	CGContextMoveToPoint(context, 40.0, 190.0);
	CGContextAddLineToPoint(context, 160.0, 70.0);
	CGContextAddLineToPoint(context, 280.0, 190.0);
    
	// Set the line width & join for the join demo
	CGContextSetLineWidth(context, self.width);
	CGContextSetLineJoin(context, self.join);
	CGContextStrokePath(context);
    
	// Restore the previous drawing state.
	CGContextRestoreGState(context);
    
    
    /**
     *  3.
     */
	// If the stroke width is large enough, display the path that generated these lines
	if (self.width >= 4.0) // arbitrarily only show when the line is at least twice as wide as our target stroke
	{
		CGContextSetRGBStrokeColor(context, 1.0, 0.0, 0.0, 1.0);
		CGContextMoveToPoint(context, 40.0, 30.0);
		CGContextAddLineToPoint(context, 280.0, 30.0);
		CGContextMoveToPoint(context, 40.0, 190.0);
		CGContextAddLineToPoint(context, 160.0, 70.0);
		CGContextAddLineToPoint(context, 280.0, 190.0);
		CGContextSetLineWidth(context, 2.0);
		CGContextStrokePath(context);
	}
}

-(void)setCap:(CGLineCap)c
{
	if(c != _cap)
	{
		_cap = c;
		[self setNeedsDisplay];
	}
}

-(void)setJoin:(CGLineJoin)j
{
	if(j != _join)
	{
		_join = j;
		[self setNeedsDisplay];
	}
}

-(void)setWidth:(CGFloat)w
{
	if(w != _width)
	{
		_width = w;
		[self setNeedsDisplay];
	}
}

@end



#pragma mark -

@implementation QuartzDashView
{
	CGFloat dashPattern[10];
	size_t dashCount;
}


-(void)setDashPhase:(CGFloat)phase
{
	if (phase != _dashPhase)
	{
		_dashPhase = phase;
		[self setNeedsDisplay];
	}
}


-(void)setDashPattern:(CGFloat *)pattern count:(size_t)count
{
	if ((count != dashCount) || (memcmp(dashPattern, pattern, sizeof(CGFloat) * count) != 0))
	{
		memcpy(dashPattern, pattern, sizeof(CGFloat) * count);
		dashCount = count;
		[self setNeedsDisplay];
	}
}


-(void)drawInContext:(CGContextRef)context
{
	// Drawing lines with a white stroke color
	CGContextSetRGBStrokeColor(context, 1.0, 1.0, 1.0, 1.0);
	
	// Each dash entry is a run-length in the current coordinate system
	// The concept is first you determine how many points in the current system you need to fill.
	// Then you start consuming that many pixels in the dash pattern for each element of the pattern.
	// So for example, if you have a dash pattern of {10, 10}, then you will draw 10 points, then skip 10 points, and repeat.
	// As another example if your dash pattern is {10, 20, 30}, then you draw 10 points, skip 20 points, draw 30 points,
	// skip 10 points, draw 20 points, skip 30 points, and repeat.
	// The dash phase factors into this by stating how many points into the dash pattern to skip.
	// So given a dash pattern of {10, 10} with a phase of 5, you would draw 5 points (since phase plus 5 yields 10 points),
	// then skip 10, draw 10, skip 10, draw 10, etc.
	
	CGContextSetLineDash(context, self.dashPhase, dashPattern, dashCount);
	
	// Draw a horizontal line, vertical line, rectangle and circle for comparison
	CGContextMoveToPoint(context, 10.0, 20.0);
	CGContextAddLineToPoint(context, 310.0, 20.0);
	CGContextMoveToPoint(context, 160.0, 30.0);
	CGContextAddLineToPoint(context, 160.0, 130.0);
	CGContextAddRect(context, CGRectMake(10.0, 30.0, 100.0, 100.0));
	CGContextAddEllipseInRect(context, CGRectMake(210.0, 30.0, 100.0, 100.0));
	// And width 2.0 so they are a bit more visible
	CGContextSetLineWidth(context, 2.0);
	CGContextStrokePath(context);
}

@end




#import "QuartzPolygons.h"

@implementation QuartzRectView

-(void)drawInContext:(CGContextRef)context
{
    /**
     *  1.
     */
	// Drawing with a white stroke color
	CGContextSetRGBStrokeColor(context, 1.0, 1.0, 1.0, 1.0);
	// And drawing with a blue fill color
	CGContextSetRGBFillColor(context, 0.0, 0.0, 1.0, 1.0);
	// Draw them with a 2.0 stroke width so they are a bit more visible.
	CGContextSetLineWidth(context, 2.0);
	
	// Add Rect to the current path, then stroke it
	CGContextAddRect(context, CGRectMake(30.0, 30.0, 60.0, 60.0));
	CGContextStrokePath(context);
	
	// Stroke Rect convenience that is equivalent to above
	CGContextStrokeRect(context, CGRectMake(30.0, 120.0, 60.0, 60.0));
	
	// Stroke rect convenience equivalent to the above, plus a call to CGContextSetLineWidth().
	CGContextStrokeRectWithWidth(context, CGRectMake(30.0, 210.0, 60.0, 60.0), 10.0);
	// Demonstate the stroke is on both sides of the path.
	CGContextSaveGState(context);
	CGContextSetRGBStrokeColor(context, 1.0, 0.0, 0.0, 1.0);
	CGContextStrokeRectWithWidth(context, CGRectMake(30.0, 210.0, 60.0, 60.0), 2.0);
	CGContextRestoreGState(context);
	
    
    /**
     *  2.
     */
	CGRect rects[] = 
	{
		CGRectMake(120.0, 30.0, 60.0, 60.0),
		CGRectMake(120.0, 120.0, 60.0, 60.0),
		CGRectMake(120.0, 210.0, 60.0, 60.0),
	};
	// Bulk call to add rects to the current path.
	CGContextAddRects(context, rects, sizeof(rects)/sizeof(rects[0]));
	CGContextStrokePath(context);
	
    
    /**
     *  3.
     */
	// Create filled rectangles via two different paths.
	// Add/Fill path
	CGContextAddRect(context, CGRectMake(210.0, 30.0, 60.0, 60.0));
	CGContextFillPath(context);
	// Fill convienience.
	CGContextFillRect(context, CGRectMake(210.0, 120.0, 60.0, 60.0));
}

@end




@implementation QuartzPolygonView

-(void)setDrawingMode:(CGPathDrawingMode)mode
{
	if (mode != _drawingMode)
	{
		_drawingMode = mode;
		[self setNeedsDisplay];
	}
}

-(void)drawInContext:(CGContextRef)context
{
	// Drawing with a white stroke color
	CGContextSetRGBStrokeColor(context, 1.0, 1.0, 1.0, 1.0);
	// Drawing with a blue fill color
	CGContextSetRGBFillColor(context, 0.0, 0.0, 1.0, 1.0);
	// Draw them with a 2.0 stroke width so they are a bit more visible.
	CGContextSetLineWidth(context, 2.0);

	CGPoint center;

    
    /**
     *  1.
     */
	// Add a star to the current path
	center = CGPointMake(90.0, 90.0);
	CGContextMoveToPoint(context, center.x, center.y + 60.0);
	for(int i = 1; i < 5; ++i)
	{
		CGFloat x = 60.0 * sinf(i * 4.0 * M_PI / 5.0);
		CGFloat y = 60.0 * cosf(i * 4.0 * M_PI / 5.0);
		CGContextAddLineToPoint(context, center.x + x, center.y + y);
	}
	// And close the subpath.
	CGContextClosePath(context);

    
    /**
     *  2.
     */
	// Now add the hexagon to the current path
	center = CGPointMake(210.0, 90.0);
	CGContextMoveToPoint(context, center.x, center.y + 60.0);
	for(int i = 1; i < 6; ++i)
	{
		CGFloat x = 60.0 * sinf(i * 2.0 * M_PI / 6.0);
		CGFloat y = 60.0 * cosf(i * 2.0 * M_PI / 6.0);
		CGContextAddLineToPoint(context, center.x + x, center.y + y);
	}
	// And close the subpath.
	CGContextClosePath(context);
	
	// Now draw the star & hexagon with the current drawing mode.
	CGContextDrawPath(context, self.drawingMode);
    
    
    /**
     奇偶规则
     
     　　最外层的边界代表内部都有效，都要填充；之后向内第二个边界代表它的内部无效，不需填充；如此规则继续向内寻找边界线。我们的情况非常简单，所以使用奇偶规则就很容易了。这里我们使用CGContextEOCllip设置裁剪区域然后进行绘图。
     */
}

@end

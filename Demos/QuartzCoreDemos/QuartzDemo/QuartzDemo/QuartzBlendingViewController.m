

#import "QuartzBlendingViewController.h"
#import "QuartzBlending.h"


/*
 These strings represent the actual blend mode constants that are passed to CGContextSetBlendMode and so should not be localized in the context of this sample.
 */
static NSString *blendModes[] = {
	// PDF Blend Modes.
	@"Normal",
	@"Multiply",
	@"Screen",
	@"Overlay",
	@"Darken",
	@"Lighten",
	@"ColorDodge",
	@"ColorBurn",
	@"SoftLight",
	@"HardLight",
	@"Difference",
	@"Exclusion",
	@"Hue",
	@"Saturation",
	@"Color",
	@"Luminosity",
	// Porter-Duff Blend Modes.
	@"Clear",
	@"Copy",
	@"SourceIn",
	@"SourceOut",
	@"SourceAtop",
	@"DestinationOver",
	@"DestinationIn",
	@"DestinationOut",
	@"DestinationAtop",
	@"XOR",
	@"PlusDarker",
	@"PlusLighter",
	// If Quartz provides more blend modes in the future, add them here.
};
static NSInteger blendModeCount = sizeof(blendModes) / sizeof(blendModes[0]);


// Calculate the luminance for an arbitrary UIColor instance
CGFloat luminanceForColor(UIColor *color)
{
	CGColorRef cgColor = color.CGColor;
	const CGFloat *components = CGColorGetComponents(cgColor);
	CGFloat luminance = 0.0;
	switch(CGColorSpaceGetModel(CGColorGetColorSpace(cgColor)))
	{
		case kCGColorSpaceModelMonochrome:
			// For grayscale colors, the luminance is the color value
			luminance = components[0];
			break;

		case kCGColorSpaceModelRGB:
			/*
             For RGB colors, we calculate luminance assuming sRGB Primaries as per http://en.wikipedia.org/wiki/Luminance_(relative).
			*/
            luminance = 0.2126 * components[0] + 0.7152 * components[1] + 0.0722 * components[2];
			break;

		default:
			/*
             We don't implement support for non-gray, non-rgb colors at this time. Because our only consumer is colorSortByLuminance, we return a larger than normal value to ensure that these types of colors are sorted to the end of the list.
             */
			luminance = 2.0;
	}
	return luminance;
}



@interface QuartzBlendingViewController()

@property (nonatomic, weak) IBOutlet QuartzBlendingView *quartzBlendingView;
@property (nonatomic, weak) IBOutlet UIPickerView *picker;
@property (nonatomic, readonly) NSArray *colors;

@end



@implementation QuartzBlendingViewController

-(void)viewDidLoad
{
	[super viewDidLoad];

    // Setup the view's and picker's default components.
	QuartzBlendingView *qbv = self.quartzBlendingView;

    qbv.sourceColor = [UIColor whiteColor];
    qbv.destinationColor = [UIColor blackColor];
    qbv.blendMode = kCGBlendModeNormal;

    [self.picker selectRow:[self.colors indexOfObject:qbv.destinationColor] inComponent:0 animated:NO];
	[self.picker selectRow:[self.colors indexOfObject:qbv.sourceColor] inComponent:1 animated:NO];
	[self.picker selectRow:qbv.blendMode inComponent:2 animated:NO];
}


- (NSArray*)colors
{
	static NSArray *colorArray = nil;

	if (colorArray == nil)
	{
		/*
         If you want to add more colors, do so here. You can also add patterns, they will simply be sorted to the end of the list.
         */
		NSArray *unsortedArray = @[[UIColor redColor], [UIColor greenColor], [UIColor blueColor], [UIColor yellowColor], [UIColor magentaColor], [UIColor cyanColor], [UIColor orangeColor], [UIColor purpleColor], [UIColor brownColor], [UIColor whiteColor], [UIColor lightGrayColor], [UIColor darkGrayColor], [UIColor blackColor]];

        colorArray = [unsortedArray sortedArrayUsingComparator:^NSComparisonResult(id color1, id color2) {
            // Sort two colors by luminance.
            CGFloat luminance1 = luminanceForColor(color1);
            CGFloat luminance2 = luminanceForColor(color2);
            if (luminance1 == luminance2)
            {
                return NSOrderedSame;
            }
            else if (luminance1 < luminance2)
            {
                return NSOrderedAscending;
            }
            else
            {
                return NSOrderedDescending;
            }
        }];

	}
	return colorArray;
}

#pragma mark UIPickerViewDelegate & UIPickerViewDataSource methods

-(NSInteger)numberOfComponentsInPickerView:(UIPickerView *)pickerView
{
	return 3;
}


-(NSInteger)pickerView:(UIPickerView *)pickerView numberOfRowsInComponent:(NSInteger)component
{
    if (component == 2) {
        return blendModeCount;
    }

	return [self.colors count];
}


-(CGFloat)pickerView:(UIPickerView *)pickerView widthForComponent:(NSInteger)component
{
    if (component == 2) {
        return 200.0;
    }

	return 40.0;
}


#define kColorTag 1
#define kLabelTag 2

/*
 Return an attributes string that shows the color or the name of the blend mode as appropriate.
 */
- (NSAttributedString *)pickerView:(UIPickerView *)pickerView attributedTitleForRow:(NSInteger)row forComponent:(NSInteger)component
{

    if (component == 2) {
        return [[NSAttributedString alloc] initWithString:blendModes[row]];
    }

    static NSString *squareString = nil;
    if (squareString == nil) {
        // This is a Unicode character for a simple square block.
        unichar squareCharacter = 0x2588;
        squareString = [[NSString alloc] initWithFormat:@"%C", squareCharacter];
    }
    
    NSDictionary *attributes = @{ NSForegroundColorAttributeName : self.colors[row], NSBackgroundColorAttributeName : [UIColor lightGrayColor] };
    NSAttributedString *attributedString = [[NSAttributedString alloc] initWithString:squareString attributes:attributes];

	return attributedString;
}


-(void)pickerView:(UIPickerView *)pickerView didSelectRow:(NSInteger)row inComponent:(NSInteger)component
{
	QuartzBlendingView *qbv = (QuartzBlendingView*)self.quartzBlendingView;
    
	qbv.destinationColor = (self.colors)[[self.picker selectedRowInComponent:0]];
	qbv.sourceColor = (self.colors)[[self.picker selectedRowInComponent:1]];
	qbv.blendMode = [self.picker selectedRowInComponent:2];
}


@end

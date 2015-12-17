

#import "QuartzPolyViewController.h"
#import "QuartzPolygons.h"


@interface QuartzPolyViewController()

@property(nonatomic, readwrite, strong) IBOutlet UIPickerView *picker;
@property (nonatomic, weak) IBOutlet QuartzPolygonView *quartzPolygonView;

@end



/*
 These strings represent the actual drawing mode constants that are passed to CGContextDrawpath and as such should not be localized in the context of this sample.
 */
static NSString *drawModes[] = {
	@"Fill",//0
	@"EOFill",//1
	@"Stroke",//2
	@"FillStroke",//3
	@"EOFillStroke"//4
};
static NSInteger drawModeCount = sizeof(drawModes) / sizeof(drawModes[0]);


@implementation QuartzPolyViewController

// Setup the picker's default components.
-(void)viewDidLoad
{
	[super viewDidLoad];
	[self.picker selectRow:self.quartzPolygonView.drawingMode inComponent:0 animated:NO];
}


#pragma mark UIPickerViewDelegate & UIPickerViewDataSource methods

-(NSInteger)numberOfComponentsInPickerView:(UIPickerView *)pickerView
{
	return 1;
}


-(NSInteger)pickerView:(UIPickerView *)pickerView numberOfRowsInComponent:(NSInteger)component
{
	return drawModeCount;
}


-(NSString *)pickerView:(UIPickerView *)pickerView titleForRow:(NSInteger)row forComponent:(NSInteger)component;
{
	return drawModes[row];
}


-(void)pickerView:(UIPickerView *)pickerView didSelectRow:(NSInteger)row inComponent:(NSInteger)component
{
	self.quartzPolygonView.drawingMode = (CGPathDrawingMode)[self.picker selectedRowInComponent:0];
}

@end

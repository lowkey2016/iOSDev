

#import "QuartzDashViewController.h"
#import "QuartzLines.h"

@interface QuartzDashViewController()

@property(nonatomic, weak) IBOutlet QuartzDashView *quartzDashView;

@property(nonatomic, weak) IBOutlet UIPickerView *picker;
@property(nonatomic, weak) IBOutlet UISlider *phaseSlider;

@end



typedef struct {
	CGFloat pattern[5];
	size_t count;
} Pattern;

static Pattern patterns[] = {
	{{10.0, 10.0}, 2},
	{{10.0, 20.0, 10.0}, 3},
	{{10.0, 20.0, 30.0}, 3},
	{{10.0, 20.0, 10.0, 30.0}, 4},
	{{10.0, 10.0, 20.0, 20.0}, 4},
	{{10.0, 10.0, 20.0, 30.0, 50.0}, 5},
};
static NSInteger patternCount = sizeof(patterns) / sizeof(patterns[0]);


@implementation QuartzDashViewController


// Setup the picker's default components.
-(void)viewDidLoad
{
	[super viewDidLoad];
    [self.quartzDashView setDashPattern:patterns[0].pattern count:patterns[0].count];
	[self.picker selectRow:0 inComponent:0 animated:NO];
}


-(IBAction)takeDashPhaseFrom:(UISlider *)sender
{
	self.quartzDashView.dashPhase = sender.value;
}


-(IBAction)reset:sender
{
	self.phaseSlider.value = 0.0;
	self.quartzDashView.dashPhase = 0.0;
}


#pragma mark UIPickerViewDelegate & UIPickerViewDataSource methods

-(NSInteger)numberOfComponentsInPickerView:(UIPickerView *)pickerView
{
	return 1;
}


-(NSInteger)pickerView:(UIPickerView *)pickerView numberOfRowsInComponent:(NSInteger)component
{
	return patternCount;
}


-(NSString *)pickerView:(UIPickerView *)pickerView titleForRow:(NSInteger)row forComponent:(NSInteger)component;
{
	Pattern p = patterns[row];
	NSMutableString *title = [NSMutableString stringWithFormat:@"%.0f", p.pattern[0]];
	for (size_t i = 1; i < p.count; ++i)
	{
		[title appendFormat:@"-%.0f", p.pattern[i]];
	}
	return title;
}


-(void)pickerView:(UIPickerView *)pickerView didSelectRow:(NSInteger)row inComponent:(NSInteger)component
{
	[self.quartzDashView setDashPattern:patterns[row].pattern count:patterns[row].count];
}


@end

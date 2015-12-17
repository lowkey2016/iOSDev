

#import "QuartzLineViewController.h"
#import "QuartzLines.h"


@interface QuartzLineViewController ()
@property (nonatomic, weak) IBOutlet QuartzCapJoinWidthView *quartzCapJoinWidthView;

@property (nonatomic, weak) IBOutlet UISegmentedControl *capSegmentedControl;
@property (nonatomic, weak) IBOutlet UISegmentedControl *joinSegmentedControl;
@property (nonatomic, weak) IBOutlet UISlider *lineWidthSlider;

@end


@implementation QuartzLineViewController

-(void)viewDidLoad
{
    [super viewDidLoad];
    
	self.quartzCapJoinWidthView.cap = (CGLineCap)[self.capSegmentedControl selectedSegmentIndex];
    self.quartzCapJoinWidthView.join = (CGLineJoin)[self.joinSegmentedControl selectedSegmentIndex];
	self.quartzCapJoinWidthView.width = self.lineWidthSlider.value;
}

-(IBAction)takeLineCapFrom:(UISegmentedControl *)sender
{
	self.quartzCapJoinWidthView.cap = (CGLineCap)[sender selectedSegmentIndex];
}

-(IBAction)takeLineJoinFrom:(UISegmentedControl *)sender
{
	self.quartzCapJoinWidthView.join = (CGLineJoin)[sender selectedSegmentIndex];
}

-(IBAction)takeLineWidthFrom:(UISlider *)sender
{
	self.quartzCapJoinWidthView.width = sender.value;
}

@end

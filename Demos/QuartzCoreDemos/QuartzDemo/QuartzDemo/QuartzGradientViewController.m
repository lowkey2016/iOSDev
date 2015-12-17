

#import "QuartzGradientViewController.h"
#import "QuartzRendering.h"

@interface QuartzGradientViewController()

@property (nonatomic, weak) IBOutlet QuartzGradientView *quartzGradientView;

@property (nonatomic, weak) IBOutlet UISegmentedControl *gradientTypeSegmentedControl;
@property (nonatomic, weak) IBOutlet UISwitch *extendsPastStartSwitch;
@property (nonatomic, weak) IBOutlet UISwitch *extendsPastEndSwitch;

@end


@implementation QuartzGradientViewController

-(IBAction)takeGradientTypeFrom:(UISegmentedControl *)sender
{
	self.quartzGradientView.type = [sender selectedSegmentIndex];
}


-(IBAction)takeExtendsPastStartFrom:(UISwitch *)sender
{
	self.quartzGradientView.extendsPastStart = [sender isOn];
}


-(IBAction)takeExtendsPastEndFrom:(UISwitch *)sender
{
	self.quartzGradientView.extendsPastEnd = [sender isOn];
}


-(void)viewDidLoad
{
    [super viewDidLoad];
	self.quartzGradientView.type = [self.gradientTypeSegmentedControl selectedSegmentIndex];
	self.quartzGradientView.extendsPastStart = [self.extendsPastStartSwitch isOn];
	self.quartzGradientView.extendsPastEnd = [self.extendsPastEndSwitch isOn];
}


@end

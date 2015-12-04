# FFSS开发笔记（2）修复快速重复点击 NavigationItem 导致的导航栈错乱问题

## 又出 BUG 了

昨晚项目老大 monkey test 下我的 FFSS App，首页左上角有一个 NavigationItem，点击后将新建一个 XXViewController，然后 self.navigationController push XXViewController，如果快速重复点击这个 item ，就会出现 push 动画还没执行完，left navigation item 就恢复点击并响应，导致一个新的 XXViewController 被 push 了若干次。

另外，发现微信第二个Tab的添加好友 right navigation item 也有类似的问题，Coding.net客户端也有，还是乖乖做些防御行为吧。

## 怎么办？

为了避免对带有 NavigationItems 的 ViewController 逐个逐个改，要想一个全局的方法，目前想到的方法是：

目前我在项目中写了一个 UINavigationController 的子类 CRNavigationController，在初始化该类时设置 delegate 为 self，然后覆写 pushViewController:animated: 方法，在该方法中禁用 navigationBar，等 didShowViewController 后，再启用 navigationBar，代码如下：

```
@interface CRNavigationController () <UINavigationControllerDelegate>

@end

@implementation CRNavigationController

#pragma mark - Init

- (instance)init {
	 // ...
	 self.delegate = self;
	 // ...
}

- (instance)initWithRootViewController:(UIViewController *)rootViewController {
	 // ...
	 self.delegate = self;
	 // ...
}

#pragma mark - UINavigationControllerDelegate

- (void)navigationController:(UINavigationController *)navigationController didShowViewController:(UIViewController *)viewController animated:(BOOL)animated
{
    self.navigationBar.userInteractionEnabled = YES;
}

- (void)pushViewController:(UIViewController *)viewController animated:(BOOL)animated {
    [super pushViewController:viewController animated:animated];
    
    self.navigationBar.userInteractionEnabled = NO;
}

@end
```

## 小结

没啥好小结的，Swift今天开源了。。。好多东西要看。。。

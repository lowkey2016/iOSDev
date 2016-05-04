# iOS 工程规范

## 规范实行方式建议

* 下面规范将作为 iOS 工程师的职级考核的衡量标准之一，无论哪个职级的工程师在申请升级时如果下面列出的规范如果没有遵守的应该当作减分项，并且要修正。
* 定期的代码互查。

## Xcode 工程结构

### 注意事项

1. 工程命名应该和项目一致，遵循 UpperCamelCase 写法（第一个词的首字母，以及后面每个词的首字母都大写，除了 iOS 的 i 这种），禁用中文。
2. 为了避免文件杂乱，物理文件应该保持和 Xcode 项目文件同步。Xcode 创建的任何组（group）都必须在文件系统有相应的映射。
3. 工程文件里不能记录某些账号和密码。
4. 尽量不要有 `warning`: 类似数据类型隐式转换这种低级的 `warning` 绝不能出现。类似 `perform unrecognizer selector` 这种 `warning` 可以用 `#pragma clang diagnostic push` 这种编译指令将其去掉（所有 `warning` 参见 [fuckingclangwarnings.com](http://fuckingclangwarnings.com/)）。对于 `CocoaPods` 安装第三方库带来的 `warning` 可以在 `Podfile` 中配置 `inhibit_all_warnings!` 去掉。对于开发者自己打的 `warning` ，在发布版本之前要逐个检查，确认无误或者完成后才能发布。
5. 工程必须要有 `README.md` 和 `CHANGELOG.md` ，建议每个代码文件夹写一个 `README.md` 说明该模块是做什么的，起到文档作用。
6. 工程中每个自己新建的文件都必须带有前缀标识，前缀标识必须全局一致，全部字母大写。

### App 工程结构（目前仅适用于 Objective-C 工程，传统的 MVC 架构）

两种建议（假设下面的工程以 DMP 为前缀）：

第一种是先按代码逻辑划分，再在每个目录中按功能模块细分：

	|—— DemoProject
	|	|—— Common: 存放全局通用的头文件，例如 DMPConstants.h, DMPAppKeys.h, DMPMacros.h
	|	|—— Vendor: 不适合通过 CocoaPods 引入的第三方类库，例如需要经常改动的或者自己定制的
	|	|—— Resources: 存放各种资源，例如语言国际化文件组成的 bundle 文件，Images.xcassets 等
	|	|—— Utils: 工具类，可以便捷地迁移到其它工程
	|	|	|—— Categories: 存放各种 Category
	|	|	|—— Helpers: 例如获取设备信息、App 信息之类的工具类
	|	|—— Models: 数据模型类
	|	|—— Logic: 各种业务逻辑类
	|	|	|—— Global: 例如 App Config，Notification Center 这种全局通用的
	|	|	|—— SDKWrapper: 为了避免 AppDelegate.m 过于庞大，可以把一些 SDK 逻辑封装下单独出一个类
	|	|	|—— Network: 网络逻辑
	|	|	|—— Storage: 数据持久化
	|	|	|—— Cache: 缓存
	|	|	|—— 其它根据工程自行拓展
	|	|—— Views: 视图类
	|	|	|—— Common: 所有全局共用的 UI 组件
	|	|	|—— TableView:
	|	|	|	|—— Headers: UITableView 的 Headers
	|	|	|	|—— Cells: UITableViewCell 子类
	|	|	|	|—— Footers: UITableView 的 Footers
	|	|	|—— CollectionView:
	|	|	|	|—— ReusableViews: UICollectionReusableView 子类
	|	|	|	|—— Cells: UICollectionViewCell 子类
	|	|	|—— Storyboards: 存放一个或多个 storyboard 文件
	|	|	|—— Others: 针对特定场景定制的 UI 组件，根据功能划分模块，例如 Login, Home, My
	|	|—— Controllers: 视图控制器类
	|	|	|—— Base: 各种 ViewController 的根类，例如 DMPBaseViewController, DMPBaseTableViewController
	|	|	|—— Entrance: 存放各种 App 启动时的入口页面控制器，例如配置入口的 DMPControllersManager， 闪屏 DMPSplashController, 引导页 DMPIntroduceController, 正常入口 DMPRootTabBarController 等
	|	|	|—— 根据功能划分模块，例如 Login, Home, My
	|	|—— AppDelegate.h/m
	|	|—— Supporting Files
	|	|	|—— Info.plist, main.m, pch 等
	|—— DemoProjectUnitTests: 单元测试对应的目录
	|—— Scripts: 在 Archive 时自动保存 dSYM 文件的脚本，读取 dSYM 和 Crash 的脚本等，不用添加到 Xcode 工程中
	|	|—— dSYM: 存放每次 Archive 生成的 dSYM

第二种是先按功能模块划分，再按代码逻辑划分：

假设有 Entrance, Home, Games, My 几个功能模块，分别表示程序入口，主页，游戏页面，个人主页。

	|—— DemoProject
	|	|—— Vendor: 不适合通过 CocoaPods 引入的第三方类库，例如需要经常改动的或者自己定制的
	|	|—— Resources: 存放各种资源，例如语言国际化文件组成的 bundle 文件，Images.xcassets 等
	|	|—— Base: 基础模块，为具体功能模块做支撑
	|	|	|—— Common: 存放全局通用的头文件，例如 DMPConstants.h, DMPAppKeys.h, DMPMacros.h
	|	|	|—— Models: 数据模型类
	|	|	|—— Views: 全局通用的视图类，自定的 UI 组件祖先类放在这里
	|	|	|—— Controllers: 各种 ViewController 的根类，例如 DMPBaseViewController, DMPBaseTableViewController
	|	|	|—— Helpers: 便于迁移到其它工程的工具类
	|	|	|—— Categories: 各种 Category
	|	|	|—— Logic: 负责各种基础逻辑的类
	|	|	|	|—— Global: 例如 App Config，Notification Center 这种全局通用的
	|	|	|	|—— SDKWrapper: 为了避免 AppDelegate.m 过于庞大，可以把一些 SDK 逻辑封装下单独出一个类
	|	|	|	|—— Network: 网络逻辑
	|	|	|	|—— Storage: 数据持久化
	|	|	|	|—— Cache: 缓存
	|	|	|	|—— 其它根据工程自行拓展
	|	|—— Modules: 各种功能模块
	|	|	|—— Entrance: App 入口模块
	|	|	|	|—— Interfaces: 本模块公用的头文件，例如一些公用的常数、宏、Protocol、enum 定义等
	|	|	|	|—— Models: 本模块用到的数据模型类
	|	|	|	|—— Views: 本模块涉及的页面类
	|	|	|	|—— Controllers: 本模块涉及的视图控制器类
	|	|	|	|—— Helpers: 本模块涉及的业务逻辑类，例如负责布局的 LayoutUtil，负责动画的 AnimationUtil
	|	|	|—— Home: 主页模块
	|	|	|	|—— ... 
	|	|	|—— Games: 游戏模块
	|	|	|	|—— ...
	|	|	|—— My: 个人主页模块
	|	|	|	|—— ...
	|	|—— AppDelegate.h/m
	|	|—— Supporting Files
	|	|	|—— Info.plist, main.m, pch 等
	|—— DemoProjectUnitTests: 单元测试对应的目录
	|—— Scripts: 在 Archive 时自动保存 dSYM 文件的脚本，读取 dSYM 和 Crash 的脚本等，不用添加到 Xcode 工程中
	|	|—— dSYM: 存放每次 Archive 生成的 dSYM

两种各有优缺点，可以自行根据喜好选择合适的结构。

在 Build Settings 中设置 Enable Modules 和 Link Frameworks Automatically 为 YES，避免手动引入各种系统 frameworks.

### 图片资源管理

App 尽量使用 Images.xcassets 进行管理，必须包含 @2x 和 @3x 文件，较大的图片或背景图片可以使用 JPEG 格式代替。

图片文件命名采用 `prefix_module_identifier_state` 规则。

`prefix` 表示图片类型的前缀，举例：

* icon
* btn
* bg
* line
* logo
* pic
* img

`module` 表示所属的场景模块，例如：common, home, my 等。

`identifier` 表示图片的标识。

`state` 表示素材的状态，例如按钮处于正常状态还是选中状态。

举例：icon_common_setting, btn_home_play_selected.

## 依赖管理

App 统一使用 CocoaPods 进行第三方依赖管理， SDK 尽量避免引入第三方类库。

Podfile 示例：

```
platform :ios, '7.0' # 指定 App 最低版本

# Target for App
target "H5GameCenter" do
    
    pod 'AFNetworking', '~> 2.6.0' # 需要指定版本号

    inhibit_all_warnings! # 禁止所有 warnings
    
end

# Target for Unit Tests
target "HGCUnitTests" do

    pod 'OHHTTPStubs', '~> 4.3.0'
    
    inhibit_all_warnings!
    
end
```

小提示：如果每次都用 `pod install` 命令安装，会非常慢，因为 CocoaPods 会检测类库是否需要更新，可以使用 `pod install --no-repo-update` 绕过检测更新进行安装。

## 代码管理

1.分支管理统一用 git flow

2.Objective-C 工程 .gitignore 规范

```
# Xcode
#
# gitignore contributors: remember to update Global/Xcode.gitignore, Objective-C.gitignore & Swift.gitignore

## Build generated
build/
DerivedData/

## Various settings
*.pbxuser
!default.pbxuser
*.mode1v3
!default.mode1v3
*.mode2v3
!default.mode2v3
*.perspectivev3
!default.perspectivev3
xcuserdata/

## Other
*.moved-aside
*.xccheckout
*.xcscmblueprint

## Obj-C/Swift specific
*.hmap
*.ipa

# CocoaPods
#
# We recommend against adding the Pods directory to your .gitignore. However
# you should judge for yourself, the pros and cons are mentioned at:
# https://guides.cocoapods.org/using/using-cocoapods.html#should-i-check-the-pods-directory-into-source-control
#
# Pods/

# Carthage
#
# Add this line if you want to avoid checking in source code from Carthage dependencies.
# Carthage/Checkouts

Carthage/Build

# fastlane
#
# It is recommended to not store the screenshots in the git repo. Instead, use fastlane to re-generate the 
# screenshots whenever they are needed.
# For more information about the recommended setup visit:
# https://github.com/fastlane/fastlane/blob/master/docs/Gitignore.md

fastlane/report.xml
fastlane/screenshots
```

3.一个产品的代码应该集中放在一个分组里，不能放在个人项目下。

4.commit message 不能太随意

## 测试

对关键的逻辑必须要有单元测试。

## Code Review

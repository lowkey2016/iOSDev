Pokemon Go 破解笔记

# 破解GPS锁区

## 总体的流程

第一步，前往 [rpplusplus/PokemonHook](https://github.com/rpplusplus/PokemonHook) clone项目。原理很简单，对系统的 coordinate 这个方法做 method swizzling ，然后自己修改坐标到澳大利亚的位置。

```
#import <Foundation/Foundation.h>
#import <CoreLocation/CoreLocation.h>
#import <objc/runtime.h>

@interface CLLocation(Swizzle)

@end

@implementation CLLocation(Swizzle)

static float x = -1;
static float y = -1;

+ (void) load {
	
	// 1. 方法交换

    Method m1 = class_getInstanceMethod(self, @selector(coordinate));
    Method m2 = class_getInstanceMethod(self, @selector(coordinate_));
    
    method_exchangeImplementations(m1, m2);
    
    // 2. 读取 UserDefaults，为全局变量 x, y 赋值
    
    if ([[NSUserDefaults standardUserDefaults] valueForKey:@"_fake_x"]) {
        x = [[[NSUserDefaults standardUserDefaults] valueForKey:@"_fake_x"] floatValue];
    };
    
    if ([[NSUserDefaults standardUserDefaults] valueForKey:@"_fake_y"]) {
        y = [[[NSUserDefaults standardUserDefaults] valueForKey:@"_fake_y"] floatValue];
    };
}

- (CLLocationCoordinate2D) coordinate_ {
    
    CLLocationCoordinate2D pos = [self coordinate_];
    
    // 算与联合广场的坐标偏移量
    if (x == -1 && y == -1) { // 第一次启动的情况
        x = pos.latitude - 37.7883923;
        y = pos.longitude - (-122.4076413);
        
	    // 比如广州 pos = (23, 113)
	    // x = 23 - 37.7xxx
	    // y = 113 - (-122.4xxx)
        
        [[NSUserDefaults standardUserDefaults] setValue:@(x) forKey:@"_fake_x"];
        [[NSUserDefaults standardUserDefaults] setValue:@(y) forKey:@"_fake_y"];
        [[NSUserDefaults standardUserDefaults] synchronize];
    }
    
    // 联合广场的位置是: 东经122.4xxx, 南纬 37.7xxx
    // 最后返回的都是 (x的偏移值 + 37.7xxx, y的偏移值 + (-122.4xxx))
    return CLLocationCoordinate2DMake(pos.latitude-x, pos.longitude-y);
}

@end
```

第二步，配置证书，编译产生重签名的动态库。

![](./dylib-codesign.png)

第三步，把重签名的动态库打进 ipa. Xcode 脚本如下：

```
/opt/iOSOpenDev/bin/iosod --xcbp

SRC_DYLIB_NAME="LocationFaker.dylib"
DES_DYLIB_NAME="lib${SRC_DYLIB_NAME}"

APP_NAME="pokemongo"
PAYLOAD_NAME="${APP_NAME}.app"

// 复制生成的动态库文件
cp "${BUILT_PRODUCTS_DIR}/${SRC_DYLIB_NAME}" ~/Desktop/PokemonHook/Payload/${PAYLOAD_NAME}/${DES_DYLIB_NAME}

// 打包成ipa
cd ~/Desktop/PokemonHook/

zip -r "${APP_NAME}.zip" Payload
mv "${APP_NAME}.zip" "${APP_NAME}.ipa"
```

第四步，对 ipa 进行重签名。我使用了 iResign 做重签名，注意要使用和重签名动态库时相同的 provision profile 文件。

第五步，如果是 dev 的包就用同步推助手直接安装，包括非越狱机器。如果是 In House 的包就发上内测网站发布。

## 遇到的坑

我在重签名ipa的时候，有两个证书选择，第一个是 HA Youmi Inc 的 dev 证书，还有一个是 HA Youmi INC 的 In House 证书。由于两个证书的名字差别只在于大小写，所以在签名动态库的时候，Xcode无法识别用哪个证书来签名，从而编译不过。解决方法是把另一个证书先从 keychain 导出来备份，然后删除。从而只有一个证书。

有些 provision profile 会重复下载几个，在重签名的时候为了避免用错 profile，注意先删除多余的，确保只留有一个。文件的定位方法是，commond + , 打开账户设置，然后选择团队和看到证书列表。如下图所示：

![](./show-profiles-1.png)
![](./show-profiles-2.png)

# Chrome控制模拟定位

[huacnlee/PokemonGoMove](https://github.com/huacnlee/PokemonGoMove)

# iOS控制模拟定位

## 准备

先把**《破解GPS锁区》**的地址偏移逻辑去掉。

开头要注意三个概念：

1. 控制器（类似于手柄，这里假设是 i5）
2. 信号中转站（Macbook 中的 Xcode）
3. 游戏（装有 Pokemon Go 的设备，这里假设是 i6）

## 总体流程

第一步，前往 [kahopoon/Pokemon-Go-Controller](https://github.com/kahopoon/Pokemon-Go-Controller) 下载工程

第二步，修改 readAnChangeXML.py 中的 IP 地址为 i5， gpx 文件的生成地址为 Macbook 的文件路径。并启动该文件。

```
import xml.etree.cElementTree as ET
import urllib2
import json

lastLat = ""
lastLng = ""

# 从 i5 的 Web Server 读取 i5 当前的 GPS 地址
def getPokemonLocation():
	try:
		response = urllib2.urlopen("http://192.168.1.108/（这里修改为 i5 的 IP 地址）", timeout = 1)
		return json.load(response)
	except urllib2.URLError as e:
		print e.reason

def generateXML():
	global lastLat, lastLng
	geo = getPokemonLocation()
	if geo != None:
		if geo["lat"] != lastLat or geo["lng"] != lastLng:
			lastLat = geo["lat"]
			lastLng = geo["lng"]
			gpx = ET.Element("gpx", version="1.1", creator="Xcode")
			wpt = ET.SubElement(gpx, "wpt", lat=geo["lat"], lon=geo["lng"])
			ET.SubElement(wpt, "name").text = "PokemonLocation"
			ET.ElementTree(gpx).write("pokemonLocation.gpx（这里修改为 Macbook 中 gpx 文件的生成地址）")
			print "Location Updated!", "latitude:", geo["lat"], "longitude:" ,geo["lng"]

def start():
	# 不断轮询 i5 的 Web Server
	while True:
		generateXML()

start()
```

**readAnChangeXML.py** 文件做的事就是不断向 i5 本地的 Web Server 发送 GET 请求，解析返回的数据得到 i5 当前的 GPS 地址，并写到 Macbook 本地的 gpx XML 文件中，从而获取到 i5 最新的 GPS 地址。

第三步，运行 **Pokemon-Go-Controller 工程**到 i5. 这个工程的核心代码是：

```
override func viewDidLoad() {
    super.viewDidLoad()
    
    if getSavedLocation() { showMapOnLocation() }
    
    startWebServer()
}
    
func startWebServer() {
	// 在本地开了一个 Web Server, 专门处理来自 Macbook 的 GET 请求，返回的数据是当前的 GPS 地址
    webServer.addDefaultHandlerForMethod("GET", requestClass: GCDWebServerRequest.self, processBlock: {request in
        return GCDWebServerDataResponse.init(JSONObject: self.getCurrentLocationDict())
    })
    webServer.startWithPort(80, bonjourName: "pokemonController")
}

func getCurrentLocationDict() -> [String:String] {
    return ["lat":"\(currentLocation.latitude)", "lng":"\(currentLocation.longitude)"]
}
```

最终效果是，在 i5 上点击上下左右的按钮，从而在 Macbook 中生成对应的 gpx 文件，假设为 **pokemonLocation.gpx**，该文件记录了 i5 最新的 GPS 地址。如果该步骤成功，终端会打出相应的 log.

第四步，用 Xcode 创建空白的工程 **Blank**，引用第3步生成的 **pokemonLocation.gpx** 文件，注意是引用而不是添加，因为后续这个文件的内容会不断更新。然后把 Blank 程序安装到 i6 中。

第五步，创建 **autoclick.py** 和 **sim_loc.scpt** 文件。代码如下：

**autoclick.py**

```
import os
import urllib2
import json
import time

def clickAction():
	cmd = "osascript ./sim_loc.scpt"
	os.system(cmd)
	time.sleep(1)
	print "clicking!!"

def start():
	while True:
		clickAction()

start()
```

**sim_loc.scpt**

```
delay 0.01activate application "Xcode"tell application "System Events"	tell process "Xcode"		click menu item "pokemonLocation" of menu 1 of menu item "Simulate Location" of menu 1 of menu bar item "Debug" of menu bar 1	end tellend tell
```

其中 **sim_loc.scpt** 用于模拟点击 Xcode 顶部菜单中的 `Debug - Simulate Location - pokemonLocation`，而 **autoclick.py** 文件负责不断循环调用 **sim_loc.scpt** 文件。

第六步，确保 **Blank 工程**一直运行在 i6 中并保持在后台，需要一直连着电脑。

第七步，在 Macbook 中启动 **autoclick.py**，启动 i6 中的 Pokemon Go 游戏。

第八步，在 i5 中点击上下左右导致的坐标变换，将直接影响到 Pokemon Go 游戏中 GPS 位置的变更。完成。

## 原理

![](./controller.png)

核心是利用 Xcode 调试时的 Simulate Location 功能来模拟设备的全局地理位置，从而影响到 Pokemon Go 游戏。

i5 的 Pokemon-Go-Controller 程序在点击上下左右时会更新 UserDefaults 中的位置，该程序在本地开了一个 Web Server 。

Macbook 的 readAnChangeXML.py 会不断轮询发请求给 i5 的 Web Server，此时 i5 会把更新的地理位置发给 Macbook。Macbook 在收到信号后，把更新的地理位置写到本地的 pokemonLocation.gpx 文件中，并通过 autoclick.py 定时调用 Xcode 的模拟定位功能，将 GPS 地址传递给 i6 的 Blank 程序来更新全局的地理位置，从而影响到 i6 中 Pokemon Go 游戏中人物的位置移动。

# 参考资料

[粉丝福利，Pokemon Go 锁区破解](https://mp.weixin.qq.com/s?__biz=MzIwMTYzMzcwOQ==&mid=2650948432&idx=1&sn=125742722bbbce53774199a587688088&scene=1&srcid=0710GvowrtsnfF7Q5bNUCnZW&from=singlemessage&isappinstalled=0&uin=MTYwNDUxOTkyMg%3D%3D&key=77421cf58af4a653142704946199941d97d718a68258b0b9e66e467dcb43ce8d19eaa7be84cc216c58f3a09e988cb144&devicetype=iMac+MacBookPro11%2C2+OSX+OSX+10.11.2+build(15C50)&version=11020201&lang=zh_CN&pass_ticket=LYtMDFDzEsG9WJcs26ppR61aKettmZ3%2FUI6fBh9cXiTnlpzBM9baxsF1FWE8lkxG)
[自己动手实现 Pokemon Go 锁区破解 —— 记一次重签名](http://kittenyang.com/pokemongocrack/)

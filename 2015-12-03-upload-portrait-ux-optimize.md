# FFSS开发笔记（1）优化用户更新头像的体验

## 写在前面的废话

昨天和同事吃饭，一个同事在玩我们的 App FFSS 的时候，吐槽上传用户头像太慢了，而我之前设定的交互是：上传头像的时候，界面会被 HUD 卡死，如果网速慢图片大，会卡得死死的。然后项目老大吐槽：你没压缩过图片吗。。我就裁剪了一下，不过依然是 640 * 640 分辨率的 PNG 文件，一张正常的图片大概有500K，再 Base64 一下，660多K吧，确实挺大的了。然后昨天搜了一下图片压缩相关的东西，其实压成 JPEG，0.7左右的品质都是非常清晰的，不过体验了一下微信/支付宝的上传头像功能，都是“秒传”不阻塞的，而且在网络较差的情况下也能保证头像会更新到服务器，于是我怒了，决定也写一个类似的交互。

## 需求分析

* 没网络的情况下不要上传，提示用户网络中断
* session失效的情况下，要引导用户重新登录
* 即使网络情况较差，也要"秒传"，不用用户等待
* 更新头像后，所有需要显示用户头像的界面都要更新
* 如果上传图片失败了，不要提示用户重传，而是 App 自己选择在网络好的情况下自动重传
* 如果 App 本次生命周期没有上传成功，重启 App 后，头像显示的依然是新的头像，并且在用户不知道的情况下重传
* 如果用户重复上传头像，那么覆盖旧的，无论成功与否

## "秒传"思路

### 用户上传图片的大致流程是：

* 从相机或相册中获取到要上传的图片文件 Portrait Image
* 把 Portrait Image 作为参数发起网络请求更新到服务端
* 如果成功服务端将回调用户头像地址

我的想法是，写一个类叫 UserInfoManager

### 上传头像的流程如下：

* 用户从相机或相册中获取到要上传的图片文件 Portrait Image
* 如果当前网络断开就直接提示用户错误信息，否则下一步
* 如果当前 session 已经失效，就引导用户重新登录，否则下一步
* UserInfoManager 把 Portrait Image 保存到磁盘（保存的是JPEG），并另外保存一张 resize to 150 * 150 的缩略图到磁盘，保存成功后回调 succ 并展示成功的UI，HUD必须停下来，不要阻塞用户的下一步操作
* UserInfoManager 开一个后台线程来上传缓存的 Portrait Image，如果上传成功，就以服务端回调的 portrait url 为 key 并使用 SDWebImage 来缓存当前的 Portrait Image，再把磁盘的图片文件删掉并把服务端返回的JSON同步到本地的数据库（例如UserModel），如果上传失败就判断失败的原因，如果是服务端拒绝或者奇葩错误就不要重传了，并把磁盘的文件清掉，如果是网络较差（例如AFNetworking的fail callback）就开个 NSTimer 在2分钟后重传
* 重传的时候如果网络不可用，就再等2分钟之后再重传

### UI和其它情况考虑：

* 对于用户登录、注销、session失效（多终端互踢）的情况，需要把磁盘的图片清掉，放弃重传
* "秒传"之后，在图片上传到服务器之前，使用的都是磁盘的本地文件，所以所有需要显示用户头像的UI都需要先判断 Disk Image 是否存在，如果存在就用 Disk Image（为了避免IO，UserInfoManager应该在 App 启动后就读磁盘图片到内存，并用一个指针指向该图片对象），不存在再用 SDWebImage 来 load portrait url
* 如果用户在图片上传成功之前立即又上传新的头像，就应该用新的图片数据覆写现有的图片文件，并取消之前的网络请求（所以网络请求必须是可取消的），关闭之前的定时器等等，释放上一次的资源，再进入"秒传"的逻辑

### App启动后要怎么处理

* 同步读 Portrait Image 缩略图
* 异步读 Portrait Image 原图，避免磁盘 IO 阻塞 App 启动
* 监听用户登录、注销、session失效的消息
* 如果发现 Portrait Image 原图存在，就启动重传图片的逻辑
* 对于使用到用户头像的 UI，先判断 Portrait Image 原图是否存在，如果不存在（还没完全从磁盘读取到数据），再判断 Portrait Image 缩略图是否存在，如果不存在再用 SDWebImage load portrait url

因此，缩略图的作用是避免 App 启动时被阻塞，以及对于还没上传成功的用户头像，可以让用户看到“正确的”假数据。

为了避免读写图片文件数据不一致，读写图片文件还要加上递归锁。

## 源码

**HGCUserInfoManager.h**

```
#import <Foundation/Foundation.h>

#define mHGCUserInfoManager [HGCUserInfoManager sharedInstance]

@class HGCSessionModel;
@class HGCUserModel;

@interface HGCUserInfoManager : NSObject

+ (instancetype)sharedInstance;

/* Get */
- (HGCSessionModel *)getCurrentSession;
- (HGCUserModel *)getCurrentUser;

/* Insert or Update */
- (void)addCurrentSession:(HGCSessionModel *)session;
- (void)addCurrentUser:(HGCUserModel *)user;

/* Delete */
- (void)deleteCurrentSession;
- (void)deleteCurrentUser;

/* User Portrait */
- (NSString *)fullPortraitURLStringFrom:(NSString *)srcURLString;
- (UIImage *)srcOrCompressUploadingPortraitImage;
- (void)updateUserPortrait:(UIImage *)portraitImage handler:(HGCSuccFailCallback)handler;

@end
```

**HGCUserInfoManager.m**
```
#import "HGCUserInfoManager.h"
#import "HGCUserModel.h"
#import "JTTFileManager.h"
#import <NYXImagesKit/NYXImagesKit.h>
#import <SDWebImage/SDWebImageManager.h>
#import "HGCGlobalFunctions.h"

#import "HGCNetworkOperationManager.h"
#import "HGCGameStorageManager.h"
#import "HGCGameStorageManager+HGCUserSession.h"
#import "HGCLoginManager.h"


///////////////////////////////////////////////////////////////////////////////////////////


static NSString * const kHGCUserInfoFolderName = @"HGCUserInfo";

@interface HGCUserInfoManager ()

@property (nonatomic, assign) BOOL userSessionDidFail;
@property (nonatomic, strong) NSRecursiveLock *lock;

@property (nonatomic, strong) NSTimer *reuploadPortraitTimer;
@property (nonatomic, readwrite, strong) UIImage *compressUploadingPortraitImage;
@property (nonatomic, readwrite, strong) UIImage *uploadingPortraitImage;
@property (nonatomic, strong) HGCNetworkOperation *uploadingOperation;

@end

@implementation HGCUserInfoManager


///////////////////////////////////////////////////////////////////////////////////////////


#pragma mark - Singleton

+ (instancetype)sharedInstance {
    static id _sharedInstance = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        _sharedInstance = [[self alloc] init];
    });
    
    return _sharedInstance;
}

- (instancetype)init {
    self = [super init];
    if (self) {
        [self setup];
    }
    return self;
}

- (void)setup {
    _userSessionDidFail = NO;
    
    _lock = [[NSRecursiveLock alloc] init];
    _lock.name = @"HGCUserInfoManagerLock";
    
    // 经过压缩的小图片，可以同步读取
    [_lock lock];
    NSData *compressImgData = [[NSData alloc] initWithContentsOfFile:[self _hgc_compressImageFilePath]];
    _compressUploadingPortraitImage = [UIImage imageWithData:compressImgData];
    [_lock unlock];
    
    // 初始的大图片，异步读取
    dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
        [_lock lock];
        NSData *srcImgData = [[NSData alloc] initWithContentsOfFile:[self _hgc_srcImageFilePath]];
        _uploadingPortraitImage = [UIImage imageWithData:srcImgData];
        if (_uploadingPortraitImage) {
            // 重传图片
            DDLogWarn(@"Will resend user portrait");
            [self _hgc_uploadPortraitImageInBackground];
        }
        [_lock unlock];
    });
    
    // 用户重新登录、注销、session失效都要释放之前的资源
    [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(handleUserDidLoginNotification:) name:HGCUserDidLoginNotification object:nil];
    [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(handleUserDidLogoutNotification:) name:HGCUserDidLogoutNotification object:nil];
    [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(handleUserSessionDidFailNotification:) name:HGCUserSessionDidFailNotification object:nil];
}

- (void)dealloc {
    if (_reuploadPortraitTimer && [_reuploadPortraitTimer isValid]) {
        [_reuploadPortraitTimer invalidate];
    }
    _reuploadPortraitTimer = nil;
    _compressUploadingPortraitImage = nil;
    _uploadingPortraitImage = nil;
    _uploadingOperation = nil;
}


///////////////////////////////////////////////////////////////////////////////////////////


#pragma mark - Current User and Session

/* Get */

- (HGCSessionModel *)getCurrentSession {
    return [mHGCGameStorageManager getCurrentSession];
}

- (HGCUserModel *)getCurrentUser {
    return [mHGCGameStorageManager getCurrentUser];
}

/* Insert or Update */

- (void)addCurrentSession:(HGCSessionModel *)session {
    [mHGCGameStorageManager addCurrentSession:session];
}

- (void)addCurrentUser:(HGCUserModel *)user {
    [mHGCGameStorageManager addCurrentUser:user];
}

/* Delete */

- (void)deleteCurrentSession {
    [mHGCGameStorageManager deleteCurrentSession];
}

- (void)deleteCurrentUser {
    [mHGCGameStorageManager deleteCurrentUser];
}


///////////////////////////////////////////////////////////////////////////////////////////


#pragma mark - File Path

- (NSString *)_hgc_userInfoFolderPath {
    NSString *userinfoFolderPath = [[mJTTFileManager documentsPath] stringByAppendingPathComponent:kHGCUserInfoFolderName];
    [mJTTFileManager createFolderIfNotExists:userinfoFolderPath];
    
    return userinfoFolderPath;
}

- (NSString *)_hgc_compressImageFilePath {
    return [[self _hgc_userInfoFolderPath] stringByAppendingPathComponent:@"compr_portrait"];
}

- (NSString *)_hgc_srcImageFilePath {
    return [[self _hgc_userInfoFolderPath] stringByAppendingPathComponent:@"src_portrait"];
}

#pragma mark - Upload

- (void)_hgc_uploadPortraitImageInBackground {
    // 先取消之前的上传请求
    [self _hgc_cancelPreviousOperation];
    // 关闭定时器
    [self _hgc_invalidateReuploadTimer];
    
    // 如果网络连接中断，2分钟后重传
    if ([mHGCNetworkOperationManager isNetworkRechable] == NO) {
        [self _hgc_fireReuploadPortraitImageTimer];
        
        return;
    }
    
    // 后台上传
    __weak typeof(self) weakself = self;
    self.uploadingOperation = [HGCNetworkOperation new];
    _uploadingOperation.shouldHandleSessionFail = NO;
    [_uploadingOperation setCurrentUserInfoWithNickname:nil portraitImage:_uploadingPortraitImage portraitQuality:1.0 handler:^(BOOL succ, id responseObject, NSString *errorDesc) {
        
        __strong typeof(weakself) strongself = weakself;
        if (strongself == nil) {
            return;
        }
        
        if (succ == NO) {
            [strongself _hgc_uploadPortraitImageDidFail:errorDesc];
        }
        else {
            if (responseObject && [responseObject isEqual:[NSNull null]] == NO) {
                NSString *portrait = responseObject[@"userImg"];
                if (portrait && [portrait hgc_isNotEmpty]) {
                    // 上传成功
                    [strongself _hgc_uploadPortraitImageDidSucc:portrait];
                }
                else {
                    // 服务端返回非法，需要重传
                    [strongself _hgc_fireReuploadPortraitImageTimer];
                }
            }
            else {
                // 服务端返回非法，需要重传
                [strongself _hgc_fireReuploadPortraitImageTimer];
            }
        }
    }];
    [mHGCNetworkOperationManager addOperation:_uploadingOperation];
}

- (void)_hgc_fireReuploadPortraitImageTimer {
    // 先停掉之前的重传定时器
    [self _hgc_invalidateReuploadTimer];
    
    // 2分钟后重传，不重复
    DDLogWarn(@"Reupload Portrait Image Timer Fire");
    self.reuploadPortraitTimer = [NSTimer timerWithTimeInterval:120 target:self selector:@selector(_hgc_uploadPortraitImageInBackground) userInfo:nil repeats:NO];
    [[NSRunLoop mainRunLoop] addTimer:_reuploadPortraitTimer forMode:NSRunLoopCommonModes];
}

- (void)_hgc_uploadPortraitImageDidSucc:(NSString *)portrait {
    DDLogInfo(@"Upload Portrait Image Succ");
    
    // 还原网络请求
    self.uploadingOperation = nil;
    self.userSessionDidFail = NO;
    
    // 关闭定时器
    [self _hgc_invalidateReuploadTimer];
    
    // 在删除磁盘图片之前，按需手动设置缓存
    UIImage *tmpPortrait = _uploadingPortraitImage;
    NSString *fullPortraitURLString = [self fullPortraitURLStringFrom:portrait];
    [[[SDWebImageManager sharedManager] imageCache] storeImage:tmpPortrait forKey:fullPortraitURLString toDisk:YES];
    
    // 删除磁盘的图片
    [self _hgc_removePortraitImagesInDisk];
    
    // 更新当前登录的用户Model
    HGCUserModel *curUserModel = [self getCurrentUser];
    curUserModel.portraitURLString = portrait;
    [self addCurrentUser:curUserModel];
    [[NSNotificationCenter defaultCenter] postNotificationName:HGCUserProfileDidUpdateNotification object:nil];
}

- (void)_hgc_uploadPortraitImageDidFail:(NSString *)errorDesc {
    DDLogError(@"Upload Portrait Image Fail: %@", errorDesc);
    
    // 还原网络请求
    self.uploadingOperation = nil;
    
    if ([errorDesc isEqualToString:HGCLocalizedString(@"kHGCLocalize_error_network_badnetwork")]) {
        // 网络不好，需要重传
        [self _hgc_fireReuploadPortraitImageTimer];
    }
    else {
        // 其它网络错误，包括 session fail ，放弃上传图片
        
        if ([errorDesc isEqualToString:HGCLocalizedString(@"kHGCLocalize_error_network_sessionVerifyFail")]) {
            self.userSessionDidFail = YES;
        }
        
        // 关闭定时器
        [self _hgc_invalidateReuploadTimer];
        // 删除磁盘的图片
        [self _hgc_removePortraitImagesInDisk];
    }
}

#pragma mark - Clear

/**
 *  用户重新登录，注销登录，session失效，都要调用下列方法
 */

- (void)_hgc_cancelPreviousOperation {
    // 取消或还原网络请求
    if (_uploadingOperation) {
        [mHGCNetworkOperationManager cancelOperation:_uploadingOperation];
        self.uploadingOperation = nil;
    }
}

- (void)_hgc_invalidateReuploadTimer {
    // 关闭定时器
    if (_reuploadPortraitTimer && [_reuploadPortraitTimer isValid]) {
        [_reuploadPortraitTimer invalidate];
    }
    self.reuploadPortraitTimer = nil;
}

- (void)_hgc_removePortraitImagesInDisk {
    // 删除磁盘的图片
    [_lock lock];
    [mJTTFileManager removeItemAtPath:[self _hgc_srcImageFilePath]];
    [mJTTFileManager removeItemAtPath:[self _hgc_compressImageFilePath]];
    self.uploadingPortraitImage = nil;
    self.compressUploadingPortraitImage = nil;
    [_lock unlock];
}


///////////////////////////////////////////////////////////////////////////////////////////


#pragma mark - Public Methods

- (NSString *)fullPortraitURLStringFrom:(NSString *)portraitURLString {
    NSRange range = [portraitURLString rangeOfString:@"!" options:NSBackwardsSearch];
    NSString *fullPortraitURLString = portraitURLString;
    if (range.location != NSNotFound) {
        fullPortraitURLString = [portraitURLString substringToIndex:range.location];
    }
    
    return fullPortraitURLString;
}

- (UIImage *)srcOrCompressUploadingPortraitImage {
    return _uploadingPortraitImage ? _uploadingPortraitImage : (_compressUploadingPortraitImage ? _compressUploadingPortraitImage : nil);
}

/**
 *  提供给上传用户头像的 Controller 调用的接口
 */
- (void)updateUserPortrait:(UIImage *)portraitImage handler:(HGCSuccFailCallback)handler {
    if ([mHGCNetworkOperationManager isNetworkRechable] == NO) {
        // 网络中断，直接提示用户
        !handler ?: handler(NO, nil, HGCLocalizedString(@"kHGCLocalize_error_network_disconnected"));
    }
    else if (_userSessionDidFail) {
        // session 失效，提示用户重新登录
        [mHGCLoginManager handleSessionDisconnected];
        !handler ?: handler(NO, nil, HGCLocalizedString(@"kHGCLocalize_error_network_sessionVerifyFail"));
    }
    else {
        /** "秒传" */
        
        // 先保存原图和缩略图到磁盘
        [_lock lock];
        self.uploadingPortraitImage = portraitImage;
        NSData *srcImageData = HGCFDataFromImage(_uploadingPortraitImage);
        BOOL writeSrcImgSucc = [srcImageData writeToFile:[self _hgc_srcImageFilePath] atomically:YES];
        if (writeSrcImgSucc == NO) {
            DDLogWarn(@"Save src portrait fail");
        }
        self.compressUploadingPortraitImage = [portraitImage scaleToFillSize:CGSizeMake(150, 150)];
        NSData *comprImageData = HGCFDataFromImage(_compressUploadingPortraitImage);
        BOOL writeComprImgSucc = [comprImageData writeToFile:[self _hgc_compressImageFilePath] atomically:YES];
        if (writeComprImgSucc == NO) {
            DDLogWarn(@"Save compr portrait fail");
        }
        [_lock unlock];
        
        // 在后台开线程上传原图
        [self _hgc_uploadPortraitImageInBackground];
        
        // 回调成功给用户
        !handler ?: handler(YES, nil, nil);
    }
}


///////////////////////////////////////////////////////////////////////////////////////////


#pragma mark - Notifications Handlers

- (void)handleUserDidLoginNotification:(NSNotification *)noti {
    [self _hgc_cancelPreviousOperation];
    [self _hgc_invalidateReuploadTimer];
    [self _hgc_removePortraitImagesInDisk];
    
    self.userSessionDidFail = NO;
}

- (void)handleUserDidLogoutNotification:(NSNotification *)noti {
    [self _hgc_cancelPreviousOperation];
    [self _hgc_invalidateReuploadTimer];
    [self _hgc_removePortraitImagesInDisk];
    
    self.userSessionDidFail = NO;
}

- (void)handleUserSessionDidFailNotification:(NSNotification *)noti {
    [self _hgc_cancelPreviousOperation];
    [self _hgc_invalidateReuploadTimer];
    [self _hgc_removePortraitImagesInDisk];
    
    self.userSessionDidFail = YES;
}

@end
```

还需要在 AppDelegate.m 的 App Launch 方法中调用

```
mHGCUserInfoManager;
```

## 小结

一个看似简单的功能，如果要保证各种情况下都有效，尤其是网络不好等情况，就会变得非常的复杂。

或许这就是学校的玩具项目和公司的生产环境的最大区别吧。

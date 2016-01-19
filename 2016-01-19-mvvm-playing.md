# 初尝 MVVM

这两天硬着头皮把 MVVM 架构套进了当前的项目，目前的项目还是非常的不 MVVM ，等我多学习几篇文章代码后再来改造吧，现在生搬硬套地改造只是乱来。下面写一下实践的一些小想法，当然很不标准，只是记录下想法而已。后续会有更多关于 MVVM 的文章。

* 什么是 MVVM ？

```
Model-View-ViewModel，该架构可以解决 Massive View Controller 的问题。在该架构中 Controller 的大部分业务逻辑被挪到了 ViewModel 中去，例如 Presentation Logic ，目前初步理解就是把 Model 转换为 View/ViewController 可以展示的数据的逻辑。
```

* 把 Model 传给 View ？

```
之前看了 objcio 的 light view controller ，就一直把 cell config 的工作写成：把 Model 传给 Cell ，然后 Cell 内部自行装配 Model 的数据，另外 Cell 自己还负责计算自己的高度，包括动态算高等。后来看了某篇架构比较的神文，才知道这样其实违反了 MVC 架构，因为 View 不应该知道 Model 的存在，所以这里犯了很严重的错误，当然算高逻辑也不应该放在 Cell 内部做，这样虽然为 Controller 瘦身了，但是 View 能够知道 Model 并不是什么好事，这个得改进。而 ViewModel 可以做到，它把 Model to Data 的数据做了，既瘦身了 Controller，也解耦了 View 和 Model.
```

* 数据绑定？

```
MVVM 中有一个非常重要的概念就是数据绑定，目前本人的肤浅理解就是 View 的某属性和 ViewModel 的某属性有一个绑定关系，当 View 的该属性变化时，ViewModel 的对应属性也跟着变化；当 ViewModel 的该属性变化时，View 的对应属性也会变化，形成了一种联动效果。

在 Cocoa Touch 中没有专门的数据绑定 API ，目前做得最好的就是 RAC ，但是这货我现在还玩不转，目前只能用一些简陋的手段，例如代理、KVO、setter/getter、通知。
```

* 大概工作流程

```
ViewModel 层直接操作 Model 层，承担了获取数据、解析数据、转换数据等职责。
View 层包括 View 和 ViewController ，View 会持有一个 ViewModel ，并和其绑定，ViewModel 会暴露一些 readonly 的 properties 出来给 View 去获取装配。但是 ViewModel 不应该知道 View 的存在，只能通过数据绑定把数据回调到 View. 
```

* 怎么看一个架构好不好？

```
直接抄网上看到的：职责分离程度、可测试性、可维护性。
```

这是目前的粗略理解，后续。

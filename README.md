# 概览

![Auto generate data and push](https://github.com/ecator/2019-ncov-statusbar/workflows/Auto%20generate%20data%20and%20push/badge.svg?branch=master&event=schedule)

生成2019武汉新型冠状病毒疫情状态图，数据来自于[canghailan/Wuhan-2019-nCoV](https://github.com/canghailan/Wuhan-2019-nCoV) :cat:

可以直接以图片的方式嵌入到网页中。

# 使用

## 环境

> 请使用Python3

初期克隆下来后需要初始化子模块：

```
git submodule update --init
```

可能需要安装`Pillow`：

```
pip3 install Pillow
```

## 市/区/县状态

可以用下面的命令生成`2020年2月9日 湖北省 武汉市`的状态图：

```
./gen.py --date '2020-2-9' --country CN --province 420000 --city 420100 --out out.png
```

效果如下：

![CN-420000-420000](https://raw.githubusercontent.com/ecator/2019-ncov-statusbar/gen-all/all/CN-420000-420100.png)

## 省状态

如果想查看`湖北省`整体数据的话可以用下面的命令：

```
./gen.py --province 420000 --city '' --out out.png
```

省略`-date`的话默认是系统日期，省略`--country`的话默认是`CN`，上面的效果如下：

![CN-420000](https://raw.githubusercontent.com/ecator/2019-ncov-statusbar/gen-all/all/CN-420000.png)

## 国家状态

如果输出国家整体状态的话可以用下面的命令：

```
./gen.py --province '' --city '' --out out.png
```

上面会输出`中国`的状态：

![CN](https://raw.githubusercontent.com/ecator/2019-ncov-statusbar/gen-all/all/CN.png)


输出`日本`的状态：

```
./gen.py --country JP --province '' --city '' --out out.png
```

![JP](https://raw.githubusercontent.com/ecator/2019-ncov-statusbar/gen-all/all/JP.png)


## 注意事项

生成脚本依赖[canghailan/Wuhan-2019-nCoV](https://github.com/canghailan/Wuhan-2019-nCoV)提供数据，所以最好每次都运行一次下面的命令来更新最新的数据：

```
git submodule update --remote Wuhan-2019-nCoV 
```

命令涉及到的国家代码可以参考[Wuhan-2019-nCoV/CountryCode.csv](https://github.com/canghailan/Wuhan-2019-nCoV/blob/master/CountryCode.csv)，中国地区代码可以参考[Wuhan-2019-nCoV/ChinaAreaCode.csv](https://github.com/canghailan/Wuhan-2019-nCoV/blob/master/ChinaAreaCode.csv)。

另外生成图片第一行括号中的时间是图片生成时间，并不是数据更新时间，请注意。

命令参数的具体帮助可以输入`./gen.py -h`查看。


# 自动生成

本仓库利用[Action](https://github.com/ecator/2019-ncov-statusbar/actions)在每个小时的第5分钟会自动生成全部图片，结果可以在[gen-all/all](https://github.com/ecator/2019-ncov-statusbar/tree/gen-all/all)直接引用，文件名以`国家代码-省代码-城市代码.png`方式命名。

# LICENCE

遵循MIT开源许可。

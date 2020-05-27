#!/bin/bash

# 在 all 目录中生成所有状态图片
# 生成之前清除旧文件

out=all
data=data

[ -e $out ] && rm -rf $out
[ -e $data ] && rm -rf $data

mkdir $out
mkdir $data

curl -fsSL -o data/ChinaAreaCode.csv  https://raw.githubusercontent.com/canghailan/Wuhan-2019-nCoV/master/ChinaAreaCode.csv
if [ $? -ne 0 ]
then
  echo get ChinaAreaCode.csv error >&2
  exit 1
fi

curl -fsSL -o data/CountryCode.csv  https://raw.githubusercontent.com/canghailan/Wuhan-2019-nCoV/master/CountryCode.csv
if [ $? -ne 0 ]
then
  echo get CountryCode.csv error >&2
  exit 1
fi

curl -fsSL -o data/Wuhan-2019-nCoV.csv  https://raw.githubusercontent.com/canghailan/Wuhan-2019-nCoV/master/Wuhan-2019-nCoV.csv
if [ $? -ne 0 ]
then
  echo get Wuhan-2019-nCoV.csv error >&2
  exit 1
fi

./gen.py --all true --out $out
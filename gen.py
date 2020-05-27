#!/usr/bin/env python3

from PIL import Image, ImageFont, ImageDraw
import csv
import argparse
import datetime
import time
import re
import os


CSV_CHAINA_AREA_CODE = "data/ChinaAreaCode.csv"
CSV_COUNTRY_CODE = "data/CountryCode.csv"
CSV_DATA = "data/Wuhan-2019-nCoV.csv"
FONT_YHEI = "fonts/yhei.ttf"
FONT_GO_MONO = "fonts/go-mono.ttf"


def drawImg(title, confirmed, confirmed_change, suspected, suspected_change, cured, cured_change, dead, dead_change, out_file=""):
    """
    生成图像
    """
    font_size = 20
    font_change_size = 10
    im_len = 9*font_size*4
    im = Image.new("RGB", (im_len, font_size*2), "white")
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(FONT_YHEI, font_size)
    font_title = ImageFont.truetype(FONT_YHEI, font_size//3*2)
    font_num = ImageFont.truetype(FONT_GO_MONO, font_size)
    font_change = ImageFont.truetype(FONT_GO_MONO, font_change_size)

    # 标题
    draw.text((1, 1), title, fill="black", font=font_title)

    next_x = 1

    # 详细部分
    for t, v, v_c, c in (("确诊：", confirmed, confirmed_change, "red"),
                         ("疑似：", suspected, suspected_change, "Coral"),
                         ("治愈：", cured, cured_change, "Aqua"),
                         ("死亡：", dead, dead_change, "DimGray")):
        draw.text((next_x, font_size*0.8), t, fill="black", font=font)
        next_x += len(t)*font_size
        draw.text((next_x, font_size*0.9), v, fill=c, font=font_num)
        draw.text((next_x+len(v)*font_size*4/7, font_size), v_c, fill=c, font=font_change)
        next_x += 6*font_size

    if out_file == "":
        im.show()
    else:
        im.save(out_file)


def getDataRows(file_name):
    """
    读取CSV文件返回字典列表
    """
    rows = []
    with open(file_name) as fo:
        reader = csv.DictReader(fo)
        for i in reader:
            rows.append(i)
    return rows


def getNameByCode(code, file_name):
    """
    根据代码返回名称
    """
    if code == "":
        return ""
    with open(file_name) as fo:
        reader = csv.DictReader(fo)
        for i in reader:
            if i["code"] == code:
                return i["name"]
    return ""


def findData(rows, date, countryCode, provinceCode="", cityCode=""):
    """
    精确查找对应数据
    """
    for r in rows:
        if r["date"] == date and r["countryCode"] == countryCode and r["provinceCode"] == provinceCode and r["cityCode"] == cityCode:
            return r["confirmed"], r["suspected"], r["cured"], r["dead"]
    return 0, 0, 0, 0


def getArgs():
    """
    解析参数
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.datetime.now().strftime("%Y-%m-%d"), help="date")
    parser.add_argument("--country", default="CN", help='country code eg. CN JP')
    parser.add_argument("--province", default="420000", help='province code eg. 420000[湖北省]')
    parser.add_argument("--city", default="420100", help='province code eg. 420100[武汉市]')
    parser.add_argument("--out", default="", help='output file eg. out.jpg')
    parser.add_argument("--all", default=False, type=bool,
                        help='output all status, --out must be a directory, and will ignore --country --province -city')
    args = parser.parse_args()
    return vars(args)


def genAll(today, yesterday, rows, out_dir):
    """
    生成所有状态
    """
    # 找到所有国家
    countrys = getDataRows(CSV_COUNTRY_CODE)
    # 找到所有省市
    cities = []
    with open(CSV_CHAINA_AREA_CODE) as fo:
        province_code = ""
        province_name = ""
        for r in csv.DictReader(fo):
            if r["code"].endswith("0000"):
                province_code = r["code"]
                province_name = r["name"]
                cities.append({"province_code": province_code,
                               "province_name": province_name,
                               "city_code": "",
                               "city_name": ""})
            else:
                cities.append({"province_code": province_code,
                               "province_name": province_name,
                               "city_code": r["code"],
                               "city_name": r["name"]})
    # 生成
    for country in countrys:
        # 生成国家数据
        today_data = findData(rows, today, country["code"])
        yesterday_data = findData(rows, yesterday, country["code"])
        changes = makeChanges(today_data, yesterday_data)
        title = makeTitle(today, country["name"])
        out_file = makeOutName(out_dir, country["code"])
        drawImg(title, *changes, out_file=out_file)
        # 生成中国省市数据
        if country["code"] == "CN":
            for city in cities:
                today_data = findData(rows, today, country["code"], city["province_code"], city["city_code"])
                yesterday_data = findData(rows, yesterday, country["code"], city["province_code"], city["city_code"])
                changes = makeChanges(today_data, yesterday_data)
                title = makeTitle(today, country["name"], city["province_name"], city["city_name"])
                out_file = makeOutName(out_dir, country["code"], city["province_code"], city["city_code"])
                drawImg(title, *changes, out_file=out_file)


def makeOutName(out_dir, country, province='', city=''):
    """
    生成 out_dir/country-province-city.png 形式的文件名
    """
    if province == '':
        file_name = os.path.join(out_dir, country+".png")
    elif city == '':
        file_name = os.path.join(out_dir, country+"-"+province+".png")
    else:
        file_name = os.path.join(out_dir, country+"-"+province+"-"+city+".png")
    return file_name


def makeChanges(today_data, yesterday_data):
    """
    取得变化值
    """
    changes = []
    for i in range(len(today_data)):
        change = int(today_data[i])-int(yesterday_data[i])
        if change >= 0:
            change = "+"+str(change)
        else:
            change = str(change)
        changes.append(str(today_data[i]))
        changes.append(str(change))
    return changes


def makeTitle(today, country, province="", city=""):
    """
    生成标题
    """
    title = "%s %s %s %s 疫情动态(%s)" % (today,
                                      country,
                                      province,
                                      city,
                                      time.strftime("%Y-%m-%d %X %z"))
    title = re.sub(" +", " ", title)
    return title


if __name__ == "__main__":
    args = getArgs()
    print(args)
    today = datetime.datetime.strptime(args["date"], "%Y-%m-%d")
    today = today.strftime("%Y-%m-%d")
    country = args["country"]
    province = args["province"]
    city = args["city"]
    out = args["out"]
    is_all = args["all"]
    yesterday = datetime.date(*(int(x) for x in today.split("-")))-datetime.timedelta(days=1)
    yesterday = yesterday.strftime("%Y-%m-%d")
    rows = getDataRows(CSV_DATA)
    if is_all:
        if out == "":
            raise SyntaxError("--out can't be empty when --all is true")
        elif os.path.isdir(out) == False:
            raise FileNotFoundError("--out must be a directory when --all is true")
        else:
            # 生成所有数据
            genAll(today, yesterday, rows, out)
            exit(0)

    # 生成指定状态
    today_data = findData(rows, today, country, province, city)
    print("today", today, today_data)
    yesterday_data = findData(rows, yesterday,  country, province, city)
    print("yesterday", yesterday, yesterday_data)
    changes = makeChanges(today_data, yesterday_data)
    print("changes", changes)
    title = makeTitle(today,
                      getNameByCode(country, CSV_COUNTRY_CODE),
                      getNameByCode(province, CSV_CHAINA_AREA_CODE),
                      getNameByCode(city, CSV_CHAINA_AREA_CODE))
    drawImg(title, *changes, out)

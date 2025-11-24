
import requests
import pandas as pd
import time
import json
from datetime import datetime

# 请确保你的API密钥有效
# 这是一个示例密钥，实际使用时请替换为你自己的
API_KEY = "726956faf3d2d738dc220db738bd44c4"
API_URL = "https://api.tanshuapi.com/api/traffic_restriction/v1/index"

# 测试城市列表
cities = [
    # 北京市（直辖市）
    "北京市",
    # 上海市（直辖市）
    "上海市",
    # 天津市（直辖市）
    "天津市",
    # 重庆市（直辖市）
    "重庆市",
    # 河北省
    "石家庄市", "唐山市", "秦皇岛市", "邯郸市", "邢台市", "保定市", "张家口市", "承德市", "沧州市", "廊坊市", "衡水市",
    # 山西省
    "太原市", "大同市", "阳泉市", "长治市", "晋城市", "朔州市", "晋中市", "运城市", "忻州市", "临汾市", "吕梁市",
    # 内蒙古自治区
    "呼和浩特市", "包头市", "乌海市", "赤峰市", "通辽市", "鄂尔多斯市", "呼伦贝尔市", "巴彦淖尔市", "乌兰察布市", "兴安盟", "锡林郭勒盟", "阿拉善盟",
    # 辽宁省
    "沈阳市", "大连市", "鞍山市", "抚顺市", "本溪市", "丹东市", "锦州市", "营口市", "阜新市", "辽阳市", "盘锦市", "铁岭市", "朝阳市", "葫芦岛市",
    # 吉林省
    "长春市", "吉林市", "四平市", "辽源市", "通化市", "白山市", "松原市", "白城市", "延边朝鲜族自治州",
    # 黑龙江省
    "哈尔滨市", "齐齐哈尔市", "鸡西市", "鹤岗市", "双鸭山市", "大庆市", "伊春市", "佳木斯市", "七台河市", "牡丹江市", "黑河市", "绥化市", "大兴安岭地区",
    # 江苏省
    "南京市", "无锡市", "徐州市", "常州市", "苏州市", "南通市", "连云港市", "淮安市", "盐城市", "扬州市", "镇江市", "泰州市", "宿迁市",
    # 浙江省
    "杭州市", "宁波市", "温州市", "嘉兴市", "湖州市", "绍兴市", "金华市", "衢州市", "舟山市", "台州市", "丽水市",
    # 安徽省
    "合肥市", "芜湖市", "蚌埠市", "淮南市", "马鞍山市", "淮北市", "铜陵市", "安庆市", "黄山市", "滁州市", "阜阳市", "宿州市", "六安市", "亳州市", "池州市", "宣城市",
    # 福建省
    "福州市", "厦门市", "莆田市", "三明市", "泉州市", "漳州市", "南平市", "龙岩市", "宁德市",
    # 江西省
    "南昌市", "景德镇市", "萍乡市", "九江市", "新余市", "鹰潭市", "赣州市", "吉安市", "宜春市", "抚州市", "上饶市",
    # 山东省
    "济南市", "青岛市", "淄博市", "枣庄市", "东营市", "烟台市", "潍坊市", "济宁市", "泰安市", "威海市", "日照市", "临沂市", "德州市", "聊城市", "滨州市", "菏泽市",
    # 河南省
    "郑州市", "开封市", "洛阳市", "平顶山市", "安阳市", "鹤壁市", "新乡市", "焦作市", "濮阳市", "许昌市", "漯河市", "三门峡市", "南阳市", "商丘市", "信阳市", "周口市", "驻马店市", "济源市",
    # 湖北省
    "武汉市", "黄石市", "十堰市", "宜昌市", "襄阳市", "鄂州市", "荆门市", "孝感市", "荆州市", "黄冈市", "咸宁市", "随州市", "恩施土家族苗族自治州", "仙桃市", "潜江市", "天门市", "神农架林区",
    # 湖南省
    "长沙市", "株洲市", "湘潭市", "衡阳市", "邵阳市", "岳阳市", "常德市", "张家界市", "益阳市", "郴州市", "永州市", "怀化市", "娄底市", "湘西土家族苗族自治州",
    # 广东省
    "广州市", "深圳市", "珠海市", "汕头市", "佛山市", "韶关市", "湛江市", "肇庆市", "江门市", "茂名市", "惠州市", "梅州市", "汕尾市", "河源市", "阳江市", "清远市", "东莞市", "中山市", "潮州市", "揭阳市", "云浮市",
    # 广西壮族自治区
    "南宁市", "柳州市", "桂林市", "梧州市", "北海市", "防城港市", "钦州市", "贵港市", "玉林市", "百色市", "贺州市", "河池市", "来宾市", "崇左市",
    # 海南省
    "海口市", "三亚市", "三沙市", "儋州市", "五指山市", "琼海市", "文昌市", "万宁市", "东方市", "定安县", "屯昌县", "澄迈县", "临高县", "白沙黎族自治县", "昌江黎族自治县", "乐东黎族自治县", "陵水黎族自治县", "保亭黎族苗族自治县", "琼中黎族苗族自治县",
    # 四川省
    "成都市", "自贡市", "攀枝花市", "泸州市", "德阳市", "绵阳市", "广元市", "遂宁市", "内江市", "乐山市", "南充市", "眉山市", "宜宾市", "广安市", "达州市", "雅安市", "巴中市", "资阳市", "阿坝藏族羌族自治州", "甘孜藏族自治州", "凉山彝族自治州",
    # 贵州省
    "贵阳市", "六盘水市", "遵义市", "安顺市", "毕节市", "铜仁市", "黔西南布依族苗族自治州", "黔东南苗族侗族自治州", "黔南布依族苗族自治州",
    # 云南省
    "昆明市", "曲靖市", "玉溪市", "保山市", "昭通市", "丽江市", "普洱市", "临沧市", "楚雄彝族自治州", "红河哈尼族彝族自治州", "文山壮族苗族自治州", "西双版纳傣族自治州", "大理白族自治州", "德宏傣族景颇族自治州", "怒江傈僳族自治州", "迪庆藏族自治州",
    # 西藏自治区
    "拉萨市", "日喀则市", "昌都市", "林芝市", "山南市", "那曲市", "阿里地区",
    # 陕西省
    "西安市", "铜川市", "宝鸡市", "咸阳市", "渭南市", "延安市", "汉中市", "榆林市", "安康市", "商洛市",
    # 甘肃省
    "兰州市", "嘉峪关市", "金昌市", "白银市", "天水市", "武威市", "张掖市", "平凉市", "酒泉市", "庆阳市", "定西市", "陇南市", "临夏回族自治州", "甘南藏族自治州",
    # 青海省
    "西宁市", "海东市", "海北藏族自治州", "黄南藏族自治州", "海南藏族自治州", "果洛藏族自治州", "玉树藏族自治州", "海西蒙古族藏族自治州",
    # 宁夏回族自治区
    "银川市", "石嘴山市", "吴忠市", "固原市", "中卫市",
    # 新疆维吾尔自治区
    "乌鲁木齐市", "克拉玛依市", "吐鲁番市", "哈密市", "昌吉回族自治州", "博尔塔拉蒙古自治州", "巴音郭楞蒙古自治州", "阿克苏地区", "克孜勒苏柯尔克孜自治州", "喀什地区", "和田地区", "伊犁哈萨克自治州", "塔城地区", "阿勒泰地区", "石河子市", "阿拉尔市", "图木舒克市", "五家渠市", "北屯市", "铁门关市", "双河市", "可克达拉市", "昆玉市", "胡杨河市", "新星市"
]

def fetch_data(city):
 
    try:
        params = {"key": API_KEY, "city": city}
        response = requests.get(API_URL, params=params, timeout=15)
        response.encoding = response.apparent_encoding
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print(f"[网络超时] {city}: 请求超时")
        return None
    except requests.exceptions.RequestException as e:
        print(f"[网络错误] {city}: {str(e)}")
        return None
    except json.JSONDecodeError:
        print(f"[解析错误] {city}: 无法解析返回的JSON数据，内容: {response.text}")
        return None


def parse_data(result, city):
    """
    解析API响应数据

    """
    if not result or result.get("code") != 1:
        print(f"[API错误] {city}: {result.get('msg', '未知错误') if result else '无响应'}")
        return []

    data = result.get("data", {})
    if not data:
        print(f"[数据错误] {city}: 响应中 'data' 字段为空")
        return []

    all_rules = []


    traffic_title = data.get("remark", "常规限行")

    # 安全地处理本地车和外地车限行信息
    local_data_list = data.get("local", [])
    local_info = local_data_list[0] if local_data_list else {}

    foreign_data_list = data.get("foreign", [])
    foreign_info = foreign_data_list[0] if foreign_data_list else {}

    # 处理详细的限行规则列表
    data_list = data.get("data_list", [])
    if not data_list:
        if local_info or foreign_info:
            all_rules.append({
                "城市": city,
                "车辆类型": "今日综合信息",
                "限行标题": traffic_title,
                "限行区域": "见今日限行",
                "限行时间": "见今日限行",
                "限行规则": "见今日限行",
                "本地车限行日期": local_info.get("date_info", "无"),
                "本地车限行尾号": local_info.get("xianxing_num", "无"),
                "外地车限行日期": foreign_info.get("date_info", "无"),
                "外地车限行尾号": foreign_info.get("xianxing_num", "无"),
                "更新时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        else:
            print(f"[数据提示] {city}: 未找到有效的限行规则信息。")

    for rule_type in data_list:
        vehicle_type = rule_type.get("type", "未知类型")
        for rule in rule_type.get("list", []):
            all_rules.append({
                "城市": city,
                "车辆类型": vehicle_type,
                "限行标题": traffic_title,
                "限行区域": rule.get("zone", "无"),
                "限行时间": rule.get("time", "无"),
                "限行规则": rule.get("rule", "无"),
                "本地车限行日期": local_info.get("date_info", "无"),
                "本地车限行尾号": local_info.get("xianxing_num", "无"),
                "外地车限行日期": foreign_info.get("date_info", "无"),
                "外地车限行尾号": foreign_info.get("xianxing_num", "无"),
                "更新时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    return all_rules


def main():
    """主执行函数"""
    all_data = []

    for city in cities:
        print(f"\n>>> 正在处理: {city}")
        result = fetch_data(city)
        if not result:
            continue
        city_data = parse_data(result, city)
        if city_data:
            all_data.extend(city_data)
            print(f"    -> 获取到 {len(city_data)} 条限行规则")
        time.sleep(1)

    if all_data:
        df = pd.DataFrame(all_data)

        final_columns_order = [
            '城市',
            '车辆类型',
            '限行标题',
            '限行区域',
            '限行时间',
            '限行规则',
            '本地车限行日期',
            '本地车限行尾号',
            '外地车限行日期',
            '外地车限行尾号',
            '更新时间' # 保留“更新时间”列以追溯数据时效性
        ]
        
        # 重新排列DataFrame的列
        df = df[final_columns_order]

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"城市限行数据_{timestamp}.xlsx"

        try:
            with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='限行数据')
                workbook = writer.book
                worksheet = writer.sheets['限行数据']
                wrap_format = workbook.add_format({'text_wrap': True, 'valign': 'top'})


                column_settings = [
                    ('A', 10, None),         # 城市
                    ('B', 18, None),         # 车辆类型
                    ('C', 30, wrap_format),  # 限行标题 (新)
                    ('D', 40, wrap_format),  # 限行区域
                    ('E', 30, wrap_format),  # 限行时间
                    ('F', 60, wrap_format),  # 限行规则
                    ('G', 20, None),         # 本地车限行日期
                    ('H', 20, None),         # 本地车限行尾号
                    ('I', 20, None),         # 外地车限行日期
                    ('J', 20, None),         # 外地车限行尾号
                    ('K', 20, None)          # 更新时间
                ]
                for col, width, fmt in column_settings:
                    worksheet.set_column(f'{col}:{col}', width, fmt)

            print(f"\n[成功] 数据已保存！共 {len(all_data)} 条记录 -> {filename}")
        except Exception as e:
            print(f"\n[保存失败] 保存Excel文件时出错: {e}")
            csv_filename = f"城市限行数据_{timestamp}.csv"
            df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
            print(f"[备用方案] 已将数据保存为CSV文件: {csv_filename}")
    else:
        print("\n[总结] 本次运行没有获取到任何有效的限行数据。")


if __name__ == "__main__":
    main()

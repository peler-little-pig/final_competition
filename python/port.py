import random

import serial
import serial.tools.list_ports
from pyecharts import options as opts
from pyecharts.faker import Faker
from pyecharts.charts import Bar, Tab, Bar3D, Gauge


class Port(object):
    def __init__(self) -> None:
        self.arduino: serial.Serial

    def get_port(self):
        l = []
        for i in list(serial.tools.list_ports.comports()):
            l.append(list(i)[0])
        return l

    def begin(self, port, pot):
        self.arduino = serial.Serial(port, pot)
        print("hello")

    def load_data(self):
        # self.arduino.write("d".encode())
        # self.draw(eval("[" + self.arduino.readline().decode()[:-1] + "]"))

        self.draw([0, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4])

    def draw(self, data):
        o = data.count(0)
        t = data.count(1)
        h = data.count(2)
        f = data.count(3)
        v = data.count(4)

        table1 = (
            Bar()
                .add_xaxis(["0", "1", "2", "3", "4"])
                .add_yaxis("分数", [o, t, h, f, v])
                .set_global_opts(
                title_opts=opts.TitleOpts(title=""),
                toolbox_opts=opts.ToolboxOpts(),
                legend_opts=opts.LegendOpts(is_show=False),
            )
        )

        table2 = (
            Bar()
                .add_xaxis([1,2,3,4,5,6,7])
                .add_yaxis("次数", Faker.days_values)
                .set_global_opts(
                title_opts=opts.TitleOpts(title="每天测试数据"),
                datazoom_opts=opts.DataZoomOpts(),
            )
        )

        data = [(i, j, random.randint(0, 12)) for i in range(6) for j in range(24)]
        table3 = (
            Bar3D()
                .add(
                "",
                [[d[1], d[0], d[2]] for d in data],
                xaxis3d_opts=opts.Axis3DOpts(Faker.clock, type_="category"),
                yaxis3d_opts=opts.Axis3DOpts(Faker.week_en, type_="category"),
                zaxis3d_opts=opts.Axis3DOpts(type_="value"),
            )
                .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(max_=20),
                title_opts=opts.TitleOpts(title="测试情况"),
            )
        )

        table4 = (
            Gauge(init_opts=opts.InitOpts(width="800px", height="400px"))
                .add(series_name="业务指标", data_pair=[["", 91.5]])
                .set_global_opts(
                legend_opts=opts.LegendOpts(is_show=False),
                tooltip_opts=opts.TooltipOpts(is_show=True, formatter="{a} <br/>{b} : {c}%"),
            )
        )

        tab = Tab()
        tab.add(table1, "得分情况")
        tab.add(table2, "每天测试数据")
        tab.add(table3, "测试情况")
        tab.add(table4, "完成率")
        tab.render("data.html")

        print("ffff")

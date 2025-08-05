import random

from dome.common.readyaml import ReadYamlData


class DebugTalk():
    def __init__(self):
        self.read = ReadYamlData()

    def get_extract_data_list(self, node_name, randoms=None) -> str:
        """
        获取extract.yaml数据，首先判断randoms是否为数字类型，如果不是就获取下一个node节点的数据
        :param node_name: extract.yaml文件中的key值
        :param randoms: int类型，0：随机读取；-1：读取全部，返回字符串形式；-2：读取全部，返回列表形式；其他根据列表索引取值，取第一个值为1，第二个为2，以此类推;
        :return:
        """
        # if randoms is not None and bool(re.compile(r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$').match(randoms)):
        data = self.read.get_extract_yaml(node_name)
        if randoms is not None:
            randoms = int(randoms)
            data_value = {
                randoms: 1,
                0: random.choice(data),
                -1: ','.join(data),
                -2: ','.join(data).split(','),
            }
            data = data_value[randoms]
        else:
            data = self.read.get_extract_yaml(node_name, randoms)
        return data

    def get_extract_data(self, node_name, randoms=None) -> str:
        """
        获取extract.yaml数据，首先判断randoms是否为数字类型，如果不是就获取下一个node节点的数据
        :param node_name: extract.yaml文件中的key值
        :param randoms: int类型，0：随机读取；-1：读取全部，返回字符串形式；-2：读取全部，返回列表形式；其他根据列表索引取值，取第一个值为1，第二个为2，以此类推;
        :return:
        """
        data = self.read.get_extract_yaml(node_name)
        # if randoms is not None and bool(re.compile(r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$').match(randoms)):
        if randoms is not None:
            randoms = int(randoms)
            data_value = {
                randoms: self.get_extract_order_data(data, randoms),
                0: random.choice(data),
                -1: ','.join(data),
                -2: ','.join(data).split(','),
            }
            data = data_value[randoms]
        else:
            data = self.read.get_extract_yaml(node_name, randoms)
        return data

    def get_extract_order_data(self, data, randoms):
        """获取extract.yaml数据，不为0、-1、-2，则按顺序读取文件key的数据"""
        if randoms not in [0, -1, -2]:
            return data[randoms - 1]


if __name__ == '__main__':
    d = DebugTalk()
    print(d.get_extract_data('Params', 0))
    print(d.get_extract_data('Params', -1))
    print(d.get_extract_data('Params', -2))

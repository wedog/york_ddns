# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import sys

from Tea.core import TeaCore
from typing import List

from alibabacloud_alidns20150109.client import Client as DnsClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_darabonba_env.client import Client as EnvClient
from alibabacloud_alidns20150109 import models as dns_models
from alibabacloud_tea_console.client import Client as ConsoleClient
from alibabacloud_tea_util.client import Client as UtilClient

import socket


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def initialization(
            region_id: str,
    ) -> DnsClient:
        """
        Initialization  初始化公共请求参数
        """
        config = open_api_models.Config()
        # 您的AccessKey ID
        config.access_key_id = EnvClient.get_env('ACCESS_KEY_ID')
        # 您的AccessKey Secret
        config.access_key_secret = EnvClient.get_env('ACCESS_KEY_SECRET')
        # 您的可用区ID
        config.region_id = region_id
        return DnsClient(config)

    @staticmethod
    def describe_domain_records(
            client: DnsClient,
            domain_name: str
    ) -> dns_models.DescribeDomainRecordsResponse:
        """
        获取主域名的所有解析记录列表
        """
        req = dns_models.DescribeDomainRecordsRequest()
        # 主域名
        req.domain_name = domain_name
        try:
            resp = client.describe_domain_records(req)
            ConsoleClient.log('-------------------获取主域名的所有解析记录列表--------------------')
            ConsoleClient.log(UtilClient.to_jsonstring(TeaCore.to_map(resp)))
            return resp
        except Exception as error:
            ConsoleClient.log(error.message)
        return

    @staticmethod
    async def describe_domain_records_async(
            client: DnsClient,
            domain_name: str,
            rr: str,
            record_type: str,
    ) -> dns_models.DescribeDomainRecordsResponse:
        """
        获取主域名的所有解析记录列表
        """
        req = dns_models.DescribeDomainRecordsRequest()
        # 主域名
        req.domain_name = domain_name
        # 主机记录
        req.rrkey_word = rr
        # 解析记录类型
        req.type = record_type
        try:
            resp = await client.describe_domain_records_async(req)
            ConsoleClient.log('-------------------获取主域名的所有解析记录列表--------------------')
            ConsoleClient.log(UtilClient.to_jsonstring(TeaCore.to_map(resp)))
            return resp
        except Exception as error:
            ConsoleClient.log(error.message)
        return

    @staticmethod
    def update_domain_record(
            client: DnsClient,
            req: dns_models.UpdateDomainRecordRequest,
    ) -> None:
        """
        修改解析记录
        """
        try:
            resp = client.update_domain_record(req)
            ConsoleClient.log('-------------------修改解析记录--------------------')
            ConsoleClient.log(UtilClient.to_jsonstring(TeaCore.to_map(resp)))
        except Exception as error:
            ConsoleClient.log(error.message)

    @staticmethod
    async def update_domain_record_async(
            client: DnsClient,
            req: dns_models.UpdateDomainRecordRequest,
    ) -> None:
        """
        修改解析记录
        """
        try:
            resp = await client.update_domain_record_async(req)
            ConsoleClient.log('-------------------修改解析记录--------------------')
            ConsoleClient.log(UtilClient.to_jsonstring(TeaCore.to_map(resp)))
        except Exception as error:
            ConsoleClient.log(error.message)

    @staticmethod
    def main(
            args: List[str],
    ) -> None:
        regionid = args[0]
        current_host_ip = args[1]
        domain_name = args[2]
        client = Sample.initialization(regionid)
        resp = Sample.describe_domain_records(client, domain_name)
        if UtilClient.is_unset(resp) or UtilClient.is_unset(resp.body.domain_records.record[0]):
            ConsoleClient.log('错误参数！')
            return
        # record = resp.body.domain_records.record[0]
        records = resp.body.domain_records.record
        ConsoleClient.log(f'-------------------当前主机公网IP为：{current_host_ip}--------------------')
        is_debug = EnvClient.get_env('IS_DEBUG')
        for record in records:
            # 记录ID
            record_id = record.record_id
            # 记录值
            record_value = record.value
            # 记录类型
            record_type = record.type
            # 主机记录
            rr = record.rr
            ConsoleClient.log(f'记录ID: {record_id}, 记录类型: {record_type}, 主机记录: {rr}, 记录值: {record_value}')
            if UtilClient.equal_string(record_type, 'AAAA') and not UtilClient.equal_string(current_host_ip,
                                                                                            record_value) and not is_debug:
                # 修改解析记录
                req = dns_models.UpdateDomainRecordRequest()
                # 主机记录
                req.rr = rr
                # 记录ID
                req.record_id = record_id
                # 将主机记录值改为当前主机IP
                req.value = current_host_ip
                # 解析记录类型
                req.type = record_type
                Sample.update_domain_record(client, req)

    @staticmethod
    async def main_async(
            args: List[str],
    ) -> None:
        regionid = args[0]
        current_host_ip = args[1]
        domain_name = args[2]
        rr = args[3]
        record_type = args[4]
        client = Sample.initialization(regionid)
        resp = await Sample.describe_domain_records_async(client, domain_name, rr, record_type)
        if UtilClient.is_unset(resp) or UtilClient.is_unset(resp.body.domain_records.record[0]):
            ConsoleClient.log('错误参数！')
            return
        record = resp.body.domain_records.record[0]
        # 记录ID
        record_id = record.record_id
        # 记录值
        records_value = record.value
        ConsoleClient.log(f'-------------------当前主机公网IP为：{current_host_ip}--------------------')
        if not UtilClient.equal_string(current_host_ip, records_value):
            # 修改解析记录
            req = dns_models.UpdateDomainRecordRequest()
            # 主机记录
            req.rr = rr
            # 记录ID
            req.record_id = record_id
            # 将主机记录值改为当前主机IP
            req.value = current_host_ip
            # 解析记录类型
            req.type = record_type
            await Sample.update_domain_record_async(client, req)

    @staticmethod
    def get_current_host_ipv6() -> str:
        # 创建一个UDP套接字对象
        sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        try:
            # 连接到阿里云公共 DNS服务器（仅作为测试）
            sock.connect(('2400:3200::1', 53))
            # 获取本地IPv6地址
            local_addr = sock.getsockname()[0]
            return local_addr
        except Exception as e:
            print("Error occurred while getting IPv6 address:", str(e))
            return []
        finally:
            # 关闭Socket连接
            sock.close()


if __name__ == '__main__':
    ali_arg: str = ['cn-chengdu', '', 'york8.cn']
    ali_arg[1] = Sample.get_current_host_ipv6()
    Sample.main(ali_arg)
    # Sample.main(sys.argv[1:])

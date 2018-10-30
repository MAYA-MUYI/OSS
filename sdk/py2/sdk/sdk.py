# -*- coding: utf-8 -*
import oss2
import os
import shutil


access_key_id = os.getenv('OSS_TEST_ACCESS_KEY_ID', 'your key')
access_key_secret = os.getenv('OSS_TEST_ACCESS_KEY_SECRET', 'your secret')
bucket_name = os.getenv('OSS_TEST_BUCKET', 'maya-test3')
endpoint = os.getenv('OSS_TEST_ENDPOINT', 'http://oss-cn-beijing.aliyuncs.com')
path = os.path.abspath('.')
dirs = os.listdir(path)


def showBucket():
    print("**********   获取bucket信息  *******")
    service = oss2.Service(oss2.Auth(access_key_id, access_key_secret), endpoint)
    print("*****************************")
    print("     现有bucket有：      ")
    print('\n'.join(info.name for info in oss2.BucketIterator(service)))
    buckets = oss2.BucketIterator(service)
    print("*****************************")


def createBucket():
    print("**********   创建  *******")

    bucket_input = raw_input("请输入想创建的bucket名：   ")
    # 创建Bucket对象，所有Object相关的接口都可以通过Bucket对象来进行
    bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name=bucket_input)

    '''
    permission(str) – 指定Bucket的ACL。可以是oss2.BUCKET_ACL_PRIVATE（推荐、缺省）、oss2.BUCKET_ACL_PUBLIC_READ或是
    oss2.BUCKET_ACL_PUBLIC_READ_WRITE。
    '''
    # 带权限与存储类型创建bucket
    bucket.create_bucket(permission=oss2.BUCKET_ACL_PRIVATE,
                         input=oss2.models.BucketCreateConfig(oss2.BUCKET_STORAGE_CLASS_STANDARD))
    if oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name):
        print("     成功创建%s") %bucket_input
        showBucket()
    print("***************************")

def bucketInfo():
    print("**********   获取bucket_info  *******")
    bucket_input = raw_input('请输入bucket名：   ')
    # 获取bucket相关信息
    bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name=bucket_input)
    bucket_info = bucket.get_bucket_info()
    print("     bucket_info:")
    print(' name: ' + bucket_info.name)
    print(' storage class: ' + bucket_info.storage_class)
    print(' creation date: ' + bucket_info.creation_date)
    print("*******************************")

    print("*******************************")
    print("     bucket_stat:")
    bucket_stat = bucket.get_bucket_stat()
    print(' storage: ' + str(bucket_stat.storage_size_in_bytes))
    print(' object count: ' + str(bucket_stat.object_count))
    print(' multi part upload count: ' + str(bucket_stat.multi_part_upload_count))
    print("********************************")



def upload():
    print("**********   上传  *******")
    # 把本地文件 “座右铭.txt” 上传到OSS，新的Object叫做 “我的座右铭.txt”
    # 注意到，这次put_object()的第二个参数是file object；而上次上传是一个字符串。
    # put_object()能够识别不同的参数类型
    bucket_input = raw_input('请输入要传入的bucket名：   ')
    print("**************************")
    print("     当前目录下所有文件：")
    for file in dirs:
        print(file)
    print("***************************")

    filename = raw_input('请输入要上传的文件名： ')
    cloud_name = raw_input('请输入云端文件名：   ')
    bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name=bucket_input)
    with open(oss2.to_unicode(filename), 'rb') as f:
        bucket.put_object(cloud_name, f)
    meta = bucket.get_object_meta(cloud_name)
    if meta:
        print("     上传成功")
        print("     云端所有文件：")
        for i in oss2.ObjectIterator(bucket):
            print(i.key)

    else:
        print("     上传失败")





def download():
    print("**********   下载  *******")
    bucket_input = raw_input('请输入bucket名：')
    bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name=bucket_input)
    print("     %s下有如下文件：") %bucket_input
    for i in oss2.ObjectIterator(bucket):
        print(i.key)
    print("***************************")
    cloud_name = raw_input('请输入要下载的文件名：'    )
    file_name = raw_input('请输入保存至本地文件名：'    )
    bucket.get_object_to_file(cloud_name, file_name)
    if file_name in dirs:
        print("     下载成功")
        print("**************************")
        print("     当前目录下所有文件：")
        for file in dirs:
            print(file)
        print("***************************")



def remove():
    print("**********   删除  *******")
    bucket_input = raw_input('请输入bucket名：'  )
    bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name=bucket_input)
    print("     %s下有如下文件(删除前)：") % bucket_input
    for i in oss2.ObjectIterator(bucket):
        print(i.key)
    print("***************************")
    file_name = raw_input('请输入要删除的文件名：'  )

    # 删除名为motto.txt的Object
    bucket.delete_object(file_name)
    print("     成功删除%s") %file_name
    print("     %s下有如下文件(删除后)：") % bucket_input
    for i in oss2.ObjectIterator(bucket):
        print(i.key)

def main():
    print("************************")
    print("     「指令数字」：")
    print("0. 获取bucket信息")
    print("1. 查看具体bucket信息")
    print("2. 创建bucket")
    print("3. 上传文件")
    print("4. 下载文件")
    print("5. 删除文件")
    print("6. 退出")
    print("************************")
    while 1:
        num = int(raw_input('请输入指令数：'))
        if num == 0:
            showBucket()
        elif num == 1:
            bucketInfo()
        elif num == 2:
            createBucket()
        elif num == 3:
            upload()
        elif num == 4:
            download()
        elif num == 5:
            remove()
        else:
            break



if __name__ == '__main__':
    main()

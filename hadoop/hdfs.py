import pywebhdfs.webhdfs
import os

host = os.getenv('KNOX_IP', '10.108.66.117')
port = os.getenv('KNOX_PORT', '8080')

# create a new client instance
hdfs = pywebhdfs.webhdfs.PyWebHdfsClient(
    base_uri_pattern=f"http://{host}:{port}/webhdfs/v1/",
    request_extra_opts={'verify': False,
                        'auth': ('root', 'root-password')})

# List root dir
print('Listing /user/root/:')
root_dir = hdfs.list_dir("/user/root/input")
print(root_dir)
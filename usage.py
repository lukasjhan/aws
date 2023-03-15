import AwsHelper
import config

aws_config = config.load_config('test')
awshelper = AwsHelper(aws_config)

awshelper.get_bucket('util').download_file('target.tar.gz', './dist/target.tar.gz')
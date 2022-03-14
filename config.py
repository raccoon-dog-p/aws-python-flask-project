class Config :
    JWT_SECRET_KEY = 'yh@1234'
    S3_BUCKET = "pys9-csvfiles"
    S3_KEY = "AKIAY2KXTZ5XALFXA2MU"
    S3_SECRET = "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"
    S3_LOCATION = 'https://{}.s3.amazonaws.com/'.format(S3_BUCKET)


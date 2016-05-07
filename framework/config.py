"""Flask config object."""


class Config:
    """TODO.

    + Config dict should be simple Json.
    """

    def __init__(self):
        """Depreceated."""

        # SQLAlchemy
        self.SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}'.format(
            user='anavah',
            pwd='seal-hello-boat',  # TODO: This is a bad idea.
            host='anavah-dev.celgo7igyrro.us-east-1.rds.amazonaws.com',
            port='3306',
            db='anavah'
        )
        self.SQLALCHEMY_ECHO = False
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False

        # Security
        self.SECRET_KEY = 'secret'
        self.WTF_CSRF_ENABLED = True
        self.WTF_CSRF_SECRET_KEY = 'secret'

        # General
        self.DEBUG = True

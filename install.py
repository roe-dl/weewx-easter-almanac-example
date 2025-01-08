# installer almanac extension example
# Copyright 2025 Johanna Roedenbeck
# Distributed under the terms of the GNU Public License (GPLv3)

from weecfg.extension import ExtensionInstaller

def loader():
    return EasterExampleInstaller()

class EasterExampleInstaller(ExtensionInstaller):
    def __init__(self):
        super(EasterExampleInstaller, self).__init__(
            version="0.1",
            name='EasterExample',
            description='almanac extension example that calculates easter date',
            author="Johanna Roedenbeck",
            author_email="",
            prep_services='user.easteralmanac.EasterService',
            files=[('bin/user', ['bin/user/easteralmanac.py'])]
        )

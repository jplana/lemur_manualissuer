import random

import lemur_manualissuer

from lemur.plugins.bases.issuer import IssuerPlugin

class ManualIssuer(IssuerPlugin):
    title = 'Manual Issuer'
    slug = 'manual-issuer'
    description = 'A plugin to interact with a CA manually.'
    version = lemur_manualissuer.VERSION

    author = 'Jose Plana'
    author_url = 'https://github.com/jplana/lemur_manualissuer'

    options = [
        {
            'name': 'documentation',
            'type': 'str',
            'required': True,
            'validation': '/^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$/',
            'helpMessage': 'Must be a valid web url starting with http[s]://',
        },
        {
            'name': 'ca_certificate',
            'type': 'textarea',
            'default': '',
            'validation': '/^-----BEGIN CERTIFICATE-----/',
            'helpMessage': 'Root Certificate of the CA'
        },
        {
            'name': 'ca_intermediate_certificate',
            'type': 'textarea',
            'default': '',
            'validation': '/^-----BEGIN CERTIFICATE-----/',
            'helpMessage': 'Intermediate Root Certificate'
        },

    ]

    def __init__(self, *args, **kwargs):
        super(ManualIssuer, self).__init__(*args, **kwargs)

    def create_certificate(self, csr, issuer_options):
        authority = issuer_options['authority'].name
        reference = random.getrandbits(64)
        external_id = '{0}-{1:02x}'.format(authority, reference).upper()
        return None, None, external_id

    def revoke_certificate(self, certificate, comments):
        pass

    def get_ordered_certificate(self, order_id):
        pass

    def canceled_ordered_certificate(self, pending_cert, **kwargs):
        pass

    @staticmethod
    def create_authority(options):
        root_cert = ''
        intermediate_cert = ''

        plugin_options = options.get('plugin', {}).get('plugin_options')

        if not plugin_options:
            error = "Invalid options for lemur_manualissuer plugin: {}".format(options)
            current_app.logger.error(error)
            raise InvalidConfiguration(error)

        for option in plugin_options:
            if option.get('name') == 'ca_certificate':
                root_cert = option.get('value')
            if option.get('name') == 'ca_intermediate_certificate':
                intermediate_cert = option.get('value')

        if not root_cert:
            error = "You need to specify the CA certificate"
            raise InvalidConfiguration(error)

        role = dict(username='user', password='password', name='generatedAuthority')
        return root_cert, intermediate_cert, [role]

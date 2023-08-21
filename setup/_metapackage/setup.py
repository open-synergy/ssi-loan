import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-ssi-loan",
    description="Meta package for open-synergy-ssi-loan Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_loan',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)

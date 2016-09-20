from setuptools import setup

setup(
    name='superdome',
    version='0.1',
    packages=['superdome', 'superdome.jinja2ext', 'superdome.postgresqlext', 'superdome.redisext',
              'superdome.sqliteext'],
    package_dir={'': 'src'},
    install_requires=['Jinja2==2.8', 'pgwizard==0.1', 'whodat==0.1'],
    author='Rodrigo A. Lima',
    description='Batteries for whodat web framework.',
    license='BSD',
    keywords='web wsgi whodat',
)

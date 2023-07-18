READ ME!

# Create Directory
mkdir work16
mkdir custom_addons

# Add odoo enterprise
copy odoo enterprise and paste in work16 directory

# Download odoo 16 community
git clone git@github.com:odoo/odoo.git -b 16.0 --depth=1

# Check Python if installed
python3 --version
pip3 --version

# Install Postgresql
sudo apt install postgresql postgresql-client
sudo -u postgres createuser -s $USER
createdb $USER

# Dependencies
sudo apt install python3-dev libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev \
    libtiff5-dev libjpeg8-dev libopenjp2-7-dev zlib1g-dev libfreetype6-dev \
    liblcms2-dev libwebp-dev libharfbuzz-dev libfribidi-dev libxcb1-dev libpq-dev

# Create virtual environment
python3 -m venv .venv
. .venv/bin/activate

# Download dependencies
pip3 install -r odoo/requirements.txt 

# install odoo
pip3 install setuptools wheel
pip3 install -e odoo

# Dependencies
sed -n -e '/^Depends:/,/^Pre/ s/ python3-\(.*\),/python3-\1/p' debian/control | sudo xargs apt-get install -y
npm install -g npm@9.8.0
sudo npm install -g rtlcss

# Check version
odoo --version
odoo/odoo-bin --version

# Run Odoo
python3 odoo/odoo-bin --addons-path=enterprise,odoo/addons,custom_addons -d db-project -u loan_app,loan_borrower --dev xml --xmlrpc-port=8000

# Run this will get you an error: don't worry
odoo/odoo-bin --addons-path=odoo/enterprise,library,odoo/addons -d dbWork -c library.conf --save --stop

# Using scaffold
odoo scaffold library_app library
odoo scaffold library_app odoo/library

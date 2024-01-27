#!/bin/bash

# set permissions for script files
chmod a+x /data/home/root/arduino_power_display/run
chmod 755 /data/home/root/arduino_power_display/run

# create sym-link to run script in deamon
ln -s /data/home/root/arduino_power_display /service/arduino_power_display

# add install-script to rc.local to be ready for firmware update
filename=/data/rc.local
if [ ! -f $filename ]
then
    touch $filename
    chmod 755 $filename
    echo "#!/bin/bash" >> $filename
    echo >> $filename
fi

grep -qxF '/data/home/root/arduino_power_display/install.sh' $filename || echo '/data/home/root/arduino_power_display/install.sh' >> $filename

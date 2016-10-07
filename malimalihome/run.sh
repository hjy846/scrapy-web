running_date=`date +%Y%m%d`
echo ${running_date}

save_path="./logs"
if [ ! -d $save_path ]
then
    mkdir $save_path
fi

/Users/huangjingye/Library/Enthought/Canopy_64bit/User/bin/scrapy crawl malimalihome --logfile=${save_path}/running_${running_date}.log -a crawl_date=yesterday -a region=taipa >>${save_path}/log
/Users/huangjingye/Library/Enthought/Canopy_64bit/User/bin/scrapy crawl malimalihome --logfile=${save_path}/running_${running_date}.log -a crawl_date=yesterday -a region=macau >>${save_path}/log
/Users/huangjingye/Library/Enthought/Canopy_64bit/User/bin/scrapy crawl malimalihome --logfile=${save_path}/running_${running_date}.log -a crawl_date=yesterday -a region=coloane >>${save_path}/log
#scrapy crawl residence_image --logfile=${save_path}/running_${running_date}.log -a crawl_date=yesterday >>log
/Users/huangjingye/Library/Enthought/Canopy_64bit/User/bin/python scripts/preprocess.py yesterday >>${save_path}/log

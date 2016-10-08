running_date=`date +%Y%m%d`
echo ${running_date}

save_path="./logs"
if [ ! -d $save_path ]
then
    mkdir $save_path
fi

scrapy crawl residence --logfile=${save_path}/running_${running_date}.log -a crawl_date=yesterday -a region=taipa >>${save_path}/log
scrapy crawl residence --logfile=${save_path}/running_${running_date}.log -a crawl_date=yesterday -a region=macau >>${save_path}/log
scrapy crawl residence --logfile=${save_path}/running_${running_date}.log -a crawl_date=yesterday -a region=coloane >>${save_path}/log
scrapy crawl residence_image --logfile=${save_path}/running_${running_date}.log -a crawl_date=yesterday >>log
python scripts/preprocess.py yesterday >>${save_path}/log

running_date=`date +%Y-%m-%d`
echo ${running_date}

save_path="./logs"
if [ ! -d $save_path ]
then
    mkdir $save_path
fi

scrapy crawl residence --logfile=${save_path}/running_${running_date}.log -a crawl_date=${running_date} -a region=taipa >>${save_path}/log
scrapy crawl residence --logfile=${save_path}/running_${running_date}.log -a crawl_date=${running_date} -a region=macau >>${save_path}/log
scrapy crawl residence --logfile=${save_path}/running_${running_date}.log -a crawl_date=${running_date} -a region=coloane >>${save_path}/log
python scripts/preprocess.py ${running_date} >>${save_path}/log
#scrapy crawl residence_image --logfile=${save_path}/running_${running_date}.log -a crawl_date=${running_date} >>${save_path}/log

#scrapy crawl centaline --logfile=${save_path}/running_${running_date}.log >>${save_path}/log
#scrapy crawl dsf -s DOWNLOAD_TIMEOUT=1800 --logfile=${save_path}/running_${running_date}.log >>${save_path}/log
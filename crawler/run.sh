
running_date=`date +%Y-%m-%d -d "yesterday"`
echo ${running_date}

log_date=`date +%Y-%m-%d`
echo ${log_date}

save_path="./logs"
if [ ! -d $save_path ]
then
    mkdir $save_path
fi


#scrapy crawl residence --logfile=${save_path}/running_${running_date}.log -a crawl_date=${running_date} -a region=taipa >>${save_path}/log
#scrapy crawl residence --logfile=${save_path}/running_${running_date}.log -a crawl_date=${running_date} -a region=macau >>${save_path}/log
#scrapy crawl residence --logfile=${save_path}/running_${running_date}.log -a crawl_date=${running_date} -a region=coloane >>${save_path}/log
#python scripts/preprocess.py ${running_date} >>${save_path}/log
scrapy crawl residence_image --logfile=${save_path}/image_${log_date}.log -a crawl_date=${running_date} >>${save_path}/image_${log_date}.output
python scripts/convert_image.py ${running_date} >>${save_path}/convert_image_${log_date}.output
scrapy crawl centaline --logfile=${save_path}/centaline_${log_date}.log >>${save_path}/centaline_${log_date}.output
scrapy crawl dsf -s DOWNLOAD_TIMEOUT=1800 --logfile=${save_path}/dsf_${log_date}.log >>${save_path}/dsf_${log_date}.output


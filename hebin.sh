video_save='/data/video_save/'
list=`ls *.ts |sort -n`
file_name=`basename $PWD`
[ ! -d $video_save ] && mkdir -p $video_save
cat $list >$video_save$file_name'.ts'
if [ $? -eq 0 ];then
echo "合并成功，开始清理视频片段"
#rm -f $list $0
fi


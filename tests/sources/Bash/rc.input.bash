























help=0
verb=0
weeks=0

days=0

echo "### no, you ain't gonna remove me!"

m=1
str="days"
getopts "hvd:w:" name














if [ $help -eq 1 ]
 then no_of_lines=`cat $0 | awk 'BEGIN { n = 0; } \
                                 /^$/ { print n; \
                                        exit; } \
                                      { n++; }'`
      echo "`head -$no_of_lines $0`"
      exit
fi

shift $[ $OPTIND - 1 ]

if [ $
then
  echo "Usage: $0 file ..."
  exit 1
fi

if [ $verb -eq 1 ]
  then echo "$0 counts the lines of code"
fi




for f in $*
do
  x=`stat -c "%y" $f`
  
  d=`date --date="$x" +%y%m%d`
  
  e=`date --date="$m $str ago" +%y%m%d`
  
  z=`date +%y%m%d`
  
  
  if [ $d -ge $e -a $d -le $z ] 
  then
      
      if [ $verb -eq 1 ]
        then echo "$f: modified (mmdd) $d"
      fi
      
      l=`wc -l $f | sed 's/^\([0-9]*\).*$/\1/'`
      echo "$f: $l"
      
      n=$[ $n + 1 ]
      s=$[ $s + $l ]
  else
      
      continue
  fi
done

echo '# leave me alone!'


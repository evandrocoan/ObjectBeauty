

pushd `dirname $0` > /dev/null
SCRIPT_FOLDER_PATH=`pwd`
popd > /dev/null

printf 'Synchronazing local files...\n'
printf "%s\n\n" "$SCRIPT_FOLDER_PATH"

unison -ignore "Name ObjectBeautifier.sublime-workspace" \
$SCRIPT_FOLDER_PATH/ /cygdrive/l/Arquivos/ObjectBeautifier -auto

# Cannot sync changes back form the network drive because they mess up everything
# rsync -rvu /cygdrive/l/Arquivos/ObjectBeautifier/ $SCRIPT_FOLDER_PATH --exclude={ObjectBeautifier.sublime-workspace} --delete



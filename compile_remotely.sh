

pushd `dirname $0` > /dev/null
SCRIPT_FOLDER_PATH=`pwd`
popd > /dev/null

printf 'Synchronazing local files...\n'
printf "%s\n\n" "$SCRIPT_FOLDER_PATH"

unison -ignore "Name ObjectBeautifier.sublime-workspace" \
$SCRIPT_FOLDER_PATH/ /cygdrive/l/Arquivos/ObjectBeautifier -auto



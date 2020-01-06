# Download an unpack nauty
curl http://users.cecs.anu.edu.au/~bdm/nauty/nauty26r12.tar.gz | tar -xz
# grab the folder name TODO[michaelr]: Make this less magic
nauty=`ls | grep nauty`
(cd $nauty && ./configure CFLAGS='-O4 -fPIC' && make)
curl https://web.cs.dal.ca/~peter/software/pynauty/pynauty-0.6.0.tar.gz | tar -xz
pynauty=`ls | grep pynauty`
cd $pynauty
x=../$nauty
echo $x
ln -s ../$nauty nauty
make pynauty
